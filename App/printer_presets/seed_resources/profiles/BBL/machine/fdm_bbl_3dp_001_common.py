from __future__ import annotations

# source: profiles/BBL/machine/fdm_bbl_3dp_001_common.json
DATA = {'bed_exclude_area': ['0x0', '28x0', '28x28', '0x28', '0x28', '8x28', '8x256', '0x256'],
 'change_filament_gcode': 'M620 S[next_extruder]A\n'
                          'M204 S9000\n'
                          'G1 Z{max_layer_z + 3.0} F1200\n'
                          '\n'
                          'G1 X70 F21000\n'
                          'G1 Y245\n'
                          'G1 Y265 F3000\n'
                          'M400\n'
                          'M106 P1 S0\n'
                          'M106 P2 S0\n'
                          '{if old_filament_temp > 142 && next_extruder < 255}\n'
                          'M104 S[old_filament_temp]\n'
                          '{endif}\n'
                          'G1 X90 F3000\n'
                          'G1 Y255 F4000\n'
                          'G1 X100 F5000\n'
                          'G1 X120 F15000\n'
                          '\n'
                          'G1 X20 Y50 F21000\n'
                          'G1 Y-3\n'
                          '{if toolchange_count == 2}\n'
                          '; get travel path for change filament\n'
                          'M620.1 X[travel_point_1_x] Y[travel_point_1_y] F21000 P0\n'
                          'M620.1 X[travel_point_2_x] Y[travel_point_2_y] F21000 P1\n'
                          'M620.1 X[travel_point_3_x] Y[travel_point_3_y] F21000 P2\n'
                          '{endif}\n'
                          'M620.1 E F[old_filament_e_feedrate] T{nozzle_temperature_range_high[previous_extruder]}\n'
                          'T[next_extruder]\n'
                          'M620.1 E F[new_filament_e_feedrate] T{nozzle_temperature_range_high[next_extruder]}\n'
                          '\n'
                          '{if next_extruder < 255}\n'
                          'M400\n'
                          '\n'
                          'G92 E0\n'
                          '{if flush_length_1 > 1}\n'
                          '; FLUSH_START\n'
                          '; always use highest temperature to flush\n'
                          'M400\n'
                          'M109 S[nozzle_temperature_range_high]\n'
                          '{if flush_length_1 > 23.7}\n'
                          'G1 E23.7 F{old_filament_e_feedrate} ; do not need pulsatile flushing for start part\n'
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
                          '; FLUSH_END\n'
                          'G1 E-[old_retract_length_toolchange] F1800\n'
                          'G1 E[old_retract_length_toolchange] F300\n'
                          '{endif}\n'
                          '\n'
                          '{if flush_length_2 > 1}\n'
                          '; FLUSH_START\n'
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
                          '; FLUSH_END\n'
                          'G1 E-[new_retract_length_toolchange] F1800\n'
                          'G1 E[new_retract_length_toolchange] F300\n'
                          '{endif}\n'
                          '\n'
                          '{if flush_length_3 > 1}\n'
                          '; FLUSH_START\n'
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
                          '; FLUSH_END\n'
                          'G1 E-[new_retract_length_toolchange] F1800\n'
                          'G1 E[new_retract_length_toolchange] F300\n'
                          '{endif}\n'
                          '\n'
                          '{if flush_length_4 > 1}\n'
                          '; FLUSH_START\n'
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
                          '; FLUSH_END\n'
                          '{endif}\n'
                          '; FLUSH_START\n'
                          'M400\n'
                          'M109 S[new_filament_temp]\n'
                          'G1 E2 F{new_filament_e_feedrate} ;Compensate for filament spillage during waiting '
                          'temperature\n'
                          '; FLUSH_END\n'
                          'M400\n'
                          'G92 E0\n'
                          'G1 E-[new_retract_length_toolchange] F1800\n'
                          'M106 P1 S255\n'
                          'M400 S3\n'
                          'G1 X80 F15000\n'
                          'G1 X60 F15000\n'
                          'G1 X80 F15000\n'
                          'G1 X60 F15000; shake to put down garbage\n'
                          '\n'
                          'G1 X70 F5000\n'
                          'G1 X90 F3000\n'
                          'G1 Y255 F4000\n'
                          'G1 X100 F5000\n'
                          'G1 Y265 F5000\n'
                          'G1 X70 F10000\n'
                          'G1 X100 F5000\n'
                          'G1 X70 F10000\n'
                          'G1 X100 F5000\n'
                          'G1 X165 F15000; wipe and shake\n'
                          'G1 Y256 ; move Y to aside, prevent collision\n'
                          'M400\n'
                          'G1 Z{max_layer_z + 3.0} F3000\n'
                          '{if layer_z <= (initial_layer_print_height + 0.001)}\n'
                          'M204 S[initial_layer_acceleration]\n'
                          '{else}\n'
                          'M204 S[default_acceleration]\n'
                          '{endif}\n'
                          '{else}\n'
                          'G1 X[x_after_toolchange] Y[y_after_toolchange] Z[z_after_toolchange] F12000\n'
                          '{endif}\n'
                          'M621 S[next_extruder]A',
 'default_filament_profile': ['Bambu PLA Basic @BBL X1C'],
 'default_nozzle_volume_type': ['Standard'],
 'default_print_profile': '0.16mm Optimal @BBL X1C',
 'deretraction_speed': ['30'],
 'enable_long_retraction_when_cut': ['0'],
 'extruder_clearance_height_to_lid': '90',
 'extruder_clearance_max_radius': '68',
 'extruder_colour': ['#018001'],
 'extruder_printable_area': [],
 'extruder_printable_height': [],
 'extruder_type': ['Direct Drive'],
 'extruder_variant_list': ['Direct Drive Standard'],
 'from': 'system',
 'head_wrap_detect_zone': [],
 'inherits': 'fdm_machine_common',
 'instantiation': 'false',
 'layer_change_gcode': '; layer num/total_layer_count: {layer_num+1}/[total_layer_count]\n'
                       '; update layer progress\n'
                       'M73 L{layer_num+1}\n'
                       'M991 S0 P{layer_num} ;notify layer change',
 'machine_end_gcode': ';===== date: 20230428 =====================\n'
                      'M400 ; wait for buffer to clear\n'
                      'G92 E0 ; zero the extruder\n'
                      'G1 E-0.8 F1800 ; retract\n'
                      'G1 Z{max_layer_z + 0.5} F900 ; lower z a little\n'
                      'G1 X65 Y245 F12000 ; move to safe pos \n'
                      'G1 Y265 F3000\n'
                      '\n'
                      'G1 X65 Y245 F12000\n'
                      'G1 Y265 F3000\n'
                      'M140 S0 ; turn off bed\n'
                      'M106 S0 ; turn off fan\n'
                      'M106 P2 S0 ; turn off remote part cooling fan\n'
                      'M106 P3 S0 ; turn off chamber cooling fan\n'
                      '\n'
                      'G1 X100 F12000 ; wipe\n'
                      '; pull back filament to AMS\n'
                      'M620 S255\n'
                      'G1 X20 Y50 F12000\n'
                      'G1 Y-3\n'
                      'T255\n'
                      'G1 X65 F12000\n'
                      'G1 Y265\n'
                      'G1 X100 F12000 ; wipe\n'
                      'M621 S255\n'
                      'M104 S0 ; turn off hotend\n'
                      '\n'
                      'M622.1 S1 ; for prev firmware, default turned on\n'
                      'M1002 judge_flag timelapse_record_flag\n'
                      'M622 J1\n'
                      '    M400 ; wait all motion done\n'
                      '    M991 S0 P-1 ;end smooth timelapse at safe pos\n'
                      '    M400 S3 ;wait for last picture to be taken\n'
                      'M623; end of "timelapse_record_flag"\n'
                      '\n'
                      'M400 ; wait all motion done\n'
                      'M17 S\n'
                      'M17 Z0.4 ; lower z motor current to reduce impact if there is something in the bottom\n'
                      '{if (max_layer_z + 100.0) < 250}\n'
                      '    G1 Z{max_layer_z + 100.0} F600\n'
                      '    G1 Z{max_layer_z +98.0}\n'
                      '{else}\n'
                      '    G1 Z250 F600\n'
                      '    G1 Z248\n'
                      '{endif}\n'
                      'M400 P100\n'
                      'M17 R ; restore z current\n'
                      '\n'
                      'G90\n'
                      'G1 X128 Y250 F3600\n'
                      '\n'
                      'M220 S100  ; Reset feedrate magnitude\n'
                      'M201.2 K1.0 ; Reset acc magnitude\n'
                      'M73.2   R1.0 ;Reset left time magnitude\n'
                      'M1002 set_gcode_claim_speed_level : 0\n'
                      '\n'
                      'M17 X0.8 Y0.8 Z0.5 ; lower motor current to 45% power\n',
 'machine_max_acceleration_e': ['5000', '5000'],
 'machine_max_acceleration_extruding': ['20000', '20000'],
 'machine_max_acceleration_retracting': ['5000', '5000'],
 'machine_max_acceleration_travel': ['9000', '9000'],
 'machine_max_acceleration_x': ['20000', '20000'],
 'machine_max_acceleration_y': ['20000', '20000'],
 'machine_max_acceleration_z': ['500', '200'],
 'machine_max_jerk_e': ['2.5', '2.5'],
 'machine_max_jerk_x': ['9', '9'],
 'machine_max_jerk_y': ['9', '9'],
 'machine_max_jerk_z': ['3', '3'],
 'machine_max_speed_e': ['30', '30'],
 'machine_max_speed_x': ['500', '200'],
 'machine_max_speed_y': ['500', '200'],
 'machine_max_speed_z': ['20', '20'],
 'machine_min_extruding_rate': ['0', '0'],
 'machine_min_travel_rate': ['0', '0'],
 'machine_pause_gcode': 'M400 U1',
 'name': 'fdm_bbl_3dp_001_common',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': ['hardened_steel'],
 'nozzle_volume': ['107'],
 'physical_extruder_map': ['0'],
 'printable_area': ['0x0', '256x0', '256x256', '0x256'],
 'printer_extruder_id': ['1'],
 'printer_extruder_variant': ['Direct Drive Standard'],
 'printer_variant': '0.4',
 'retract_before_wipe': ['0%'],
 'retract_length_toolchange': ['2'],
 'retract_lift_above': ['0'],
 'retract_lift_below': ['249'],
 'retraction_length': ['0.8'],
 'retraction_minimum_travel': ['1'],
 'retraction_speed': ['30'],
 'time_lapse_gcode': ';========Date 20250206========\n'
                     'M622.1 S1 ; for prev firmware, default turned on\n'
                     'M1002 judge_flag timelapse_record_flag\n'
                     'M622 J1\n'
                     '{if timelapse_type == 0} ; timelapse without wipe tower\n'
                     'M971 S11 C10 O0\n'
                     '{elsif timelapse_type == 1} ; timelapse with wipe tower\n'
                     'G92 E0\n'
                     'G1 X65 Y245 F20000 ; move to safe pos\n'
                     'G17\n'
                     'G2 Z{layer_z} I0.86 J0.86 P1 F20000\n'
                     'G1 Y265 F3000\n'
                     'M400 P300\n'
                     'M971 S11 C10 O0\n'
                     'G92 E0\n'
                     'G1 X100 F5000\n'
                     'G1 Y255 F20000\n'
                     '{endif}\n'
                     'M623\n',
 'type': 'machine',
 'wipe_distance': ['2'],
 'z_hop': ['0.4'],
 'z_hop_types': ['Auto Lift']}
