from __future__ import annotations

# source: profiles/FLSun/machine/FLSun QQ-S Pro 0.4 nozzle.json
DATA = {'auxiliary_fan': '0',
 'change_filament_gcode': '',
 'default_filament_profile': ['FLSun Generic PLA'],
 'default_print_profile': '0.20mm Standard @FLSun QQSPro',
 'deretraction_speed': ['40'],
 'from': 'system',
 'gcode_flavor': 'marlin',
 'inherits': 'fdm_machine_common',
 'instantiation': 'true',
 'machine_end_gcode': '; printing object ENDGCODE\n'
                      'G92 E0.0 ; prepare to retract\n'
                      'G1 E-6 F3000; retract to avoid stringing\n'
                      '; Anti-stringing end wiggle\n'
                      '{if layer_z < max_print_height}G1 Z{min(layer_z+100, max_print_height)}{endif} F4000 ; Move '
                      'print head up\n'
                      'G1 X0 Y120 F3000 ; present print\n'
                      '; Reset print setting overrides\n'
                      'G92 E0\n'
                      'M200 D0 ; disable volumetric e\n'
                      'M220 S100 ; reset speed factor to 100%\n'
                      'M221 S100 ; reset extruder factor to 100%\n'
                      ';M900 K0 ; reset linear acceleration(Marlin)\n'
                      '; Shut down printer\n'
                      'M104 S0 ; turn off temperature\n'
                      'M140 S0 ; turn off heatbed\n'
                      'M107 ; turn off fan\n'
                      'M18 S180 ;disable motors after 180s\n'
                      'M300 S40 P10 ; Bip\n'
                      'M117 Print finish.',
 'machine_max_acceleration_e': ['3000', '800'],
 'machine_max_acceleration_extruding': ['1500', '800'],
 'machine_max_acceleration_retracting': ['2000', '800'],
 'machine_max_acceleration_travel': ['1500', '800'],
 'machine_max_acceleration_x': ['1500', '800'],
 'machine_max_acceleration_y': ['1500', '800'],
 'machine_max_acceleration_z': ['1500', '800'],
 'machine_max_jerk_e': ['5', '5'],
 'machine_max_jerk_x': ['5', '10'],
 'machine_max_jerk_y': ['5', '10'],
 'machine_max_jerk_z': ['5', '10'],
 'machine_max_speed_e': ['60', '30'],
 'machine_max_speed_x': ['200', '150'],
 'machine_max_speed_y': ['200', '150'],
 'machine_max_speed_z': ['200', '150'],
 'machine_pause_gcode': 'M400 U1\n',
 'machine_start_gcode': ';STARTGCODE\n'
                        'M117 Initializing\n'
                        '; Set coordinate modes\n'
                        'G90 ; use absolute coordinates\n'
                        'M83 ; extruder relative mode\n'
                        '; Reset speed and extrusion rates\n'
                        'M200 D0 ; disable volumetric E\n'
                        'M220 S100 ; reset speed\n'
                        '; Set initial warmup temps\n'
                        'M117 Nozzle preheat\n'
                        'M104 S100 ; preheat extruder to no ooze temp\n'
                        'M140 S[bed_temperature_initial_layer_single] ; set bed temp\n'
                        'M190 S[bed_temperature_initial_layer_single] ; wait for bed final temp\n'
                        'M300 S40 P10 ; Bip\n'
                        '; Home\n'
                        'M117 Homing\n'
                        'G28 ; home all with default mesh bed level\n'
                        '; For ABL users put G29 for a leveling request\n'
                        '; Final warmup routine\n'
                        'M117 Final warmup\n'
                        'M104 S[nozzle_temperature_initial_layer] ; set extruder final temp\n'
                        'M109 S[nozzle_temperature_initial_layer] ; wait for extruder final temp\n'
                        'M190 S[bed_temperature_initial_layer_single] ; wait for bed final temp\n'
                        'M300 S440 P200; 1st beep for printer ready and allow some time to clean nozzle\n'
                        'M300 S0 P250; wait between dual beep\n'
                        'M300 S440 P200; 2nd beep for printer ready\n'
                        'G4 S10; wait to clean the nozzle\n'
                        'M300 S440 P200; 3rd beep for ready to start printing\n'
                        '; Prime line routine\n'
                        'M117 Printing prime line\n'
                        ';M900 K0; Disable Linear Advance (Marlin) for prime line\n'
                        'G92 E0.0; reset extrusion distance\n'
                        'G1 X-54.672 Y-95.203 Z0.3 F4000; go outside print area\n'
                        'G92 E0.0; reset extrusion distance\n'
                        'G1 E2 F1000 ; de-retract and push ooze\n'
                        'G3 X38.904 Y-102.668 I54.672 J95.105 E20.999\n'
                        'G3 X54.671 Y-95.203 I-38.815 J102.373 E5.45800\n'
                        'G92 E0.0\n'
                        'G1 E-5 F3000 ; retract 5mm\n'
                        'G1 X52.931 Y-96.185 F1000 ; wipe\n'
                        'G1 X50.985 Y-97.231 F1000 ; wipe\n'
                        'G1 X49.018 Y-98.238 F1000 ; wipe\n'
                        'G1 X0 Y-109.798 F1000\n'
                        'G1 E4.8 F1500; de-retract\n'
                        'G92 E0.0 ; reset extrusion distance\n'
                        '; Final print adjustments\n'
                        'M117 Preparing to print\n'
                        ';M82 ; extruder absolute mode\n'
                        'M221 S{if layer_height<0.075}100{else}95{endif}\n'
                        'M300 S40 P10 ; chirp\n'
                        'M117 Print [output_filename_format]; Display: Printing started...',
 'max_layer_height': ['0.32'],
 'min_layer_height': ['0.08'],
 'name': 'FLSun QQ-S Pro 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'hardened_steel',
 'printable_area': ['129.505x11.3302',
                    '128.025x22.5743',
                    '125.57x33.6465',
                    '122.16x44.4626',
                    '117.82x54.9404',
                    '112.583x65',
                    '106.49x74.5649',
                    '99.5858x83.5624',
                    '91.9239x91.9239',
                    '83.5624x99.5858',
                    '74.5649x106.49',
                    '65x112.583',
                    '54.9404x117.82',
                    '44.4626x122.16',
                    '33.6465x125.57',
                    '22.5743x128.025',
                    '11.3302x129.505',
                    '7.9602e-15x130',
                    '-11.3302x129.505',
                    '-22.5743x128.025',
                    '-33.6465x125.57',
                    '-44.4626x122.16',
                    '-54.9404x117.82',
                    '-65x112.583',
                    '-74.5649x106.49',
                    '-83.5624x99.5858',
                    '-91.9239x91.9239',
                    '-99.5858x83.5624',
                    '-106.49x74.5649',
                    '-112.583x65',
                    '-117.82x54.9404',
                    '-122.16x44.4626',
                    '-125.57x33.6465',
                    '-128.025x22.5743',
                    '-129.505x11.3302',
                    '-130x1.59204e-14',
                    '-129.505x-11.3302',
                    '-128.025x-22.5743',
                    '-125.57x-33.6465',
                    '-122.16x-44.4626',
                    '-117.82x-54.9404',
                    '-112.583x-65',
                    '-106.49x-74.5649',
                    '-99.5858x-83.5624',
                    '-91.9239x-91.9239',
                    '-83.5624x-99.5858',
                    '-74.5649x-106.49',
                    '-65x-112.583',
                    '-54.9404x-117.82',
                    '-44.4626x-122.16',
                    '-33.6465x-125.57',
                    '-22.5743x-128.025',
                    '-11.3302x-129.505',
                    '-2.38806e-14x-130',
                    '11.3302x-129.505',
                    '22.5743x-128.025',
                    '33.6465x-125.57',
                    '44.4626x-122.16',
                    '54.9404x-117.82',
                    '65x-112.583',
                    '74.5649x-106.49',
                    '83.5624x-99.5858',
                    '91.9239x-91.9239',
                    '99.5858x-83.5624',
                    '106.49x-74.5649',
                    '112.583x-65',
                    '117.82x-54.9404',
                    '122.16x-44.4626',
                    '125.57x-33.6465',
                    '128.025x-22.5743',
                    '129.505x-11.3302',
                    '130x-3.18408e-14'],
 'printable_height': '360',
 'printer_model': 'FLSun QQ-S Pro',
 'printer_settings_id': 'FLSun',
 'retract_before_wipe': ['70%'],
 'retract_length_toolchange': ['1'],
 'retraction_length': ['5'],
 'retraction_minimum_travel': ['2'],
 'retraction_speed': ['30'],
 'scan_first_layer': '0',
 'setting_id': 'GM003',
 'single_extruder_multi_material': '1',
 'thumbnails': ['260x260'],
 'type': 'machine'}
