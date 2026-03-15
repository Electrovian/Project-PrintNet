from __future__ import annotations

# source: profiles/Vzbot/machine/fdm_klipper_common.json
DATA = {'auxiliary_fan': '0',
 'bed_exclude_area': ['0x0'],
 'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n',
 'change_filament_gcode': '',
 'default_filament_profile': ['Vzbot Generic ABS'],
 'default_print_profile': '0.20mm Standard @Vzbot',
 'deretraction_speed': ['80'],
 'extruder_clearance_height_to_lid': '140',
 'extruder_clearance_height_to_rod': '36',
 'extruder_clearance_radius': '45',
 'from': 'system',
 'gcode_flavor': 'klipper',
 'inherits': 'fdm_machine_common',
 'instantiation': 'false',
 'layer_change_gcode': ';DSLR_SNAPSHOT\nTIMELAPSE_TAKE_FRAME',
 'machine_end_gcode': 'G91; //rel pos\n'
                      'G1 E-5 f2000\n'
                      'G1 Z10 F600 ; lift nozzle 10mm/s\n'
                      'G1 E-29 f600\n'
                      'M104 S0\n'
                      'M140 S0 ; turn off bed\n'
                      '\n'
                      'M107\n'
                      'G90\n'
                      'G0 X117 Y200  F6000; move to back\n'
                      'M84     ; disable motors\n'
                      'DSLR_SNAPSHOT\n'
                      'RSCS_off\n'
                      '\n'
                      'exhaustfan_on\n'
                      'TIMELAPSE_RENDER\n'
                      '\n'
                      'G4 P60000 ; //Dwell for 1min\n'
                      'M107 \n'
                      'exhaustfan_off\n'
                      '\n'
                      'G4 P120000\n'
                      '\n'
                      'power_off ; //this is with moonraker',
 'machine_max_acceleration_e': ['20000', '20000'],
 'machine_max_acceleration_extruding': ['50000', '50000'],
 'machine_max_acceleration_retracting': ['10000', '10000'],
 'machine_max_acceleration_travel': ['50000', '50000'],
 'machine_max_acceleration_x': ['50000', '50000'],
 'machine_max_acceleration_y': ['50000', '50000'],
 'machine_max_acceleration_z': ['1000', '500'],
 'machine_max_jerk_e': ['0', '0'],
 'machine_max_jerk_x': ['0', '0'],
 'machine_max_jerk_y': ['0', '0'],
 'machine_max_jerk_z': ['0', '0'],
 'machine_max_speed_e': ['100', '100'],
 'machine_max_speed_x': ['2000', '2000'],
 'machine_max_speed_y': ['2000', '2000'],
 'machine_max_speed_z': ['15', '15'],
 'machine_min_extruding_rate': ['0', '0'],
 'machine_min_travel_rate': ['0', '0'],
 'machine_pause_gcode': 'PAUSE\n',
 'machine_start_gcode': 'BED_MESH_PROFILE LOAD=default \n'
                        'M190 S[bed_temperature_initial_layer_single] ;set bed temp \n'
                        'G28; \n'
                        'G1 X2 Y2 Z0 F9000  ; move to corner \n'
                        'M109 S[nozzle_temperature_initial_layer] ; set nozzle temp \n'
                        'G1 Z0.2 F300 ; raise nozzle to 0.2\n'
                        'G92 E0.0 ; reset extruder distance position\n'
                        'G1 X60.0 E9.0 F1000.0 ; intro line\n'
                        'G1 X100.0 E21.5 F1000.0 ; intro line\n'
                        'G0 Z2\n'
                        '\n'
                        'G92 E0.0 ; reset extruder distance position',
 'max_layer_height': ['0.32'],
 'min_layer_height': ['0.08'],
 'name': 'fdm_klipper_common',
 'nozzle_type': 'undefine',
 'printable_height': '200',
 'printer_settings_id': '',
 'printer_technology': 'FFF',
 'printer_variant': '0.4',
 'retract_before_wipe': ['70%'],
 'retract_length_toolchange': ['2'],
 'retract_restart_extra': ['0'],
 'retract_restart_extra_toolchange': ['0'],
 'retract_when_changing_layer': ['1'],
 'retraction_length': ['0.5'],
 'retraction_minimum_travel': ['1'],
 'retraction_speed': ['30'],
 'scan_first_layer': '0',
 'silent_mode': '0',
 'single_extruder_multi_material': '1',
 'type': 'machine',
 'wipe': ['1'],
 'z_hop': ['0'],
 'z_lift_type': 'NormalLift'}
