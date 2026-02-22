from __future__ import annotations

# source: profiles/Sovol/machine/fdm_machine_common.json
DATA = {'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n',
 'change_filament_gcode': '',
 'default_print_profile': '',
 'deretraction_speed': ['40'],
 'extruder_clearance_height_to_lid': '140',
 'extruder_clearance_height_to_rod': '36',
 'extruder_clearance_radius': '65',
 'extruder_colour': ['#FCE94F'],
 'extruder_offset': ['0x0'],
 'from': 'system',
 'gcode_flavor': 'marlin',
 'instantiation': 'false',
 'machine_end_gcode': '',
 'machine_max_acceleration_e': ['5000'],
 'machine_max_acceleration_extruding': ['500'],
 'machine_max_acceleration_retracting': ['1000'],
 'machine_max_acceleration_x': ['500'],
 'machine_max_acceleration_y': ['500'],
 'machine_max_acceleration_z': ['100'],
 'machine_max_jerk_e': ['5'],
 'machine_max_jerk_x': ['8'],
 'machine_max_jerk_y': ['8'],
 'machine_max_jerk_z': ['0.4'],
 'machine_max_speed_e': ['60'],
 'machine_max_speed_x': ['500'],
 'machine_max_speed_y': ['500'],
 'machine_max_speed_z': ['10'],
 'machine_min_extruding_rate': ['0'],
 'machine_min_travel_rate': ['0'],
 'machine_start_gcode': 'G90\n'
                        'G1 X0 Y0 F8000\n'
                        'M140 S[bed_temperature_initial_layer_single] ;set bed temp\n'
                        'M104 S[nozzle_temperature_initial_layer] ;set extruder temp\n'
                        'M190 S[bed_temperature_initial_layer_single] ;wait for bed temp\n'
                        'M109 S[nozzle_temperature_initial_layer];wait for extruder temp\n'
                        '\n'
                        'START_PRINT\n'
                        '\n'
                        'M400\n'
                        'G90\n'
                        'M83\n'
                        'G1 Z0.500 F1200\n'
                        'G1 E10\n'
                        'G1 E-0.200 Z5 F1200\n'
                        'G1 X78.000 Y0.000 F8000\n'
                        'G1 Z0.300 F1200\n'
                        'G1 X128.000 E12 F{outer_wall_volumetric_speed * 1.0 /(0.3*0.5) * 30}\n'
                        'G1 X178.000 E8 F{outer_wall_volumetric_speed * 1.0 /(0.3*0.5) * 60}\n'
                        'G1 X188.000 E-0.200 Z1\n'
                        'M400\n'
                        '\n'
                        'G90\n'
                        'M83\n'
                        'G1 X78.000 Y1.000 F8000\n'
                        'G1 Z0.300 F1200\n'
                        'G1 X128.000 E12 F{outer_wall_volumetric_speed * 1.0 /(0.3*0.5) * 30}\n'
                        'G1 X178.000 E8 F{outer_wall_volumetric_speed * 1.0 /(0.3*0.5) * 60}\n'
                        'G1 X188.000 E-0.500 Z1\n'
                        'M400\n'
                        '\n',
 'max_layer_height': ['0.32'],
 'min_layer_height': ['0.08'],
 'name': 'fdm_machine_common',
 'nozzle_diameter': ['0.4'],
 'printable_height': '250',
 'printer_settings_id': '',
 'printer_technology': 'FFF',
 'printer_variant': '0.4',
 'retract_before_wipe': ['70%'],
 'retract_length_toolchange': ['1'],
 'retract_lift_below': ['0'],
 'retract_restart_extra': ['0'],
 'retract_restart_extra_toolchange': ['0'],
 'retract_when_changing_layer': ['1'],
 'retraction_length': ['1'],
 'retraction_minimum_travel': ['2'],
 'retraction_speed': ['60'],
 'silent_mode': '0',
 'single_extruder_multi_material': '1',
 'type': 'machine',
 'wipe': ['1'],
 'z_hop': ['0'],
 'z_hop_types': 'Normal Lift',
 'z_lift_type': 'NormalLift'}
