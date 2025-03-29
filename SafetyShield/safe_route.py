import streamlit as st
import requests
import folium
from folium.plugins import HeatMap
import pandas as pd
from streamlit_folium import folium_static
import json
import polyline
import time
from datetime import datetime
import math
import numpy as np

# Set up the page
st.set_page_config(
    page_title="Safe Route Finder",
    page_icon="🧭",
    layout="wide"
)

st.title("🧭 Safe Route Finder")
st.write("Find the safest route between two locations in real-time")

# Sidebar for inputs
with st.sidebar:
    st.header("Enter Locations")
    start_location = st.text_input("Starting Location", "Times Square, New York")
    end_location = st.text_input("Destination", "Central Park, New York")
    
    st.header("API Keys")
    openroute_key = st.text_input("OpenRouteService API Key", 
                                 help="Get a free key at https://openrouteservice.org/dev/#/signup")
    crimemap_enabled = st.checkbox("Enable Crime Data Overlay", value=True)
    
    st.header("Route Preferences")
    route_profile = st.selectbox(
        "Travel Mode",
        ["driving-car", "foot-walking", "cycling-regular"]
    )
    
    show_alternative_routes = st.checkbox("Show Alternative Routes", value=True, 
                                        help="Show multiple route options with safety ratings")
    
    avoid_options = st.multiselect(
        "Avoid (When Possible)",
        ["highways", "tollways", "ferries", "high_crime_areas"]
    )
    
    st.header("Safety Settings")
    safety_weight = st.slider("Safety Priority", 0, 10, 5, 
                            help="Higher values prioritize safety over travel time")
    time_of_day = st.selectbox(
        "Time of Day",
        ["Current Time", "Morning (6AM-10AM)", "Afternoon (10AM-4PM)", 
         "Evening (4PM-8PM)", "Night (8PM-6AM)"]
    )
    
    find_route = st.button("Find Safe Route")

# Main content
col1, col2 = st.columns([2, 1])

# Helper function to get coordinates from location names
def geocode_location(location_name, api_key):
    base_url = "https://api.openrouteservice.org/geocode/search"
    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml',
        'Authorization': api_key
    }
    params = {
        'text': location_name,
        'size': 1
    }
    
    try:
        response = requests.get(base_url, headers=headers, params=params)
        data = response.json()
        if 'features' in data and len(data['features']) > 0:
            coordinates = data['features'][0]['geometry']['coordinates']
            return coordinates  # [longitude, latitude]
        else:
            return None
    except Exception as e:
        st.error(f"Error geocoding location: {e}")
        return None

# Function to calculate distance between two coordinates (in km)
def haversine_distance(coord1, coord2):
    # Convert coordinates from [lon, lat] to [lat, lon] for calculation
    lon1, lat1 = coord1
    lon2, lat2 = coord2
    
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers
    
    return c * r

# Function to generate intermediate waypoints for long routes
def generate_waypoints(start_coords, end_coords, max_segment_distance=5000):
    total_distance = haversine_distance(start_coords, end_coords)
    
    if total_distance <= max_segment_distance:
        return []  # No waypoints needed for short routes
    
    # Calculate how many segments we need
    num_segments = math.ceil(total_distance / max_segment_distance)
    
    # Generate intermediate points
    waypoints = []
    for i in range(1, num_segments):
        # Calculate intermediate point (simple linear interpolation)
        fraction = i / num_segments
        lon = start_coords[0] + (end_coords[0] - start_coords[0]) * fraction
        lat = start_coords[1] + (end_coords[1] - start_coords[1]) * fraction
        waypoints.append([lon, lat])
    
    return waypoints

