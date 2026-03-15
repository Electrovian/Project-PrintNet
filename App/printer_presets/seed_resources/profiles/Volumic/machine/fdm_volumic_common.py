from __future__ import annotations

# source: profiles/Volumic/machine/fdm_volumic_common.json
DATA = {'bed_exclude_area': ['0x0'],
 'before_layer_change_gcode': 'G92 E0',
 'change_filament_gcode': 'M600',
 'default_filament_profile': ['Volumic UNIVERSAL Ultra'],
 'emit_machine_limits_to_gcode': ['0'],
 'from': 'system',
 'gcode_flavor': 'marlin',
 'instantiation': 'false',
 'machine_end_gcode': 'M107\nM104 S0\nM140 S0\nG0 X1 Y299 F5000\nM84\nM300',
 'machine_max_acceleration_e': ['0', '0'],
 'machine_max_acceleration_extruding': ['0', '0'],
 'machine_max_acceleration_retracting': ['0', '0'],
 'machine_max_acceleration_travel': ['0', '0'],
 'machine_max_acceleration_x': ['0', '0'],
 'machine_max_acceleration_y': ['0', '0'],
 'machine_max_acceleration_z': ['0', '0'],
 'machine_max_jerk_e': ['0', '0'],
 'machine_max_jerk_x': ['0', '0'],
 'machine_max_jerk_y': ['0', '0'],
 'machine_max_jerk_z': ['0', '0'],
 'machine_max_speed_e': ['0', '0'],
 'machine_max_speed_x': ['0', '0'],
 'machine_max_speed_y': ['0', '0'],
 'machine_max_speed_z': ['0', '0'],
 'machine_min_extruding_rate': ['0', '0'],
 'machine_min_travel_rate': ['0', '0'],
 'machine_pause_gcode': 'M601',
 'machine_start_gcode': 'M117 Demarrage\n'
                        'M106 S0\n'
                        'M140 S[first_layer_bed_temperature]\n'
                        'M104 T0 S[first_layer_temperature]\n'
                        'G28\n'
                        'G90\n'
                        'M82\n'
                        'G92 E0\n'
                        'G1 Z5 F600\n'
                        'G1 X1 Y299 F6000\n'
                        'M109 T0 S[first_layer_temperature]\n'
                        'M300 P350\n'
                        'G92 E0\n'
                        'M117 Impression',
 'name': 'fdm_volumic_common',
 'nozzle_type': 'undefine',
 'printer_settings_id': '',
 'printer_technology': 'FFF',
 'printer_variant': '0.4',
 'retract_before_wipe': ['70%'],
 'retract_length_toolchange': ['6'],
 'retract_when_changing_layer': ['1'],
 'retraction_length': ['2.4'],
 'retraction_minimum_travel': ['1'],
 'retraction_speed': ['30'],
 'scan_first_layer': '0',
 'silent_mode': '0',
 'single_extruder_multi_material': '1',
 'type': 'machine',
 'wipe': ['1'],
 'z_hop': ['0']}
