from __future__ import annotations

# source: profiles/Qidi/machine/Qidi X-Plus 4 0.4 nozzle.json
DATA = {'bed_exclude_area': ['0x305',
                      '0x302',
                      '35x302',
                      '35x305',
                      '305x305',
                      '305x305',
                      '305x305',
                      '305x20',
                      '293x20',
                      '293x0',
                      '305x0',
                      '305x20',
                      '305x305'],
 'change_filament_gcode': '{if max_layer_z < 12}\n'
                          'G1 Z15 F1200\n'
                          '{else}\n'
                          'G1 Z{max_layer_z + 3.0} F1200\n'
                          '{endif}\n'
                          'TOOL_CHANGE_START F=[current_extruder] T=[next_extruder]\n'
                          'DISABLE_ALL_SENSOR\n'
                          '{if long_retractions_when_cut[previous_extruder]}\n'
                          'MOVE_TO_TRASH\n'
                          'G1 E-{retraction_distances_when_cut[previous_extruder]} F{old_filament_e_feedrate}\n'
                          'M400\n'
                          '{else}\n'
                          'G1 E-5 F{old_filament_e_feedrate}\n'
                          '{endif}\n'
                          'CUT_FILAMENT T=[current_extruder]\n'
                          'MOVE_TO_TRASH\n'
                          'M400\n'
                          '{if nozzle_temperature_range_high[current_extruder] >= '
                          'nozzle_temperature_range_high[next_extruder]}\n'
                          'M104 S{nozzle_temperature_range_high[current_extruder]}\n'
                          '{else}\n'
                          'M104 S{nozzle_temperature_range_high[next_extruder]}\n'
                          '{endif}\n'
                          'M106 S0\n'
                          'M106 P2 S0\n'
                          'UNLOAD_T[current_extruder]\n'
                          'G92 E0\n'
                          'M83\n'
                          'G1 E2 F50\n'
                          'T[next_extruder]\n'
                          '{if nozzle_temperature_range_high[current_extruder] >= '
                          'nozzle_temperature_range_high[next_extruder]}\n'
                          'SET_HEATER_TEMPERATURE HEATER=extruder '
                          'TARGET={nozzle_temperature_range_high[current_extruder]} WAIT=1\n'
                          '{else}\n'
                          'SET_HEATER_TEMPERATURE HEATER=extruder '
                          'TARGET={nozzle_temperature_range_high[next_extruder]} WAIT=1\n'
                          '{endif}\n'
                          '{if long_retractions_when_cut[previous_extruder]}\n'
                          'G1 E{retraction_distances_when_cut[previous_extruder]} F{old_filament_e_feedrate}\n'
                          '{endif}\n'
                          'M400\n'
                          'M106 S60\n'
                          '; FLUSH_START\n'
                          'G1 E1 F50\n'
                          'G1 E{65.5 * 0.58} F{old_filament_e_feedrate}\n'
                          'G1 E{65.5 * 0.02} F50\n'
                          'G1 E{65.5 * 0.18} F{old_filament_e_feedrate}\n'
                          'G1 E{65.5 * 0.02} F50\n'
                          'G1 E{65.5 * 0.18} F{old_filament_e_feedrate}\n'
                          'G1 E{65.5 * 0.02} F50\n'
                          'G1 E-[old_retract_length_toolchange] F1800\n'
                          '; FLUSH_END\n'
                          '{if flush_length_1 > 1}\n'
                          'M400\n'
                          'M106 S255\n'
                          'G91\n'
                          'G1 X-5 F60\n'
                          'G1 X5 F60\n'
                          'G90\n'
                          'CLEAR_FLUSH\n'
                          'M400\n'
                          'M106 S60\n'
                          '; FLUSH_START\n'
                          'G1 E[old_retract_length_toolchange] F300\n'
                          'G1 E{flush_length_1 * 0.58} F{new_filament_e_feedrate}\n'
                          'G1 E{flush_length_1 * 0.02} F50\n'
                          'G1 E{flush_length_1 * 0.18} F{new_filament_e_feedrate}\n'
                          'G1 E{flush_length_1 * 0.02} F50\n'
                          'G1 E{flush_length_1 * 0.18} F{new_filament_e_feedrate}\n'
                          'G1 E{flush_length_1 * 0.02} F50\n'
                          'G1 E-[old_retract_length_toolchange] F1800\n'
                          '; FLUSH_END\n'
                          '{endif}\n'
                          '{if flush_length_2 > 1}\n'
                          'M400\n'
                          'M106 S255\n'
                          'G91\n'
                          'G1 X-5 F60\n'
                          'G1 X5 F60\n'
                          'G90\n'
                          'CLEAR_FLUSH\n'
                          'M400\n'
                          'M106 S60\n'
                          '; FLUSH_START\n'
                          'G1 E[old_retract_length_toolchange] F300\n'
                          'G1 E{flush_length_2 * 0.58} F{new_filament_e_feedrate}\n'
                          'G1 E{flush_length_2 * 0.02} F50\n'
                          'G1 E{flush_length_2 * 0.18} F{new_filament_e_feedrate}\n'
                          'G1 E{flush_length_2 * 0.02} F50\n'
                          'G1 E{flush_length_2 * 0.18} F{new_filament_e_feedrate}\n'
                          'G1 E{flush_length_2 * 0.02} F50\n'
                          'G1 E-[new_retract_length_toolchange] F1800\n'
                          '; FLUSH_END\n'
                          '{endif}\n'
                          '{if flush_length_3 > 1}\n'
                          'M400\n'
                          'M106 S255\n'
                          'G91\n'
                          'G1 X-5 F60\n'
                          'G1 X5 F60\n'
                          'G90\n'
                          'CLEAR_FLUSH\n'
                          'M400\n'
                          'M106 S60\n'
                          '; FLUSH_START\n'
                          'G1 E[new_retract_length_toolchange] F300\n'
                          'G1 E{flush_length_3 * 0.58} F{new_filament_e_feedrate}\n'
                          'G1 E{flush_length_3 * 0.02} F50\n'
                          'G1 E{flush_length_3 * 0.18} F{new_filament_e_feedrate}\n'
                          'G1 E{flush_length_3 * 0.02} F50\n'
                          'G1 E{flush_length_3 * 0.18} F{new_filament_e_feedrate}\n'
                          'G1 E{flush_length_3 * 0.02} F50\n'
                          'G1 E-[new_retract_length_toolchange] F1800\n'
                          '; FLUSH_END\n'
                          '{endif}\n'
                          '{if flush_length_4 > 1}\n'
                          'M400\n'
                          'M106 S255\n'
                          'G91\n'
                          'G1 X-5 F60\n'
                          'G1 X5 F60\n'
                          'G90\n'
                          'CLEAR_FLUSH\n'
                          'M400\n'
                          'M106 S60\n'
                          '; FLUSH_START\n'
                          'G1 E[new_retract_length_toolchange] F300\n'
                          'G1 E{flush_length_4 * 0.58} F{new_filament_e_feedrate}\n'
                          'G1 E{flush_length_4 * 0.02} F50\n'
                          'G1 E{flush_length_4 * 0.18} F{new_filament_e_feedrate}\n'
                          'G1 E{flush_length_4 * 0.02} F50\n'
                          'G1 E{flush_length_4 * 0.18} F{new_filament_e_feedrate}\n'
                          'G1 E{flush_length_4 * 0.02} F50\n'
                          'G1 E-[new_retract_length_toolchange] F1800\n'
                          '; FLUSH_END\n'
                          '{endif}\n'
                          'M104 S[new_filament_temp]\n'
                          'M400\n'
                          'M106 S255\n'
                          'G91\n'
                          'G1 X-5 F60\n'
                          'G1 X5 F60\n'
                          'G90\n'
                          'M109 S[new_filament_temp]\n'
                          'G92 E0\n'
                          'M400\n'
                          'CLEAR_FLUSH\n'
                          'CLEAR_OOZE\n'
                          'M400\n'
                          'M106 S0\n'
                          'TOOL_CHANGE_END\n'
                          'G1 Y305 F9000\n'
                          'ENABLE_ALL_SENSOR',
 'default_filament_profile': ['Qidi Generic PLA @Qidi X-Plus 4 0.4 nozzle'],
 'default_print_profile': '0.20mm Standard @Qidi XPlus4',
 'deretraction_speed': ['0'],
 'extruder_clearance_height_to_lid': '135',
 'extruder_clearance_height_to_rod': '32',
 'extruder_clearance_radius': '72',
 'from': 'system',
 'gcode_flavor': 'klipper',
 'inherits': 'fdm_qidi_x3_common',
 'instantiation': 'true',
 'layer_change_gcode': '{if timelapse_type == 1} ; timelapse with wipe tower\n'
                       'G92 E0\n'
                       'G1 E-[retraction_length] F1800\n'
                       'G2 Z{layer_z + 0.4} I0.86 J0.86 P1 F20000 ; spiral lift a little\n'
                       'G1 Y304 F20000\n'
                       'G1 X95 F20000\n'
                       'G92 E0\n'
                       'M400\n'
                       'TIMELAPSE_TAKE_FRAME\n'
                       'G1 Y324 F5000\n'
                       'G1 E[retraction_length] F300\n'
                       'G1 X65 F5000\n'
                       'G1 Y290 F20000\n'
                       '{elsif timelapse_type == 0} ; timelapse without wipe tower\n'
                       'TIMELAPSE_TAKE_FRAME\n'
                       '{endif}\n'
                       'G92 E0\n'
                       'SET_PRINT_STATS_INFO CURRENT_LAYER={layer_num + 1}',
 'machine_end_gcode': 'DISABLE_BOX_HEATER\n'
                      'M141 S0\n'
                      'M140 S0\n'
                      'DISABLE_ALL_SENSOR\n'
                      'G1 E-3 F1800\n'
                      'G0 Z{max_layer_z + 3} F600\n'
                      'UNLOAD_FILAMENT T=[current_extruder]\n'
                      'G0 Y290 F12000\n'
                      'G0 X90 Y290 F12000\n'
                      '{if max_layer_z < max_print_height / 2}G1 Z{max_print_height / 2 + 10} F600{else}G1 '
                      'Z{min(max_print_height, max_layer_z + 3)}{endif}\n'
                      'M104 S0',
 'machine_max_acceleration_retracting': ['20000'],
 'machine_max_jerk_e': ['4'],
 'machine_max_jerk_x': ['9'],
 'machine_max_jerk_y': ['9'],
 'machine_max_jerk_z': ['4'],
 'machine_max_speed_z': ['20'],
 'machine_pause_gcode': 'M0',
 'machine_start_gcode': 'INIT_MAPPING_VALUE\n'
                        'PRINT_START BED=[bed_temperature_initial_layer_single] '
                        'HOTEND=[nozzle_temperature_initial_layer] CHAMBER=[chamber_temperature] '
                        'EXTRUDER=[initial_no_support_extruder]\n'
                        'SET_PRINT_STATS_INFO TOTAL_LAYER=[total_layer_count]\n'
                        'M83\n'
                        'M140 S[bed_temperature_initial_layer_single]\n'
                        'M104 S[nozzle_temperature_initial_layer]\n'
                        'M141 S[chamber_temperature]\n'
                        'G4 P3000\n'
                        'T[initial_tool]\n'
                        'G0 X{max((min(print_bed_max[0] - 12, first_layer_print_min[0] + 80) - 85), 0)} '
                        'Y{max((min(print_bed_max[1] - 3, first_layer_print_min[1] + 80) - 85), 0)} Z5 F6000\n'
                        'G0 Z[initial_layer_print_height] F600\n'
                        'G1 E3 F1800\n'
                        'G1 X{(min(print_bed_max[0] - 12, first_layer_print_min[0] + 80))} E{85 * 0.5 * '
                        'initial_layer_print_height * nozzle_diameter[0]} F3000\n'
                        'G1 Y{max((min(print_bed_max[1] - 3, first_layer_print_min[1] + 80) - 85), 0) + 2} E{2 * 0.5 * '
                        'initial_layer_print_height * nozzle_diameter[0]} F3000\n'
                        'G1 X{max((min(print_bed_max[0] - 12, first_layer_print_min[0] + 80) - 85), 0)} E{85 * 0.5 * '
                        'initial_layer_print_height * nozzle_diameter[0]} F3000\n'
                        'G1 Y{max((min(print_bed_max[1] - 3, first_layer_print_min[1] + 80) - 85), 0) + 85} E{83 * 0.5 '
                        '* initial_layer_print_height * nozzle_diameter[0]} F3000\n'
                        'G1 X{max((min(print_bed_max[0] - 12, first_layer_print_min[0] + 80) - 85), 0) + 2} E{2 * 0.5 '
                        '* initial_layer_print_height * nozzle_diameter[0]} F3000\n'
                        'G1 Y{max((min(print_bed_max[1] - 3, first_layer_print_min[1] + 80) - 85), 0) + 3} E{82 * 0.5 '
                        '* initial_layer_print_height * nozzle_diameter[0]} F3000\n'
                        'G1 X{max((min(print_bed_max[0] - 12, first_layer_print_min[0] + 80) - 85), 0) + 3} Z0\n'
                        'G1 X{max((min(print_bed_max[0] - 12, first_layer_print_min[0] + 80) - 85), 0) + 6}\n'
                        'G1 Z1 F600\n'
                        'SET_PRINT_STATS_INFO CURRENT_LAYER=1',
 'max_layer_height': ['0.32'],
 'min_layer_height': ['0.08'],
 'name': 'Qidi X-Plus 4 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'hardened_steel',
 'printable_area': ['0x0', '305x0', '305x305', '0x305'],
 'printable_height': '280',
 'printer_model': 'Qidi X-Plus 4',
 'printer_settings_id': 'Qidi',
 'retract_before_wipe': ['0%'],
 'retract_length_toolchange': ['2'],
 'retract_lift_below': ['279'],
 'retraction_length': ['0.8'],
 'retraction_minimum_travel': ['1'],
 'setting_id': 'GM001',
 'single_extruder_multi_material': '1',
 'thumbnails': ['272x272', '96x96'],
 'thumbnails_format': 'PNG',
 'time_lapse_gcode': '{if timelapse_type == 1} ; timelapse with wipe tower\n'
                     'G92 E0\n'
                     'G1 E-[retraction_length] F1800\n'
                     'G2 Z{layer_z + 0.4} I0.86 J0.86 P1 F20000 ; spiral lift a little\n'
                     'G1 Y304 F20000\n'
                     'G1 X95 F20000\n'
                     'G92 E0\n'
                     'M400\n'
                     'TIMELAPSE_TAKE_FRAME\n'
                     'G1 Y324 F5000\n'
                     'G1 E[retraction_length] F300\n'
                     'G1 X65 F5000\n'
                     'G1 Y290 F20000\n'
                     '{elsif timelapse_type == 0} ; timelapse without wipe tower\n'
                     'TIMELAPSE_TAKE_FRAME\n'
                     '{endif}',
 'type': 'machine',
 'wipe_distance': ['2']}
