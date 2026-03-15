from __future__ import annotations

# source: profiles/Flashforge/machine/Flashforge Guider 2s 0.4 nozzle.json
DATA = {'auxiliary_fan': '1',
 'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\n;[layer_z]',
 'change_filament_gcode': '',
 'default_filament_profile': ['Flashforge Generic PLA'],
 'default_print_profile': '0.20mm Standard @Flashforge Guider 2s 0.4 nozzle',
 'extruder_clearance_height_to_lid': '70',
 'extruder_clearance_height_to_rod': '23',
 'extruder_clearance_radius': '40',
 'extruder_offset': ['-20', '10'],
 'from': 'system',
 'gcode_flavor': 'marlin',
 'inherits': 'fdm_flashforge_common',
 'instantiation': 'true',
 'layer_change_gcode': ';AFTER_LAYER_CHANGE\n;[layer_z]',
 'machine_end_gcode': 'M104 S0 T0; cool down extruder\n'
                      'M140 S0 T0; cool down bed\n'
                      'G162 Z F1800\n'
                      'G28 X Y; home axes\n'
                      'M132 X Y A B; recall home offsets from EPROM\n'
                      'M652; turn off rear fan\n'
                      'G91; set to relative positioning\n'
                      'M18; disable stepper motors',
 'machine_max_acceleration_e': ['200', '200'],
 'machine_max_acceleration_extruding': ['200', '200'],
 'machine_max_acceleration_retracting': ['200', '200'],
 'machine_max_acceleration_travel': ['200', '200'],
 'machine_max_acceleration_x': ['200', '200'],
 'machine_max_acceleration_y': ['200', '200'],
 'machine_max_acceleration_z': ['200', '200'],
 'machine_max_jerk_e': ['2.5', '2.5'],
 'machine_max_jerk_x': ['9', '9'],
 'machine_max_jerk_y': ['9', '9'],
 'machine_max_jerk_z': ['3', '3'],
 'machine_max_speed_e': ['100', '100'],
 'machine_max_speed_x': ['200', '200'],
 'machine_max_speed_y': ['200', '200'],
 'machine_max_speed_z': ['20', '20'],
 'machine_pause_gcode': 'M25',
 'machine_start_gcode': 'M118 X10 Y10 Z10\n'
                        'M140 S[bed_temperature_initial_layer_single]; set initial bed temp\n'
                        'M104 S[nozzle_temperature_initial_layer] T0; set initial extruder temp\n'
                        'M107; disable cooling fan\n'
                        'G90; set to absolute positioning\n'
                        'G28; home axes\n'
                        'M132 X Y A B; recall home offsets from EPROM\n'
                        'G1 Z50.0 F420; adjust Z\n'
                        'G161 X Y F3300\n'
                        'M7; wait for bed to stabilize\n'
                        'M6 T0; wait for extruder to stabilize\n'
                        'M651 S255; start case fan\n'
                        'G1 Z0.3 F3600; move down to purge\n'
                        'G92 E0; zero extruders\n'
                        'G1 X120 Y-125 E20 F2000; extrude a line of filament across the front edge of the bed\n'
                        'G1 X130 Y-125 F180; wait for ooze\n'
                        'G1 X140 Y-125 F5000; fast wipe\n'
                        'G1 Z1 F100; lift\n'
                        'G92 E0; zero extruders again\n'
                        'G1 E-1.0000 F1800',
 'max_layer_height': ['0.8'],
 'min_layer_height': ['0.02'],
 'name': 'Flashforge Guider 2s 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'undefine',
 'printable_area': ['-140x-125', '140x-125', '140x125', '-140x125'],
 'printable_height': '300',
 'printer_model': 'Flashforge Guider 2s',
 'printer_settings_id': 'Flashforge',
 'printer_variant': '0.4',
 'retract_before_wipe': ['100%'],
 'retract_length_toolchange': ['2'],
 'retraction_length': ['1'],
 'retraction_minimum_travel': ['1'],
 'retraction_speed': ['100'],
 'setting_id': 'GM001',
 'single_extruder_multi_material': '0',
 'type': 'machine',
 'use_relative_e_distances': '0',
 'wipe_distance': '2',
 'z_hop': ['0']}
