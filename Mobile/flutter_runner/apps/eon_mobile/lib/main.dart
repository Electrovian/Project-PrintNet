import "package:eon_shared/eon_shared.dart";
import "package:flutter/material.dart";

void main() {
  runApp(const EonTempApp());
}

class EonTempApp extends StatelessWidget {
  const EonTempApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: EonShared.appName,
      home: Scaffold(
        appBar: AppBar(title: const Text("EON Flutter Runner")),
        body: const Center(
          child: Text("Temp shared runner for Android, iOS, and web"),
        ),
      ),
    );
  }
}
