from __future__ import annotations

# source: profiles/Elegoo/machine/Elegoo Neptune 2 0.4 nozzle.json
DATA = {'auxiliary_fan': '0',
 'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\nG92 E0\n;[layer_z]\n\n',
 'change_filament_gcode': '',
 'default_filament_profile': ['Generic PLA @Elegoo'],
 'default_print_profile': '0.20mm Standard @Elegoo Neptune2',
 'deretraction_speed': ['40'],
 'from': 'system',
 'inherits': 'fdm_elegoo_common',
 'instantiation': 'true',
 'layer_change_gcode': ';AFTER_LAYER_CHANGE\n;[layer_z]',
 'machine_end_gcode': '{if max_layer_z < printable_height}G1 Z{z_offset+min(max_layer_z+2, printable_height)} F600 ; '
                      'Move print head up{endif}\n'
                      'G1 X5 Y{print_bed_max[1]*0.8} F{travel_speed*60} ; present print\n'
                      '{if max_layer_z < printable_height-10}G1 Z{z_offset+min(max_layer_z+70, printable_height-10)} '
                      'F600 ; Move print head further up{endif}\n'
                      '{if max_layer_z < printable_height*0.6}G1 Z{printable_height*0.6} F600 ; Move print head '
                      'further up{endif}\n'
                      'M140 S0 ; turn off heatbed\n'
                      'M104 S0 ; turn off temperature\n'
                      'M107 ; turn off fan\n'
                      'M84 X Y E ; disable motors',
 'machine_max_acceleration_extruding': ['500', '500'],
 'machine_max_acceleration_retracting': ['1000', '1000'],
 'machine_max_acceleration_travel': ['500', '500'],
 'machine_max_acceleration_x': ['500', '500'],
 'machine_max_acceleration_y': ['500', '500'],
 'machine_max_acceleration_z': ['100', '100'],
 'machine_max_jerk_e': ['5', '5'],
 'machine_max_jerk_x': ['8', '8'],
 'machine_max_jerk_y': ['8', '8'],
 'machine_max_jerk_z': ['0.4', '0.4'],
 'machine_max_speed_e': ['60', '60'],
 'machine_max_speed_x': ['500', '500'],
 'machine_max_speed_y': ['500', '500'],
 'machine_max_speed_z': ['10', '10'],
 'machine_pause_gcode': 'M0',
 'machine_start_gcode': 'M413 S0 ; disable Power Loss Recovery\n'
                        'G90 ; use absolute coordinates\n'
                        'M83 ; extruder relative mode\n'
                        'M104 S120 ; set temporary nozzle temp to prevent oozing during homing and auto bed leveling\n'
                        'M140 S[bed_temperature_initial_layer_single] ; set final bed temp\n'
                        'G4 S10 ; allow partial nozzle warmup\n'
                        'G28 ; home all axis\n'
                        ';G29 ; run abl mesh\n'
                        'M420 S1 ; load mesh\n'
                        'G1 Z50 F240\n'
                        'G1 X2 Y10 F3000\n'
                        'M104 S[nozzle_temperature_initial_layer] ; set final nozzle temp\n'
                        'M190 S[bed_temperature_initial_layer_single] ; wait for bed temp to stabilize\n'
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
 'name': 'Elegoo Neptune 2 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'hardened_steel',
 'printable_area': ['0x0', '220x0', '220x220', '0x220'],
 'printable_height': '250',
 'printer_model': 'Elegoo Neptune 2',
 'printer_settings_id': 'Elegoo',
 'retract_before_wipe': ['70%'],
 'retract_length_toolchange': ['1'],
 'retraction_length': ['2.5'],
 'retraction_minimum_travel': ['2'],
 'retraction_speed': ['60'],
 'scan_first_layer': '0',
 'setting_id': 'GM001',
 'single_extruder_multi_material': '1',
 'type': 'machine'}
