# PrintNet User Manual

## System Overview
PrintNet acts as a layer between users and physical 3D printers.

It integrates with services like:
- OctoPrint
- 3DPrinterOS

## Print Workflow
1. User uploads a model
2. Model is sliced into G-code
3. G-code is sent to printer API
4. Printer firmware executes instructions

## Printer States
- Idle
- Printing
- Error
- Offline

## Error Handling
- Offline printers generate alerts
- Invalid files are rejected
- Failed jobs are logged
