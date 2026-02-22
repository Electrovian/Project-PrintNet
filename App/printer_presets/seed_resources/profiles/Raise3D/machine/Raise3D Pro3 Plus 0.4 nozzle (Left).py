from __future__ import annotations

# source: profiles/Raise3D/machine/Raise3D Pro3 Plus 0.4 nozzle (Left).json
DATA = {'auxiliary_fan': '0',
 'before_layer_change_gcode': '; before layer [layer_num] change\n'
                              '{if layer_z <= initial_layer_print_height + layer_height * 2}\n'
                              'M109 T0 S{nozzle_temperature_initial_layer[0]}\n'
                              'M140 S[bed_temperature_initial_layer_single]\n'
                              '{else}\n'
                              'M109 T0 S{nozzle_temperature[0]}\n'
                              'M140 S{bed_temperature[0]}\n'
                              '{endif}\n'
                              '{if (filament_type[0] =="PLA" or filament_type[0] =="PETG")}\n'
                              '{if layer_z >= initial_layer_print_height + layer_height * 2}\n'
                              'M106 P2 S150\n'
                              '{elsif layer_z >= initial_layer_print_height + layer_height * 1}\n'
                              'M106 P2 S100\n'
                              '{else}\n'
                              'M106 P2 S0\n'
                              '{endif}\n'
                              '{endif}',
 'change_filament_gcode': '',
 'default_filament_profile': ['Generic PLA @System'],
 'default_print_profile': '0.20mm Standard @Raise3D Pro3Plus',
 'deretraction_speed': ['0', '0'],
 'extruder_colour': ['#FCE94F', '#FCE94F'],
 'extruder_offset': ['0x0', '0x0'],
 'from': 'system',
 'inherits': 'fdm_machine_common',
 'instantiation': 'true',
 'layer_change_gcode': ';AFTER_LAYER_CHANGE\n;[layer_z]',
 'machine_end_gcode': 'M1002\n'
                      'M221 T0 S100\n'
                      'M104 S0\n'
                      'M140 S0\n'
                      'M107\n'
                      'M106 P2 S0\n'
                      'G91\n'
                      'G1 E-1 F300\n'
                      'G1 Z+0.5 E-5 X-20 Y-20 F9000.00\n'
                      'G28 X0 Y0\n'
                      'M84\n'
                      'G90\n',
 'machine_max_acceleration_e': ['3000', '3000'],
 'machine_max_acceleration_extruding': ['1000', '300'],
 'machine_max_acceleration_retracting': ['3000', '1500'],
 'machine_max_acceleration_travel': ['1500', '500'],
 'machine_max_acceleration_x': ['1000', '1000'],
 'machine_max_acceleration_y': ['1000', '1000'],
 'machine_max_acceleration_z': ['100', '100'],
 'machine_max_jerk_e': ['5', '5'],
 'machine_max_jerk_x': ['5', '5'],
 'machine_max_jerk_y': ['5', '5'],
 'machine_max_jerk_z': ['0.4', '0.4'],
 'machine_max_speed_e': ['120', '120'],
 'machine_max_speed_x': ['500', '200'],
 'machine_max_speed_y': ['500', '200'],
 'machine_max_speed_z': ['12', '12'],
 'machine_pause_gcode': '; pause print\nM2000',
 'machine_start_gcode': ';Bounding Box: {digits(first_layer_print_min[0],0,2)} '
                        '{if(first_layer_print_max[0]>300)}{300}{else}{digits(first_layer_print_max[0],0,2)}{endif} '
                        '{digits(first_layer_print_min[1],0,2)} '
                        '{if(first_layer_print_max[1]>300)}{300}{else}{digits(first_layer_print_max[1],0,2)}{endif}\n'
                        '\n'
                        'M104 T0 S{nozzle_temperature_initial_layer[0] - 20} ; raise left extruder temp\n'
                        'M140 S[bed_temperature_initial_layer_single] ; raise bed temp\n'
                        'M190 S{bed_temperature_initial_layer_single} ; wait for bed temp\n'
                        'M109 T0 S{nozzle_temperature_initial_layer[0] - 20} ; wait for left extruder temp\n'
                        'M104 T0 S[nozzle_temperature_initial_layer] ; set left extruder temp\n'
                        'M109 T0 S[nozzle_temperature_initial_layer] ; wait for left extruder temp\n'
                        'T0\n'
                        'G21\n'
                        'G90\n'
                        'M82\n'
                        'M107\n'
                        'M106 P2 S0\n'
                        'G1 Z0.3 F500\n'
                        'G92 E0\n'
                        'G1 Z0.3 F400\n'
                        'G1 X100 Y{random(2,8)} F1000\n'
                        'G1 X170 Y{random(2,8)} E15 F200\n'
                        'G1 Z5 E15 F200\n'
                        'G92 E0\n'
                        'G1 Z10 F2000 ; move up from purge line\n'
                        'G1 Y30 F2000 ; move away from purge line\n'
                        'G1 X{(first_layer_print_max[0] + first_layer_print_min[0])/2} Y{(first_layer_print_max[1] + '
                        'first_layer_print_min[1])/2} Z{initial_layer_print_height} ; move to center of print\n'
                        'M117 Printing...\n'
                        'M1001',
 'max_layer_height': ['0.4', '0.4'],
 'min_layer_height': ['0.1', '0.1'],
 'name': 'Raise3D Pro3 Plus 0.4 nozzle (Left)',
 'nozzle_diameter': ['0.4', '0.4'],
 'nozzle_type': 'hardened_steel',
 'printable_area': ['0x0', '340x0', '340x300', '0x300'],
 'printable_height': '605',
 'printer_model': 'Raise3D Pro3 Plus',
 'printer_settings_id': 'Raise3D',
 'retract_before_wipe': ['0%', '0%'],
 'retract_length_toolchange': ['2', '2'],
 'retract_restart_extra': ['0', '0'],
 'retract_restart_extra_toolchange': ['0', '0'],
 'retract_when_changing_layer': ['1', '1'],
 'retraction_length': ['0.5', '0.5'],
 'retraction_minimum_travel': ['0.6', '0.6'],
 'retraction_speed': ['40', '40'],
 'scan_first_layer': '0',
 'setting_id': 'GM001',
 'single_extruder_multi_material': '1',
 'toolchange_gcode': '; layer [layer_num] tool change',
 'type': 'machine',
 'wipe': ['1', '1']}
