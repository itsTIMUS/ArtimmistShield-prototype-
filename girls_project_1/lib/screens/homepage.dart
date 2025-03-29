import 'package:flutter/material.dart';
import 'package:girls_project_1/screens/pairSafetyDevice.dart';
import 'package:girls_project_1/screens/profile.dart';
import 'package:geolocator/geolocator.dart';
import 'package:flutter_sms/flutter_sms.dart';
import 'package:url_launcher/url_launcher.dart';

class HomePage extends StatelessWidget {
  HomePage({super.key});

  final List<String> parentNumbers = [
    "+919330241900",
    "+919330241900",
  ]; // Parent's phone numbers

  final String liveMapUrl =
      "https://safetyshield.streamlit.app/"; // Streamlit Live Map URL

  final String forumUrl =
      "https://preview--women-guardian-app.lovable.app/forum"; // Forum Page URL

  Future<String> _getLocation() async {
    try {
      LocationPermission permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied ||
          permission == LocationPermission.deniedForever) {
        await Geolocator.requestPermission();
      }

      Position position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
        timeLimit: const Duration(seconds: 5),
      );

      return "https://www.google.com/maps?q=${position.latitude},${position.longitude}";
    } catch (e) {
      return "Location unavailable";
    }
  }

  Future<void> _sendSOS(BuildContext context) async {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) {
        return const AlertDialog(
          title: Text("Sending SOS..."),
          content: Center(child: CircularProgressIndicator()),
        );
      },
    );

    String location = await _getLocation();
    String message =
        "🚨 SOS Alert! 🚨\nI am in danger. My current location: $location";

    try {
      await sendSMS(message: message, recipients: parentNumbers);
      Navigator.of(context).pop();

      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text("SOS Sent Successfully!")));
    } catch (e) {
      Navigator.of(context).pop();

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Failed to send SOS. Try again!")),
      );
    }
  }

  void _openLiveMap() async {
    Uri url = Uri.parse(liveMapUrl);
    if (await canLaunchUrl(url)) {
      await launchUrl(url, mode: LaunchMode.externalApplication);
    } else {
      debugPrint("Could not launch $liveMapUrl");
    }
  }

  void _openForumPage() async {
    Uri url = Uri.parse(forumUrl);
    if (await canLaunchUrl(url)) {
      await launchUrl(url, mode: LaunchMode.externalApplication);
    } else {
      debugPrint("Could not launch $forumUrl");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            Image.asset('assets/shieldLogo.jpeg', height: 50, width: 50),
            const SizedBox(width: 8),
            const Text(
              "Artimmist Shield",
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
          ],
        ),
        actions: [
          SizedBox(
            height: 60,
            width: 60,
            child: IconButton(
              icon: const Icon(Icons.person),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => const ProfileScreen(),
                  ),
                );
              },
            ),
          ),
        ],
      ),
      body: Column(
        children: [
          const SizedBox(height: 30),

          // Live Map Section - Opens Streamlit URL
          GestureDetector(
            onTap: _openLiveMap,
            child: Container(
              height: 200,
              width: double.infinity,
              decoration: BoxDecoration(
                color: Colors.grey.shade300,
                borderRadius: BorderRadius.circular(10),
              ),
              child: const Center(child: Text("Live Map (Click to Open)")),
            ),
          ),
          const SizedBox(height: 40),

          ElevatedButton(
            onPressed: () => _sendSOS(context),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.purpleAccent,
              padding: const EdgeInsets.symmetric(vertical: 15, horizontal: 50),
            ),
            child: const Text("Alert"),
          ),
          const SizedBox(height: 20),

          ElevatedButton(
            onPressed: () => _sendSOS(context),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.purpleAccent,
              padding: const EdgeInsets.symmetric(vertical: 15, horizontal: 50),
            ),
            child: const Text("Location Sharing"),
          ),

          const Spacer(),

          BottomNavigationBar(
            items: const [
              BottomNavigationBarItem(
                icon: Icon(Icons.location_on),
                label: "Destination",
              ),
              BottomNavigationBarItem(icon: Icon(Icons.forum), label: "Forum"),
              BottomNavigationBarItem(
                icon: Icon(Icons.devices),
                label: "Pair Device",
              ),
            ],
            onTap: (index) {
              if (index == 0) {
                _openLiveMap();
              } else if (index == 1) {
                _openForumPage(); // Open Forum Page
              } else if (index == 2) {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => const PairDeviceScreen(),
                  ),
                );
              }
            },
          ),
        ],
      ),
    );
  }
}

