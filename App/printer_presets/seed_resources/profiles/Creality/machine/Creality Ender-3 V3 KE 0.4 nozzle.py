from __future__ import annotations

# source: profiles/Creality/machine/Creality Ender-3 V3 KE 0.4 nozzle.json
DATA = {'auxiliary_fan': '0',
 'change_filament_gcode': 'M600',
 'default_filament_profile': ['Creality Generic PLA @Ender-3V3-all'],
 'default_print_profile': '0.20mm Standard @Creality Ender3V3KE',
 'deretraction_speed': ['0'],
 'extruder_clearance_height_to_rod': '47',
 'extruder_clearance_radius': '90',
 'from': 'system',
 'gcode_flavor': 'klipper',
 'inherits': 'fdm_creality_common',
 'instantiation': 'true',
 'machine_end_gcode': 'G92 E0 ;Reset Extruder\n'
                      'G1 E-1.2 Z{max_layer_z + 0.5} F1800 ;Retract and raise Z\n'
                      '{if max_layer_z < 50}\n'
                      'G1 Z{max_layer_z + 25} F900 ;Raise Z more\n'
                      '{endif}\n'
                      '\n'
                      'G1 X2 Y218 F3000 ;Present print\n'
                      'M106 S0 ;Turn-off fan\n'
                      'M104 S0 ;Turn-off hotend\n'
                      'M140 S0 ;Turn-off bed\n'
                      '\n'
                      'M84 X Y E ;Disable all steppers but Z',
 'machine_load_filament_time': '11',
 'machine_max_acceleration_extruding': ['8000', '8000'],
 'machine_max_acceleration_retracting': ['5000', '5000'],
 'machine_max_acceleration_travel': ['8000', '8000'],
 'machine_max_acceleration_x': ['8000', '8000'],
 'machine_max_acceleration_y': ['8000', '8000'],
 'machine_max_acceleration_z': ['300', '300'],
 'machine_max_jerk_e': ['5', '5'],
 'machine_max_jerk_x': ['7', '7'],
 'machine_max_jerk_y': ['7', '7'],
 'machine_max_jerk_z': ['0.4', '0.4'],
 'machine_max_speed_e': ['40', '40'],
 'machine_max_speed_x': ['500', '500'],
 'machine_max_speed_y': ['500', '500'],
 'machine_max_speed_z': ['30', '30'],
 'machine_pause_gcode': 'PAUSE',
 'machine_start_gcode': 'SET_GCODE_VARIABLE MACRO=PRINTER_PARAM VARIABLE=fan0_min VALUE=30 ;compensate for fan speed\n'
                        'SET_VELOCITY_LIMIT ACCEL_TO_DECEL=2500 ;revert accel_to_decel back to 2500\n'
                        'M220 S100 ;Reset Feedrate\n'
                        'M221 S100 ;Reset Flowrate\n'
                        '\n'
                        'M140 S[bed_temperature_initial_layer_single] ;Set bed temp\n'
                        'G28 X Y ;Home XY axes\n'
                        'M190 S[bed_temperature_initial_layer_single] ;Wait for bed temp to stabilize\n'
                        'G28 Z ;Home Z axis & load bed mesh\n'
                        'BED_MESH_CALIBRATE PROBE_COUNT=5,5 ;Auto bed level\n'
                        '\n'
                        'M104 S[nozzle_temperature_initial_layer] ;Set nozzle temp\n'
                        'G92 E0 ;Reset Extruder\n'
                        'G1 X-2.0 Y20 Z0.3 F5000.0 ;Move to start position\n'
                        'M109 S[nozzle_temperature_initial_layer] ;Wait for nozzle temp to stabilize\n'
                        'G1 Z0.2 ;Lower nozzle to printing height\n'
                        'G1 Y145.0 F1500.0 E15 ;Draw the first line\n'
                        'G1 X-1.7 F5000.0 ;Move to side a little\n'
                        'G1 Y30 F1500.0 E15 ;Draw the second line\n'
                        'G92 E0 ;Reset Extruder',
 'manual_filament_change': '1',
 'max_layer_height': ['0.32'],
 'min_layer_height': ['0.08'],
 'name': 'Creality Ender-3 V3 KE 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'brass',
 'printable_area': ['0x0', '220x0', '220x220', '0x220'],
 'printable_height': '245',
 'printer_model': 'Creality Ender-3 V3 KE',
 'printer_settings_id': 'Creality',
 'printer_structure': 'i3',
 'retract_before_wipe': ['100%'],
 'retract_length_toolchange': ['1'],
 'retraction_length': ['0.5'],
 'retraction_minimum_travel': ['2'],
 'retraction_speed': ['30'],
 'scan_first_layer': '0',
 'setting_id': 'GM001',
 'single_extruder_multi_material': '1',
 'thumbnails': ['96x96', '300x300'],
 'type': 'machine',
 'wipe_distance': ['2'],
 'z_hop': ['0.2']}
