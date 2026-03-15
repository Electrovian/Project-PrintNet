from __future__ import annotations

# source: profiles/Geeetech/machine/Geeetech Mizar Max 0.6 nozzle.json
DATA = {'auxiliary_fan': '0',
 'default_filament_profile': ['Generic PLA @System'],
 'default_print_profile': '0.30mm Standard @Geeetech common 0.6 nozzle',
 'extruder_type': ['Bowden'],
 'from': 'system',
 'inherits': 'fdm_geeetech_common',
 'instantiation': 'true',
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
 'machine_start_gcode': ';Custom Start G-code\n'
                        'M104 S[first_layer_temperature] ; set extruder temp\n'
                        'M140 S[first_layer_bed_temperature] ; set bed temp\n'
                        'M190 S[first_layer_bed_temperature] ; wait for bed temp\n'
                        'M109 S[first_layer_temperature] ; wait for extruder temp\n'
                        'M220 S100 ;Reset Feedrate\n'
                        'M221 S100 ;Reset Flowrate\n'
                        'G92 E0 ; Reset Extruder\n'
                        'G28 ; Home all axes\n'
                        'M107 ;Off Fan\n'
                        'G1 Z5.0 F3000 ;Move Z Axis up little to prevent scratching of Heat Bed\n'
                        'G1 X0.1 Y20 Z1.4 F6000 ; Move to start position\n'
                        'G1 X0.1 Y80.0 Z1.4 F1000 E25 ; Draw the first line\n'
                        'G92 E0 ; Reset Extruder\n'
                        'G1 X0.4 Y80.0 Z1.4 F6000 ; Move to side a little\n'
                        'G1 X1.4 Y20 Z1.4 F1000 E20 ; Draw the second line\n'
                        'G92 E0 ; Reset Extruder\n'
                        'G1 Z2.0 F3000 ; Move Z Axis up little to prevent scratching of Heat Bed\n'
                        'G1 X5 Y20 Z0.28 F3000.0 ; Move over to prevent blob squish\n'
                        'G92 E0',
 'max_layer_height': ['0.42'],
 'min_layer_height': ['0.12'],
 'name': 'Geeetech Mizar Max 0.6 nozzle',
 'nozzle_diameter': ['0.6'],
 'nozzle_type': 'brass',
 'printable_area': ['0x0', '320x0', '320x320', '0x320'],
 'printable_height': '400',
 'printer_model': 'Geeetech Mizar Max',
 'printer_variant': '0.6',
 'retract_lift_below': ['399'],
 'setting_id': 'GM_GEEETECH_019',
 'type': 'machine'}
