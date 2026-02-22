from __future__ import annotations

# source: profiles/Chuanying/machine/fdm_x1_common.json
DATA = {'auxiliary_fan': '1',
 'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\n;[layer_z]',
 'change_filament_gcode': '',
 'default_filament_profile': ['Chuanying Generic PLA'],
 'deretraction_speed': ['35'],
 'extruder_clearance_height_to_lid': ['150'],
 'extruder_clearance_height_to_rod': ['27'],
 'extruder_clearance_radius': ['76'],
 'from': 'system',
 'gcode_flavor': 'klipper',
 'inherits': 'fdm_chuanying_common',
 'instantiation': 'false',
 'layer_change_gcode': ';AFTER_LAYER_CHANGE\n;[layer_z]',
 'machine_end_gcode': 'G1 E-3 F3600\nG0 X50 Y50 F30000\nM104 S0 ; turn off temperature',
 'machine_max_acceleration_e': ['5000', '5000'],
 'machine_max_acceleration_extruding': ['20000', '20000'],
 'machine_max_acceleration_retracting': ['5000', '5000'],
 'machine_max_acceleration_travel': ['20000', '20000'],
 'machine_max_acceleration_x': ['20000', '20000'],
 'machine_max_acceleration_y': ['20000', '20000'],
 'machine_max_acceleration_z': ['500', '500'],
 'machine_max_jerk_e': ['2.5', '2.5'],
 'machine_max_jerk_x': ['9', '9'],
 'machine_max_jerk_y': ['9', '9'],
 'machine_max_jerk_z': ['3', '3'],
 'machine_max_speed_e': ['30', '30'],
 'machine_max_speed_x': ['600', '600'],
 'machine_max_speed_y': ['600', '600'],
 'machine_max_speed_z': ['20', '20'],
 'machine_pause_gcode': 'M25',
 'machine_start_gcode': 'M190 S[bed_temperature_initial_layer_single]\n'
                        'M104 S[nozzle_temperature_initial_layer]\n'
                        'G90\n'
                        'M83\n'
                        'G1 Z5 F6000\n'
                        'G1 E-0.2 F800\n'
                        'G1 X110 Y-110 F6000\n'
                        'G1 E2 F800\n'
                        'G1 Y-110 X55 Z0.25 F4800\n'
                        'G1 X-55 E8 F2400\n'
                        'G1 Y-109.6 F2400\n'
                        'G1 X55 E5 F2400\n'
                        'G1 Y-110 X55 Z0.45 F4800\n'
                        'G1 X-55 E8 F2400\n'
                        'G1 Y-109.6 F2400\n'
                        'G1 X55 E5 F2400\n'
                        'G92 E0',
 'name': 'fdm_x1_common',
 'printable_area': ['-110x-110', '110x-110', '110x110', '-110x110'],
 'printable_height': '220',
 'printer_settings_id': 'Chuanying',
 'retract_before_wipe': ['100%'],
 'retract_length_toolchange': ['2'],
 'retraction_minimum_travel': ['1'],
 'retraction_speed': ['35'],
 'scan_first_layer': '0',
 'single_extruder_multi_material': '0',
 'thumbnails': ['140x110'],
 'type': 'machine',
 'use_relative_e_distances': '1',
 'wipe_distance': '2',
 'z_hop': ['0.4'],
 'z_hop_types': 'Auto Lift'}
