from __future__ import annotations

# source: profiles/Anycubic/machine/Anycubic Kobra 0.4 nozzle.json
DATA = {'auxiliary_fan': '0',
 'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\nG92 E0.0\n;[layer_z]\n\n',
 'change_filament_gcode': 'M600',
 'default_filament_profile': ['Anycubic Generic PLA'],
 'default_print_profile': '0.20mm Standard @Anycubic Kobra',
 'deretraction_speed': ['50'],
 'from': 'system',
 'inherits': 'fdm_machine_common',
 'instantiation': 'true',
 'layer_change_gcode': ';AFTER_LAYER_CHANGE\n;[layer_z]',
 'machine_end_gcode': 'G1 E-1.0 F2100 ; retract\n'
                      'G92 E0.0\n'
                      'G1 X0{if max_layer_z < printable_height} Z{z_offset+min(max_layer_z+30, '
                      'printable_height)}{endif} E-34.0 F{travel_speed*60} ; move print head up & retract filament\n'
                      'G4 ; wait\n'
                      'M104 S0 ; turn off temperature\n'
                      'M140 S0 ; turn off heatbed\n'
                      'M107 ; turn off fan\n'
                      'G1 X0 Y105 F{travel_speed*60} ; park print head\n'
                      'M84 ; disable motors',
 'machine_max_acceleration_extruding': ['1000', '1000'],
 'machine_max_acceleration_retracting': ['1000', '1000'],
 'machine_max_acceleration_travel': ['1000', '1000'],
 'machine_max_acceleration_x': ['700', '700'],
 'machine_max_acceleration_y': ['600', '600'],
 'machine_max_acceleration_z': ['50', '50'],
 'machine_max_jerk_e': ['10', '10'],
 'machine_max_jerk_x': ['20', '20'],
 'machine_max_jerk_y': ['20', '20'],
 'machine_max_jerk_z': ['0.6', '0.6'],
 'machine_max_speed_e': ['80', '80'],
 'machine_max_speed_x': ['300', '300'],
 'machine_max_speed_y': ['250', '250'],
 'machine_max_speed_z': ['20', '20'],
 'machine_pause_gcode': 'M601',
 'machine_start_gcode': 'G90 ; use absolute coordinates\n'
                        'M83 ; extruder relative mode\n'
                        'M204 P[machine_max_acceleration_extruding] R[machine_max_acceleration_retracting] '
                        'T[machine_max_acceleration_travel]\n'
                        'M104 S[nozzle_temperature_initial_layer] ; set extruder temp\n'
                        'M140 S[bed_temperature_initial_layer_single] ; set bed temp\n'
                        'G28 ; home all\n'
                        'G1 Y1.0 Z0.3 F{travel_speed*60} ; move print head up\n'
                        'M190 S[bed_temperature_initial_layer_single] ; wait for bed temp\n'
                        'M109 S[nozzle_temperature_initial_layer] ; wait for extruder temp\n'
                        'G92 E0.0\n'
                        '; initial load\n'
                        'G1 X205.0 E19 F1000\n'
                        'G1 Y1.6\n'
                        'G1 X5.0 E19 F1000\n'
                        'G92 E0.0\n'
                        '; intro line\n'
                        'G1 Y2.0 Z0.2 F1000\n'
                        'G1 X65.0 E9.0 F1000\n'
                        'G1 X105.0 E12.5 F1000\n'
                        'G92 E0.0',
 'max_layer_height': ['0.3'],
 'min_layer_height': ['0.05'],
 'name': 'Anycubic Kobra 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'undefine',
 'printable_area': ['0x0', '220x0', '220x220', '0x220'],
 'printable_height': '250',
 'printer_model': 'Anycubic Kobra',
 'printer_settings_id': 'Anycubic',
 'retract_before_wipe': ['60%'],
 'retract_length_toolchange': ['1'],
 'retraction_length': ['6'],
 'retraction_minimum_travel': ['1.5'],
 'retraction_speed': ['40'],
 'scan_first_layer': '0',
 'setting_id': 'GM001',
 'single_extruder_multi_material': '1',
 'type': 'machine'}
