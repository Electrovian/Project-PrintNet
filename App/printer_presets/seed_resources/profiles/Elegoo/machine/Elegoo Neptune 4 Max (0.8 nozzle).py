from __future__ import annotations

# source: profiles/Elegoo/machine/Elegoo Neptune 4 Max (0.8 nozzle).json
DATA = {'auxiliary_fan': '1',
 'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\nG92 E0\n;[layer_z]\n\n',
 'change_filament_gcode': 'M600',
 'cooling_tube_length': '5',
 'cooling_tube_retraction': '91.5',
 'default_filament_profile': ['Generic PLA @Elegoo'],
 'default_print_profile': '0.20mm Standard @Elegoo Neptune4Max (0.6 nozzle)',
 'deretraction_speed': ['45'],
 'enable_filament_ramming': '1',
 'extra_loading_move': '-2',
 'extruder_clearance_height_to_lid': '34',
 'extruder_clearance_height_to_rod': '34',
 'extruder_clearance_radius': '47',
 'extruder_colour': ['#FCE94F'],
 'extruder_offset': ['0x0'],
 'fan_kickstart': '0',
 'fan_speedup_overhangs': '1',
 'fan_speedup_time': '0',
 'from': 'system',
 'gcode_flavor': 'klipper',
 'high_current_on_filament_swap': '0',
 'host_type': 'octoprint',
 'inherits': 'fdm_neptune_4_common',
 'instantiation': 'true',
 'layer_change_gcode': ';AFTER_LAYER_CHANGE\n;[layer_z]',
 'machine_end_gcode': ';PRINT_END\n'
                      'G91 ;Relative positionning\n'
                      'G1 E-2 F2700 ;Retract a bit\n'
                      'G1 E-8 X5 Y5 Z3 F3000 ;Retract\n'
                      'G90 ;Absolute positionning\n'
                      'G1 X10 Y400 F6000;Finish print\n'
                      'M106 S0 ;Turn-off fan\n'
                      'M104 S0 ;Turn-off hotend\n'
                      'M140 S0 ;Turn-off bed\n'
                      'M84 X Y E ;Disable all steppers but Z',
 'machine_load_filament_time': '0',
 'machine_max_speed_x': ['300', '300'],
 'machine_max_speed_y': ['300', '300'],
 'machine_pause_gcode': 'PAUSE',
 'machine_start_gcode': ';ELEGOO NEPTUNE 4 MAX\n'
                        'M220 S100 ;Set the feed speed to 100%\n'
                        'M221 S100 ;Set the flow rate to 100%\n'
                        'M104 S140\n'
                        'M190 S[bed_temperature_initial_layer_single]\n'
                        'G90\n'
                        'G28 ;home\n'
                        'G1 Z10 F300\n'
                        'G1 X165 Y0.5 F6000\n'
                        'G1 Z0 F300\n'
                        'M109 S[nozzle_temperature_initial_layer]\n'
                        'G92 E0 ;Reset Extruder\n'
                        'G1 X165 Y0.5 Z0.4 F300 ;Move to start position\n'
                        'G1 X265 E30 F400 ;Draw the first line\n'
                        'G1 Z0.6 F120.0 ;Move to side a little\n'
                        'G1 X260 F3000\n'
                        'G92 E0 ;Reset Extruder',
 'machine_unload_filament_time': '0',
 'max_layer_height': ['0.64'],
 'min_layer_height': ['0.20'],
 'name': 'Elegoo Neptune 4 Max (0.8 nozzle)',
 'nozzle_diameter': ['0.8'],
 'nozzle_hrc': '0',
 'nozzle_type': 'brass',
 'nozzle_volume': '0',
 'parking_pos_retraction': '92',
 'printable_area': ['0x0', '420x0', '420x420', '0x420'],
 'printable_height': '480',
 'printer_model': 'Elegoo Neptune 4 Max',
 'printer_notes': '',
 'printer_settings_id': 'Elegoo',
 'printer_variant': '0.8',
 'retract_before_wipe': ['85%'],
 'retract_length_toolchange': ['2'],
 'retract_lift_above': ['0'],
 'retract_lift_below': ['0'],
 'retract_lift_enforce': ['All Surfaces'],
 'retract_restart_extra': ['0'],
 'retract_restart_extra_toolchange': ['0'],
 'retract_when_changing_layer': ['1'],
 'retraction_length': ['0.7'],
 'retraction_minimum_travel': ['1'],
 'retraction_speed': ['60'],
 'scan_first_layer': '0',
 'setting_id': 'GM001',
 'single_extruder_multi_material': '1',
 'type': 'machine',
 'use_firmwware_retraction': '0',
 'use_relative_e_distances': '1',
 'wipe': ['1'],
 'wipe_distance': ['1'],
 'z_hop': ['0.4'],
 'z_hop_types': ['Normal Lift']}
