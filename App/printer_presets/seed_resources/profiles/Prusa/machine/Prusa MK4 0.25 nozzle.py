from __future__ import annotations

# source: profiles/Prusa/machine/Prusa MK4 0.25 nozzle.json
DATA = {'auxiliary_fan': '0',
 'bed_exclude_area': ['0x0'],
 'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\n'
                              'G92 E0.0\n'
                              ';[layer_z]\n'
                              'M201 X{interpolate_table(extruded_weight_total, (0,4000), (1400,2500), (10000,2500))} '
                              'Y{interpolate_table(extruded_weight_total, (0,4000), (1400,2500), (10000,2500))}\n'
                              '{if !spiral_mode}M74 W[extruded_weight_total]{endif}',
 'change_filament_gcode': 'M600\nG1 E0.4 F1500 ; prime after color change',
 'default_filament_profile': ['Prusa Generic PLA @MK4'],
 'default_print_profile': '0.08mm Standard @MK4',
 'from': 'system',
 'gcode_flavor': 'marlin2',
 'host_type': 'prusalink',
 'inherits': 'fdm_machine_common',
 'instantiation': 'true',
 'layer_change_gcode': ';AFTER_LAYER_CHANGE\n;[layer_z]',
 'machine_end_gcode': '{if layer_z < max_print_height}G1 Z{z_offset+min(layer_z+1, max_print_height)} F720 ; Move '
                      'print head up{endif}\n'
                      'M104 S0 ; turn off temperature\n'
                      'M140 S0 ; turn off heatbed\n'
                      'M107 ; turn off fan\n'
                      'G1 X241 Y170 F3600 ; park\n'
                      '{if layer_z < max_print_height}G1 Z{z_offset+min(layer_z+23, max_print_height)} F300 ; Move '
                      'print head up{endif}\n'
                      'G4 ; wait\n'
                      'M572 S0 ; reset PA\n'
                      'M593 X T2 F0 ; disable IS\n'
                      'M593 Y T2 F0 ; disable IS\n'
                      'M84 X Y E ; disable motors\n'
                      '; max_layer_z = [max_layer_z]',
 'machine_load_filament_time': '17',
 'machine_max_acceleration_e': ['2500', '2500'],
 'machine_max_acceleration_extruding': ['4000', '4000'],
 'machine_max_acceleration_retracting': ['1200', '1200'],
 'machine_max_acceleration_travel': ['4000', '4000'],
 'machine_max_acceleration_x': ['4000', '4000'],
 'machine_max_acceleration_y': ['4000', '4000'],
 'machine_max_acceleration_z': ['200', '200'],
 'machine_pause_gcode': 'M601',
 'machine_start_gcode': 'M17 ; enable steppers\n'
                        'M862.1 P[nozzle_diameter] ; nozzle diameter check\n'
                        'M862.3 P "MK4" ; printer model check\n'
                        'M862.5 P2 ; g-code level check\n'
                        'M862.6 P"Input shaper" ; FW feature check\n'
                        'M115 U5.0.0-RC+11963\n'
                        '\n'
                        'M555 X{(min(print_bed_max[0], first_layer_print_min[0] + 32) - 32)} Y{(max(0, '
                        'first_layer_print_min[1]) - 4)} W{((min(print_bed_max[0], max(first_layer_print_min[0] + 32, '
                        'first_layer_print_max[0])))) - ((min(print_bed_max[0], first_layer_print_min[0] + 32) - 32))} '
                        'H{((first_layer_print_max[1])) - ((max(0, first_layer_print_min[1]) - 4))}\n'
                        '\n'
                        'G90 ; use absolute coordinates\n'
                        'M83 ; extruder relative mode\n'
                        '\n'
                        'M140 S[first_layer_bed_temperature] ; set bed temp\n'
                        '{if filament_type[initial_tool]=="PC" or filament_type[initial_tool]=="PA"}\n'
                        'M104 S{first_layer_temperature[initial_tool]-25} ; set extruder temp for bed leveling\n'
                        'M109 R{first_layer_temperature[initial_tool]-25} ; wait for temp\n'
                        '{elsif filament_type[initial_tool]=="FLEX"}\n'
                        'M104 S210 ; set extruder temp for bed leveling\n'
                        'M109 R210 ; wait for temp\n'
                        '{else}\n'
                        'M104 S170 ; set extruder temp for bed leveling\n'
                        'M109 R170 ; wait for temp\n'
                        '{endif}\n'
                        '\n'
                        'M84 E ; turn off E motor\n'
                        '\n'
                        'G28 ; home all without mesh bed level\n'
                        '\n'
                        'G1 X{10 + 32} Y-4 Z5 F4800\n'
                        '\n'
                        'M302 S160 ; lower cold extrusion limit to 160C\n'
                        '\n'
                        '{if filament_type[initial_tool]=="FLEX"}\n'
                        'G1 E-4 F2400 ; retraction\n'
                        '{else}\n'
                        'G1 E-2 F2400 ; retraction\n'
                        '{endif}\n'
                        '\n'
                        'M84 E ; turn off E motor\n'
                        '\n'
                        'G29 P9 X10 Y-4 W32 H4\n'
                        '\n'
                        '{if first_layer_bed_temperature[initial_tool]<=60}M106 S100{endif}\n'
                        '\n'
                        'G0 Z40 F10000\n'
                        '\n'
                        'M190 S[first_layer_bed_temperature] ; wait for bed temp\n'
                        '\n'
                        'M107\n'
                        '\n'
                        ';\n'
                        '; MBL\n'
                        ';\n'
                        'M84 E ; turn off E motor\n'
                        'G29 P1 ; invalidate mbl & probe print area\n'
                        'G29 P1 X0 Y0 W50 H20 C ; probe near purge place\n'
                        'G29 P3.2 ; interpolate mbl probes\n'
                        'G29 P3.13 ; extrapolate mbl outside probe area\n'
                        'G29 A ; activate mbl\n'
                        '\n'
                        '; prepare for purge\n'
                        'M104 S{first_layer_temperature[0]}\n'
                        'G0 X0 Y-4 Z15 F4800 ; move away and ready for the purge\n'
                        'M109 S{first_layer_temperature[0]}\n'
                        '\n'
                        'G92 E0\n'
                        'M569 S0 E ; set spreadcycle mode for extruder\n'
                        '\n'
                        ';\n'
                        '; Extrude purge line\n'
                        ';\n'
                        'G92 E0 ; reset extruder position\n'
                        'G1 E{(filament_type[0] == "FLEX" ? 4 : 2)} F2400 ; deretraction after the initial one before '
                        'nozzle cleaning\n'
                        'G0 E7 X15 Z0.2 F500 ; purge\n'
                        'G0 X25 E4 F500 ; purge\n'
                        'G0 X35 E4 F650 ; purge\n'
                        'G0 X45 E4 F800 ; purge\n'
                        'G0 X{45 + 3} Z{0.05} F{8000} ; wipe, move close to the bed\n'
                        'G0 X{45 + 3 * 2} Z0.2 F{8000} ; wipe, move quickly away from the bed\n'
                        '\n'
                        'G92 E0\n'
                        'M221 S100 ; set flow to 100%',
 'machine_unload_filament_time': '16',
 'max_layer_height': ['0.16'],
 'min_layer_height': ['0.04'],
 'name': 'Prusa MK4 0.25 nozzle',
 'nozzle_diameter': ['0.25'],
 'nozzle_type': 'hardened_steel',
 'printable_area': ['0x0', '250x0', '250x210', '0x210'],
 'printable_height': '220',
 'printer_model': 'Prusa MK4',
 'printer_notes': 'Don\'t remove the following keywords! These keywords are used in the "compatible printer" condition '
                  'of the print and filament profiles to link the particular print and filament profiles to this '
                  'printer profile.\n'
                  'PRINTER_MODEL_MK4IS\n'
                  'PG',
 'printer_variant': '0.25',
 'scan_first_layer': '0',
 'setting_id': 'GM004',
 'thumbnails': ['16x16/QOI', '313x173/QOI', '440x240/QOI', '480x240/QOI', '640x480/PNG'],
 'type': 'machine'}
