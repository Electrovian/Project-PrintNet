from __future__ import annotations

# source: profiles/Creality/machine/Creality Ender-3 V2 Neo 0.4 nozzle.json
DATA = {'auxiliary_fan': '0',
 'default_filament_profile': ['Creality Generic PLA'],
 'default_print_profile': '0.20mm Standard @Creality Ender3V2 Neo',
 'from': 'system',
 'inherits': 'fdm_creality_common',
 'instantiation': 'true',
 'machine_end_gcode': 'G91 ;Relative positionning\n'
                      'G1 E-2 F2700 ;Retract a bit\n'
                      'G1 E-2 Z0.2 F2400 ;Retract and raise Z\n'
                      'G1 X5 Y5 F3000 ;Wipe out\n'
                      'G1 Z10 ;Raise Z more\n'
                      'G90 ;Absolute positionning\n'
                      '\n'
                      'G1 X0 Y0 ;Present print\n'
                      'M106 S0 ;Turn-off fan\n'
                      'M104 S0 ;Turn-off hotend\n'
                      'M140 S0 ;Turn-off bed\n'
                      '\n'
                      'M84 X Y E ;Disable all steppers but Z',
 'machine_max_acceleration_extruding': ['5000', '5000'],
 'machine_max_acceleration_retracting': ['5000', '5000'],
 'machine_max_acceleration_travel': ['500', '500'],
 'machine_max_acceleration_x': ['500', '500'],
 'machine_max_acceleration_y': ['500', '500'],
 'machine_max_acceleration_z': ['100', '100'],
 'machine_max_jerk_e': ['5', '5'],
 'machine_max_jerk_x': ['10', '10'],
 'machine_max_jerk_y': ['10', '10'],
 'machine_max_jerk_z': ['0.4', '0.4'],
 'machine_max_speed_e': ['50', '50'],
 'machine_max_speed_x': ['500', '500'],
 'machine_max_speed_y': ['500', '500'],
 'machine_max_speed_z': ['10', '10'],
 'machine_start_gcode': 'M220 S100 ;Reset Feedrate\n'
                        'M221 S100 ;Reset Flowrate\n'
                        'M140 S[bed_temperature_initial_layer_single] ;Set final bed temp\n'
                        'M104 S[nozzle_temperature_initial_layer] ;Set final nozzle temp\n'
                        '\n'
                        'G28 ;Home\n'
                        'G29 ;Auto bed leveling (create mesh if not already stored)\n'
                        'M420 S1 ;Enable mesh leveling\n'
                        '\n'
                        'G92 E0 ;Reset Extruder\n'
                        'G1 Z2.0 F3000 ;Move Z Axis up\n'
                        'G1 X10.1 Y20 Z0.28 F5000.0 ;Move to start position\n'
                        'M190 S[bed_temperature_initial_layer_single] ;Wait for bed temp to stabilize\n'
                        'M109 S[nozzle_temperature_initial_layer] ;Wait for nozzle temp to stabilize\n'
                        'G1 X10.1 Y145.0 Z0.28 F1500.0 E15 ;Draw the first line\n'
                        'G1 X10.4 Y145.0 Z0.28 F5000.0 ;Move to side a little\n'
                        'G1 X10.4 Y20 Z0.28 F1500.0 E30 ;Draw the second line\n'
                        'G92 E0  ;Reset Extruder\n'
                        'G1 E-1.0000 F1800 ;Retract a bit\n'
                        'G1 Z2.0 F3000 ;Move Z Axis up\n'
                        'G1 E0.0000 F1800',
 'name': 'Creality Ender-3 V2 Neo 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'brass',
 'printable_area': ['0x0', '220x0', '220x220', '0x220'],
 'printable_height': '250',
 'printer_model': 'Creality Ender-3 V2 Neo',
 'printer_structure': 'i3',
 'setting_id': 'GM001',
 'thumbnails': ['200x200'],
 'thumbnails_format': 'JPG',
 'type': 'machine'}
