from __future__ import annotations

# source: profiles/Geeetech/machine/fdm_Geeetech_HS_common.json
DATA = {'auxiliary_fan': '1',
 'change_filament_gcode': '',
 'default_filament_profile': ['Generic PLA @System'],
 'from': 'system',
 'gcode_flavor': 'klipper',
 'inherits': 'fdm_geeetech_common',
 'instantiation': 'false',
 'machine_end_gcode': 'M104 S0\n'
                      'M140 S0\n'
                      'G92 E0\n'
                      'G1 E-3 F1800\n'
                      'G90\n'
                      'G0 Z{min(max_print_height,max_layer_z+10)} F600\n'
                      'G0 X0 Y{print_bed_max[1]} F12000',
 'machine_max_acceleration_e': ['5000', '5000'],
 'machine_max_acceleration_extruding': ['20000', '20000'],
 'machine_max_acceleration_retracting': ['5000', '5000'],
 'machine_max_acceleration_travel': ['20000', '20000'],
 'machine_max_acceleration_x': ['20000', '20000'],
 'machine_max_acceleration_y': ['20000', '20000'],
 'machine_max_acceleration_z': ['500', '500'],
 'machine_max_jerk_e': ['2.5', '2.5'],
 'machine_max_jerk_x': ['12', '12'],
 'machine_max_jerk_y': ['12', '12'],
 'machine_max_jerk_z': ['2', '2'],
 'machine_max_speed_e': ['30', '30'],
 'machine_max_speed_x': ['600', '600'],
 'machine_max_speed_y': ['600', '600'],
 'machine_max_speed_z': ['20', '20'],
 'machine_pause_gcode': 'M0',
 'machine_start_gcode': 'G28\n'
                        'M141 S0\n'
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
 'name': 'fdm_Geeetech_HS_common',
 'scan_first_layer': '0',
 'type': 'machine'}
