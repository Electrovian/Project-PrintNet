from __future__ import annotations

# source: profiles/Tronxy/machine/Tronxy X5SA 400 0.4 nozzle.json
DATA = {'default_filament_profile': 'Generic PLA @System',
 'default_print_profile': '0.20mm Standard @Tronxy',
 'from': 'system',
 'inherits': 'fdm_machine_common',
 'instantiation': 'true',
 'machine_start_gcode': 'M104 S[nozzle_temperature_initial_layer] ; start heat nozzle\n'
                        'M140 S[bed_temperature_initial_layer] ; start heat bed\n'
                        'G90 ; abs coords\n'
                        'M83 ; extrude relative\n'
                        'G28 ; home\n'
                        'M190 S[bed_temperature_initial_layer] ; wait for bed temp\n'
                        'M109 S[nozzle_temperature_initial_layer] ; wait for nozzle temp\n'
                        'G1 X10.1 Y20 Z0.28 F5000.0 ; purge line\n'
                        'G1 X10.1 Y200.0 Z0.28 F1500.0 E15\n'
                        'G1 X10.4 Y200.0 Z0.28 F5000.0\n'
                        'G1 X10.4 Y20 Z0.28 F1500.0 E15\n'
                        'G1 Z5.0 F3000 ; move Z up',
 'name': 'Tronxy X5SA 400 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'printable_area': ['0x0', '400x0', '400x400', '0x400'],
 'printable_height': '400',
 'printer_model': 'Tronxy X5SA 400 Marlin Firmware',
 'setting_id': 'GM003',
 'type': 'machine'}
