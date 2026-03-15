from __future__ import annotations

# source: profiles/Anycubic/machine/Anycubic Kobra Plus 0.4 nozzle.json
DATA = {'auxiliary_fan': '0',
 'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\n;G92 E0.0\n;[layer_z]\n\n',
 'change_filament_gcode': 'M600',
 'default_filament_profile': ['Anycubic Generic PLA'],
 'default_print_profile': '0.20mm Standard @Anycubic KobraPlus',
 'deretraction_speed': ['40'],
 'from': 'system',
 'inherits': 'fdm_machine_common',
 'instantiation': 'true',
 'layer_change_gcode': ';AFTER_LAYER_CHANGE\n;[layer_z]',
 'machine_end_gcode': 'M104 S0;extruder heater off\n'
                      'M140 S0;heated bed heater off (if you have it)\n'
                      'G91;relative positioning\n'
                      'G1 Z+10 F3600 ;move Z up a bit\n'
                      'G90;absolute positioning\n'
                      'G1 X10 F3000; get the head off the bed\n'
                      'G1 F3000 Y400 ;kick the bed out\n'
                      'M84;steppers off\n'
                      'M355 S0;turn off the case light',
 'machine_max_acceleration_e': ['3000', '5000'],
 'machine_max_acceleration_extruding': ['4000', '1250'],
 'machine_max_acceleration_retracting': ['1000', '1250'],
 'machine_max_acceleration_travel': ['4000', '1250'],
 'machine_max_acceleration_x': ['700', '960'],
 'machine_max_acceleration_y': ['600', '960'],
 'machine_max_acceleration_z': ['100', '200'],
 'machine_max_jerk_e': ['5', '4.5'],
 'machine_max_jerk_x': ['20', '8'],
 'machine_max_jerk_y': ['20', '8'],
 'machine_max_jerk_z': ['0.3', '0.4'],
 'machine_max_speed_e': ['60', '120'],
 'machine_max_speed_x': ['300', '100'],
 'machine_max_speed_y': ['300', '100'],
 'machine_max_speed_z': ['40', '12'],
 'machine_pause_gcode': 'M601',
 'machine_start_gcode': "M104 S140;start the nozzle preheat and don't wait\n"
                        'G21;metric values\n'
                        'G90;absolute positioning\n'
                        'M82;set extruder to absolute mode\n'
                        'M107;start with the fan off\n'
                        'G28;home all\n'
                        'M190 S[bed_temperature_initial_layer_single] ; set wait for bed temp\n'
                        'M355 S1;turn on the case light\n'
                        'M109 S[nozzle_temperature_initial_layer]; wait for extruder temp\n'
                        'G1 Z15.0 F1000 ;move the nozzle up 15mm\n'
                        'G92 E0;zero the extruded length\n'
                        'G1 F100 E60;extrude 60mm of feed stock\n'
                        'G92 E0;zero the extruded length again',
 'max_layer_height': ['0.3'],
 'min_layer_height': ['0.15'],
 'name': 'Anycubic Kobra Plus 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'undefine',
 'printable_area': ['0x0', '300x0', '300x300', '0x300'],
 'printable_height': '350',
 'printer_model': 'Anycubic Kobra Plus',
 'printer_settings_id': 'Anycubic',
 'retract_before_wipe': ['70%'],
 'retract_length_toolchange': ['4'],
 'retraction_length': ['6'],
 'retraction_minimum_travel': ['5'],
 'retraction_speed': ['40'],
 'scan_first_layer': '0',
 'setting_id': 'GM001',
 'single_extruder_multi_material': '1',
 'type': 'machine'}
