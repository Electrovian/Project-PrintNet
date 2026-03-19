from __future__ import annotations

# source: profiles/Sovol/machine/Sovol Zero 0.4 nozzle.json
DATA = {'auxiliary_fan': '1',
 'before_layer_change_gcode': 'TIMELAPSE_TAKE_FRAME\nG92 E0\nSET_PRINT_STATS_INFO CURRENT_LAYER=[layer_num]\n',
 'default_filament_profile': ['Sovol Zero PLA Basic'],
 'default_print_profile': '0.20mm Standard @Sovol Zero 0.4 nozzle',
 'deretraction_speed': ['40'],
 'from': 'system',
 'gcode_flavor': 'klipper',
 'inherits': 'fdm_machine_common',
 'instantiation': 'true',
 'machine_end_gcode': 'END_PRINT\n',
 'machine_max_acceleration_e': ['20000'],
 'machine_max_acceleration_extruding': ['40000'],
 'machine_max_acceleration_retracting': ['20000'],
 'machine_max_acceleration_travel': ['40000'],
 'machine_max_acceleration_x': ['40000'],
 'machine_max_acceleration_y': ['40000'],
 'machine_max_acceleration_z': ['1000'],
 'machine_max_jerk_e': ['2.5'],
 'machine_max_jerk_x': ['5'],
 'machine_max_jerk_y': ['5'],
 'machine_max_jerk_z': ['0.5'],
 'machine_max_speed_e': ['50'],
 'machine_max_speed_x': ['1200'],
 'machine_max_speed_y': ['1200'],
 'machine_max_speed_z': ['30'],
 'machine_start_gcode': 'M140 S[bed_temperature_initial_layer_single] ;set bed temp\n'
                        'M190 S[bed_temperature_initial_layer_single] ;wait for bed temp\n'
                        'G28\n'
                        'START_PRINT\n'
                        'G28\n'
                        'G90\n'
                        'G1 X0 Y0 F12000\n'
                        'G1 Z0.300 F600\n'
                        'M104 S[nozzle_temperature_initial_layer] ;set extruder temp\n'
                        'M109 S[nozzle_temperature_initial_layer];wait for extruder temp\n'
                        '{if first_layer_print_min[1] - 6 > print_bed_min[1]}\n'
                        'G90\n'
                        'M83\n'
                        'G1 E-0.5 F600\n'
                        'G1 X{first_layer_print_min[0] + (first_layer_print_max[0] - first_layer_print_min[0]) / 4} '
                        'Y{first_layer_print_min[1] - 5} F12000\n'
                        'G0 Z0.3 F600 ;Move to start position\n'
                        'G1 E0.200 F600\n'
                        '{if first_layer_print_max[0] - first_layer_print_min[0] > 50}\n'
                        'G0 X{first_layer_print_min[0] + (first_layer_print_max[0] - first_layer_print_min[0]) / 4 + '
                        '5*1} E{5 * 0.2}  F{outer_wall_volumetric_speed/(24/20)    * 60}\n'
                        'G0 X{first_layer_print_min[0] + (first_layer_print_max[0] - first_layer_print_min[0]) / 4 + '
                        '5*2} E{5 * 0.2}  F{outer_wall_volumetric_speed/(0.3*0.5)/4     * 60}\n'
                        'G0 X{first_layer_print_min[0] + (first_layer_print_max[0] - first_layer_print_min[0]) / 4 + '
                        '5*3} E{5 * 0.2}  F{outer_wall_volumetric_speed/(24/20)    * 60}\n'
                        'G0 X{first_layer_print_min[0] + (first_layer_print_max[0] - first_layer_print_min[0]) / 4 + '
                        '5*4} E{5 * 0.2}  F{outer_wall_volumetric_speed/(0.3*0.5)/4     * 60}\n'
                        'G0 X{first_layer_print_min[0] + (first_layer_print_max[0] - first_layer_print_min[0]) / 4 + '
                        '5*5} E{5 * 0.2}  F{outer_wall_volumetric_speed/(24/20)    * 60}\n'
                        'G0 X{first_layer_print_min[0] + (first_layer_print_max[0] - first_layer_print_min[0]) / 4 + '
                        '5*6} E{5 * 0.2}  F{outer_wall_volumetric_speed/(0.3*0.5)/4     * 60}\n'
                        'G0 X{first_layer_print_min[0] + (first_layer_print_max[0] - first_layer_print_min[0]) / 4 + '
                        '5*7} E{5 * 0.2}  F{outer_wall_volumetric_speed/(24/20)    * 60}\n'
                        'G0 X{first_layer_print_min[0] + (first_layer_print_max[0] - first_layer_print_min[0]) / 4 + '
                        '5*8} E{5 * 0.2}  F{outer_wall_volumetric_speed/(0.3*0.5)/4     * 60}\n'
                        'G0 X{first_layer_print_min[0] + (first_layer_print_max[0] - first_layer_print_min[0]) / 4 + '
                        '5*9} E{5 * 0.2}  F{outer_wall_volumetric_speed/(0.3*0.5)/4     * 60}\n'
                        'G0 X{first_layer_print_min[0] + (first_layer_print_max[0] - first_layer_print_min[0]) / 4 + '
                        '5*10} E{5 * 0.2}  F{outer_wall_volumetric_speed/(0.3*0.5)/4     * 60}\n'
                        '{else}\n'
                        'G0 X{first_layer_print_min[0] + (first_layer_print_max[0] - first_layer_print_min[0]) / 2} '
                        'E{(first_layer_print_max[0] - first_layer_print_min[0]) / 2 * 0.2}  '
                        'F{outer_wall_volumetric_speed/(24/20)    * 60}\n'
                        'G0 X{first_layer_print_min[0] + (first_layer_print_max[0] - first_layer_print_min[0])} '
                        'E{(first_layer_print_max[0] - first_layer_print_min[0]) / 2 * 0.2}  '
                        'F{outer_wall_volumetric_speed/(0.3*0.5)/4     * 60}\n'
                        '{endif}\n'
                        'G1 E-0.300 F600\n'
                        'G0 Z1 F600\n'
                        'G1 X{first_layer_print_min[0] + (first_layer_print_max[0] - first_layer_print_min[0]) / 4} '
                        'Y{first_layer_print_min[1] - 4} F12000\n'
                        'G0 Z0.3 F600 ;Move to start position\n'
                        'G1 E0.200 F600\n'
                        '{if first_layer_print_max[0] - first_layer_print_min[0] > 50}\n'
                        'G0 X{first_layer_print_min[0] + (first_layer_print_max[0] - first_layer_print_min[0]) / 4 + '
                        '5*1} E{5 * 0.2}  F{outer_wall_volumetric_speed/(24/20)    * 60}\n'
                        'G0 X{first_layer_print_min[0] + (first_layer_print_max[0] - first_layer_print_min[0]) / 4 + '
                        '5*2} E{5 * 0.2}  F{outer_wall_volumetric_speed/(0.3*0.5)/4     * 60}\n'
                        'G0 X{first_layer_print_min[0] + (first_layer_print_max[0] - first_layer_print_min[0]) / 4 + '
                        '5*3} E{5 * 0.2}  F{outer_wall_volumetric_speed/(24/20)    * 60}\n'
                        'G0 X{first_layer_print_min[0] + (first_layer_print_max[0] - first_layer_print_min[0]) / 4 + '
                        '5*4} E{5 * 0.2}  F{outer_wall_volumetric_speed/(0.3*0.5)/4     * 60}\n'
                        'G0 X{first_layer_print_min[0] + (first_layer_print_max[0] - first_layer_print_min[0]) / 4 + '
                        '5*5} E{5 * 0.2}  F{outer_wall_volumetric_speed/(24/20)    * 60}\n'
                        'G0 X{first_layer_print_min[0] + (first_layer_print_max[0] - first_layer_print_min[0]) / 4 + '
                        '5*6} E{5 * 0.2}  F{outer_wall_volumetric_speed/(0.3*0.5)/4     * 60}\n'
                        'G0 X{first_layer_print_min[0] + (first_layer_print_max[0] - first_layer_print_min[0]) / 4 + '
                        '5*7} E{5 * 0.2}  F{outer_wall_volumetric_speed/(24/20)    * 60}\n'
                        'G0 X{first_layer_print_min[0] + (first_layer_print_max[0] - first_layer_print_min[0]) / 4 + '
                        '5*8} E{5 * 0.2}  F{outer_wall_volumetric_speed/(0.3*0.5)/4     * 60}\n'
                        'G0 X{first_layer_print_min[0] + (first_layer_print_max[0] - first_layer_print_min[0]) / 4 + '
                        '5*9} E{5 * 0.2}  F{outer_wall_volumetric_speed/(0.3*0.5)/4     * 60}\n'
                        'G0 X{first_layer_print_min[0] + (first_layer_print_max[0] - first_layer_print_min[0]) / 4 + '
                        '5*10} E{5 * 0.2}  F{outer_wall_volumetric_speed/(0.3*0.5)/4     * 60}\n'
                        '{else}\n'
                        'G0 X{first_layer_print_min[0] + (first_layer_print_max[0] - first_layer_print_min[0]) / 2} '
                        'E{(first_layer_print_max[0] - first_layer_print_min[0]) / 2 * 0.2}  '
                        'F{outer_wall_volumetric_speed/(24/20)    * 60}\n'
                        'G0 X{first_layer_print_min[0] + (first_layer_print_max[0] - first_layer_print_min[0])} '
                        'E{(first_layer_print_max[0] - first_layer_print_min[0]) / 2 * 0.2}  '
                        'F{outer_wall_volumetric_speed/(0.3*0.5)/4     * 60}\n'
                        '{endif}\n'
                        'G1 E-0.300 F600\n'
                        'G0 Z5 F600\n'
                        'M400\n'
                        '{else}\n'
                        'G90\n'
                        'M83\n'
                        'G1 E-0.300 Z3 F600\n'
                        'G1 X{print_bed_max[1] / 3} F{outer_wall_volumetric_speed/(24/20)    * 60}\n'
                        'G1 Z0.3 F600\n'
                        'G1 E0.300 F600\n'
                        'G1 X{print_bed_max[1] / 3 + 5*1} E{5 * 0.2} F{outer_wall_volumetric_speed/(24/20)    * 60}\n'
                        'G1 X{print_bed_max[1] / 3 + 5*2} E{5 * 0.2} F{outer_wall_volumetric_speed/(0.3*0.5)/4     * '
                        '60}\n'
                        'G1 X{print_bed_max[1] / 3 + 5*3} E{5 * 0.2} F{outer_wall_volumetric_speed/(24/20)    * 60}\n'
                        'G1 X{print_bed_max[1] / 3 + 5*4} E{5 * 0.2} F{outer_wall_volumetric_speed/(0.3*0.5)/4     * '
                        '60}\n'
                        'G1 X{print_bed_max[1] / 3 + 5*5} E{5 * 0.2} F{outer_wall_volumetric_speed/(24/20)    * 60}\n'
                        'G1 X{print_bed_max[1] / 3 + 5*6} E{5 * 0.2} F{outer_wall_volumetric_speed/(0.3*0.5)/4     * '
                        '60}\n'
                        'G1 X{print_bed_max[1] / 3 + 5*7} E{5 * 0.2} F{outer_wall_volumetric_speed/(24/20)    * 60}\n'
                        'G1 X{print_bed_max[1] / 3 + 5*8} E{5 * 0.2} F{outer_wall_volumetric_speed/(0.3*0.5)/4     * '
                        '60}\n'
                        'G1 X{print_bed_max[1] / 3 + 5*9} E{5 * 0.2} F{outer_wall_volumetric_speed/(24/20)    * 60}\n'
                        'G1 X{print_bed_max[1] / 3 + 5*10} E{5 * 0.2} F{outer_wall_volumetric_speed/(0.3*0.5)/4     * '
                        '60}\n'
                        'G1 X{print_bed_max[1] / 3} Y1 F{outer_wall_volumetric_speed/(0.3*0.5)/4     * 60}\n'
                        'G1 X{print_bed_max[1] / 3 + 5*1} E{5 * 0.2} F{outer_wall_volumetric_speed/(24/20)    * 60}\n'
                        'G1 X{print_bed_max[1] / 3 + 5*2} E{5 * 0.2} F{outer_wall_volumetric_speed/(0.3*0.5)/4     * '
                        '60}\n'
                        'G1 X{print_bed_max[1] / 3 + 5*3} E{5 * 0.2} F{outer_wall_volumetric_speed/(24/20)    * 60}\n'
                        'G1 X{print_bed_max[1] / 3 + 5*4} E{5 * 0.2} F{outer_wall_volumetric_speed/(0.3*0.5)/4     * '
                        '60}\n'
                        'G1 X{print_bed_max[1] / 3 + 5*5} E{5 * 0.2} F{outer_wall_volumetric_speed/(24/20)    * 60}\n'
                        'G1 X{print_bed_max[1] / 3 + 5*6} E{5 * 0.2} F{outer_wall_volumetric_speed/(0.3*0.5)/4     * '
                        '60}\n'
                        'G1 X{print_bed_max[1] / 3 + 5*7} E{5 * 0.2} F{outer_wall_volumetric_speed/(24/20)    * 60}\n'
                        'G1 X{print_bed_max[1] / 3 + 5*8} E{5 * 0.2} F{outer_wall_volumetric_speed/(0.3*0.5)/4     * '
                        '60}\n'
                        'G1 X{print_bed_max[1] / 3 + 5*9} E{5 * 0.2} F{outer_wall_volumetric_speed/(24/20)    * 60}\n'
                        'G1 X{print_bed_max[1] / 3 + 5*10} E{5 * 0.2} F{outer_wall_volumetric_speed/(0.3*0.5)/4     * '
                        '60}\n'
                        'G1 E-0.300 Z3 F600\n'
                        'M400\n'
                        '{endif}\n'
                        'SET_PRINT_STATS_INFO TOTAL_LAYER=[total_layer_count]\n'
                        '\n',
 'name': 'Sovol Zero 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'printable_area': ['0x0', '152.4x0', '152.4x152.4', '0x152.4'],
 'printable_height': '152.4',
 'printer_model': 'Sovol Zero',
 'printer_variant': '0.4',
 'retract_before_wipe': ['100%'],
 'retract_length_toolchange': ['2'],
 'retract_lift_below': ['150'],
 'retraction_length': ['0.8'],
 'retraction_minimum_travel': ['0'],
 'retraction_speed': ['40'],
 'setting_id': 'GM001',
 'thumbnails': ['300x300', '32x32'],
 'thumbnails_format': 'PNG',
 'type': 'machine',
 'wipe': ['1'],
 'wipe_distance': ['2'],
 'z_hop': ['0.4'],
 'z_hop_types': ['Auto Lift']}
