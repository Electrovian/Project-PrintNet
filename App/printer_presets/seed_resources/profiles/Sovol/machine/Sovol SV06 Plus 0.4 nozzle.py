from __future__ import annotations

# source: profiles/Sovol/machine/Sovol SV06 Plus 0.4 nozzle.json
DATA = {'auxiliary_fan': '0',
 'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\nG92 E0.0\n;[layer_z]\n\n',
 'change_filament_gcode': 'M600\nG1 E0.4 F1500 ; prime after color change',
 'default_filament_profile': ['Generic PLA @System'],
 'default_print_profile': '0.20mm Standard @Sovol SV06Plus',
 'deretraction_speed': ['30'],
 'from': 'system',
 'inherits': 'fdm_machine_common',
 'instantiation': 'true',
 'layer_change_gcode': ';AFTER_LAYER_CHANGE\n;[layer_z]',
 'machine_end_gcode': 'M117 READY\n'
                      '\n'
                      'G1 E0 F1000 ; reset extruder\n'
                      '\n'
                      'G91 ; relative positioning\n'
                      'G1 Z2 F1000 ; lift nozzle\n'
                      '\n'
                      'G90 ; absolute positioning\n'
                      'G27 P2 ; park extruder\n'
                      '\n'
                      'M140 S0 ; turn off heatbed\n'
                      'M104 S0 ; turn off temperature\n'
                      'M107 ; turn off fan\n'
                      'M84 X Y E ; disable motors',
 'machine_max_acceleration_extruding': ['1000', '1250'],
 'machine_max_acceleration_retracting': ['1000', '1250'],
 'machine_max_acceleration_travel': ['1500', '1250'],
 'machine_max_acceleration_x': ['1500', '960'],
 'machine_max_acceleration_y': ['1500', '960'],
 'machine_max_acceleration_z': ['200', '200'],
 'machine_max_jerk_e': ['10', '4.5'],
 'machine_max_jerk_x': ['8', '8'],
 'machine_max_jerk_y': ['8', '8'],
 'machine_max_jerk_z': ['2', '0.4'],
 'machine_max_speed_e': ['120', '120'],
 'machine_max_speed_x': ['140', '140'],
 'machine_max_speed_y': ['140', '140'],
 'machine_max_speed_z': ['12', '12'],
 'machine_pause_gcode': 'M601',
 'machine_start_gcode': 'G90 ; use absoulte coordinates\n'
                        'M83 ; extruder relative mode\n'
                        '\n'
                        'M104 S150 ; set nozzle temp to 150\n'
                        '\n'
                        'G28 ; home all axes\n'
                        'M420 S1 ;load mesh\n'
                        '\n'
                        'M140 S[bed_temperature_initial_layer_single] ; set bed temp\n'
                        'M190 S[bed_temperature_initial_layer_single] ; wait for bed temp to stabilize\n'
                        'M104 S[nozzle_temperature_initial_layer] ; set final extruder temp\n'
                        'M109 S[nozzle_temperature_initial_layer] ; wait for extruder temp\n'
                        '\n'
                        'G1 X0.1 Y10 Z5.0 F1500 ; move to start position\n'
                        'G1 Z0.26 F150 ; Move lower\n'
                        'G4 S0.5 ; wait 0.5 seconds\n'
                        '\n'
                        'G1 X0.1 Y150 Z0.3 F1500 E10 ; prime the nozzle\n'
                        'G1 X0.3 F1500\n'
                        'G1 X0.4 Y15 Z0.3 F1500 E15 ; prime the nozzle\n'
                        'G4 S0.1 ; wait 0.1 seconds\n'
                        '\n'
                        'G1 Z0.6 F150 ; lift nozzle\n'
                        'G92 E0 ; Reset Extruder\n'
                        'G1 Z2 F150 ; lift nozzle more\n',
 'max_layer_height': ['0.25'],
 'min_layer_height': ['0.07'],
 'name': 'Sovol SV06 Plus 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'undefine',
 'printable_area': ['0x0', '300x0', '300x300', '0x300'],
 'printable_height': '340',
 'printer_model': 'Sovol SV06 Plus',
 'printer_settings_id': 'Sovol',
 'retract_before_wipe': ['0%'],
 'retract_length_toolchange': ['1'],
 'retraction_length': ['0.5'],
 'retraction_minimum_travel': ['0.5'],
 'retraction_speed': ['30'],
 'scan_first_layer': '0',
 'setting_id': 'GM001',
 'single_extruder_multi_material': '1',
 'type': 'machine'}
