# ArtimmistShield-prototype-
 Our Women Safety Device is an IoT-based SOS button that sends an emergency alert with the user's location and details when pressed. It notifies nearby users and the nearest police station for quick assistance and pairs seamlessly with our mobile app for real-time tracking.

How to Run Artemisst Shield Locally on Chrome Web (Flutter Web)

Prerequisites:

Flutter SDK (Latest stable version) → Install Guide: https://docs.flutter.dev/get-started/install

Git (Required for version control) → Download Git: https://git-scm.com/downloads

Chrome Browser (For running the web app)

VS Code or Android Studio (Recommended for coding)

Steps to Set Up & Run the App on Chrome Web:

Clone the Repository
Open Git Bash or Command Prompt, then run:
git clone https://github.com/your-github-username/Artemisst-Shield.git
(Replace "your-github-username" with your actual GitHub username.)
This will create a folder named "Artemisst-Shield" on your local system.

Navigate to the Project Directory
cd Artemisst-Shield

Check Flutter Installation
Run this command to verify your Flutter setup:
flutter doctor
If there are no critical issues, proceed to the next step.

Enable Flutter for Web (If Not Already Enabled)
flutter config --enable-web

Install Dependencies
Run:
flutter pub get
This will install all required packages from pubspec.yaml.

Run the App on Chrome
Use the following command:
flutter run -d chrome
This will start the Flutter app in Chrome.

Additional Notes:

Hot Reload: If you make changes, use "r" in the terminal to reload.

Stopping the App: Press "Ctrl + C" in the terminal.

Common Errors: If errors occur, try "flutter clean" and "flutter pub get" again.



# Safe Route Finder[for running this on your local server]

Safe Route Finder is a Streamlit-based application designed to help users find the safest route between two locations in real time. By integrating routing data from OpenRouteService with simulated crime statistics, the app provides multiple route options along with safety ratings and turn-by-turn directions.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

Safe Route Finder leverages several Python libraries—including Streamlit, Folium, Requests, Pandas, and Polyline—to provide an interactive web application. Users can input a starting location and destination, specify their route preferences, and optionally enable a crime data overlay. The app calculates multiple route options, ranks them by safety, and displays the results on an interactive map with helpful metrics such as estimated travel time, distance, and safety score.

## Features

- **Interactive Interface:** A simple and intuitive interface built with Streamlit.
- **Real-Time Routing:** Uses OpenRouteService to generate route options.
- **Crime Data Overlay:** Simulated crime data is used to rate the safety of each route.
- **Alternative Routes:** Displays multiple routing options with comparative safety ratings.
- **Turn-by-Turn Directions:** Provides detailed step-by-step directions.
- **Automatic Waypoint Generation:** Splits long routes into manageable segments for efficient routing.

## Prerequisites

Before running the app, ensure that you have the following installed:

- Python 3.x
- Git

Additionally, you'll need an API key from [OpenRouteService](https://openrouteservice.org/dev/#/signup).

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/23nash-naaz/SafetyShield.git
   cd SafetyShield

2)**Install dependencies:**

A requirements.txt file is included with the project. Install the necessary libraries by running:

##pip install -r requirements.txt

The requirements.txt file includes libraries such as:

1)streamlit

2)requests

3)folium

4)pandas

5)streamlit-folium

6)polyline

7)numpy

**Usage**

Run the Application:

Start the Streamlit app by running:

##streamlit run app.py


**Input Parameters:**

Enter the starting location and destination in the sidebar.

##Provide your OpenRouteService API key.

Choose your travel mode (e.g., driving, walking, or cycling) and set route preferences.

Optionally, enable the crime data overlay and adjust safety settings.

Click the Find Safe Route button to calculate the safest path based on your inputs.

View Results:

The app displays an interactive map with the recommended route, alternative routes (if available), and corresponding safety metrics.

Route details include distance, estimated time, and a safety score.

Turn-by-turn directions are provided for the main route.

A legend explains the color coding used for route safety: green (high safety), orange (medium safety), and red (lower safety).


# AI Passive SOS(for running on local server)

## Overview
AI Passive SOS is a real-time distress detection system that passively listens to audio, transcribes it using AssemblyAI, and sends SOS alerts via email if distress keywords are detected. This system is designed to enhance personal safety by providing automatic emergency alerts.

## Features
- **Real-time audio monitoring**: Continuously records short audio chunks.
- **Automatic transcription**: Uses AssemblyAI to transcribe speech.
- **Distress detection**: Detects distress keywords like "help," "sos," "emergency."
- **SOS alert via email**: Sends an automated email alert upon detecting distress signals.
- **Streamlit-based UI**: User-friendly web application interface.

## Technologies Used
- **Python**: Core language.
- **Streamlit**: Web interface for real-time control.
- **AssemblyAI API**: For speech-to-text transcription.
- **Sounddevice**: Capturing live audio.
- **smtplib**: Sending SOS email alerts.
- **Threading**: For handling background recording.

## Setup Instructions

### Prerequisites
Ensure you have Python 3.7+ installed on your system.

### Installation
1. Clone the repository:
   
   git clone <repository_url>
   cd AI-Passive-SOS
   
2. Install the required dependencies:
   
   pip install -r requirements.txt
   

### Configuration
1. **AssemblyAI API Key**: Obtain an API key from [AssemblyAI](https://www.assemblyai.com) and replace the placeholder in the script:
   
   ASSEMBLYAI_API_KEY = "your_api_key_here"
   
2. **Email Credentials**: Use your email credentials to send SOS alerts.
   - Use an [App Password](https://support.google.com/accounts/answer/185833) for Gmail authentication.
   - Input sender and recipient emails in the Streamlit UI.

### Running the Application
To start the application, run:

streamlit run app.py


## How It Works
1. The application starts recording audio in short chunks.
2. Each chunk is saved and uploaded to AssemblyAI for transcription.
3. The transcript is analyzed for distress keywords.
4. If distress is detected, an SOS email is sent to the designated recipient.
5. Recording stops automatically upon distress detection.

## Deployment
### Deploy on Render
1. Create a **new Render Web Service**.
2. Select the **GitHub repository** containing your project.
3. Set the **Start Command**:
   `
   streamlit run app.py
  
4. Choose an appropriate instance type and deploy.

## Requirements.txt

requests
streamlit
sounddevice
numpy
wave

(Note: `smtplib` is a built-in Python module and does not need to be installed.)

## Contribution
Feel free to contribute by improving the distress keyword detection or integrating additional safety features.



