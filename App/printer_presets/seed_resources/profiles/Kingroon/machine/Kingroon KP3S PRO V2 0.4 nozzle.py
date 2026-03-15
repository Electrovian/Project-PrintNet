from __future__ import annotations

# source: profiles/Kingroon/machine/Kingroon KP3S PRO V2 0.4 nozzle.json
DATA = {'bed_exclude_area': ['0x0'],
 'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n',
 'default_filament_profile': 'Generic PLA @System',
 'default_print_profile': '0.20mm Standard @Kingroon KP3S PRO V2',
 'deretraction_speed': ['45'],
 'extruder_colour': ['#FCE94F'],
 'from': 'system',
 'inherits': 'fdm_klipper_common',
 'instantiation': 'true',
 'layer_change_gcode': ';AFTER_LAYER_CHANGE\n;[layer_z]',
 'machine_end_gcode': '{if max_layer_z < max_print_height}G1 Z{z_offset+min(max_layer_z+2, max_print_height)} F600 ; '
                      'Move print head up{endif}\n'
                      'G1 X5 Y200 F6000 ; present print\n'
                      '{if max_layer_z < max_print_height-10}G1 Z{z_offset+min(max_layer_z+20, max_print_height-10)} '
                      'F600 ; Move print head further up{endif}\n'
                      '{if max_layer_z < max_print_height*0.6}G1 Z{max_print_height*0.6} F600 ; Move print head '
                      'further up{endif}\n'
                      'M140 S0 ; turn off heatbed\n'
                      'M104 S0 ; turn off temperature\n'
                      'M107 ; turn off fan\n'
                      'M84 X Y E ; disable motors\n'
                      'END_PRINT',
 'machine_max_acceleration_e': ['10000', '5000'],
 'machine_max_acceleration_extruding': ['10000', '9000'],
 'machine_max_acceleration_retracting': ['10000', '9000'],
 'machine_max_acceleration_x': ['10000', '9000'],
 'machine_max_acceleration_y': ['10000', '9000'],
 'machine_max_acceleration_z': ['10000', '100'],
 'machine_max_jerk_e': ['20', '5'],
 'machine_max_jerk_x': ['20', '7'],
 'machine_max_jerk_y': ['20', '7'],
 'machine_start_gcode': 'START_PRINT EXTRUDER_TEMP=[first_layer_temperature] BED_TEMP=[first_layer_bed_temperature]\n'
                        'CANCEL_POWEROFF\n'
                        'G90 ; use absolute coordinates\n'
                        'M83 ; extruder relative mode\n'
                        'G92 E0',
 'max_layer_height': ['0.32'],
 'name': 'Kingroon KP3S PRO V2 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'printable_area': ['0x0', '205x0', '205x205', '0x205'],
 'printable_height': '200',
 'printer_model': 'Kingroon KP3S PRO V2',
 'retraction_length': ['0.8'],
 'retraction_speed': ['45'],
 'setting_id': 'GM003',
 'type': 'machine',
 'use_firmware_retraction': '1',
 'wipe': ['0'],
 'z_hop': ['0']}
