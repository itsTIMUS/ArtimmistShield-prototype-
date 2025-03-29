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
