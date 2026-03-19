from __future__ import annotations

# source: profiles/FlyingBear/machine/FlyingBear Ghost 6 0.4 nozzle.json
DATA = {'auxiliary_fan': '1',
 'change_filament_gcode': 'M600',
 'default_filament_profile': ['FlyingBear Generic PLA'],
 'default_print_profile': '0.20mm Standard @FlyingBear Ghost 6',
 'deretraction_speed': ['35'],
 'extruder_clearance_height_to_lid': '80',
 'extruder_clearance_height_to_rod': '64',
 'extruder_clearance_radius': '55',
 'from': 'system',
 'gcode_flavor': 'marlin2',
 'inherits': 'fdm_marlin_common',
 'instantiation': 'true',
 'machine_end_gcode': 'G91 ;use relative coordinates\n'
                      'G1 E-4 F1500 ;retract the filament\n'
                      'G1 X5 Y5 Z0.2 F5000 ;wipe\n'
                      'G1 Z5 F1500 ;raise z\n'
                      'G90 ;use absolute coordinates\n'
                      'G1 X10 Y210 F5000 ;park print head\n'
                      '\n'
                      'M107 ;turn off fan\n'
                      'M104 S0 ;turn off hotend\n'
                      'M140 S0 ;turn off heatbed\n'
                      'M84 ;disable motors',
 'machine_max_acceleration_e': ['2000', '2000'],
 'machine_max_acceleration_extruding': ['1500', '1500'],
 'machine_max_acceleration_retracting': ['3000', '3000'],
 'machine_max_acceleration_travel': ['2000', '2000'],
 'machine_max_acceleration_x': ['1500', '1500'],
 'machine_max_acceleration_y': ['1500', '1500'],
 'machine_max_acceleration_z': ['100', '100'],
 'machine_max_jerk_e': ['2.0', '2.0'],
 'machine_max_jerk_x': ['15', '15'],
 'machine_max_jerk_y': ['15', '15'],
 'machine_max_jerk_z': ['0.4', '0.4'],
 'machine_max_speed_e': ['45', '45'],
 'machine_max_speed_x': ['200', '200'],
 'machine_max_speed_y': ['200', '200'],
 'machine_max_speed_z': ['4', '4'],
 'machine_pause_gcode': 'M25',
 'machine_start_gcode': 'M220 S100 ;reset feedrate\n'
                        'M221 S100 ;reset flowrate\n'
                        'G21 ;set units to millimeters\n'
                        'G90 ;use absolute coordinates\n'
                        'M82 ;absolute extrusion mode\n'
                        'M107 ;turn off colling fan\n'
                        '\n'
                        'M140 S[bed_temperature_initial_layer] ;set bed temperature continue without waiting\n'
                        'M104 S[nozzle_temperature_initial_layer] ;set hotend temperature continue without waiting\n'
                        '\n'
                        'G28 ;home\n'
                        'G1 Z2 F1500 ;raise z\n'
                        'G92 E0 ;reset extruder\n'
                        '\n'
                        'M190 S[bed_temperature_initial_layer] ;wait for bed temperature\n'
                        'M109 S[nozzle_temperature_initial_layer] ;wait for hotend temperature\n'
                        '\n'
                        'G1 X20 Y20 F5000 ;start position \n'
                        'G1 Z0.28 F1500 ;lower z\n'
                        'G1 E4 F500 ;prime the filament\n'
                        '\n'
                        'G1 X20 Y20.0 Z0.28 F3000.0  ;start position \n'
                        'G1 X20 Y170.0 Z0.28 F1500.0 E12 ;1st line\n'
                        'G1 X20.3 F1500\n'
                        'G1 X20.3 Y20.0 Z0.28 F1500.0 E18 ;2nd line\n'
                        '\n'
                        'G92 E0 ;reset extruder\n'
                        'G1 Z2 F1500 ;raise z\n'
                        'G92 E0 ;reset extruder\n',
 'manual_filament_change': '1',
 'max_layer_height': ['0.3'],
 'min_layer_height': ['0.05'],
 'name': 'FlyingBear Ghost 6 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'brass',
 'printable_area': ['0x0', '255x0', '255x210', '0x210'],
 'printable_height': '210',
 'printer_model': 'FlyingBear Ghost 6',
 'printer_settings_id': '',
 'printer_variant': '0.4',
 'retract_before_wipe': ['0%'],
 'retract_length_toolchange': ['1'],
 'retraction_length': ['0.8'],
 'retraction_minimum_travel': ['3'],
 'retraction_speed': ['35'],
 'scan_first_layer': '0',
 'setting_id': 'GM001',
 'single_extruder_multi_material': '1',
 'support_air_filtration': '1',
 'support_multi_bed_types': '1',
 'thumbnails': ['100x100', '320x320'],
 'type': 'machine',
 'wipe_distance': ['2'],
 'z_hop': ['0.2']}
