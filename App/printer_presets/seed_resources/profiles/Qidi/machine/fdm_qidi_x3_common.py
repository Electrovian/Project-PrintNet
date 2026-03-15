from __future__ import annotations

# source: profiles/Qidi/machine/fdm_qidi_x3_common.json
DATA = {'auxiliary_fan': '1',
 'change_filament_gcode': '',
 'from': 'system',
 'gcode_flavor': 'klipper',
 'inherits': 'fdm_machine_common',
 'instantiation': 'false',
 'machine_end_gcode': 'M141 S0\n'
                      'M104 S0\n'
                      'M140 S0\n'
                      'G1 E-3 F1800\n'
                      'G0 Z{min(max_print_height, max_layer_z + 3)} F600\n'
                      'G0 X0 Y0 F12000\n'
                      '{if max_layer_z < max_print_height / 2}G1 Z{max_print_height / 2 + 10} F600{else}G1 '
                      'Z{min(max_print_height, max_layer_z + 3)}{endif}',
 'machine_pause_gcode': 'M0',
 'machine_start_gcode': 'PRINT_START\n'
                        'G28\n'
                        'M141 S0\n'
                        'G0 Z50 F600\n'
                        'M190 S[hot_plate_temp_initial_layer]\n'
                        'G28 Z\n'
                        'G29; mesh bed leveling ,comment this code to close it\n'
                        'G0 X0 Y0 Z50 F6000\n'
                        'M141 S{overall_chamber_temperature}\n'
                        'M109 S[nozzle_temperature_initial_layer]\n'
                        'M106 P3 S255\n'
                        'M83\n'
                        'G4 P3000\n'
                        'G0 X{max((min(print_bed_max[0], first_layer_print_min[0] + 80) - 85),0)} '
                        'Y{max((min(print_bed_max[1], first_layer_print_min[1] + 80) - 85),0)} Z5 F6000\n'
                        'G0 Z[initial_layer_print_height] F600\n'
                        'G1 E3 F1800\n'
                        'G1 X{(min(print_bed_max[0], first_layer_print_min[0] + 80))} E{85 * 0.5 * '
                        'initial_layer_print_height * nozzle_diameter[0]} F3000\n'
                        'G1 Y{max((min(print_bed_max[1], first_layer_print_min[1] + 80) - 85),0) + 2} E{2 * 0.5 * '
                        'initial_layer_print_height * nozzle_diameter[0]} F3000\n'
                        'G1 X{max((min(print_bed_max[0], first_layer_print_min[0] + 80) - 85),0)} E{85 * 0.5 * '
                        'initial_layer_print_height * nozzle_diameter[0]} F3000\n'
                        'G1 Y{max((min(print_bed_max[1], first_layer_print_min[1] + 80) - 85),0) + 85} E{83 * 0.5 * '
                        'initial_layer_print_height * nozzle_diameter[0]} F3000\n'
                        'G1 X{max((min(print_bed_max[0], first_layer_print_min[0] + 80) - 85),0) + 2} E{2 * 0.5 * '
                        'initial_layer_print_height * nozzle_diameter[0]} F3000\n'
                        'G1 Y{max((min(print_bed_max[1], first_layer_print_min[1] + 80) - 85),0) + 3} E{82 * 0.5 * '
                        'initial_layer_print_height * nozzle_diameter[0]} F3000\n'
                        'G1 X{max((min(print_bed_max[0], first_layer_print_min[0] + 80) - 85),0) + 12} E{-10 * 0.5 * '
                        'initial_layer_print_height * nozzle_diameter[0]} F3000\n'
                        'G1 E{10 * 0.5 * initial_layer_print_height * nozzle_diameter[0]} F3000\n',
 'name': 'fdm_qidi_x3_common',
 'retraction_length': ['1'],
 'retraction_speed': ['30'],
 'scan_first_layer': '0',
 'support_chamber_temp_control': '1',
 'thumbnails': ['380x380/COLPIC', '210x210/COLPIC', '110x110/PNG'],
 'type': 'machine',
 'z_hop': ['0.4']}
