from __future__ import annotations

# source: profiles/Anycubic/machine/Anycubic Kobra 2 0.4 nozzle.json
DATA = {'auxiliary_fan': '0',
 'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\n[layer_num] @ [layer_z]mm\nG92 E0',
 'change_filament_gcode': 'M600',
 'default_filament_profile': ['Anycubic Generic PLA'],
 'default_print_profile': '0.20mm Standard @Anycubic Kobra2',
 'deretraction_speed': ['80'],
 'from': 'system',
 'inherits': 'fdm_machine_common',
 'instantiation': 'true',
 'layer_change_gcode': ';AFTER_LAYER_CHANGE\n[layer_num] @ [layer_z]mm',
 'machine_end_gcode': 'M104 S0 ;Extruder off\n'
                      'M140 S0 ;Heatbed off\n'
                      'M107 ;Fan off\n'
                      'G91 ;Relative positioning\n'
                      'G1 E-5 F3000 ;Retract filament\n'
                      'G1 Z+0.3 F3000 ;Lift print head\n'
                      'G28 X0 F3000 ;Home X axis\n'
                      'M84 ;Disable stepper motors',
 'machine_max_acceleration_extruding': ['2500', '2500'],
 'machine_max_acceleration_retracting': ['2500', '2500'],
 'machine_max_acceleration_travel': ['3000', '1250'],
 'machine_max_acceleration_x': ['2500', '2500'],
 'machine_max_acceleration_y': ['2500', '2500'],
 'machine_max_acceleration_z': ['800', '800'],
 'machine_max_jerk_e': ['10', '10'],
 'machine_max_jerk_x': ['15', '15'],
 'machine_max_jerk_y': ['10', '10'],
 'machine_max_jerk_z': ['2', '2'],
 'machine_max_speed_e': ['80', '80'],
 'machine_max_speed_x': ['300', '300'],
 'machine_max_speed_y': ['250', '250'],
 'machine_max_speed_z': ['8', '8'],
 'machine_pause_gcode': 'M601',
 'machine_start_gcode': 'G90 ;Use absolute coordinates\n'
                        'M83 ;Extruder relative mode\n'
                        'M104 S[first_layer_temperature] ;Set extruder temp\n'
                        'M140 S[first_layer_bed_temperature] ;Set bed temp\n'
                        'M190 S[first_layer_bed_temperature] ;Wait for bed temp\n'
                        'M109 S[first_layer_temperature] ;Wait for extruder temp\n'
                        'G28 ;Move X/Y/Z to min endstops\n'
                        'G1 Z0.28 ;Lift nozzle a bit\n'
                        'G92 E0 ;Specify current extruder position as zero\n'
                        'G1 Y3 F1800 ;Move Y to purge point\n'
                        'G1 X60 E25 F500 ;Extrude 25mm of filament in a 5cm line\n'
                        'G92 E0 ;Zero the extruded length again\n'
                        'G1 E-2 F500 ;Retract a little\n'
                        'G1 X70 F4000 ;Quickly wipe away from the filament line\n'
                        'M117',
 'max_layer_height': ['0.32'],
 'min_layer_height': ['0.04'],
 'name': 'Anycubic Kobra 2 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'undefine',
 'printable_area': ['0x0', '220x0', '220x220', '0x220'],
 'printable_height': '250',
 'printer_model': 'Anycubic Kobra 2',
 'printer_settings_id': 'Anycubic',
 'retract_before_wipe': ['70%'],
 'retract_length_toolchange': ['1'],
 'retraction_length': ['2'],
 'retraction_minimum_travel': ['1'],
 'retraction_speed': ['80'],
 'scan_first_layer': '0',
 'setting_id': 'GM001',
 'single_extruder_multi_material': '1',
 'type': 'machine'}
