from __future__ import annotations

# source: profiles/Qidi/machine/fdm_machine_common.json
DATA = {'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n',
 'change_filament_gcode': '',
 'default_print_profile': '',
 'deretraction_speed': ['40'],
 'extruder_clearance_height_to_lid': '140',
 'extruder_clearance_height_to_rod': '36',
 'extruder_clearance_radius': '65',
 'extruder_colour': [''],
 'extruder_offset': ['0x0'],
 'from': 'system',
 'gcode_flavor': 'marlin',
 'instantiation': 'false',
 'machine_end_gcode': 'M104 S0\n'
                      'M140 S0\n'
                      'G92 E0\n'
                      'G1 E-3 F1800\n'
                      'G90\n'
                      '{if max_layer_z < max_print_height / 2}\n'
                      'G1 Z{max_print_height / 2 + 10} F600\n'
                      '{else}\n'
                      'G1 Z{min(max_print_height, max_layer_z + 10)}\n'
                      '{endif}\n'
                      'G0 X5 Y{print_bed_max[1]-11} F12000\n'
                      'M141 S0',
 'machine_max_acceleration_e': ['5000'],
 'machine_max_acceleration_extruding': ['20000'],
 'machine_max_acceleration_retracting': ['5000'],
 'machine_max_acceleration_x': ['20000'],
 'machine_max_acceleration_y': ['20000'],
 'machine_max_acceleration_z': ['500'],
 'machine_max_jerk_e': ['2'],
 'machine_max_jerk_x': ['9'],
 'machine_max_jerk_y': ['9'],
 'machine_max_jerk_z': ['3'],
 'machine_max_speed_e': ['30'],
 'machine_max_speed_x': ['600'],
 'machine_max_speed_y': ['600'],
 'machine_max_speed_z': ['10'],
 'machine_min_extruding_rate': ['0'],
 'machine_min_travel_rate': ['0'],
 'machine_start_gcode': 'G28\n'
                        'G0 Z50 F600\n'
                        'M190 S[first_layer_bed_temperature]\n'
                        'G28 Z\n'
                        'G29 ; mesh bed leveling ,comment this code to close it\n'
                        'G0 X0 Y0 Z50 F6000\n'
                        'M109 S[first_layer_temperature]\n'
                        'M83\n'
                        'G0 Z5 F1200\n'
                        'G0 X{first_layer_print_min[0]} Y{max(0, first_layer_print_min[1] - 2)} F12000\n'
                        'G0 Z0.2 F600\n'
                        'G1 E3 F1800\n'
                        'G0 Z0.3 F600\n'
                        'G1 X{min(first_layer_print_min[0] + 30,print_bed_max[0])} E6 F600',
 'max_layer_height': ['0.32'],
 'min_layer_height': ['0.08'],
 'name': 'fdm_machine_common',
 'nozzle_diameter': ['0.4'],
 'printable_height': '250',
 'printer_settings_id': '',
 'printer_technology': 'FFF',
 'printer_variant': '0.4',
 'retract_before_wipe': ['0%'],
 'retract_length_toolchange': ['2'],
 'retract_restart_extra': ['0'],
 'retract_restart_extra_toolchange': ['0'],
 'retract_when_changing_layer': ['1'],
 'retraction_length': ['1'],
 'retraction_minimum_travel': ['1'],
 'retraction_speed': ['30'],
 'silent_mode': '0',
 'single_extruder_multi_material': '1',
 'time_lapse_gcode': ';TIMELAPSE_TAKE_FRAME\n',
 'type': 'machine',
 'wipe': ['1'],
 'z_hop': ['0'],
 'z_hop_types': ['Auto Lift']}
