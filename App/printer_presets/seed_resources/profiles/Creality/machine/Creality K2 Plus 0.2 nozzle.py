from __future__ import annotations

# source: profiles/Creality/machine/Creality K2 Plus 0.2 nozzle.json
DATA = {'auxiliary_fan': '1',
 'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n',
 'change_filament_gcode': 'G2 Z{z_after_toolchange + 0.4} I0.86 J0.86 P1 F10000 ; spiral lift a little from second '
                          'lift\n'
                          'G1 X0 Y245 F30000\n'
                          'G1 Z{z_after_toolchange} F600',
 'cooling_tube_length': '0',
 'cooling_tube_retraction': '0',
 'default_filament_profile': ['Creality Generic PLA @K2-all'],
 'default_print_profile': '0.14mm Optimal @Creality K2 Plus 0.2 nozzle',
 'deretraction_speed': ['40'],
 'enable_filament_ramming': '0',
 'extra_loading_move': '0',
 'extruder_clearance_height_to_lid': '118',
 'extruder_clearance_height_to_rod': '24',
 'extruder_clearance_radius': '64',
 'from': 'system',
 'gcode_flavor': 'klipper',
 'inherits': 'fdm_creality_common',
 'instantiation': 'true',
 'machine_end_gcode': 'END_PRINT',
 'machine_max_acceleration_e': ['5000', '5000'],
 'machine_max_acceleration_extruding': ['30000', '30000'],
 'machine_max_acceleration_retracting': ['5000', '5000'],
 'machine_max_acceleration_travel': ['30000', '30000'],
 'machine_max_acceleration_x': ['30000', '30000'],
 'machine_max_acceleration_y': ['30000', '30000'],
 'machine_max_acceleration_z': ['5000', '5000'],
 'machine_max_jerk_e': ['10', '10'],
 'machine_max_jerk_x': ['20', '20'],
 'machine_max_jerk_y': ['20', '20'],
 'machine_max_jerk_z': ['5', '5'],
 'machine_max_speed_e': ['50', '50'],
 'machine_max_speed_x': ['800', '800'],
 'machine_max_speed_y': ['800', '800'],
 'machine_max_speed_z': ['10', '10'],
 'machine_pause_gcode': 'PAUSE',
 'machine_start_gcode': 'M140 S0\n'
                        'M104 S0 \n'
                        'START_PRINT EXTRUDER_TEMP=[nozzle_temperature_initial_layer] '
                        'BED_TEMP=[bed_temperature_initial_layer_single]\n'
                        'T[initial_no_support_extruder]\n'
                        'M109 S[nozzle_temperature_initial_layer]\n'
                        'M204 S2000\n'
                        'G1 Z3 F600\n'
                        'M83\n'
                        'G1 Y150 F12000\n'
                        'G1 X0 F12000\n'
                        'G1 Z0.2 F600\n'
                        'G1 X0 Y150 F6000\n'
                        'G1 X0 Y0 E15 F6000\n'
                        'G1 X150 Y0 E15 F6000\n'
                        'G92 E0\n'
                        'G1 Z1 F600',
 'manual_filament_change': '0',
 'max_layer_height': ['0.3'],
 'min_layer_height': ['0.08'],
 'name': 'Creality K2 Plus 0.2 nozzle',
 'nozzle_diameter': ['0.2'],
 'nozzle_type': 'hardened_steel',
 'nozzle_volume': '183',
 'parking_pos_retraction': '0',
 'printable_area': ['0x0', '350x0', '350x350', '0x350'],
 'printable_height': '350',
 'printer_model': 'Creality K2 Plus',
 'printer_settings_id': 'Creality',
 'printer_variant': '0.2',
 'purge_in_prime_tower': '0',
 'retract_before_wipe': ['70%'],
 'retract_length_toolchange': ['0'],
 'retract_lift_above': ['0'],
 'retract_lift_below': ['349'],
 'retraction_length': ['0.5'],
 'retraction_minimum_travel': ['1'],
 'retraction_speed': ['40'],
 'scan_first_layer': '0',
 'setting_id': 'GM001',
 'single_extruder_multi_material': '1',
 'support_air_filtration': '1',
 'support_multi_bed_types': '1',
 'thumbnails': ['300x300', '96x96'],
 'thumbnails_format': 'PNG',
 'type': 'machine',
 'wipe_distance': ['1'],
 'z_hop': ['0.4']}
