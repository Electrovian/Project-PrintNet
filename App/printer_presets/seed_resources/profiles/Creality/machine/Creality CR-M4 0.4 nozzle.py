from __future__ import annotations

# source: profiles/Creality/machine/Creality CR-M4 0.4 nozzle.json
DATA = {'auxiliary_fan': '0',
 'default_filament_profile': ['Creality Generic PLA'],
 'default_print_profile': '0.20mm Standard @Creality CR-M4',
 'from': 'system',
 'gcode_flavor': 'marlin',
 'inherits': 'fdm_creality_common',
 'instantiation': 'true',
 'machine_end_gcode': 'G91 ;Relative positionning\n'
                      'G1 E-2 F2700 ;Retract a bit\n'
                      'G1 E-2 Z0.2 F2400 ;Retract and raise Z\n'
                      'G1 X5 Y5 F3000 ;Wipe out\n'
                      'G1 Z10 ;Raise Z more\n'
                      'G90 ;Absolute positionning\n'
                      'G1 X0 Y0 ;Present print\n'
                      'M106 S0 ;Turn-off fan\n'
                      'M104 S0 ;Turn-off hotend\n'
                      'M140 S0 ;Turn-off bed\n'
                      'M84 X Y E ;Disable all steppers but Z',
 'machine_max_acceleration_extruding': ['700', '700'],
 'machine_max_acceleration_z': ['100', '100'],
 'machine_max_jerk_x': ['10', '10'],
 'machine_max_jerk_y': ['10', '10'],
 'machine_max_speed_e': ['50', '50'],
 'machine_start_gcode': 'M220 S100 ;Reset Feedrate\n'
                        'M221 S100 ;Reset Flowrate\n'
                        'M140 S[bed_temperature_initial_layer_single] ; set final bed temp\n'
                        'G28 ;Home\n'
                        'G92 E0 ;Reset Extruder\n'
                        'G1 Z2.0 F3000 ;Move Z Axis up\n'
                        'G1 X10.1 Y20 Z0.28 F5000.0 ;Move to start position\n'
                        'M104 S[nozzle_temperature_initial_layer] ; set final nozzle temp\n'
                        'M190 S[bed_temperature_initial_layer_single] ; wait for bed temp to stabilize\n'
                        'M109 S[nozzle_temperature_initial_layer] ; wait for nozzle temp to stabilize\n'
                        'G1 X10.1 Y145.0 Z0.28 F1500.0 E15 ;Draw the first line\n'
                        'G1 X10.4 Y145.0 Z0.28 F5000.0 ;Move to side a little\n'
                        'G1 X10.4 Y20 Z0.28 F1500.0 E30 ;Draw the second line\n'
                        'G92 E0 ;Reset Extruder\n'
                        'G1 E-1.0000 F1800 ;Retract a bit\n'
                        'G1 Z2.0 F3000 ;Move Z Axis up\n'
                        'G1 E0.0000 F1800',
 'name': 'Creality CR-M4 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'undefine',
 'printable_area': ['0x0', '450x0', '450x450', '0x450'],
 'printable_height': '470',
 'printer_model': 'Creality CR-M4',
 'printer_structure': 'i3',
 'retraction_length': ['0.8'],
 'retraction_minimum_travel': ['0.8'],
 'retraction_speed': ['40'],
 'setting_id': 'GM001',
 'type': 'machine'}
