from __future__ import annotations

# source: profiles/Qidi/machine/Qidi Q2 0.4 nozzle.json
DATA = {'bed_exclude_area': ['0x0,11x0,11x16,0x16'],
 'box_id': '1',
 'change_filament_gcode': 'G1 Z{max_layer_z + 3.0} F1200\n'
                          'TOOL_CHANGE_START F=[current_extruder] T=[next_extruder]\n'
                          'BUFFER_MONITORING ENABLE=0\n'
                          'DISABLE_ALL_SENSOR\n'
                          'M106 S255\n'
                          'MOVE_TO_TRASH\n'
                          '{if long_retractions_when_cut[previous_extruder]}\n'
                          'G1 E-{retraction_distances_when_cut[previous_extruder]} F{old_filament_e_feedrate}\n'
                          '{else}\n'
                          'G1 E-10 F{old_filament_e_feedrate}\n'
                          '{endif}\n'
                          'M400\n'
                          'CUT_FILAMENT T=[current_extruder]\n'
                          'MOVE_TO_TRASH\n'
                          'M106 P2 S0\n'
                          'UNLOAD_T[current_extruder]\n'
                          'T[next_extruder]\n'
                          '{if nozzle_temperature_range_high[current_extruder] >= '
                          'nozzle_temperature_range_high[next_extruder]}\n'
                          'M104 S{nozzle_temperature_range_high[current_extruder]}\n'
                          '{else}\n'
                          'M104 S{nozzle_temperature_range_high[next_extruder]}\n'
                          '{endif}\n'
                          '; FLUSH_START\n'
                          'M106 S25\n'
                          'G1 E30 F300\n'
                          '; FLUSH_END\n'
                          '{if long_retractions_when_cut[previous_extruder]}\n'
                          'G1 E{retraction_distances_when_cut[previous_extruder]} F{old_filament_e_feedrate}\n'
                          '{endif}\n'
                          '{if flush_length_1 > 1}\n'
                          '; FLUSH_START\n'
                          '{if flush_length_1 > 23.7}\n'
                          'G1 E23.7 F{old_filament_e_feedrate}\n'
                          'G1 E{(flush_length_1 - 23.7) * 0.02} F50\n'
                          'G1 E{(flush_length_1 - 23.7) * 0.23} F{old_filament_e_feedrate}\n'
                          'G1 E{(flush_length_1 - 23.7) * 0.02} F50\n'
                          'G1 E{(flush_length_1 - 23.7) * 0.23} F{new_filament_e_feedrate}\n'
                          'G1 E{(flush_length_1 - 23.7) * 0.02} F50\n'
                          'G1 E{(flush_length_1 - 23.7) * 0.23} F{new_filament_e_feedrate}\n'
                          'G1 E{(flush_length_1 - 23.7) * 0.02} F50\n'
                          'G1 E{(flush_length_1 - 23.7) * 0.23} F{new_filament_e_feedrate}\n'
                          '{else}\n'
                          'G1 E{flush_length_1} F{old_filament_e_feedrate}\n'
                          '{endif}\n'
                          'G1 E-[old_retract_length_toolchange] F1800\n'
                          '; FLUSH_END\n'
                          '{endif}\n'
                          '{if flush_length_2 > 1}\n'
                          '; FLUSH_START\n'
                          'G1 X92 F9000\n'
                          'G1 E[old_retract_length_toolchange] F300\n'
                          'G1 E{flush_length_2 * 0.18} F{new_filament_e_feedrate}\n'
                          'G1 E{flush_length_2 * 0.02} F50\n'
                          'G1 E{flush_length_2 * 0.18} F{new_filament_e_feedrate}\n'
                          'G1 E{flush_length_2 * 0.02} F50\n'
                          'G1 E{flush_length_2 * 0.18} F{new_filament_e_feedrate}\n'
                          'G1 E{flush_length_2 * 0.02} F50\n'
                          'G1 E{flush_length_2 * 0.18} F{new_filament_e_feedrate}\n'
                          'G1 E{flush_length_2 * 0.02} F50\n'
                          'G1 E{flush_length_2 * 0.18} F{new_filament_e_feedrate}\n'
                          'G1 E{flush_length_2 * 0.02} F50\n'
                          'G1 E-[new_retract_length_toolchange] F1800\n'
                          '; FLUSH_END\n'
                          '{endif}\n'
                          '{if flush_length_3 > 1}\n'
                          '; FLUSH_START\n'
                          'G1 X85 F9000\n'
                          'G1 E[new_retract_length_toolchange] F300\n'
                          'G1 E{flush_length_3 * 0.18} F{new_filament_e_feedrate}\n'
                          'G1 E{flush_length_3 * 0.02} F50\n'
                          'G1 E{flush_length_3 * 0.18} F{new_filament_e_feedrate}\n'
                          'G1 E{flush_length_3 * 0.02} F50\n'
                          'G1 E{flush_length_3 * 0.18} F{new_filament_e_feedrate}\n'
                          'G1 E{flush_length_3 * 0.02} F50\n'
                          'G1 E{flush_length_3 * 0.18} F{new_filament_e_feedrate}\n'
                          'G1 E{flush_length_3 * 0.02} F50\n'
                          'G1 E{flush_length_3 * 0.18} F{new_filament_e_feedrate}\n'
                          'G1 E{flush_length_3 * 0.02} F50\n'
                          'G1 E-[new_retract_length_toolchange] F1800\n'
                          '; FLUSH_END\n'
                          '{endif}\n'
                          '{if flush_length_4 > 1}\n'
                          '; FLUSH_START\n'
                          'G1 X92 F9000\n'
                          'G1 E[new_retract_length_toolchange] F300\n'
                          'G1 E{flush_length_4 * 0.18} F{new_filament_e_feedrate}\n'
                          'G1 E{flush_length_4 * 0.02} F50\n'
                          'G1 E{flush_length_4 * 0.18} F{new_filament_e_feedrate}\n'
                          'G1 E{flush_length_4 * 0.02} F50\n'
                          'G1 E{flush_length_4 * 0.18} F{new_filament_e_feedrate}\n'
                          'G1 E{flush_length_4 * 0.02} F50\n'
                          'G1 E{flush_length_4 * 0.18} F{new_filament_e_feedrate}\n'
                          'G1 E{flush_length_4 * 0.02} F50\n'
                          'G1 E{flush_length_4 * 0.18} F{new_filament_e_feedrate}\n'
                          'G1 E{flush_length_4 * 0.02} F50\n'
                          'G1 E-[new_retract_length_toolchange] F1800\n'
                          '; FLUSH_END\n'
                          '{endif}\n'
                          'M400\n'
                          'M106 S255\n'
                          'M104 S[new_filament_temp]\n'
                          'INIT_SYNC_BUFFER_STATE\n'
                          'BUFFER_MONITORING ENABLE=1\n'
                          'G1 E10 F25 \n'
                          'M109 S[new_filament_temp]\n'
                          'G1 E-5 F1800\n'
                          'CLEAR_OOZE\n'
                          'TOOL_CHANGE_END\n'
                          'G1 Y270 F8000\n'
                          'M106 S0\n'
                          'G1 E2 F1800\n'
                          'ENABLE_ALL_SENSOR\n',
 'cooling_tube_length': '0',
 'cooling_tube_retraction': '0',
 'default_filament_profile': ['QIDI PLA Rapido @Qidi Q2 0.4 nozzle'],
 'default_print_profile': '0.20mm Standard @Qidi Q2',
 'enable_long_retraction_when_cut': '2',
 'extra_loading_move': '5',
 'extruder_clearance_height_to_lid': '120',
 'extruder_clearance_height_to_rod': '40',
 'extruder_clearance_radius': '70',
 'from': 'system',
 'gcode_flavor': 'klipper',
 'inherits': 'fdm_q_common',
 'instantiation': 'true',
 'is_support_3mf': '1',
 'is_support_multi_box': '1',
 'is_support_timelapse': '1',
 'layer_change_gcode': '{if timelapse_type == 1} ; timelapse with wipe tower\n'
                       'G92 E0\n'
                       'G1 E-[retraction_length] F1800\n'
                       'G2 Z{layer_z + 0.4} I0.86 J0.86 P1 F20000 ; spiral lift a little\n'
                       'G1 Y235 F20000\n'
                       'G1 X97 F20000\n'
                       '{if layer_z <=25}\n'
                       'G1 Z25\n'
                       '{endif}\n'
                       'G1 Y254 F2000\n'
                       'G92 E0\n'
                       'M400\n'
                       'TIMELAPSE_TAKE_FRAME\n'
                       'G1 E[retraction_length] F300\n'
                       'G1 X85 F2000\n'
                       'G1 X97 F2000\n'
                       'G1 Y220 F2000\n'
                       '{if layer_z <=25}\n'
                       'G1 Z[layer_z]\n'
                       '{endif}\n'
                       '{elsif timelapse_type == 0} ; timelapse without wipe tower\n'
                       'TIMELAPSE_TAKE_FRAME\n'
                       '{endif}\n'
                       'G92 E0\n'
                       'SET_PRINT_STATS_INFO CURRENT_LAYER={layer_num + 1}',
 'machine_end_gcode': 'DISABLE_BOX_HEATER\n'
                      'M141 S0\n'
                      'M140 S0\n'
                      'BUFFER_MONITORING ENABLE=0\n'
                      'DISABLE_ALL_SENSOR\n'
                      'G1 E-3 F1800\n'
                      'G0 Z{max_layer_z + 3} F600\n'
                      'UNLOAD_FILAMENT T=[current_extruder]\n'
                      'G0 Y270 F12000\n'
                      'G0 X90 Y270 F12000\n'
                      '{if max_layer_z < max_print_height / 2}G1 Z{max_print_height / 2 + 10} F600{else}G1 '
                      'Z{min(max_print_height, max_layer_z + 3)}{endif}\n'
                      'M104 S0',
 'machine_load_filament_time': '35',
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
                        'G1 X108.000 Y1 F30000\n'
                        'G0 Z[initial_layer_print_height] F600\n'
                        ';G1 E3 F1800\n'
                        'G90\n'
                        'M83\n'
                        'G0 X128 E8  F{outer_wall_volumetric_speed/(24/20)    * 60}\n'
                        'G0 X133 E.3742  F{outer_wall_volumetric_speed/(0.3*0.5)/4     * 60}\n'
                        'G0 X138 E.3742  F{outer_wall_volumetric_speed/(0.3*0.5)     * 60}\n'
                        'G0 X143 E.3742  F{outer_wall_volumetric_speed/(0.3*0.5)/4     * 60}\n'
                        'G0 X148 E.3742  F{outer_wall_volumetric_speed/(0.3*0.5)     * 60}\n'
                        'G0 X153 E.3742  F{outer_wall_volumetric_speed/(0.3*0.5)/4     * 60}\n'
                        'G91\n'
                        'G1 X1 Z-0.300\n'
                        'G1 X4\n'
                        'G1 Z1 F1200\n'
                        'G90\n'
                        'M400\n'
                        'G1 X108.000 Y2.5 F30000\n'
                        'G0 Z[initial_layer_print_height] F600\n'
                        'M83\n'
                        'G0 X128 E10  F{outer_wall_volumetric_speed/(24/20)    * 60}\n'
                        'G0 X133 E.3742  F{outer_wall_volumetric_speed/(0.3*0.5)/4     * 60}\n'
                        'G0 X138 E.3742  F{outer_wall_volumetric_speed/(0.3*0.5)     * 60}\n'
                        'G0 X143 E.3742  F{outer_wall_volumetric_speed/(0.3*0.5)/4     * 60}\n'
                        'G0 X148 E.3742  F{outer_wall_volumetric_speed/(0.3*0.5)     * 60}\n'
                        'G0 X153 E.3742  F{outer_wall_volumetric_speed/(0.3*0.5)/4     * 60}\n'
                        'G91\n'
                        'G1 X1 Z-0.300\n'
                        'G1 X4\n'
                        'G1 Z1 F1200\n'
                        'G90\n'
                        'M400\n'
                        'G1 Z1 F600',
 'machine_unload_filament_time': '35',
 'name': 'Qidi Q2 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_volume': ['125'],
 'parking_pos_retraction': '0',
 'printable_area': ['0x0', '270x0', '270x270', '0x270'],
 'printable_height': '256',
 'printer_model': 'Qidi Q2',
 'printer_settings_id': 'Qidi',
 'retract_lift_below': ['259'],
 'setting_id': 'GM001',
 'support_box_temp_control': '1',
 'thumbnail_size': ['50x50'],
 'thumbnails_format': 'PNG',
 'type': 'machine'}
