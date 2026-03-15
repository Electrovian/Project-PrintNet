from __future__ import annotations

# source: profiles/FLSun/machine/FLSun SR 0.4 nozzle.json
DATA = {'auxiliary_fan': '0',
 'bed_exclude_area': ['0x0'],
 'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\nG92 E0.0\n;[layer_z]',
 'change_filament_gcode': ';FILAMENT_CHANGE\nM600',
 'default_filament_profile': ['FLSun Generic PLA'],
 'default_print_profile': '0.20mm Standard @FLSun SR',
 'deretraction_speed': ['40'],
 'extruder_clearance_height_to_lid': '140',
 'extruder_clearance_height_to_rod': '36',
 'extruder_clearance_radius': '65',
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
 'machine_max_acceleration_e': ['5000', '5000'],
 'machine_max_acceleration_extruding': ['5000', '2000'],
 'machine_max_acceleration_retracting': ['5000', '5000'],
 'machine_max_acceleration_travel': ['3000', '3000'],
 'machine_max_acceleration_x': ['5000', '2000'],
 'machine_max_acceleration_y': ['5000', '2000'],
 'machine_max_acceleration_z': ['1500', '200'],
 'machine_max_jerk_e': ['2.5', '2.5'],
 'machine_max_jerk_x': ['9', '9'],
 'machine_max_jerk_y': ['9', '9'],
 'machine_max_jerk_z': ['3', '0.4'],
 'machine_max_speed_e': ['30', '25'],
 'machine_max_speed_x': ['300', '200'],
 'machine_max_speed_y': ['300', '200'],
 'machine_max_speed_z': ['20', '12'],
 'machine_min_extruding_rate': ['0', '0'],
 'machine_min_travel_rate': ['0', '0'],
 'machine_pause_gcode': 'M600',
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
                        'M140 S[first_layer_bed_temperature] ; set bed temp\n'
                        'M190 S[first_layer_bed_temperature] ; wait for bed final temp\n'
                        'M300 S40 P10 ; Bip\n'
                        '; Home\n'
                        'M117 Homing\n'
                        'G28 ; home all with default mesh bed level\n'
                        '; For ABL users put G29 for a leveling request\n'
                        '; Final warmup routine\n'
                        'M117 Final warmup\n'
                        'M104 S[first_layer_temperature] ; set extruder final temp\n'
                        'M109 S[first_layer_temperature] ; wait for extruder final temp\n'
                        'M190 S[first_layer_bed_temperature] ; wait for bed final temp\n'
                        'M300 S440 P200     ; 1st beep for printer ready and allow some time to clean nozzle\n'
                        'M300 S0 P250       ; wait between dual beep\n'
                        'M300 S440 P200     ; 2nd beep for printer ready\n'
                        'G4 S10             ; wait to clean the nozzle\n'
                        'M300 S440 P200     ; 3rd beep for ready to start printing\n'
                        '; Prime line routine\n'
                        'M117 Printing prime line\n'
                        ';M900 K0; Disable Linear Advance (Marlin) for prime line\n'
                        'G92 E0.0; reset extrusion distance\n'
                        'G1 F3000 Z1\n'
                        'G1 X-150 Y0 Z0.4\n'
                        'G92 E0\n'
                        'G3 X0 Y-130 I150 Z0.3 E30 F2000\n'
                        'G92 E0.0 ; reset extrusion distance\n'
                        '; Final print adjustments\n'
                        'M117 Preparing to print\n'
                        ';M82 ; extruder absolute mode\n'
                        'M221 S{if layer_height<0.075}100{else}95{endif}\n'
                        'M300 S40 P10 ; chirp\n'
                        'M117 Print [input_filename_base]; Display: Printing started...',
 'machine_unload_filament_time': '0',
 'max_layer_height': ['0.2'],
 'min_layer_height': ['0.08'],
 'name': 'FLSun Super Racer 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'brass',
 'printable_area': ['134.486x11.766',
                    '132.949x23.4425',
                    '130.4x34.9406',
                    '126.859x46.1727',
                    '122.352x57.0535',
                    '116.913x67.5',
                    '110.586x77.4328',
                    '103.416x86.7763',
                    '95.4594x95.4594',
                    '86.7763x103.416',
                    '77.4328x110.586',
                    '67.5x116.913',
                    '57.0535x122.352',
                    '46.1727x126.859',
                    '34.9406x130.4',
                    '23.4425x132.949',
                    '11.766x134.486',
                    '8.26637e-15x135',
                    '-11.766x134.486',
                    '-23.4425x132.949',
                    '-34.9406x130.4',
                    '-46.1727x126.859',
                    '-57.0535x122.352',
                    '-67.5x116.913',
                    '-77.4328x110.586',
                    '-86.7763x103.416',
                    '-95.4594x95.4594',
                    '-103.416x86.7763',
                    '-110.586x77.4328',
                    '-116.913x67.5',
                    '-122.352x57.0535',
                    '-126.859x46.1727',
                    '-130.4x34.9406',
                    '-132.949x23.4425',
                    '-134.486x11.766',
                    '-135x1.65327e-14',
                    '-134.486x-11.766',
                    '-132.949x-23.4425',
                    '-130.4x-34.9406',
                    '-126.859x-46.1727',
                    '-122.352x-57.0535',
                    '-116.913x-67.5',
                    '-110.586x-77.4328',
                    '-103.416x-86.7763',
                    '-95.4594x-95.4594',
                    '-86.7763x-103.416',
                    '-77.4328x-110.586',
                    '-67.5x-116.913',
                    '-57.0535x-122.352',
                    '-46.1727x-126.859',
                    '-34.9406x-130.4',
                    '-23.4425x-132.949',
                    '-11.766x-134.486',
                    '-2.47991e-14x-135',
                    '11.766x-134.486',
                    '23.4425x-132.949',
                    '34.9406x-130.4',
                    '46.1727x-126.859',
                    '57.0535x-122.352',
                    '67.5x-116.913',
                    '77.4328x-110.586',
                    '86.7763x-103.416',
                    '95.4594x-95.4594',
                    '103.416x-86.7763',
                    '110.586x-77.4328',
                    '116.913x-67.5',
                    '122.352x-57.0535',
                    '126.859x-46.1727',
                    '130.4x-34.9406',
                    '132.949x-23.4425',
                    '134.486x-11.766',
                    '135x-3.30655e-14'],
 'printable_height': '330',
 'printer_model': 'FLSun Super Racer (SR)',
 'printer_technology': 'FFF',
 'printer_variant': '0.4',
 'printhost_apikey': '',
 'printhost_authorization_type': 'key',
 'printhost_cafile': '',
 'printhost_password': '',
 'printhost_port': '',
 'printhost_ssl_ignore_revoke': '0',
 'printhost_user': '',
 'retract_before_wipe': ['70%'],
 'retract_length_toolchange': ['2'],
 'retract_lift_above': ['0'],
 'retract_lift_below': ['0'],
 'retract_restart_extra': ['0'],
 'retract_restart_extra_toolchange': ['0'],
 'retract_when_changing_layer': ['1'],
 'retraction_length': ['6.5'],
 'retraction_minimum_travel': ['1'],
 'retraction_speed': ['40'],
 'setting_id': 'GM003',
 'template_custom_gcode': ';FILAMENT_CHANGE\nM600',
 'thumbnails': ['260x260'],
 'type': 'machine',
 'wipe': ['1'],
 'wipe_distance': ['1'],
 'z_hop': ['0.3'],
 'z_hop_types': ['Normal Lift']}
