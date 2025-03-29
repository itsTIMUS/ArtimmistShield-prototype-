import 'package:flutter/material.dart';
import 'package:girls_project_1/screens/homepage.dart';
import 'package:image_picker/image_picker.dart'; // For Aadhaar upload
import 'dart:io';

class VerificationScreen extends StatefulWidget {
  const VerificationScreen({super.key});

  @override
  State<VerificationScreen> createState() => _VerificationScreenState();
}

class _VerificationScreenState extends State<VerificationScreen> {
  File? _aadhaarImage;
  final TextEditingController phoneController = TextEditingController();
  final TextEditingController otpController = TextEditingController();
  bool isOtpSent = false;

  Future<void> _pickAadhaarImage() async {
    final pickedFile = await ImagePicker().pickImage(
      source: ImageSource.gallery,
    );
    if (pickedFile != null) {
      setState(() {
        _aadhaarImage = File(pickedFile.path);
      });
    }
  }

  void _sendOTP() {
    setState(() {
      isOtpSent = true;
    });
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(const SnackBar(content: Text("OTP Sent Successfully")));
  }

  void _verifyOTP() {
    if (otpController.text.length == 6) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => HomePage(),
        ), // Navigate to HomePage
      ); // Navigate to Home Page
    } else {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text("Invalid OTP. Try Again.")));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Verification"), centerTitle: true),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            mainAxisSize: MainAxisSize.min, // Prevents unnecessary stretching
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                "Upload Aadhaar Card *",
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 10),
              GestureDetector(
                onTap: _pickAadhaarImage,
                child: Container(
                  height: 150,
                  width: double.infinity,
                  decoration: BoxDecoration(
                    border: Border.all(color: Colors.grey),
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child:
                      _aadhaarImage != null
                          ? ClipRRect(
                            borderRadius: BorderRadius.circular(10),
                            child: Image.file(
                              _aadhaarImage!,
                              fit: BoxFit.cover,
                            ),
                          )
                          : const Icon(
                            Icons.upload_file,
                            size: 50,
                            color: Colors.grey,
                          ),
                ),
              ),
              const SizedBox(height: 20),
              const Text(
                "Facial Recognition *",
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 10),
              ElevatedButton(
                onPressed: () {}, // Placeholder for AI-based facial recognition
                child: const Text("Start Facial Scan"),
              ),
              const SizedBox(height: 20),
              const Text(
                "Phone Number *",
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              TextFormField(
                controller: phoneController,
                keyboardType: TextInputType.phone,
                decoration: const InputDecoration(
                  hintText: "Enter phone number",
                  prefixIcon: Icon(Icons.phone),
                ),
              ),
              const SizedBox(height: 10),
              ElevatedButton(
                onPressed: _sendOTP,
                child: const Text("Send OTP"),
              ),
              if (isOtpSent) ...[
                const SizedBox(height: 20),
                const Text(
                  "Enter OTP *",
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                TextFormField(
                  controller: otpController,
                  keyboardType: TextInputType.number,
                  maxLength: 6,
                  decoration: const InputDecoration(
                    hintText: "Enter OTP",
                    prefixIcon: Icon(Icons.lock),
                  ),
                ),
                const SizedBox(height: 10),
                ElevatedButton(
                  onPressed: _verifyOTP,
                  child: const Text("Verify & Continue"),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}