class QuestionScreen extends StatefulWidget {
  const QuestionScreen({super.key});

  @override
  _QuestionScreenState createState() => _QuestionScreenState();
}

class _QuestionScreenState extends State<QuestionScreen> {
  String? livesAlone;
  String? safetyLevel;
  String? profession;
  String? outingFrequency;
  String? feelsSafe;
  TextEditingController addressController = TextEditingController();
  String currentLocation = "Fetching location...";

  @override
  void initState() {
    super.initState();
    _getCurrentLocation();
  }

  Future<void> _getCurrentLocation() async {
    try {
      Position position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
      );
      setState(() {
        currentLocation =
            "https://www.google.com/maps?q=${position.latitude},${position.longitude}";
      });
    } catch (e) {
      setState(() {
        currentLocation = "Location unavailable";
      });
    }
  }

  void _submitAnswers() {
    Map<String, dynamic> userResponses = {
      "Lives Alone": livesAlone,
      "Safety Level": safetyLevel,
      "Profession": profession,
      "Outing Frequency": outingFrequency,
      "Feels Safe": feelsSafe,
      "Home Address": addressController.text,
      "Current Location": currentLocation,
    };
    print(userResponses); // Store this for ML processing later
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Safety Survey")),
      body: Center(
        child: Container(
          margin: const EdgeInsets.all(20),
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(15),
            boxShadow: [
              BoxShadow(
                color: Colors.grey.withOpacity(0.5),
                spreadRadius: 2,
                blurRadius: 5,
              ),
            ],
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              // Question 1
              const Text("Do you live alone?"),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Radio(
                    value: "Yes",
                    groupValue: livesAlone,
                    onChanged: (value) => setState(() => livesAlone = value),
                  ),
                  const Text("Yes"),
                  Radio(
                    value: "No",
                    groupValue: livesAlone,
                    onChanged: (value) => setState(() => livesAlone = value),
                  ),
                  const Text("No"),
                ],
              ),

              // Question 2
              const Text("How safe is your locality? (1-5)"),
              DropdownButton<String>(
                value: safetyLevel,
                hint: const Text("Select"),
                onChanged: (value) => setState(() => safetyLevel = value),
                items:
                    ["1", "2", "3", "4", "5"].map((String value) {
                      return DropdownMenuItem<String>(
                        value: value,
                        child: Text(value),
                      );
                    }).toList(),
              ),

              // Question 3
              const Text("What profession are you in?"),
              DropdownButton<String>(
                value: profession,
                hint: const Text("Select Profession"),
                onChanged: (value) => setState(() => profession = value),
                items:
                    ["Student", "Employee", "Business", "Other"].map((
                      String value,
                    ) {
                      return DropdownMenuItem<String>(
                        value: value,
                        child: Text(value),
                      );
                    }).toList(),
              ),

              // Question 4
              const Text("How frequently do you go out?"),
              DropdownButton<String>(
                value: outingFrequency,
                hint: const Text("Select Frequency"),
                onChanged: (value) => setState(() => outingFrequency = value),
                items:
                    ["Daily", "Weekly", "Monthly", "Rarely"].map((
                      String value,
                    ) {
                      return DropdownMenuItem<String>(
                        value: value,
                        child: Text(value),
                      );
                    }).toList(),
              ),

              // Question 5
              const Text("Do you feel safe here?"),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Radio(
                    value: "Yes",
                    groupValue: feelsSafe,
                    onChanged: (value) => setState(() => feelsSafe = value),
                  ),
                  const Text("Yes"),
                  Radio(
                    value: "No",
                    groupValue: feelsSafe,
                    onChanged: (value) => setState(() => feelsSafe = value),
                  ),
                  const Text("No"),
                ],
              ),

              // Address Input
              const Text("Enter your home address:"),
              TextField(
                controller: addressController,
                decoration: const InputDecoration(border: OutlineInputBorder()),
              ),

              // Current Location
              const Text("Current Location (Auto-fetched):"),
              SelectableText(currentLocation),

              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: _submitAnswers,
                child: const Text("Submit"),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
