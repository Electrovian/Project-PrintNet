from __future__ import annotations

# source: profiles/Geeetech/machine/Geeetech A10 M 0.4 nozzle.json
DATA = {'auxiliary_fan': '0',
 'default_filament_profile': ['Generic PLA @System'],
 'default_print_profile': '0.20mm Standard @Geeetech common',
 'deretraction_speed': ['25'],
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
 'machine_start_gcode': ';Geeetech official wiki homepage for A10M: '
                        'https://www.geeetech.com/wiki/index.php/Geeetech_A10M_3D_printer \n'
                        'M104 S[nozzle_temperature_initial_layer] ; set extruder temp\n'
                        'M140 S[bed_temperature_initial_layer[initial_no_support_extruder]] ; set bed temp\n'
                        'M190 S[bed_temperature_initial_layer[initial_no_support_extruder]] ; wait for bed temp\n'
                        'M109 S[nozzle_temperature_initial_layer] ; wait for extruder temp\n'
                        'M220 S100 ;Reset Feedrate\n'
                        'M221 S100 ;Reset Flowrate\n'
                        'G92 E0 ; Reset Extruder\n'
                        'G28 ; Home all axes\n'
                        'M107 ;Off Fan\n'
                        'G1 Z5.0 F3000 ;Move Z Axis up little to prevent scratching of Heat Bed\n'
                        'G1 X0.1 Y20 Z1.4 F6000 ; Move to start position\n'
                        'T[initial_no_support_extruder] ; Choose initial filament for the first line\n'
                        'G1 X0.1 Y80.0 Z1.4 F1000 E25 ; Draw the first line\n'
                        'G92 E0 ; Reset Extruder\n'
                        'G1 X0.4 Y80.0 Z1.4 F6000 ; Move to side a little\n'
                        'G1 X1.4 Y20 Z1.4 F1000 E20 ; Draw the second line\n'
                        'G92 E0 ; Reset Extruder\n'
                        'G1 Z2.0 F3000 ; Move Z Axis up little to prevent scratching of Heat Bed\n'
                        'G1 X5 Y20 Z0.28 F3000.0 ; Move over to prevent blob squish\n'
                        'G92 E0',
 'max_layer_height': ['0.3'],
 'min_layer_height': ['0.07'],
 'name': 'Geeetech A10 M 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'brass',
 'printable_area': ['0x0', '220x0', '220x220', '0x220'],
 'printable_height': '260',
 'printer_model': 'Geeetech A10 M',
 'printer_variant': '0.4',
 'retract_lift_below': ['259'],
 'retract_restart_extra': ['-0.2'],
 'retraction_length': ['6.5'],
 'retraction_speed': ['25'],
 'setting_id': 'GM_GEEETECH_025',
 'type': 'machine'}
