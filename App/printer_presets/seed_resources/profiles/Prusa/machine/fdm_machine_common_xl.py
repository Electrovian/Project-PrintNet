from __future__ import annotations

# source: profiles/Prusa/machine/fdm_machine_common_xl.json
DATA = {'auxiliary_fan': '0',
 'bed_exclude_area': ['0x0'],
 'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\nG92 E0.0\n;[layer_z]',
 'change_filament_gcode': 'M600\nG1 E0.3 F1500 ; prime after color change',
 'detraction_speed': '25',
 'extruder_clearance_height_to_lid': '21',
 'extruder_clearance_height_to_rod': '21',
 'extruder_clearance_radius': '67',
 'from': 'system',
 'gcode_flavor': 'marlin2',
 'host_type': 'prusalink',
 'inherits': 'fdm_machine_common',
 'instantiation': 'false',
 'layer_change_gcode': ';AFTER_LAYER_CHANGE\n;[layer_z]',
 'machine_end_gcode': '{if max_layer_z < max_print_height}G1 Z{z_offset+min(max_layer_z+2, max_print_height)} '
                      'F720{endif} ; Move bed down\n'
                      'M104 S0 ; turn off temperature\n'
                      'M140 S0 ; turn off heatbed\n'
                      'M107 ; turn off fan\n'
                      'G1 X6 Y350 F6000 ; park\n'
                      '{if max_layer_z < max_print_height}G1 Z{z_offset+min(max_layer_z+100, max_print_height)} '
                      'F300{endif} ; Move bed down\n'
                      'M900 K0 ; reset LA\n'
                      'M142 S36 ; reset heatbreak target temp\n'
                      'M221 S100 ; reset flow percentage\n'
                      'M84 ; disable motors\n'
                      '; max_layer_z = [max_layer_z]',
 'machine_max_acceleration_e': ['2500', '2500'],
 'machine_max_acceleration_extruding': ['4000', '4000'],
 'machine_max_acceleration_retracting': ['1200', '1200'],
 'machine_max_acceleration_travel': ['5000', '5000'],
 'machine_max_acceleration_x': ['7000', '7000'],
 'machine_max_acceleration_y': ['7000', '7000'],
 'machine_max_acceleration_z': ['200', '200'],
 'machine_max_jerk_e': ['10', '10'],
 'machine_max_jerk_x': ['8', '8'],
 'machine_max_jerk_y': ['8', '8'],
 'machine_max_jerk_z': ['2', '2'],
 'machine_max_speed_e': ['100', '100'],
 'machine_max_speed_x': ['400', '400'],
 'machine_max_speed_y': ['400', '400'],
 'machine_max_speed_z': ['12', '12'],
 'machine_pause_gcode': 'M601',
 'machine_start_gcode': 'M17 ; enable steppers\n'
                        'M862.3 P "XL" ; printer model check\n'
                        'M115 U6.0.1+14848\n'
                        'G90 ; use absolute coordinates\n'
                        'M83 ; extruder relative mode\n'
                        '; set print area\n'
                        'M555 X{first_layer_print_min[0]} Y{first_layer_print_min[1]} W{(first_layer_print_max[0]) - '
                        '(first_layer_print_min[0])} H{(first_layer_print_max[1]) - (first_layer_print_min[1])}\n'
                        '; inform about nozzle diameter\n'
                        'M862.1 P[nozzle_diameter]\n'
                        '; set & wait for bed and extruder temp for MBL\n'
                        'M140 S[first_layer_bed_temperature] ; set bed temp\n'
                        'M104 T0 S{((filament_notes[0]=~/.*HT_MBL10.*/) ? (first_layer_temperature[0] - 10) : '
                        '(filament_type[0] == "PC" or filament_type[0] == "PA") ? (first_layer_temperature[0] - 25) : '
                        '(filament_type[0] == "FLEX") ? 210 : (filament_type[0]=~/.*PET.*/) ? 175 : 170)} ; set '
                        'extruder temp for bed leveling\n'
                        'M109 T0 R{((filament_notes[0]=~/.*HT_MBL10.*/) ? (first_layer_temperature[0] - 10) : '
                        '(filament_type[0] == "PC" or filament_type[0] == "PA") ? (first_layer_temperature[0] - 25) : '
                        '(filament_type[0] == "FLEX") ? 210 : (filament_type[0]=~/.*PET.*/) ? 175 : 170)} ; wait for '
                        'temp\n'
                        '; home carriage, pick tool, home all\n'
                        'G28 XY\n'
                        'M84 E ; turn off E motor\n'
                        'G28 Z\n'
                        'M190 S[first_layer_bed_temperature] ; wait for bed temp\n'
                        'G29 G ; absorb heat\n'
                        '; move to the nozzle cleanup area\n'
                        'G1 X{(min(((((first_layer_print_min[0] + first_layer_print_max[0]) / 2) < ((print_bed_min[0] '
                        '+ print_bed_max[0]) / 2)) ? (((first_layer_print_min[1] - 7) < -2) ? 70 : '
                        '(min(print_bed_max[0], first_layer_print_min[0] + 32) - 32)) : (((first_layer_print_min[1] - '
                        '7) < -2) ? 260 : (min(print_bed_max[0], first_layer_print_min[0] + 32) - 32))), '
                        'first_layer_print_min[0])) + 32} Y{(min((first_layer_print_min[1] - 7), '
                        'first_layer_print_min[1]))} Z{5} F4800\n'
                        'M302 S160 ; lower cold extrusion limit to 160C\n'
                        'G1 E{-(filament_type[0] == "FLEX" ? 4 : 2)} F2400 ; retraction for nozzle cleanup\n'
                        '; nozzle cleanup\n'
                        'M84 E ; turn off E motor\n'
                        'G29 P9 X{((((first_layer_print_min[0] + first_layer_print_max[0]) / 2) < ((print_bed_min[0] + '
                        'print_bed_max[0]) / 2)) ? (((first_layer_print_min[1] - 7) < -2) ? 70 : '
                        '(min(print_bed_max[0], first_layer_print_min[0] + 32) - 32)) : (((first_layer_print_min[1] - '
                        '7) < -2) ? 260 : (min(print_bed_max[0], first_layer_print_min[0] + 32) - 32)))} '
                        'Y{(first_layer_print_min[1] - 7)} W{32} H{7}\n'
                        'G0 Z10 F480 ; move away in Z\n'
                        '{if first_layer_bed_temperature[0] > 60}\n'
                        'G0 Z70 F480 ; move away (a bit more) in Z\n'
                        'G0 X30 Y{print_bed_min[1]} F6000 ; move away in X/Y for higher bed temperatures\n'
                        '{endif}\n'
                        'M106 S100 ; cool off the nozzle\n'
                        'M107 ; stop cooling off the nozzle - turn off the fan\n'
                        '; MBL\n'
                        'M84 E ; turn off E motor\n'
                        'G29 P1 ; invalidate mbl & probe print area\n'
                        'G29 P1 X30 Y0 W50 H20 C ; probe near purge place\n'
                        'G29 P3.2 ; interpolate mbl probes\n'
                        'G29 P3.13 ; extrapolate mbl outside probe area\n'
                        'G29 A ; activate mbl\n'
                        'M104 S[first_layer_temperature] ; set extruder temp\n'
                        'G1 Z10 F720 ; move away in Z\n'
                        'G0 X30 Y-8 F6000 ; move next to the sheet\n'
                        '; wait for extruder temp\n'
                        'M109 T0 S{first_layer_temperature[0]}\n'
                        ';\n'
                        '; purge\n'
                        ';\n'
                        'G92 E0 ; reset extruder position\n'
                        'G0 X{(0 == 0 ? 30 : (0 == 1 ? 150 : (0 == 2 ? 210 : 330)))} Y{(0 < 4 ? -8 : -5.5)} ; move '
                        "close to the sheet's edge\n"
                        'G1 E{(filament_type[0] == "FLEX" ? 4 : 2)} F2400 ; deretraction after the initial one before '
                        'nozzle cleaning\n'
                        'G0 E10 X40 Z0.2 F500 ; purge\n'
                        'G0 X70 E9 F800 ; purge\n'
                        'G0 X{70 + 3} Z{0.05} F{8000} ; wipe, move close to the bed\n'
                        'G0 X{70 + 3 * 2} Z0.2 F{8000} ; wipe, move quickly away from the bed\n'
                        'G92 E0 ; reset extruder position',
 'max_layer_height': '0.3',
 'min_layer_height': '0.07',
 'name': 'fdm_machine_common_xl',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'hardened_steel',
 'printable_area': ['0x0', '360x0', '360x360', '0x360'],
 'printable_height': '360',
 'printer_notes': 'Don\'t remove the following keywords! These keywords are used in the "compatible printer" condition '
                  'of the print and filament profiles to link the particular print and filament profiles to this '
                  'printer profile.\n'
                  'PRINTER_MODEL_XLIS\n'
                  'PG\n'
                  'INPUT_SHAPER',
 'printer_variant': '0.4',
 'retract_before_wipe': '80%',
 'retract_lift_below': '1.5',
 'retract_when_changing_layer': '1',
 'retraction_length': '0.8',
 'retraction_minimum_travel': '1.5',
 'retraction_speed': '35',
 'scan_first_layer': '0',
 'thumbnails': ['16x16/QOI', '313x173/QOI', '440x240/QOI', '480x240/QOI', '640x480/PNG'],
 'type': 'machine',
 'wipe': '1',
 'z_hop_types': 'Auto Lift'}
