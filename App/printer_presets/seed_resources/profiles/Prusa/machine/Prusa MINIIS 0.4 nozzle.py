from __future__ import annotations

# source: profiles/Prusa/machine/Prusa MINIIS 0.4 nozzle.json
DATA = {'auxiliary_fan': '0',
 'bed_exclude_area': ['0x0'],
 'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\n'
                              'G92 E0.0\n'
                              ';[layer_z]\n'
                              'M201 X{interpolate_table(extruded_weight_total, (0,4000), (1000,1700), (10000,1700))} '
                              'Y{interpolate_table(extruded_weight_total, (0,4000), (1000,1700), (10000,1700))}',
 'change_filament_gcode': 'M600',
 'default_filament_profile': ['Prusa Generic PLA @MINIIS'],
 'default_print_profile': '0.20mm Standard @MINIIS',
 'deretraction_speed': ['40'],
 'fan_kickstart': '0',
 'fan_speedup_overhangs': '1',
 'fan_speedup_time': '0.2',
 'from': 'system',
 'gcode_flavor': 'marlin2',
 'host_type': 'prusalink',
 'inherits': 'fdm_machine_common',
 'instantiation': 'true',
 'layer_change_gcode': ';AFTER_LAYER_CHANGE\n;[layer_z]\n{if ! spiral_mode}M74 W[extruded_weight_total]{endif}\n',
 'machine_end_gcode': '{if max_layer_z < max_print_height}G1 Z{z_offset+min(max_layer_z+2, max_print_height)} F720 ; '
                      'Move print head up{endif}\n'
                      'G1 X170 Y170 F4200 ; park print head\n'
                      '{if max_layer_z < max_print_height}G1 Z{z_offset+min(max_layer_z+50, max_print_height)} F720 ; '
                      'Move print head further up{endif}\n'
                      'G4 ; wait\n'
                      'M104 S0 ; turn off temperature\n'
                      'M140 S0 ; turn off heatbed\n'
                      'M107 ; turn off fan\n'
                      'M221 S100 ; reset flow\n'
                      'M572 S0 ; reset PA\n'
                      'M569 S1 X Y ; reset to stealthchop for X Y\n'
                      'M84 ; disable motors\n'
                      '; max_layer_z = [max_layer_z]',
 'machine_load_filament_time': '17',
 'machine_max_acceleration_e': ['5000', '5000'],
 'machine_max_acceleration_extruding': ['4000', '4000'],
 'machine_max_acceleration_retracting': ['1250', '1250'],
 'machine_max_acceleration_travel': ['4000', '4000'],
 'machine_max_acceleration_x': ['4000', '4000'],
 'machine_max_acceleration_y': ['4000', '4000'],
 'machine_max_acceleration_z': ['400', '400'],
 'machine_max_jerk_e': ['10', '2.5'],
 'machine_max_jerk_x': ['8', '8'],
 'machine_max_jerk_y': ['8', '8'],
 'machine_max_jerk_z': ['2', '2'],
 'machine_max_junction_deviation': ['0.01'],
 'machine_max_speed_e': ['80', '25'],
 'machine_max_speed_x': ['400', '400'],
 'machine_max_speed_y': ['400', '400'],
 'machine_pause_gcode': 'M601',
 'machine_start_gcode': 'M862.3 P "MINI" ; printer model check\n'
                        'M862.1 P[nozzle_diameter] ; nozzle diameter check\n'
                        'M862.5 P2 ; g-code level check\n'
                        'M862.6 P"Input shaper" ; FW feature check\n'
                        'M115 U6.4.0+11974\n'
                        'G90 ; use absolute coordinates\n'
                        'M83 ; extruder relative mode\n'
                        'G28 ; home all without mesh bed level\n'
                        'M104 S170 ; set extruder temp for bed leveling\n'
                        'M140 S[first_layer_bed_temperature] ; set bed temp\n'
                        'M109 R170 ; wait for bed leveling temp\n'
                        'M190 S[first_layer_bed_temperature] ; wait for bed temp\n'
                        'M569 S1 X Y ; set stealthchop for X Y\n'
                        'M204 T1250 ; set travel acceleration\n'
                        'G29 ; mesh bed leveling \n'
                        'M104 S[first_layer_temperature] ; set extruder temp\n'
                        'G92 E0\n'
                        '\n'
                        'G1 X0 Y-2 Z3 F2400\n'
                        '\n'
                        'M109 S[first_layer_temperature] ; wait for extruder temp\n'
                        '\n'
                        '; intro line\n'
                        'G1 X10 Z0.2 F1000\n'
                        'G1 X70 E8 F900\n'
                        'G1 X140 E10 F700\n'
                        'G92 E0\n'
                        '\n'
                        'M569 S0 X Y ; set spreadcycle for X Y\n'
                        'M204 T[machine_max_acceleration_travel] ; restore travel acceleration\n'
                        'M572 W0.06 ; set smooth time\n'
                        'M221 S95 ; set flow',
 'machine_unload_filament_time': '16',
 'name': 'Prusa MINIIS 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'brass',
 'printable_area': ['0x0', '180x0', '180x180', '0x180'],
 'printable_height': '180',
 'printer_model': 'Prusa MINI IS',
 'printer_notes': 'Don\'t remove the following keywords! These keywords are used in the "compatible printer" condition '
                  'of the print and filament profiles to link the particular print and filament profiles to this '
                  'printer profile.\n'
                  'PRINTER_VENDOR_PRUSA3D\n'
                  'PRINTER_MODEL_MINIIS\n'
                  'NO_TEMPLATES',
 'printer_variant': '0.4',
 'retraction_length': ['2.5'],
 'retraction_minimum_travel': ['1.5'],
 'retraction_speed': ['70'],
 'scan_first_layer': '0',
 'setting_id': 'GM003',
 'thumbnails': ['16x16/QOI', '220x124/QOI', '200x240/QOI', '640x480/PNG'],
 'type': 'machine',
 'z_hop': ['0.2']}
