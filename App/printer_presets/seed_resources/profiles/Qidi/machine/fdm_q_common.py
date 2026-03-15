from __future__ import annotations

# source: profiles/Qidi/machine/fdm_q_common.json
DATA = {'auxiliary_fan': '1',
 'before_layer_change_gcode': '',
 'change_filament_gcode': '',
 'default_print_profile': '0.20mm Standard @Q1 Pro',
 'deretraction_speed': ['30'],
 'extruder_clearance_height_to_lid': '140',
 'extruder_clearance_height_to_rod': '36',
 'extruder_clearance_radius': '65',
 'extruder_colour': ['#FCE94F'],
 'extruder_offset': ['0x0'],
 'from': 'system',
 'gcode_flavor': 'klipper',
 'inherits': 'fdm_qidi_x3_common',
 'instantiation': 'false',
 'layer_change_gcode': '',
 'machine_end_gcode': 'M141 S0\n'
                      'M104 S0\n'
                      'M140 S0\n'
                      'G1 E-3 F1800\n'
                      'G0 Z{max_layer_z + 3} F600\n'
                      'G0 X0 Y0 F12000\n'
                      '{if max_layer_z < max_print_height / 2}G1 Z{max_print_height / 2 + 10} F600{else}G1 '
                      'Z{min(max_print_height, max_layer_z + 3)}{endif}',
 'machine_load_filament_time': '0',
 'machine_max_acceleration_e': ['5000'],
 'machine_max_acceleration_extruding': ['20000', '20000'],
 'machine_max_acceleration_retracting': ['5000', '5000'],
 'machine_max_acceleration_travel': ['9000', '9000'],
 'machine_max_acceleration_x': ['20000'],
 'machine_max_acceleration_y': ['20000'],
 'machine_max_acceleration_z': ['500'],
 'machine_max_jerk_e': ['2'],
 'machine_max_jerk_x': ['8'],
 'machine_max_jerk_y': ['8'],
 'machine_max_jerk_z': ['3'],
 'machine_max_speed_e': ['30'],
 'machine_max_speed_x': ['600'],
 'machine_max_speed_y': ['600'],
 'machine_max_speed_z': ['10'],
 'machine_min_extruding_rate': ['0', '0'],
 'machine_min_travel_rate': ['0', '0'],
 'machine_pause_gcode': 'M0',
 'machine_start_gcode': 'PRINT_START\n'
                        'G28\n'
                        'M141 S0\n'
                        'G0 Z50 F600\n'
                        'M190 S[bed_temperature_initial_layer_single]\n'
                        'G28 Z\n'
                        'G29; mesh bed leveling ,comment this code to close it\n'
                        'G0 X0 Y0 Z50 F6000\n'
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
 'machine_switch_extruder_time': '0',
 'machine_unload_filament_time': '0',
 'max_layer_height': ['0.32'],
 'min_layer_height': ['0.08'],
 'name': 'fdm_q_common',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': ['stainless_steel'],
 'printable_height': '250',
 'printer_settings_id': '',
 'printer_structure': 'corexy',
 'printer_technology': 'FFF',
 'printer_variant': '0.4',
 'retract_before_wipe': ['0%'],
 'retract_length_toolchange': ['2'],
 'retract_restart_extra': ['0'],
 'retract_restart_extra_toolchange': ['0'],
 'retract_when_changing_layer': ['1'],
 'retraction_length': ['0.8'],
 'retraction_minimum_travel': ['1'],
 'retraction_speed': ['30'],
 'scan_first_layer': '0',
 'silent_mode': '0',
 'single_extruder_multi_material': '1',
 'support_air_filtration': ['1'],
 'support_box_temp_control': '0',
 'support_chamber_temp_control': '1',
 'thumbnail_size': ['380x380', '210x210', '110x110'],
 'type': 'machine',
 'wipe': ['1'],
 'z_hop': ['0.4'],
 'z_hop_types': ['Auto Lift']}
