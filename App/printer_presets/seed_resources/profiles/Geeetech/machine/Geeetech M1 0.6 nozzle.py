from __future__ import annotations

# source: profiles/Geeetech/machine/Geeetech M1 0.6 nozzle.json
DATA = {'auxiliary_fan': '0',
 'default_filament_profile': ['Generic PLA @System'],
 'default_print_profile': '0.30mm Standard @Geeetech M1 0.6 nozzle',
 'deretraction_speed': ['40'],
 'extruder_type': ['Direct Drive'],
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
                      'M84 X Y E ; disable motors\n'
                      'M221 S100;Slicer Flow recovery 100%\n'
                      'M220 S100 ;Set Feedrate recovery 100%\n'
                      'M204 P3000.00 R3000.00 T3000.00',
 'machine_max_acceleration_e': ['3000', '3000'],
 'machine_max_acceleration_extruding': ['3000', '3000'],
 'machine_max_acceleration_retracting': ['3000', '3000'],
 'machine_max_acceleration_travel': ['3000', '3000'],
 'machine_max_acceleration_x': ['3000', '3000'],
 'machine_max_acceleration_y': ['3000', '3000'],
 'machine_max_acceleration_z': ['500', '500'],
 'machine_max_jerk_e': ['10', '10'],
 'machine_max_jerk_x': ['10', '10'],
 'machine_max_jerk_y': ['10', '10'],
 'machine_max_jerk_z': ['3', '3'],
 'machine_max_speed_e': ['60', '60'],
 'machine_max_speed_x': ['300', '300'],
 'machine_max_speed_y': ['300', '300'],
 'machine_max_speed_z': ['25', '25'],
 'machine_start_gcode': ';Geeetech M1 official wiki URL: '
                        'https://www.geeetech.com/wiki/index.php/Geeetech_M1_3D_printer \n'
                        'M104 S[first_layer_temperature] ; Set Hotend Temperature\n'
                        'M140 S[first_layer_bed_temperature] ; set Bed Temperature\n'
                        'M190 S[first_layer_bed_temperature] ; Wait for Bed Temperature\n'
                        'M109 S[first_layer_temperature] ; wait for Hotend Temperature\n'
                        'M220 S100 ;Reset Feedrate\n'
                        'M221 S100 ;Reset Flowrate\n'
                        'G92 E0 ; Reset Extruder\n'
                        'G28 ; Home all axes\n'
                        'M107 ;Off Main Fan\n'
                        'M300 S2500 P1000 ;Play a short tune\n'
                        'G1 Z0.28 ;Move Z Axis up little to prevent scratching of Heat Bed\n'
                        'G92 E0 ;Reset Extruder\n'
                        'G1 Y3 F2400 ;Move to start position\n'
                        'G1 X75 E40 F500 ;Draw a filament line\n'
                        'G92 E0 ;Reset Extruder\n'
                        ';G1 E-0.2 F3000 ;Retract a little\n'
                        'G1 Z2.0 F3000 ;Move Z Axis up little to prevent scratching of Heat Bed\n'
                        'G1 X70 Y3 Z0.27 F3000 ;Quickly wipe away from the filament line\n'
                        'G92 E0 ;Reset Extruder',
 'max_layer_height': ['0.42'],
 'min_layer_height': ['0.12'],
 'name': 'Geeetech M1 0.6 nozzle',
 'nozzle_diameter': ['0.6'],
 'nozzle_type': 'brass',
 'printable_area': ['0x0', '105x0', '105x105', '0x105'],
 'printable_height': '95',
 'printer_model': 'Geeetech M1',
 'printer_variant': '0.6',
 'retract_lift_below': ['95'],
 'retraction_length': ['1'],
 'retraction_speed': ['40'],
 'setting_id': 'GM_GEEETECH_041',
 'type': 'machine'}
