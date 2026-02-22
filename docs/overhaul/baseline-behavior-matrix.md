# Baseline Behavior Matrix (Desktop)

Source references: `docs/_app_slicer_connect_inventory.txt`

## Prepare View
- Load model(s)
- Transform model(s)
- Trigger slice workflow

## Preview View
- Shows gcode preview and print stats
- Allows send-to-printer navigation
- Printer selection currently independent from device/control synchronization in some paths

## Device View
- Select connected printer
- Send to printer / save gcode actions
- Live status placeholder

## Control View
- Printer selection and manual controls UI
- No protocol-specific execution layer in current code

## Known Gaps
- `print_current_model` path slices selected model instead of full plate mesh.
- Printer connect path is OctoPrint-centric.
- Runtime bed limits rely on mutable global defaults.
