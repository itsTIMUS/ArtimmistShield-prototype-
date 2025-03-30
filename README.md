# Project README:-

This repository contains four distinct safety projects designed to improve personal security using modern technologies:

1. **Artemisst Shield** (Mobile app)
2. **Safe Route Finder**
3. **AI Passive SOS**
4. **Women Safety Hardware Device**
   
## 1. Artemisst Shield – Mobile app

### Project Overview
Artemisst Shield is an IoT-based SOS button that sends an emergency alert with the user's location and details when pressed. The system notifies nearby users and the nearest police station for rapid response, pairing seamlessly with our mobile app to provide real-time tracking.

### Key Features & Benefits
- **Immediate Emergency Alerts**: Sends quick SOS notifications with geolocation.
- **Real-Time Tracking**: Enables live tracking through the mobile app.
- **Community Assistance**: Notifies nearby users for prompt help.
- **Integration with Authorities**: Automatically contacts the nearest police station.

### Dependencies
- Flutter SDK (Latest stable version; see [Installation Guide](https://flutter.dev/docs/get-started/install))
- Git (for version control; [Download Git](https://git-scm.com/downloads))
- Chrome Browser (to run the web app)
- VS Code or Android Studio (recommended for development)

### Setup Instructions
1. Clone the Repository:
   ```bash
   git clone https://github.com/your-github-username/Artemisst-Shield.git
   ```
   (Replace your-github-username with your actual GitHub username.)

2. Navigate to the Project Directory:
   ```bash
   cd Artemisst-Shield
   ```

3. Verify Flutter Installation:
   ```bash
   flutter doctor
   ```

4. Enable Flutter for Web (if not already enabled):
   ```bash
   flutter config --enable-web
   ```

5. Install Dependencies:
   ```bash
   flutter pub get
   ```

6. Run the App on Chrome:
   ```bash
   flutter run -d chrome
   ```

### Additional Notes
- **Hot Reload**: Press `r` in the terminal to reload changes.
- **Stopping the App**: Press `Ctrl + C`.
- **Troubleshooting**: Run `flutter clean` followed by `flutter pub get` if you encounter errors.

## 2. Safe Route Finder

### Project Overview
Safe Route Finder is a Streamlit-based web application that computes the safest route between two locations in real time. It leverages routing data from OpenRouteService combined with simulated crime statistics to rank routes by safety and provide turn-by-turn directions.

### Key Features & Benefits
- **Interactive Interface**: User-friendly UI built with Streamlit and Folium.
- **Real-Time Routing**: Uses OpenRouteService to generate route options.
- **Safety Ratings**: Simulated crime data overlay to assess route safety.
- **Multiple Routing Options**: Provides alternative routes with safety comparisons.
- **Turn-by-Turn Directions**: Detailed navigation instructions.

### Dependencies
- Python 3.x (e.g., Python 3.9)
- Git
- Streamlit (e.g., streamlit==1.15.0)
- Requests (e.g., requests==2.28.1)
- Folium (e.g., folium==0.12.1)
- Pandas (e.g., pandas==1.5.0)
- streamlit-folium (e.g., streamlit-folium==0.8.0)
- Polyline (e.g., polyline==1.4.0)
- NumPy (e.g., numpy==1.23.0)

### Setup Instructions
1. Clone the Repository:
   ```bash
   git clone https://github.com/23nash-naaz/SafetyShield.git
   cd SafetyShield
   ```

2. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Application:
   ```bash
   streamlit run app.py
   ```

### Usage
1. **Input Parameters**: Enter the starting location, destination, and your OpenRouteService API key.
2. **Route Preferences**: Choose travel mode (driving, walking, or cycling) and enable the crime data overlay if desired.
3. **View Results**: The interactive map displays the recommended route with safety ratings (green = high safety, orange = medium safety, red = lower safety) along with distance, estimated travel time, and turn-by-turn directions.

## 3. AI Passive SOS

### Project Overview
AI Passive SOS is a real-time distress detection system that listens passively to audio, transcribes it using AssemblyAI, and sends SOS alerts via email upon detecting distress keywords. This system enhances personal safety by automating emergency alerts without user intervention.

### Key Features & Benefits
- **Real-Time Audio Monitoring**: Continuously records short audio segments.
- **Automatic Transcription**: Uses AssemblyAI for speech-to-text conversion.
- **Distress Detection**: Scans for keywords like "help," "SOS," and "emergency."
- **Immediate SOS Alerts**: Automatically sends email alerts when distress is detected.
- **User-Friendly Interface**: Built with Streamlit for real-time control.

### Dependencies
- Python 3.7+ (e.g., Python 3.9)
- Git
- Streamlit (e.g., streamlit==1.15.0)
- Sounddevice (e.g., sounddevice==0.4.6)
- NumPy (e.g., numpy==1.23.0)
- Wave (usually built-in or installable via pip)
- (Note: smtplib is a built-in Python module and does not require installation.)

### Setup Instructions
1. Clone the Repository:
   ```bash
   git clone <repository_url>
   cd AI-Passive-SOS
   ```

2. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configuration:
   - **AssemblyAI API Key**:
     Edit the script to replace the placeholder:
     ```python
     ASSEMBLYAI_API_KEY = "your_api_key_here"
     ```
   - **Email Credentials**:
     Configure your email settings (use an App Password for Gmail) and input sender/recipient emails in the Streamlit UI.

4. Run the Application:
   ```bash
   streamlit run app.py
   ```

### How It Works
1. **Audio Recording**: The application records short audio segments continuously.
2. **Transcription**: Each segment is sent to AssemblyAI for transcription.
3. **Keyword Detection**: The transcript is scanned for distress keywords.
4. **SOS Alert**: If distress is detected, an SOS email is automatically sent.
5. **Auto-Stop**: The recording stops upon detecting distress.

### Deployment
For cloud deployment (e.g., on Render):
1. Create a New Render Web Service: Connect your GitHub repository.
2. Set the Start Command:
   ```bash
   streamlit run app.py
   ```
3. Select an Appropriate Instance Type and deploy.


   # 4) Women Safety Device

This project is a women safety device that records video, captures audio, tracks GPS location, and detects motion and falls using an MPU-6050 sensor. It is designed to work on both Raspberry Pi 3B+ and Windows laptops.

## Features
- **Video Recording:** Uses OV5647 (on Raspberry Pi) or the built-in webcam (on Windows).
- **Audio Recording:** Records from a USB microphone (on Raspberry Pi) or the built-in microphone (on Windows).
- **GPS Tracking:** Retrieves real-time location using the NEO-6M module (or a mock location on Windows).
- **Fall Detection:** Uses the MPU-6050 sensor to detect sudden falls and trigger alerts.

## Installation
1. Clone the repository:
```sh
git clone https://github.com/your-repo/women-safety-device.git
cd women-safety-device
```
2. Install dependencies:
```sh
pip install -r requirements.txt
```

## Usage
Run the main script:
```sh
python main.py
```

## Hardware Requirements (For Raspberry Pi)
- Raspberry Pi 3B+
- OV5647 5MP 1080P IR-Cut Camera
- NEO-6M GPS Module
- Raspberry Pi USB Plug and Play Desktop Microphone
- MPU-6050 Sensor

## Notes
- On Windows, the GPS module and MPU-6050 are simulated for testing.
- Press 'q' to stop video recording early.

## Additional Information

### Team Member Information
- Lead Name – Nashrah Naazneen/Role-Backened developement
- Team Member 2 – Sumit Saha /Role-Flutter app development
- Team Member 3 – Nabhonil/Role-IoT based Hardware device developer
- Team Member 4-Srijanee Mitra/Role-Backened developement

### License
This project is released under the MIT License.

### Contribution Guidelines
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes with clear descriptions.
4. Submit a pull request for review.

### Future Plans
- **Artemisst Shield**: Enhance device connectivity and integrate additional alert channels.
- **Safe Route Finder**: Incorporate real-time crime data and expand route optimization features.
- **AI Passive SOS**: Improve distress keyword accuracy using advanced NLP techniques and integrate voice tone analysis.



