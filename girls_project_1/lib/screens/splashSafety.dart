import 'package:flutter/material.dart';
import 'package:girls_project_1/screens/OnboardingScreen.dart';

class Splashscreen1 extends StatefulWidget {
  const Splashscreen1({super.key});

  @override
  State<Splashscreen1> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<Splashscreen1> {
  loadNextpage() async {
    await Future.delayed(Duration(seconds: 4), () {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => OnboardingScreen(),
        ), // Fixed typo
      );
    });
  }

  @override
  void initState() {
    super.initState();
    loadNextpage();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color.fromARGB(
        255,
        255,
        255,
        255,
      ), // Light Pink Background
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center, // Centers Content
          children: [
            Image.asset(
              "assets/shieldLogo.jpeg", // Image.asset
              width: 300,
              height: 300,
              fit: BoxFit.cover,
            ),
            SizedBox(height: 20),
            Text(
              "Artimmist Shield",
              style: TextStyle(
                fontSize: 30,
                fontWeight: FontWeight.bold,
                color: Color(0xFF800000), // Maroon Color
              ),
            ),
            SizedBox(height: 40),
            Text(
              "Developed by",
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Color(0xFF800000), // Maroon Color
              ),
            ),
            Text(
              "Nashrah Nabhonil Srijanee Sumit ",
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                color: Color(0xFF800000), // Maroon Color
              ),
            ),
          ],
        ),
      ),
    );
  }
}