# Function to get route between two points with options for alternative routes
def get_route(start_coords, end_coords, profile, api_key, avoid=None, alternatives=False):
    # Check approximate distance
    approx_distance = haversine_distance(start_coords, end_coords)
    
    # For very long routes, we'll split into segments
    if approx_distance > 5000:
        waypoints = generate_waypoints(start_coords, end_coords)
        
        if waypoints:
            st.info(f"Route distance is approximately {approx_distance:.0f} km. Breaking into {len(waypoints) + 1} segments for routing.")
            
            # Create a list to hold all route segments
            all_segments = []
            prev_point = start_coords
            
            # Get route for each segment
            for i, waypoint in enumerate(waypoints + [end_coords]):
                segment = get_single_route(prev_point, waypoint, profile, api_key, avoid, alternatives=False)
                if segment:
                    all_segments.append(segment)
                else:
                    st.error(f"Could not calculate route for segment {i+1}.")
                    return None
                prev_point = waypoint
            
            # Combine all segments into one route
            return combine_route_segments(all_segments)
    
    # For shorter routes, just get a direct route
    return get_single_route(start_coords, end_coords, profile, api_key, avoid, alternatives)

# Function to get a single route segment
def get_single_route(start_coords, end_coords, profile, api_key, avoid=None, alternatives=False):
    base_url = "https://api.openrouteservice.org/v2/directions/" + profile
    headers = {
        'Accept': 'application/json, application/geo+json',
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }
    
    body = {
        "coordinates": [start_coords, end_coords],
        "instructions": True,
    }
    
    if avoid:
        avoid_features = [a for a in avoid if a != "high_crime_areas"]
        if avoid_features:
            body["options"] = {"avoid_features": avoid_features}
    
    if alternatives:
        body["alternative_routes"] = {
            "target_count": 3,
            "weight_factor": 1.6
        }
    
    try:
        response = requests.post(base_url, json=body, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            error_msg = f"Error getting route: {response.status_code}"
            try:
                error_data = response.json()
                if 'error' in error_data and 'message' in error_data['error']:
                    error_msg += f", {error_data['error']['message']}"
                    
                    # Handle specific distance limit error
                    if "distance must not be greater than" in error_data['error']['message']:
                        st.error("The route segment distance exceeds the API limit. Using automatic waypoints.")
                        return None
            except:
                error_msg += f", {response.text}"
                
            st.warning(error_msg)
            return None
    except Exception as e:
        st.error(f"Error requesting route: {e}")
        return None

# Function to combine multiple route segments into one route
def combine_route_segments(segments):
    if not segments:
        return None
    
    # Start with the first segment as our base
    combined_route = segments[0].copy()
    
    # Only process additional segments if there are any
    if len(segments) > 1:
        # For simplicity, we'll just use the first route from each segment
        first_route = combined_route['routes'][0]
        
        total_distance = first_route['summary']['distance']
        total_duration = first_route['summary']['duration']
        
        # Combine geometries and other data from additional segments
        for segment in segments[1:]:
            route = segment['routes'][0]
            
            # Add distance and duration
            total_distance += route['summary']['distance']
            total_duration += route['summary']['duration']
            
            # For a real application, you would need to merge:
            # - Geometries (decoding/encoding polylines)
            # - Steps and instructions
            # - Bounding boxes
            # For simplicity, we'll just combine summary data
            
            # Add steps to the existing route
            first_route['segments'][0]['steps'].extend(route['segments'][0]['steps'])
        
        # Update the summary with totals
        first_route['summary']['distance'] = total_distance
        first_route['summary']['duration'] = total_duration
    
    return combined_route

# Mock function to get crime data (replace with real API when available)
def get_crime_data(bbox, time_of_day):
    # This is a mock function - in a real app, you'd connect to a crime data API
    import random
    
    # Parse bbox: [min_lon, min_lat, max_lon, max_lat]
    min_lon, min_lat, max_lon, max_lat = bbox
    
    # Adjust crime density based on time of day
    density_factor = {
        "Morning (6AM-10AM)": 0.3,
        "Afternoon (10AM-4PM)": 0.4,
        "Evening (4PM-8PM)": 0.6,
        "Night (8PM-6AM)": 1.0,
        "Current Time": 0.5
    }
    
    # If it's "Current Time", determine the actual period
    if time_of_day == "Current Time":
        current_hour = datetime.now().hour
        if 6 <= current_hour < 10:
            current_period = "Morning (6AM-10AM)"
        elif 10 <= current_hour < 16:
            current_period = "Afternoon (10AM-4PM)"
        elif 16 <= current_hour < 20:
            current_period = "Evening (4PM-8PM)"
        else:
            current_period = "Night (8PM-6AM)"
        density = density_factor[current_period]
    else:
        density = density_factor[time_of_day]
    
    # Generate about 50-200 crime points depending on density
    num_points = int(50 + (150 * density))
    
    # Create crime data with concentration in certain areas
    crime_data = []
    
    # Generate some crime hotspots
    num_hotspots = 3
    hotspots = []
    for _ in range(num_hotspots):
        hotspot_lat = min_lat + (max_lat - min_lat) * random.random()
        hotspot_lon = min_lon + (max_lon - min_lon) * random.random()
        hotspot_radius = random.uniform(0.01, 0.05)  # Roughly 1-5 km
        hotspots.append((hotspot_lat, hotspot_lon, hotspot_radius))
    
    for _ in range(num_points):
        # 70% of crime in hotspots, 30% randomly distributed
        if random.random() < 0.7 and hotspots:
            # Choose a random hotspot
            hotspot = random.choice(hotspots)
            hotspot_lat, hotspot_lon, hotspot_radius = hotspot
            
            # Generate point near the hotspot using normal distribution
            lat = random.normalvariate(hotspot_lat, hotspot_radius/3)
            lon = random.normalvariate(hotspot_lon, hotspot_radius/3)
            
            # Ensure point is within the bounding box
            lat = max(min_lat, min(max_lat, lat))
            lon = max(min_lon, min(max_lon, lon))
            
            # Weight is higher for points close to hotspot center
            dist_from_center = math.sqrt((lat - hotspot_lat)**2 + (lon - hotspot_lon)**2)
            weight = 1.0 - min(1.0, dist_from_center / hotspot_radius)
            weight = max(0.2, weight)  # Minimum weight of 0.2
        else:
            # Random point in the bounding box
            lat = min_lat + (max_lat - min_lat) * random.random()
            lon = min_lon + (max_lon - min_lon) * random.random()
            weight = random.uniform(0.2, 0.5)  # Lower weights for random points
        
        crime_data.append([lat, lon, weight])
    
    return crime_data, hotspots

# Function to evaluate route safety using crime data
def evaluate_route_safety(route_coords, crime_data, hotspots):
    if not crime_data:
        return 95  # Default high safety if no crime data
    
    # Define a corridor width around the route (in degrees, approx 100m)
    corridor_width = 0.001
    
    # Count crime points near the route
    crime_count = 0
    crime_weight_sum = 0
    
    # For each point in the route, check if crime points are within the corridor
    for route_point in route_coords:
        route_lat, route_lon = route_point
        
        for crime_point in crime_data:
            crime_lat, crime_lon, crime_weight = crime_point
            
            # Calculate distance from crime point to route point
            dist = math.sqrt((crime_lat - route_lat)**2 + (crime_lon - route_lon)**2)
            
            # If crime point is within corridor, count it
            if dist < corridor_width:
                crime_count += 1
                crime_weight_sum += crime_weight
    
    # For hotspots, check if route passes through them
    for hotspot in hotspots:
        hotspot_lat, hotspot_lon, hotspot_radius = hotspot
        
        for route_point in route_coords:
            route_lat, route_lon = route_point
            
            # Distance from route point to hotspot center
            dist = math.sqrt((route_lat - hotspot_lat)**2 + (route_lon - hotspot_lon)**2)
            
            # If route passes through hotspot, add penalty
            if dist < hotspot_radius:
                crime_weight_sum += (hotspot_radius - dist) / hotspot_radius * 2
                break
    
    # Calculate safety score (inversely proportional to crime)
    if len(route_coords) > 0:
        # Normalize by route length
        normalized_crime = crime_weight_sum / len(route_coords)
        safety_score = 100 - min(100, normalized_crime * 100)
        return max(0, safety_score)
    else:
        return 95  # Default value for empty routes

# Function to find multiple route options and rate their safety
def find_safe_routes(start_coords, end_coords, profile, api_key, time_of_day, safety_weight, avoid):
    # Get route options (with alternatives if requested)
    route_data = get_route(start_coords, end_coords, profile, api_key, avoid, alternatives=True)
    
    if not route_data:
        return None, None, None, None
    
    # Get bounding box of all routes for crime data
    min_lon, min_lat, max_lon, max_lat = float('inf'), float('inf'), float('-inf'), float('-inf')
    
    routes = []
    
    # Extract geometries for all routes
    if 'routes' in route_data:
        for route in route_data['routes']:
            route_geometry = route['geometry']
            decoded_route = polyline.decode(route_geometry)
            
            # Update bounding box
            for point in decoded_route:
                lat, lon = point
                min_lat = min(min_lat, lat)
                min_lon = min(min_lon, lon)
                max_lat = max(max_lat, lat)
                max_lon = max(max_lon, lon)
            
            routes.append({
                'geometry': route_geometry,
                'decoded_route': decoded_route,
                'summary': route['summary'],
                'segments': route['segments']
            })
    
    # Add padding to the bounding box
    padding = 0.02  # About 2km padding
    bbox = [
        min_lon - padding,
        min_lat - padding,
        max_lon + padding,
        max_lat + padding
    ]
    
    # Get crime data for the area
    crime_data, hotspots = get_crime_data(bbox, time_of_day)
    
    # Evaluate safety for each route
    for route in routes:
        route['safety_score'] = evaluate_route_safety(route['decoded_route'], crime_data, hotspots)
    
    # Sort routes by safety score (if safety_weight is high) or by time (if low)
    if safety_weight > 5:
        routes.sort(key=lambda x: x['safety_score'], reverse=True)
    elif safety_weight > 3:
        # Balance between safety and time
        for route in routes:
            # Normalize time (lower is better)
            time_factor = 1 - (route['summary']['duration'] / max(r['summary']['duration'] for r in routes))
            # Normalize safety (higher is better)
            safety_factor = route['safety_score'] / 100
            
            # Combined score (higher is better)
            weight_safety = safety_weight / 10  # Convert to 0-1 scale
            weight_time = 1 - weight_safety
            
            route['combined_score'] = (weight_safety * safety_factor) + (weight_time * time_factor)
        
        routes.sort(key=lambda x: x['combined_score'], reverse=True)
    else:
        # Sort primarily by time
        routes.sort(key=lambda x: x['summary']['duration'])
    
    # Return the main route data (for compatibility) along with all route options and crime data
    return route_data, routes, crime_data, bbox

# Function to display the map with multiple routes
def display_map_with_routes(routes, crime_data, bbox, crimemap_enabled):
    if not routes:
        return None, 0, 0, 0
    
    # Get the main route (first in the sorted list)
    main_route = routes[0]
    route_coords = [[lat, lng] for lat, lng in main_route['decoded_route']]
    
    # Calculate map center based on all routes
    all_lats = [coord[0] for route in routes for coord in route['decoded_route']]
    all_lons = [coord[1] for route in routes for coord in route['decoded_route']]
    
    center_lat = sum(all_lats) / len(all_lats)
    center_lng = sum(all_lons) / len(all_lons)
    
    # Create a map
    m = folium.Map(location=[center_lat, center_lng], zoom_start=12)
    
    # Add crime heatmap if enabled
    if crimemap_enabled and crime_data:
        HeatMap(crime_data).add_to(m)
    
    # Route colors based on safety score
    def get_route_color(safety_score):
        if safety_score >= 80:
            return 'green'
        elif safety_score >= 60:
            return 'orange'
        else:
            return 'red'
    
    # Add all routes to the map
    for i, route in enumerate(routes):
        route_coords = [[lat, lng] for lat, lng in route['decoded_route']]
        
        # Main route is thicker, alternates are thinner
        weight = 6 if i == 0 else 4
        
        # Get color based on safety score
        color = get_route_color(route['safety_score'])
        
        # Add route line with popup showing safety info
        route_line = folium.PolyLine(
            route_coords,
            weight=weight,
            color=color,
            opacity=0.8 if i == 0 else 0.6,
            tooltip=f"Route {i+1}: {route['safety_score']:.0f}% safe, {route['summary']['duration']/60:.0f} min"
        )
        
        route_line.add_to(m)
        
        # For the main route, add route number markers along the path
        if i == 0:
            # Add markers at the beginning, middle and a few key points
            markers_count = min(len(route_coords), 5)
            if markers_count > 0:
                indices = [0]  # Start
                
                if markers_count > 1:
                    indices.append(len(route_coords) - 1)  # End
                    
                # Add some points in between if there are more than 2 markers
                if markers_count > 2:
                    step = len(route_coords) // (markers_count - 1)
                    indices.extend([j * step for j in range(1, markers_count - 1)])
                    indices = sorted(list(set(indices)))
                
                for idx in indices[1:-1]:  # Skip start and end
                    folium.CircleMarker(
                        location=route_coords[idx],
                        radius=6,
                        color=color,
                        fill=True,
                        fill_color=color,
                        fill_opacity=0.7,
                        tooltip=f"Route {i+1}"
                    ).add_to(m)
    
    # Add markers for start and end
    folium.Marker(
        location=route_coords[0],
        popup="Start",
        icon=folium.Icon(color="green", icon="play")
    ).add_to(m)
    
    folium.Marker(
        location=route_coords[-1],
        popup="End",
        icon=folium.Icon(color="red", icon="stop")
    ).add_to(m)
    
    # Display route statistics from main route
    distance = main_route['summary']['distance'] / 1000  # convert to km
    duration = main_route['summary']['duration'] / 60  # convert to minutes
    safety_score = main_route['safety_score']
    
    # Add a legend for safety scores
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 170px; height: 130px; 
                border:2px solid grey; z-index:9999; font-size:14px;
                background-color:white; padding: 10px; border-radius: 5px;">
      <p><b>Route Safety</b></p>
      <p><i class="fa fa-circle" style="color:green"></i> High Safety (80-100%)</p>
      <p><i class="fa fa-circle" style="color:orange"></i> Medium Safety (60-80%)</p>
      <p><i class="fa fa-circle" style="color:red"></i> Lower Safety (<60%)</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    return m, distance, duration, safety_score, routes

# Main app logic
if find_route:
    if not openroute_key:
        st.warning("Please enter your OpenRouteService API key in the sidebar.")
    else:
        with st.spinner("Finding the safest route..."):
            # Progress bar
            progress_bar = st.progress(0)
            
            # Step 1: Geocode the locations
            progress_bar.progress(10)
            st.info("Geocoding locations...")
            start_coords = geocode_location(start_location, openroute_key)
            end_coords = geocode_location(end_location, openroute_key)
            
            if not start_coords or not end_coords:
                st.error("Couldn't find one or both locations. Please check the names and try again.")
            else:
                # Step 2: Get crime data and find safe routes
                progress_bar.progress(40)
                st.info("Analyzing crime patterns and calculating multiple route options...")
                
                # Get routes with safety ratings
                route_data, routes, crime_data, bbox = find_safe_routes(
                    start_coords, end_coords, route_profile, 
                    openroute_key, time_of_day, safety_weight, avoid_options
                )
                
                if routes:
                    # Step 3: Create and display the map
                    progress_bar.progress(80)
                    st.info("Generating map and safety report...")
                    
                    with col1:
                        map_result = display_map_with_routes(
                            routes, crime_data, bbox, crimemap_enabled
                        )
                        
                        if map_result:
                            m, distance, duration, safety_score, routes = map_result
                            folium_static(m, width=800)
                        
                                            
                        # Step 4: Display route details
                        progress_bar.progress(100)
                    
                    
                        st.subheader("Recommended Route Summary")
                        
                        st.metric("Distance", f"{distance:.1f} km")
                        st.metric("Estimated Time", f"{duration:.0f} min")
                        
                        # Safety score with color
                        color = "green" if safety_score > 80 else "orange" if safety_score > 60 else "red"
                        st.markdown(f"<h3 style='color: {color}'>Safety Score: {safety_score:.0f}/100</h3>", 
                                  unsafe_allow_html=True)
                        
                        # Alternative routes if we have them and they're enabled
                        if show_alternative_routes and len(routes) > 1:
                            st.subheader("Alternative Routes")
                            
                            # Create a comparison table
                            route_data = []
                            for i, route in enumerate(routes):
                                if i > 0:  # Skip the main route (already shown above)
                                    route_data.append({
                                        "Route": f"Option {i+1}",
                                        "Safety": f"{route['safety_score']:.0f}%",
                                        "Time": f"{route['summary']['duration']/60:.0f} min",
                                        "Distance": f"{route['summary']['distance']/1000:.1f} km"
                                    })
                            
                            if route_data:
                                route_df = pd.DataFrame(route_data)
                                st.table(route_df)
                        
                        # Safety recommendations
                        st.subheader("Safety Tips")
                        
                        if safety_score < 70:
                            st.warning("This route passes through areas with higher crime rates. Consider:")
                            st.markdown("- Traveling during daylight hours if possible")
                            st.markdown("- Staying alert and aware of your surroundings")
                            st.markdown("- Keeping valuables out of sight")
                            
                            if show_alternative_routes and any(r['safety_score'] > safety_score + 5 for r in routes[1:]):
                                st.info("Consider one of the alternative routes for improved safety.")
                        else:
                            st.success("This route is generally considered safe. Standard precautions advised.")
                        
                        # Turn-by-turn directions for main route
                        st.subheader("Turn-by-Turn Directions")
                        
                        # Only display directions for the main (recommended) route
                        main_route = routes[0]
                        if 'segments' in main_route:
                            for segment in main_route['segments']:
                                for i, step in enumerate(segment['steps']):
                                    instruction = step['instruction']
                                    distance = step['distance']
                                    
                                    if distance < 1000:
                                        distance_str = f"{distance:.0f} m"
                                    else:
                                        distance_str = f"{distance/1000:.1f} km"
                                        
                                    st.markdown(f"**{i+1}.** {instruction} ({distance_str})")
                        else:
                            # Use the original route data format
                            for i, step in enumerate(route_data['routes'][0]['segments'][0]['steps']):
                                instruction = step['instruction']
                                distance = step['distance']
                                
                                if distance < 1000:
                                    distance_str = f"{distance:.0f} m"
                                else:
                                    distance_str = f"{distance/1000:.1f} km"
                                    
                                st.markdown(f"**{i+1}.** {instruction} ({distance_str})")
                else:
                    progress_bar.empty()
                    st.error("Couldn't calculate routes between these locations. Please try different locations or check your API key.")

else:
    # Initial view
    st.info("Enter your locations and API key in the sidebar, then click 'Find Safe Route'.")
    
    # Sample map centered on a default location
    default_map = folium.Map(location=[40.7128, -74.0060], zoom_start=12)
    folium_static(default_map)
    
    with col2:
        st.subheader("How to use this app")
        st.markdown("""
        1. Get a free API key from [OpenRouteService](https://openrouteservice.org/dev/#/signup)
        2. Enter your starting point and destination
        3. Adjust safety settings based on your preferences
        4. Click "Find Safe Route" to see the safest path
        """)
        
        st.subheader("Safety Features")
        st.markdown("""
        - **Color-coded routes** show safety levels at a glance
        - **Green routes** are safest
        - **Orange routes** have moderate safety concerns
        - **Red routes** may have higher safety risks
        - **Alternative routes** give you safer options
        - **Long-distance routing** automatically breaks routes into segments
        """)
        
        st.subheader("About")
        st.markdown("""
        This app combines routing data with crime statistics to recommend the safest routes 
        between locations. Perfect for travelers, commuters, and anyone concerned about 
        personal safety while navigating unfamiliar areas.
        
        The app supports both short local trips and long-distance journeys with automatic segmentation.
        """)