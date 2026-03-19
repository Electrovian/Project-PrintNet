from __future__ import annotations

# source: profiles/Flashforge/machine/fdm_adventurer3_common.json
DATA = {'auxiliary_fan': '1',
 'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\n;[layer_z]',
 'change_filament_gcode': 'M600',
 'cooling_tube_length': '0',
 'cooling_tube_retraction': '0',
 'default_filament_profile': ['Flashforge PLA'],
 'deretraction_speed': ['25'],
 'enable_filament_ramming': '0',
 'extra_loading_move': '0',
 'extruder_clearance_height_to_lid': '150',
 'extruder_clearance_height_to_rod': '24.93',
 'extruder_clearance_radius': '42.3',
 'from': 'system',
 'gcode_flavor': 'marlin',
 'inherits': 'fdm_flashforge_common',
 'instantiation': 'false',
 'layer_change_gcode': ';AFTER_LAYER_CHANGE\n;[layer_z]',
 'machine_end_gcode': 'G1 E-3 F3600\n'
                      'G0 X50 Y50 F9000\n'
                      'M104 S0 T0\n'
                      'M140 S0 T0\n'
                      'G162 Z F1800\n'
                      'G28 X Y\n'
                      'M132 X Y A B\n'
                      'M652\n'
                      'G91\n'
                      'M18',
 'machine_max_acceleration_e': ['500'],
 'machine_max_acceleration_extruding': ['500'],
 'machine_max_acceleration_retracting': ['500'],
 'machine_max_acceleration_travel': ['500'],
 'machine_max_acceleration_x': ['500'],
 'machine_max_acceleration_y': ['500'],
 'machine_max_acceleration_z': ['100'],
 'machine_max_jerk_e': ['2.5'],
 'machine_max_jerk_x': ['8'],
 'machine_max_jerk_y': ['8'],
 'machine_max_jerk_z': ['0.4'],
 'machine_max_speed_e': ['30'],
 'machine_max_speed_x': ['150'],
 'machine_max_speed_y': ['150'],
 'machine_max_speed_z': ['20'],
 'machine_pause_gcode': 'M25',
 'machine_start_gcode': 'M140 S[bed_temperature_initial_layer] T0\n'
                        'M104 S[nozzle_temperature_initial_layer] T0\n'
                        'M104 S0 T1\n'
                        'M107\n'
                        'M900 K[pressure_advance] T0\n'
                        'G90\n'
                        'G28\n'
                        'M132 X Y Z A B\n'
                        'G1 Z50.000 F420\n'
                        'G161 X Y F3300\n'
                        'M7 T0\n'
                        'M6 T0\n'
                        'M651 S255\n'
                        ';pre-extrude\n'
                        'M108 T0\n'
                        'G1 X-37.50 Y-75.00 F6000\n'
                        'M106\n'
                        'G1 Z0.200 F420\n'
                        'G1 X-37.50 Y-74.00 F6000\n'
                        'G1 X37.50 Y-74.00 E9.5 F1200\n',
 'manual_filament_change': '1',
 'name': 'fdm_adventurer3_common',
 'nozzle_type': 'stainless_steel',
 'parking_pos_retraction': '0',
 'printable_area': ['-75x-75', '75x-75', '75x75', '-75x75'],
 'printable_height': '150',
 'printer_settings_id': 'Flashforge',
 'purge_in_prime_tower': '0',
 'retract_before_wipe': ['100%'],
 'retract_length_toolchange': ['2'],
 'retraction_length': ['5'],
 'retraction_minimum_travel': ['1'],
 'retraction_speed': ['25'],
 'scan_first_layer': '0',
 'single_extruder_multi_material': '1',
 'thumbnails': '80x60',
 'type': 'machine',
 'use_relative_e_distances': '0',
 'wipe_distance': '2',
 'z_hop': ['0.4'],
 'z_hop_types': 'Auto Lift'}
