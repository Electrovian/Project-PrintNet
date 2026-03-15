from __future__ import annotations

# source: profiles/Snapmaker/machine/fdm_U1.json
DATA = {'auxiliary_fan': '0',
 'bed_mesh_max': '267,267',
 'bed_mesh_min': '3,3',
 'bed_model': 'Snapmaker U1_bed.stl',
 'bed_texture': 'Snapmaker U1_texture.svg',
 'change_filament_gcode': '',
 'deretraction_speed': ['30', '30', '30', '30', '30'],
 'extruder_colour': ['#FCE94F', '#FCE94F', '#FCE94F', '#FCE94F', '#FCE94F'],
 'extruder_offset': ['0x0', '0x0', '0x0', '0x0', '0x0'],
 'from': 'system',
 'gcode_flavor': 'klipper',
 'inherits': 'fdm_toolchanger',
 'instantiation': 'false',
 'long_retractions_when_cut': ['0', '0', '0', '0', '0'],
 'machine_pause_gcode': 'M601',
 'machine_start_gcode': ';===== machine: PR2 ========================\n'
                        ';===== date: 20250717 =====================\n'
                        'PRINT_START\n'
                        ';===== 预热热床和第一个挤出头 =================\n'
                        'M140 S{bed_temperature_initial_layer_single}\n'
                        'M104 T{initial_extruder} S140\n'
                        '\n'
                        ';===== 粗回零 =================\n'
                        'G28 X Y\n'
                        'T{initial_extruder}\n'
                        'M109 T{initial_extruder} S140\n'
                        'G28 Z\n'
                        'G90\n'
                        'G0 Z10 F10000\n'
                        'MOVE_TO_DISCARD_FILAMENT_POSITION\n'
                        'M109 S{nozzle_temperature[initial_extruder] - 50}\n'
                        'ROUGHLY_CLEAN_NOZZLE_WITH_DISCARD\n'
                        'M104 S{nozzle_temperature[initial_extruder] - 90}\n'
                        'G4 P2000\n'
                        'ROUGHLY_CLEAN_NOZZLE\n'
                        'MOVE_TO_XY_IDLE_POSITION_EXTRUDER\n'
                        '\n'
                        ';===== 检测钢板 =================\n'
                        'DETECT_BED_PLATE\n'
                        'MOVE_TO_XY_IDLE_POSITION_EXTRUDER\n'
                        '\n'
                        ';===== 自动进料  ======================\n'
                        'SM_PRINT_AUTO_FEED EXTRUDER=0\n'
                        'SM_PRINT_AUTO_FEED EXTRUDER=1\n'
                        'SM_PRINT_AUTO_FEED EXTRUDER=2\n'
                        'SM_PRINT_AUTO_FEED EXTRUDER=3\n'
                        '\n'
                        ';===== 挤出流量  ======================\n'
                        '{if (is_extruder_used[0])}\n'
                        'SM_PRINT_FLOW_CALIBRATE INDEX=0 TARGET_TEMP={nozzle_temperature[0]}\n'
                        '{endif}\n'
                        '{if (is_extruder_used[1])}\n'
                        'SM_PRINT_FLOW_CALIBRATE INDEX=1 TARGET_TEMP={nozzle_temperature[1]}\n'
                        '{endif}\n'
                        '{if (is_extruder_used[2])}\n'
                        'SM_PRINT_FLOW_CALIBRATE INDEX=2 TARGET_TEMP={nozzle_temperature[2]}\n'
                        '{endif}\n'
                        '{if (is_extruder_used[3])}\n'
                        'SM_PRINT_FLOW_CALIBRATE INDEX=3 TARGET_TEMP={nozzle_temperature[3]}\n'
                        '{endif}\n'
                        '\n'
                        ';===== 取出第一个挤出头 =================\n'
                        'T{initial_extruder}\n'
                        'SET_VELOCITY_LIMIT ACCEL=10000\n'
                        'M204 S10000\n'
                        '\n'
                        ';===== 深度清洁喷嘴 =================\n'
                        'G90\n'
                        'G0 Z10 F10000\n'
                        'ROUGHLY_CLEAN_NOZZLE_WITH_DISCARD\n'
                        'G0 Z5 F10000\n'
                        'FINELY_CLEAN_NOZZLE_STAGE_1\n'
                        'G0 Z5 F10000\n'
                        'ROUGHLY_CLEAN_NOZZLE\n'
                        'G0 Z5 F10000\n'
                        'FINELY_CLEAN_NOZZLE_STAGE_2\n'
                        'M83\n'
                        '\n'
                        ';===== 第一个挤出头降温 =================\n'
                        'M109 S{nozzle_temperature[initial_extruder] - 90}\n'
                        'M190 S{bed_temperature_initial_layer_single}\n'
                        'M106 S0\n'
                        'G90\n'
                        'G0 Z5 F10000\n'
                        'MOVE_TO_DISCARD_FILAMENT_POSITION\n'
                        'INNER_CUTOFF_BASE_DISCARD\n'
                        'INNER_ROUGHLY_CLEAN_NOZZLE_BASE_DISCARD\n'
                        'INNER_ROUGHLY_CLEAN_NOZZLE_BASE_DISCARD\n'
                        'MOVE_TO_XY_IDLE_POSITION_EXTRUDER\n'
                        '\n'
                        ';===== 精回零 =================\n'
                        'G28 Z\n'
                        ';===== 热床调平 =================\n'
                        '; Always pass `ADAPTIVE_MARGIN=0` because EON has already handled `adaptive_bed_mesh_margin` '
                        'internally\n'
                        "; Make sure to set ADAPTIVE to 0 otherwise Klipper will use it's own adaptive bed mesh logic\n"
                        'BED_MESH_CALIBRATE mesh_min={adaptive_bed_mesh_min[0]},{adaptive_bed_mesh_min[1]} '
                        'mesh_max={adaptive_bed_mesh_max[0]},{adaptive_bed_mesh_max[1]} ALGORITHM=[bed_mesh_algo] '
                        'PROBE_COUNT={bed_mesh_probe_count[0]},{bed_mesh_probe_count[1]} ADAPTIVE=0 ADAPTIVE_MARGIN=0\n'
                        '\n'
                        ';BED_MESH_CALIBRATE PROBE_COUNT=7,7\n'
                        '\n'
                        '\n'
                        ';======== 预挤出/划线 ================\n'
                        '{if (is_extruder_used[0]) and 0 != initial_extruder}\n'
                        'SM_PRINT_START_LINE INDEX=0 TARGET_TEMP={nozzle_temperature_initial_layer[0]}\n'
                        'M83\n'
                        'M104 S{nozzle_temperature[0] - 90}\n'
                        '{endif}\n'
                        '\n'
                        '{if (is_extruder_used[1]) and 1 != initial_extruder}\n'
                        'SM_PRINT_START_LINE INDEX=1 TARGET_TEMP={nozzle_temperature_initial_layer[1]}\n'
                        'M83\n'
                        'M104 S{nozzle_temperature[1] - 90}\n'
                        '{endif}\n'
                        '\n'
                        '{if (is_extruder_used[2]) and 2 != initial_extruder}\n'
                        'SM_PRINT_START_LINE INDEX=2 TARGET_TEMP={nozzle_temperature_initial_layer[2]}\n'
                        'M83\n'
                        'M104 S{nozzle_temperature[2] - 90}\n'
                        '{endif}\n'
                        '\n'
                        '{if (is_extruder_used[3]) and 3 != initial_extruder}\n'
                        'SM_PRINT_START_LINE INDEX=3 TARGET_TEMP={nozzle_temperature_initial_layer[3]}\n'
                        'M83\n'
                        'M104 S{nozzle_temperature[3] - 90}\n'
                        '{endif}\n'
                        '\n'
                        '{if (is_extruder_used[initial_extruder])}\n'
                        'SM_PRINT_START_LINE INDEX={initial_extruder} '
                        'TARGET_TEMP={nozzle_temperature_initial_layer[initial_extruder]}\n'
                        '{endif}\n'
                        'M109 S{nozzle_temperature_initial_layer[initial_extruder]} T{initial_extruder}\n'
                        'M106 S0\n'
                        '\n'
                        'TIMELAPSE_START',
 'max_layer_height': ['0.32', '0.32', '0.32', '0.32', '0.32'],
 'min_layer_height': ['0.08', '0.08', '0.08', '0.08', '0.08'],
 'name': 'fdm_U1',
 'nozzle_diameter': ['0.4', '0.4', '0.4', '0.4', '0.4'],
 'nozzle_type': 'hardened_steel',
 'purge_in_prime_tower': '0',
 'retract_before_wipe': ['70%', '70%', '70%', '70%', '70%'],
 'retract_length_toolchange': ['2', '2', '2', '2', '2'],
 'retract_lift_above': ['0', '0', '0', '0', '0'],
 'retract_lift_below': ['0', '0', '0', '0', '0'],
 'retract_lift_enforce': ['All Surfaces', 'All Surfaces', 'All Surfaces', 'All Surfaces', 'All Surfaces'],
 'retract_restart_extra': ['0', '0', '0', '0', '0'],
 'retract_restart_extra_toolchange': ['0', '0', '0', '0', '0'],
 'retract_when_changing_layer': ['1', '1', '1', '1', '1'],
 'retraction_distances_when_cut': ['18', '18', '18', '18', '18'],
 'retraction_length': ['0.8', '0.8', '0.8', '0.8', '0.8'],
 'retraction_minimum_travel': ['1', '1', '1', '1', '1'],
 'retraction_speed': ['30', '30', '30', '30', '30'],
 'scan_first_layer': '0',
 'single_extruder_multi_material': '0',
 'travel_slope': ['3', '3', '3', '3', '3'],
 'type': 'machine',
 'wipe': ['1', '1', '1', '1', '1'],
 'wipe_distance': ['1', '1', '1', '1', '1'],
 'z_hop': ['0.4', '0.4', '0.4', '0.4', '0.4'],
 'z_hop_types': ['Normal Lift', 'Normal Lift', 'Normal Lift', 'Normal Lift', 'Normal Lift']}
