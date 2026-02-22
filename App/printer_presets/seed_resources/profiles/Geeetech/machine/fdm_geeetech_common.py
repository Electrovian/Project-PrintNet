from __future__ import annotations

# source: profiles/Geeetech/machine/fdm_geeetech_common.json
DATA = {'auxiliary_fan': '0',
 'bed_exclude_area': ['0x0'],
 'change_filament_gcode': '',
 'default_filament_profile': ['Generic PLA @System'],
 'deretraction_speed': ['20'],
 'extruder_clearance_dist_to_rod': '24',
 'extruder_clearance_height_to_lid': '34',
 'extruder_clearance_height_to_rod': '34',
 'extruder_clearance_max_radius': '47',
 'from': 'system',
 'gcode_flavor': 'marlin',
 'inherits': 'fdm_machine_common',
 'instantiation': 'false',
 'layer_change_gcode': ';------------------------------------\n'
                       ';layer No: [layer_num] ———>Print Height: [layer_z] mm\n'
                       ';------------------------------------',
 'machine_end_gcode': '{if max_layer_z < printable_height}G1 Z{min(max_layer_z+2, printable_height)} F600 ; Move print '
                      'head up{endif}\n'
                      'G1 X5 Y{print_bed_max[1]*0.8} F{travel_speed*60} ; present print\n'
                      '{if max_layer_z < printable_height-10}G1 Z{min(max_layer_z+70, printable_height-10)} F600 ; '
                      'Move print head further up{endif}\n'
                      '{if max_layer_z < printable_height*0.6}G1 Z{printable_height*0.6} F600 ; Move print head '
                      'further up{endif}\n'
                      'M140 S0 ; turn off heatbed\n'
                      'M104 S0 ; turn off temperature\n'
                      'M107 ; turn off fan\n'
                      'M84 X Y E ; disable motors',
 'machine_max_acceleration_e': ['5000', '5000'],
 'machine_max_acceleration_extruding': ['1000', '1000'],
 'machine_max_acceleration_retracting': ['1000', '1000'],
 'machine_max_acceleration_travel': ['500', '500'],
 'machine_max_acceleration_x': ['500', '500'],
 'machine_max_acceleration_y': ['500', '500'],
 'machine_max_acceleration_z': ['500', '500'],
 'machine_max_jerk_e': ['5', '5'],
 'machine_max_jerk_x': ['8', '8'],
 'machine_max_jerk_y': ['8', '8'],
 'machine_max_jerk_z': ['0.4', '0.4'],
 'machine_max_speed_e': ['60', '60'],
 'machine_max_speed_x': ['200', '200'],
 'machine_max_speed_y': ['200', '200'],
 'machine_max_speed_z': ['10', '10'],
 'machine_min_extruding_rate': ['0', '0'],
 'machine_min_travel_rate': ['0', '0'],
 'machine_pause_gcode': 'M25 ;pause print',
 'machine_start_gcode': 'G90 ; use absolute coordinates\n'
                        'M83 ; extruder relative mode\n'
                        'M140 S[bed_temperature_initial_layer] ; set final bed temp\n'
                        'M104 S150 ; set temporary nozzle temp to prevent oozing during homing\n'
                        'G4 S10 ; allow partial nozzle warmup\n'
                        'G28 ; home all axis\n'
                        'G1 Z50 F240\n'
                        'G1 X2 Y10 F3000\n'
                        'M104 S[nozzle_temperature_initial_layer] ; set final nozzle temp\n'
                        'M190 S[bed_temperature_initial_layer] ; wait for bed temp to stabilize\n'
                        'M109 S[nozzle_temperature_initial_layer] ; wait for nozzle temp to stabilize\n'
                        'G1 Z0.28 F240\n'
                        'G92 E0\n'
                        'G1 Y140 E10 F1500 ; prime the nozzle\n'
                        'G1 X2.3 F5000\n'
                        'G92 E0\n'
                        'G1 Y10 E10 F1200 ; prime the nozzle\n'
                        'G92 E0',
 'max_layer_height': ['0.32'],
 'min_layer_height': ['0.08'],
 'name': 'fdm_geeetech_common',
 'nozzle_type': 'undefine',
 'printable_height': '250',
 'printer_settings_id': '',
 'printer_technology': 'FFF',
 'printer_variant': '0.4',
 'retract_before_wipe': ['70%'],
 'retract_length_toolchange': ['2'],
 'retract_restart_extra': ['0'],
 'retract_restart_extra_toolchange': ['0'],
 'retract_when_changing_layer': ['1'],
 'retraction_length': ['7'],
 'retraction_minimum_travel': ['2'],
 'retraction_speed': ['20'],
 'scan_first_layer': '0',
 'silent_mode': '0',
 'single_extruder_multi_material': '1',
 'support_multi_bed_types': '1',
 'type': 'machine',
 'wipe': ['1'],
 'z_hop': ['0'],
 'z_hop_types': 'Normal Lift'}
