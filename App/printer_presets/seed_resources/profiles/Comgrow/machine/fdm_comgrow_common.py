from __future__ import annotations

# source: profiles/Comgrow/machine/fdm_comgrow_common.json
DATA = {'auxiliary_fan': '0',
 'bed_exclude_area': ['0x0'],
 'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n',
 'change_filament_gcode': 'PAUSE',
 'default_filament_profile': ['Comgrow Generic PETG'],
 'default_print_profile': '0.20mm Standard @Comgrow T500',
 'deretraction_speed': ['30'],
 'extruder_clearance_height_to_lid': '140',
 'extruder_clearance_height_to_rod': '36',
 'extruder_clearance_radius': '65',
 'from': 'system',
 'gcode_flavor': 'klipper',
 'inherits': 'fdm_machine_common',
 'instantiation': 'false',
 'layer_change_gcode': ';AFTER_LAYER_CHANGE\n;[layer_z]',
 'machine_end_gcode': '{if max_layer_z < printable_height}G1 Z{z_offset+min(max_layer_z+2, printable_height)} F600 ; '
                      'Move print head up{endif}\n'
                      'G1 X5 Y{print_bed_max[1]*0.8} F{travel_speed*60} ; present print\n'
                      '{if max_layer_z < printable_height-10}G1 Z{z_offset+min(max_layer_z+70, printable_height-10)} '
                      'F600 ; Move print head further up{endif}\n'
                      '{if max_layer_z < max_print_height*0.6}G1 Z{printable_height*0.6} F600 ; Move print head '
                      'further up{endif}\n'
                      'M140 S0 ; turn off heatbed\n'
                      'M104 S0 ; turn off temperature\n'
                      'M107 ; turn off fan\n'
                      'M84 X Y E ; disable motors',
 'machine_max_acceleration_e': ['5000', '5000'],
 'machine_max_acceleration_extruding': ['20000', '20000'],
 'machine_max_acceleration_retracting': ['5000', '5000'],
 'machine_max_acceleration_travel': ['3000', '3000'],
 'machine_max_acceleration_x': ['3000', '3000'],
 'machine_max_acceleration_y': ['3000', '3000'],
 'machine_max_acceleration_z': ['500', '200'],
 'machine_max_jerk_e': ['2.5', '2.5'],
 'machine_max_jerk_x': ['12', '12'],
 'machine_max_jerk_y': ['12', '12'],
 'machine_max_jerk_z': ['0.2', '0.4'],
 'machine_max_speed_e': ['25', '25'],
 'machine_max_speed_x': ['300', '300'],
 'machine_max_speed_y': ['300', '300'],
 'machine_max_speed_z': ['12', '12'],
 'machine_min_extruding_rate': ['0', '0'],
 'machine_min_travel_rate': ['0', '0'],
 'machine_pause_gcode': 'PAUSE',
 'machine_start_gcode': 'G90 ; use absolute coordinates\n'
                        'M83 ; extruder relative mode\n'
                        'G28 ; home all\n'
                        'M104 S[nozzle_temperature_initial_layer] ; set extruder temp\n'
                        'M140 S[bed_temperature_initial_layer_single] ; set bed temp\n'
                        'M190 S[bed_temperature_initial_layer_single] ; wait for bed temp\n'
                        'M109 S[nozzle_temperature_initial_layer] ; wait for extruder temp\n'
                        'G1 Z2 F240\n'
                        'G1 X2 Y10 F3000\n'
                        'G1 Z0.28 F240\n'
                        'G92 E0\n'
                        'G1 Y190 E15 F1500 ; intro line\n'
                        'G1 X2.3 F5000\n'
                        'G92 E0\n'
                        'G1 Y10 E15 F1200 ; intro line\n'
                        'G92 E0',
 'max_layer_height': ['0.56'],
 'min_layer_height': ['0.08'],
 'name': 'fdm_comgrow_common',
 'nozzle_type': 'hardened_steel',
 'printable_height': '500',
 'printer_settings_id': '',
 'printer_technology': 'FFF',
 'printer_variant': '0.4',
 'retract_before_wipe': ['70%'],
 'retract_length_toolchange': ['2'],
 'retract_restart_extra': ['0'],
 'retract_restart_extra_toolchange': ['0'],
 'retract_when_changing_layer': ['1'],
 'retraction_length': ['0.5'],
 'retraction_minimum_travel': ['1'],
 'retraction_speed': ['30'],
 'scan_first_layer': '0',
 'silent_mode': '0',
 'single_extruder_multi_material': '1',
 'thumbnails': ['32x32', '300x300'],
 'thumbnails_format': 'PNG',
 'type': 'machine',
 'wipe': ['1'],
 'z_hop': ['0'],
 'z_hop_types': 'Normal Lift'}
