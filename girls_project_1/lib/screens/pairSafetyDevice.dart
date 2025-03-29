import 'dart:async';
import 'package:flutter/material.dart';

class PairDeviceScreen extends StatefulWidget {
  const PairDeviceScreen({super.key});

  @override
  _PairDeviceScreenState createState() => _PairDeviceScreenState();
}

class _PairDeviceScreenState extends State<PairDeviceScreen> {
  bool _bluetoothEnabled = false;
  bool _searching = false;
  bool _connecting = false;
  List<String> _availableDevices = [];
  String? _selectedDevice;
  String? _connectionStatus;

  @override
  void initState() {
    super.initState();
    _requestBluetoothPermission();
  }

  // Simulating Bluetooth permission request
  Future<void> _requestBluetoothPermission() async {
    await Future.delayed(const Duration(seconds: 2));
    setState(() {
      _bluetoothEnabled = true;
    });
    _searchForDevices();
  }

  // Simulating device search
  Future<void> _searchForDevices() async {
    setState(() {
      _searching = true;
      _availableDevices = [];
      _connectionStatus = null;
    });

    await Future.delayed(const Duration(seconds: 3));

    setState(() {
      _searching = false;
      _availableDevices = ["Device A", "Device B", "Device C"];
    });
  }

  // Simulating device connection
  Future<void> _connectToDevice(String device) async {
    setState(() {
      _connecting = true;
      _selectedDevice = device;
      _connectionStatus = null;
    });

    await Future.delayed(const Duration(seconds: 3));

    setState(() {
      _connecting = false;
      _connectionStatus =
          (device == "Device A")
              ? "Connected Successfully!"
              : "Connection Failed!";
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Pair Device")),
      body: Center(
        child:
            _bluetoothEnabled
                ? (_connecting
                    ? Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const CircularProgressIndicator(),
                        const SizedBox(height: 20),
                        Text(
                          "Connecting to $_selectedDevice...",
                          style: const TextStyle(fontSize: 18),
                        ),
                      ],
                    )
                    : (_searching
                        ? Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: const [
                            CircularProgressIndicator(),
                            SizedBox(height: 20),
                            Text(
                              "Searching for devices...",
                              style: TextStyle(fontSize: 18),
                            ),
                          ],
                        )
                        : (_connectionStatus != null
                            ? Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Icon(
                                  _connectionStatus == "Connected Successfully!"
                                      ? Icons.check_circle
                                      : Icons.error,
                                  color:
                                      _connectionStatus ==
                                              "Connected Successfully!"
                                          ? Colors.green
                                          : Colors.red,
                                  size: 60,
                                ),
                                const SizedBox(height: 10),
                                Text(
                                  _connectionStatus!,
                                  style: const TextStyle(
                                    fontSize: 20,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                const SizedBox(height: 20),
                                ElevatedButton(
                                  onPressed: _searchForDevices,
                                  child: const Text("Retry"),
                                ),
                              ],
                            )
                            : (_availableDevices.isNotEmpty
                                ? Column(
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  children: [
                                    const Text(
                                      "Select a device to connect:",
                                      style: TextStyle(fontSize: 18),
                                    ),
                                    const SizedBox(height: 10),
                                    Column(
                                      children:
                                          _availableDevices.map((device) {
                                            return Padding(
                                              padding:
                                                  const EdgeInsets.symmetric(
                                                    vertical: 5,
                                                  ),
                                              child: ElevatedButton(
                                                onPressed:
                                                    () => _connectToDevice(
                                                      device,
                                                    ),
                                                child: Text(device),
                                              ),
                                            );
                                          }).toList(),
                                    ),
                                  ],
                                )
                                : const Text(
                                  "No devices found. Try searching again.",
                                )))))
                : const Text("Waiting for Bluetooth Permission..."),
      ),
    );
  }
}
