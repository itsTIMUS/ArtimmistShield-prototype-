import 'package:flutter/material.dart';
import 'package:girls_project_1/screens/mobileVerification.Dart'; 

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final TextEditingController nameController = TextEditingController();
  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();
  final TextEditingController confirmPasswordController = TextEditingController();
  final TextEditingController addressController = TextEditingController();
  final TextEditingController parent1Controller = TextEditingController();
  final TextEditingController parent2Controller = TextEditingController();
  final TextEditingController parentPhoneController = TextEditingController();

  final formKey = GlobalKey<FormState>();

  void submitForm() {
  if (formKey.currentState!.validate()) {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => VerificationScreen()),
    );
  }
}

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(title: const Text("Registration"), centerTitle: true),
      body: Center(
        child: SingleChildScrollView(
          child: Container(
            margin: const EdgeInsets.symmetric(horizontal: 30, vertical: 10),
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: const Color.fromARGB(255, 241, 222, 244),
              borderRadius: BorderRadius.circular(20),
            ),
            child: Form(
              key: formKey,
              child: Column(
                children: [
                  const Text(
                    "Sign Up",
                    style: TextStyle(fontSize: 30, fontWeight: FontWeight.bold, color: Colors.purple),
                  ),
                  const SizedBox(height: 10),

                  // Name Field
                  TextFormField(
                    controller: nameController,
                    decoration: const InputDecoration(
                      prefixIcon: Icon(Icons.person),
                      labelText: "Full Name *",
                    ),
                    validator: (value) => value!.isEmpty ? "Please enter your name" : null,
                  ),

                  // Email Field
                  TextFormField(
                    controller: emailController,
                    keyboardType: TextInputType.emailAddress,
                    decoration: const InputDecoration(
                      prefixIcon: Icon(Icons.email),
                      labelText: "Email ID *",
                    ),
                    validator: (value) {
                      final bool emailValid = RegExp(
                        r"^[a-zA-Z0-9.a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~]+@[a-zA-Z0-9]+\.[a-zA-Z]+",
                      ).hasMatch(value!);
                      return emailValid ? null : "Enter a valid email address";
                    },
                  ),

                  // Password Field
                  TextFormField(
                    controller: passwordController,
                    obscureText: true,
                    decoration: const InputDecoration(
                      prefixIcon: Icon(Icons.lock),
                      labelText: "Password *",
                    ),
                    validator: (value) {
                      if (value!.length < 8) return "Password must be at least 8 characters";
                      return null;
                    },
                  ),

                  // Confirm Password Field (Linked with Password)
                  TextFormField(
                    controller: confirmPasswordController,
                    obscureText: true,
                    decoration: const InputDecoration(
                      prefixIcon: Icon(Icons.lock),
                      labelText: "Confirm Password *",
                    ),
                    validator: (value) {
                      if (value!.isEmpty) return "Please confirm your password";
                      if (value != passwordController.text) return "Passwords do not match";
                      return null;
                    },
                  ),

                  // Address Field
                  TextFormField(
                    controller: addressController,
                    decoration: const InputDecoration(
                      prefixIcon: Icon(Icons.home),
                      labelText: "Address *",
                    ),
                    validator: (value) => value!.isEmpty ? "Enter your address" : null,
                  ),

                  // Parent 1 Name (Mandatory)
                  TextFormField(
                    controller: parent1Controller,
                    decoration: const InputDecoration(
                      prefixIcon: Icon(Icons.person_outline),
                      labelText: "Parent 1 Name *",
                    ),
                    validator: (value) => value!.isEmpty ? "At least one parent's name is required" : null,
                  ),

                  // Parent 2 Name (Optional)
                  TextFormField(
                    controller: parent2Controller,
                    decoration: const InputDecoration(
                      prefixIcon: Icon(Icons.person_outline),
                      labelText: "Parent 2 Name (Optional)",
                    ),
                  ),

                  // Parent Phone Number
                  TextFormField(
                    controller: parentPhoneController,
                    keyboardType: TextInputType.phone,
                    decoration: const InputDecoration(
                      prefixIcon: Icon(Icons.phone),
                      labelText: "Parents' Phone Number *",
                    ),
                    validator: (value) {
                      if (value!.length != 10) return "Enter a valid 10-digit phone number";
                      return null;
                    },
                  ),

                  const SizedBox(height: 20),

                  // Start Verification Button
                  ElevatedButton(
                    onPressed: submitForm,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.purple,
                      padding: const EdgeInsets.symmetric(horizontal: 50, vertical: 15),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                    ),
                    child: const Text("Start Verification", style: TextStyle(color: Colors.white, fontSize: 18)),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
