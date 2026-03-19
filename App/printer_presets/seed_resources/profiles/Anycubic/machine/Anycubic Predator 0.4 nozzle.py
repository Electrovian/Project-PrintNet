from __future__ import annotations

# source: profiles/Anycubic/machine/Anycubic Predator 0.4 nozzle.json
DATA = {'auxiliary_fan': '0',
 'bed_exclude_area': ['0x0'],
 'default_print_profile': '0.20mm Standard @Anycubic Predator',
 'from': 'system',
 'gcode_flavor': 'marlin',
 'inherits': 'fdm_machine_common',
 'instantiation': 'true',
 'layer_change_gcode': '',
 'machine_end_gcode': 'M107 T0\n'
                      'M104 S0\n'
                      'M104 S0 T1\n'
                      'M140 S0\n'
                      'G92 E0\n'
                      'G91\n'
                      'G1 E-1 F300\n'
                      'G1 Z+0.5  F6000\n'
                      'G28 \n'
                      'G90 ;absolute positioning',
 'machine_pause_gcode': 'PAUSE',
 'machine_start_gcode': 'G21 ; use millimeters\n'
                        'G90 ; absolute positioning\n'
                        'M82 ; absolute extrusion\n'
                        'M107 T0 ; turn off part cooling fan\n'
                        '\n'
                        'M140 S[bed_temperature_initial_layer_single] ; set bed temp\n'
                        'M104 S[nozzle_temperature_initial_layer] T0  ; set nozzle temp\n'
                        'M190 S[bed_temperature_initial_layer_single] ; wait for bed\n'
                        'M109 S[nozzle_temperature_initial_layer] T0  ; wait for nozzle\n'
                        '\n'
                        'G28 ; home all\n'
                        'G1 X0 Y0 Z5.0 F4000 ; jump to center\n'
                        'G1 X-180 Y0 Z0.4 F2000 ; move to near bed edge\n'
                        'G92 E0 ; reset the extruder\n'
                        '\n'
                        '; --- Prime line ---\n'
                        'G1 E5 F300 ; initial prime\n'
                        'G0 X-180.00 Y0.00 Z0.30 E0 F1000\n'
                        'G1 X-179.385 Y-14.864 Z0.30 E3.57042\n'
                        'G1 X-177.545 Y-29.627 Z0.30 E7.14094\n'
                        'G1 X-174.492 Y-44.187 Z0.30 E10.71134\n'
                        'G1 X-170.247 Y-58.446 Z0.30 E14.28195\n'
                        'G1 X-164.839 Y-72.305 Z0.30 E17.85235\n'
                        'G1 X-158.305 Y-85.671 Z0.30 E21.42298\n'
                        'G1 X-150.690 Y-98.451 Z0.30 E24.99339\n'
                        'G1 X-142.045 Y-110.558 Z0.30 E27.56379 ; gradually reducing extrusion\n'
                        'G1 F1500 E26.56379 ; retract 1mm\n'
                        'G1 Z0.5 F3000 ; lift Z slightly\n'
                        'G92 E0 ; reset the extruder\n'
                        '; --- End priming line ---',
 'name': 'Anycubic Predator 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'brass',
 'printable_area': ['184.296x16.1238',
                    '182.189x32.1249',
                    '178.696x47.8815',
                    '173.843x63.2737',
                    '167.667x78.1844',
                    '160.215x92.5',
                    '151.543x106.112',
                    '141.718x118.916',
                    '130.815x130.815',
                    '118.916x141.718',
                    '106.112x151.543',
                    '92.5x160.215',
                    '78.1844x167.667',
                    '63.2737x173.843',
                    '47.8815x178.696',
                    '32.1249x182.189',
                    '16.1238x184.296',
                    '1.1328e-14x185',
                    '-16.1238x184.296',
                    '-32.1249x182.189',
                    '-47.8815x178.696',
                    '-63.2737x173.843',
                    '-78.1844x167.667',
                    '-92.5x160.215',
                    '-106.112x151.543',
                    '-118.916x141.718',
                    '-130.815x130.815',
                    '-141.718x118.916',
                    '-151.543x106.112',
                    '-160.215x92.5',
                    '-167.667x78.1844',
                    '-173.843x63.2737',
                    '-178.696x47.8815',
                    '-182.189x32.1249',
                    '-184.296x16.1238',
                    '-185x2.2656e-14',
                    '-184.296x-16.1238',
                    '-182.189x-32.1249',
                    '-178.696x-47.8815',
                    '-173.843x-63.2737',
                    '-167.667x-78.1844',
                    '-160.215x-92.5',
                    '-151.543x-106.112',
                    '-141.718x-118.916',
                    '-130.815x-130.815',
                    '-118.916x-141.718',
                    '-106.112x-151.543',
                    '-92.5x-160.215',
                    '-78.1844x-167.667',
                    '-63.2737x-173.843',
                    '-47.8815x-178.696',
                    '-32.1249x-182.189',
                    '-16.1238x-184.296',
                    '-3.39839e-14x-185',
                    '16.1238x-184.296',
                    '32.1249x-182.189',
                    '47.8815x-178.696',
                    '63.2737x-173.843',
                    '78.1844x-167.667',
                    '92.5x-160.215',
                    '106.112x-151.543',
                    '118.916x-141.718',
                    '130.815x-130.815',
                    '141.718x-118.916',
                    '151.543x-106.112',
                    '160.215x-92.5',
                    '167.667x-78.1844',
                    '173.843x-63.2737',
                    '178.696x-47.8815',
                    '182.189x-32.1249',
                    '184.296x-16.1238',
                    '185x-4.53119e-14'],
 'printable_height': '455',
 'printer_model': 'Anycubic Predator',
 'scan_first_layer': '0',
 'setting_id': 'GM003',
 'type': 'machine'}
