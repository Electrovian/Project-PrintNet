from __future__ import annotations

# source: profiles/BIQU/machine/BIQU B1 (0.4 nozzle).json
DATA = {'auxiliary_fan': '0',
 'default_print_profile': '0.20mm Standard @BIQU B1 (0.4 nozzle)',
 'deretraction_speed': ['70'],
 'from': 'system',
 'gcode_flavor': 'marlin',
 'inherits': 'fdm_biqu_common',
 'instantiation': 'true',
 'machine_end_gcode': ';BIQU B1 Default End Gcode\n'
                      'G91;Relative positioning\n'
                      'G1 E-2 F2700;Retract a bit\n'
                      'G1 E-2 Z0.2 F2400;Retract a bit more and raise Z\n'
                      'G1 X5 Y5 F3000;Wipe out\n'
                      'G1 Z10;Raise Z by 10mm\n'
                      'G90;Return to absolute positioning\n'
                      'G1 X0 Y{print_bed_max[1]};\n'
                      'M106 S0;Turn-off fan\n'
                      'M104 S0;Turn-off hotend\n'
                      'M140 S0;Turn-off bed\n'
                      'M84 X Y E;Disable all steppers but Z',
 'machine_max_acceleration_e': ['10000'],
 'machine_max_acceleration_extruding': ['1000'],
 'machine_max_acceleration_retracting': ['1000'],
 'machine_max_acceleration_x': ['1000'],
 'machine_max_acceleration_y': ['1000'],
 'machine_max_acceleration_z': ['100'],
 'machine_max_jerk_e': ['5'],
 'machine_max_jerk_x': ['10'],
 'machine_max_jerk_y': ['10'],
 'machine_max_jerk_z': ['0.3'],
 'machine_max_speed_e': ['60'],
 'machine_max_speed_x': ['500'],
 'machine_max_speed_y': ['500'],
 'machine_max_speed_z': ['10'],
 'machine_start_gcode': '; BIQU B1 Start G-code\n'
                        'M117 Getting the bed up to temp!\n'
                        'M140 S[first_layer_bed_temperature]; Set Heat Bed temperature\n'
                        'M190 S[first_layer_bed_temperature]; Wait for Heat Bed temperature\n'
                        'M117 Getting the extruder up to temp!\n'
                        'M104 S[first_layer_temperature]; Set Extruder temperature\n'
                        'G92 E0; Reset Extruder\n'
                        'M117 Homing axes\n'
                        'G28; Home all axes\n'
                        'M109 S[first_layer_temperature]; Wait for Extruder temperature\n'
                        'G1 Z2.0 F3000; Move Z Axis up little to prevent scratching of Heat Bed\n'
                        'G1 X4.1 Y20 Z0.3 F5000.0; Move to start position\n'
                        'M117 Purging\n'
                        'G1 X4.1 Y200.0 Z0.3 F1500.0 E15; Draw the first line\n'
                        'G1 X4.4 Y200.0 Z0.3 F5000.0; Move to side a little\n'
                        'G1 X4.4 Y20 Z0.3 F1500.0 E30; Draw the second line\n'
                        'G92 E0; Reset Extruder\n'
                        'M117 Lets make\n'
                        'G1 Z2.0 F3000; Move Z Axis up little to prevent scratching of Heat Bed\n'
                        'G1 X5 Y20 Z0.3 F5000.0; Move over to prevent blob squish',
 'max_layer_height': ['0.32'],
 'min_layer_height': ['0.10'],
 'name': 'BIQU B1 (0.4 nozzle)',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'undefine',
 'printable_area': ['0x0', '235x0', '235x235', '0x235'],
 'printable_height': '270',
 'printer_model': 'BIQU B1',
 'printer_variant': '0.4',
 'retraction_length': ['7'],
 'retraction_minimum_travel': ['1.5'],
 'retraction_speed': ['70'],
 'setting_id': 'GM001',
 'type': 'machine'}
