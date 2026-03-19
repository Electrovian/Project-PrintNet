from __future__ import annotations

# source: profiles/Creality/machine/Creality CR-10 V3 0.6 nozzle.json
DATA = {'auxiliary_fan': '0',
 'change_filament_gcode': 'M600',
 'default_filament_profile': ['Creality Generic PLA'],
 'default_print_profile': '0.20mm Standard @Creality CR10V3 0.6',
 'deretraction_speed': ['40'],
 'from': 'system',
 'inherits': 'fdm_creality_common',
 'instantiation': 'true',
 'machine_end_gcode': '{if max_layer_z < printable_height}G1 Z{z_offset+min(max_layer_z+2, printable_height)} '
                      'F600{endif} ; Move print head up\n'
                      'G1 X5 Y170 F{travel_speed*60} ; present print\n'
                      '{if max_layer_z < printable_height-10}G1 Z{z_offset+min(max_layer_z+70, printable_height-10)} '
                      'F600{endif} ; Move print head further up\n'
                      'M140 S0 ; turn off heatbed\n'
                      'M104 S0 ; turn off temperature\n'
                      'M107 ; turn off fan\n'
                      'M84 X Y E ; disable motors',
 'machine_max_acceleration_extruding': ['500', '500'],
 'machine_max_acceleration_retracting': ['1000', '1000'],
 'machine_max_acceleration_travel': ['1500', '1250'],
 'machine_max_acceleration_x': ['500', '500'],
 'machine_max_acceleration_y': ['500', '500'],
 'machine_max_acceleration_z': ['100', '100'],
 'machine_max_jerk_e': ['5', '5'],
 'machine_max_jerk_x': ['8', '8'],
 'machine_max_jerk_y': ['8', '8'],
 'machine_max_jerk_z': ['0.4', '0.4'],
 'machine_max_speed_e': ['60', '60'],
 'machine_max_speed_x': ['500', '500'],
 'machine_max_speed_y': ['500', '500'],
 'machine_max_speed_z': ['10', '10'],
 'machine_pause_gcode': 'M0',
 'machine_start_gcode': 'G90 ; use absolute coordinates\n'
                        'M83 ; extruder relative mode\n'
                        'M104 S[nozzle_temperature_initial_layer] ; set extruder temp\n'
                        'M140 S[bed_temperature_initial_layer_single] ; set bed temp\n'
                        'G4 S30 ; allow partial nozzle warmup\n'
                        'G28 ; home all axis\n'
                        'G1 Z50 F240\n'
                        'G1 X2.0 Y10 F3000\n'
                        'M104 S{first_layer_temperature[0]} ; set final nozzle temp\n'
                        'M190 S[bed_temperature_initial_layer_single] ; wait for bed temp\n'
                        'M109 S[nozzle_temperature_initial_layer] ; wait for extruder temp\n'
                        'G1 Z0.28 F240\n'
                        'G92 E0\n'
                        'G1 X2 Y140 E10 F1500 ; prime the nozzle\n'
                        'G1 X2.3 Y140 F5000\n'
                        'G92 E0\n'
                        'G1 X2.3 Y10 E10 F1200 ; prime the nozzle\n'
                        'G92 E0',
 'max_layer_height': ['0.42'],
 'min_layer_height': ['0.08'],
 'name': 'Creality CR-10 V3 0.6 nozzle',
 'nozzle_diameter': ['0.6'],
 'nozzle_type': 'undefine',
 'printable_area': ['5x5', '305x5', '305x305', '5x305'],
 'printable_height': '400',
 'printer_model': 'Creality CR-10 V3',
 'printer_settings_id': 'Creality',
 'printer_structure': 'i3',
 'retract_before_wipe': ['70%'],
 'retract_length_toolchange': ['1'],
 'retraction_length': ['1'],
 'retraction_minimum_travel': ['2'],
 'retraction_speed': ['60'],
 'scan_first_layer': '0',
 'setting_id': 'GM001',
 'single_extruder_multi_material': '1',
 'type': 'machine'}
