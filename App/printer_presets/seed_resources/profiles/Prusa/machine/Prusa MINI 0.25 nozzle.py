from __future__ import annotations

# source: profiles/Prusa/machine/Prusa MINI 0.25 nozzle.json
DATA = {'auxiliary_fan': '0',
 'bed_exclude_area': ['0x0'],
 'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n',
 'default_filament_profile': ['Prusa Generic PLA'],
 'default_print_profile': '0.20mm Standard @MINI 0.25',
 'from': 'system',
 'gcode_flavor': 'marlin2',
 'inherits': 'fdm_machine_common',
 'instantiation': 'true',
 'layer_change_gcode': ';AFTER_LAYER_CHANGE\n;[layer_z]',
 'machine_end_gcode': 'G1 E-1 F2100 ; retract\n'
                      '{if max_layer_z < max_print_height}G1 Z{z_offset+min(max_layer_z+2, max_print_height)} F720 ; '
                      'Move print head up{endif}\n'
                      'G1 X178 Y178 F4200 ; park print head\n'
                      '{if max_layer_z < max_print_height}G1 Z{z_offset+min(max_layer_z+30, max_print_height)} F720 ; '
                      'Move print head further up{endif}\n'
                      'G4 ; wait\n'
                      'M104 S0 ; turn off temperature\n'
                      'M140 S0 ; turn off heatbed\n'
                      'M107 ; turn off fan\n'
                      'M221 S100 ; reset flow\n'
                      'M900 K0 ; reset LA\n'
                      'M84 ; disable motors\n'
                      '; max_layer_z = [max_layer_z]',
 'machine_load_filament_time': '17',
 'machine_max_acceleration_extruding': ['1250', '2000'],
 'machine_max_acceleration_x': ['2500', '2000'],
 'machine_max_acceleration_y': ['2500', '2000'],
 'machine_max_acceleration_z': ['400', '200'],
 'machine_max_jerk_e': ['10', '2.5'],
 'machine_max_jerk_x': ['8', '9'],
 'machine_max_jerk_y': ['8', '9'],
 'machine_max_speed_e': ['80', '25'],
 'machine_max_speed_x': ['180', '200'],
 'machine_max_speed_y': ['180', '200'],
 'machine_pause_gcode': 'M601',
 'machine_start_gcode': 'M862.3 P "MINI" ; printer model check\n'
                        'G90 ; use absolute coordinates\n'
                        'M83 ; extruder relative mode\n'
                        'M104 S170 ; set extruder temp for bed leveling\n'
                        'M140 S[first_layer_bed_temperature] ; set bed temp\n'
                        'M109 R170 ; wait for bed leveling temp\n'
                        'M190 S[first_layer_bed_temperature] ; wait for bed temp\n'
                        'M204 T1250 ; set travel acceleration\n'
                        'G28 ; home all without mesh bed level\n'
                        'G29 ; mesh bed leveling \n'
                        'M204 T[machine_max_acceleration_travel] ; restore travel acceleration\n'
                        'M104 S[first_layer_temperature] ; set extruder temp\n'
                        'G92 E0\n'
                        'G1 Y-2 X179 F2400\n'
                        'G1 Z3 F720\n'
                        'M109 S[first_layer_temperature] ; wait for extruder temp\n'
                        '\n'
                        '; intro line\n'
                        'G1 X170 F1000\n'
                        'G1 Z0.2 F720\n'
                        'G1 X110 E8 F900\n'
                        'G1 X40 E10 F700\n'
                        'G92 E0\n'
                        '\n'
                        'M221 S95 ; set flow',
 'machine_unload_filament_time': '16',
 'max_layer_height': ['0.15'],
 'min_layer_height': ['0.05'],
 'name': 'Prusa MINI 0.25 nozzle',
 'nozzle_diameter': ['0.25'],
 'nozzle_type': 'hardened_steel',
 'printable_area': ['0x0', '180x0', '180x180', '0x180'],
 'printable_height': '180',
 'printer_model': 'Prusa MINI',
 'printer_notes': 'Don\'t remove the following keywords! These keywords are used in the "compatible printer" condition '
                  'of the print and filament profiles to link the particular print and filament profiles to this '
                  'printer profile.\n'
                  'PRINTER_VENDOR_PRUSA3D\n'
                  'PRINTER_MODEL_MINI\n',
 'printer_variant': '0.25',
 'retraction_length': ['3.2'],
 'retraction_minimum_travel': ['1.5'],
 'retraction_speed': ['70'],
 'scan_first_layer': '0',
 'setting_id': 'GM003',
 'thumbnails': ['16x16/QOI', '220x124/QOI', '200x240/QOI', '640x480/PNG'],
 'type': 'machine'}
