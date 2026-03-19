from __future__ import annotations

# source: profiles/TwoTrees/machine/fdm_machine_common.json
DATA = {'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n',
 'change_filament_gcode': '',
 'default_print_profile': '0.16mm Optimal @Bambu Lab X1 Carbon 0.4 nozzle',
 'deretraction_speed': ['40'],
 'extruder_clearance_height_to_lid': '140',
 'extruder_clearance_height_to_rod': '36',
 'extruder_clearance_radius': '65',
 'extruder_colour': ['#FCE94F'],
 'extruder_offset': ['0x0'],
 'from': 'system',
 'gcode_flavor': 'marlin',
 'instantiation': 'false',
 'machine_end_gcode': 'M400 ; wait for buffer to clear\n'
                      'G92 E0 ; zero the extruder\n'
                      'G1 E-4.0 F3600; retract \n'
                      'G91\n'
                      'G1 Z3;\n'
                      'M104 S0 ; turn off hotend\n'
                      'M140 S0 ; turn off bed\n'
                      'M106 S0 ; turn off fan\n'
                      'G90 \n'
                      'G0 X110 Y200 F3600 \n'
                      'print_end',
 'machine_max_acceleration_e': ['5000'],
 'machine_max_acceleration_extruding': ['10000'],
 'machine_max_acceleration_retracting': ['1000'],
 'machine_max_acceleration_x': ['10000'],
 'machine_max_acceleration_y': ['10000'],
 'machine_max_acceleration_z': ['100'],
 'machine_max_jerk_e': ['5'],
 'machine_max_jerk_x': ['8'],
 'machine_max_jerk_y': ['8'],
 'machine_max_jerk_z': ['0.4'],
 'machine_max_speed_e': ['60'],
 'machine_max_speed_x': ['500'],
 'machine_max_speed_y': ['500'],
 'machine_max_speed_z': ['10'],
 'machine_min_extruding_rate': ['0'],
 'machine_min_travel_rate': ['0'],
 'machine_start_gcode': 'G0 Z20 F9000\n'
                        'G92 E0; G1 E-10 F1200\n'
                        'G28\n'
                        'M970 Q1 A10 B10 C130 K0\n'
                        'M970 Q1 A10 B131 C250 K1\n'
                        'M974 Q1 S1 P0\n'
                        'M970 Q0 A10 B10 C130 H20 K0\n'
                        'M970 Q0 A10 B131 C250 K1\n'
                        'M974 Q0 S1 P0\n'
                        'M220 S100 ;Reset Feedrate\n'
                        'M221 S100 ;Reset Flowrate\n'
                        'G29 ;Home\n'
                        'G90;\n'
                        'G92 E0 ;Reset Extruder \n'
                        'G1 Z2.0 F3000 ;Move Z Axis up \n'
                        'G1 X10.1 Y20 Z0.28 F5000.0 ;Move to start position\n'
                        'M109 S205;\n'
                        'G1 X10.1 Y200.0 Z0.28 F1500.0 E15 ;Draw the first line\n'
                        'G1 X10.4 Y200.0 Z0.28 F5000.0 ;Move to side a little\n'
                        'G1 X10.4 Y20 Z0.28 F1500.0 E30 ;Draw the second line\n'
                        'G92 E0 ;Reset Extruder \n'
                        'G1 X110 Y110 Z2.0 F3000 ;Move Z Axis up',
 'max_layer_height': ['0.32'],
 'min_layer_height': ['0.08'],
 'name': 'fdm_machine_common',
 'nozzle_diameter': ['0.4'],
 'printable_height': '400',
 'printer_settings_id': '',
 'printer_technology': 'FFF',
 'printer_variant': '0.4',
 'retract_before_wipe': ['70%'],
 'retract_length_toolchange': ['1'],
 'retract_restart_extra': ['0'],
 'retract_restart_extra_toolchange': ['0'],
 'retract_when_changing_layer': ['1'],
 'retraction_length': ['1'],
 'retraction_minimum_travel': ['2'],
 'retraction_speed': ['60'],
 'silent_mode': '0',
 'single_extruder_multi_material': '1',
 'type': 'machine',
 'wipe': ['1'],
 'z_hop': ['0']}
