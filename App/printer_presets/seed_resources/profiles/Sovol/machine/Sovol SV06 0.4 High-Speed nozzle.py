from __future__ import annotations

# source: profiles/Sovol/machine/Sovol SV06 0.4 High-Speed nozzle.json
DATA = {'before_layer_change_gcode': 'TIMELAPSE_TAKE_FRAME\nG92 E0',
 'default_filament_profile': ['Generic PLA @System'],
 'default_print_profile': '0.20mm High-Speed @Sovol SV06',
 'deretraction_speed': ['35', '35'],
 'from': 'system',
 'inherits': 'fdm_machine_common',
 'instantiation': 'true',
 'machine_end_gcode': 'M117 READY\n'
                      '\n'
                      'G1 E0 F1000 ; reset extruder\n'
                      '\n'
                      'G91 ; relative positioning\n'
                      'G1 Z2 F1000 ; lift nozzle\n'
                      'G90 ; absolute positioning\n'
                      'G1 X5 Y5 F3000\n'
                      'G27 P2 ; park extruder\n'
                      'M140 S0 ; turn off heatbed\n'
                      'M104 S0 ; turn off temperature\n'
                      'M107 ; turn off fan\n'
                      'M84 X Y E ; disable motors\n',
 'machine_max_acceleration_e': ['5000', '5000'],
 'machine_max_acceleration_extruding': ['5000', '5000'],
 'machine_max_acceleration_retracting': ['1000', '1000'],
 'machine_max_acceleration_travel': ['1500', '1500'],
 'machine_max_acceleration_x': ['5000', '5000'],
 'machine_max_acceleration_y': ['5000', '5000'],
 'machine_max_acceleration_z': ['500', '500'],
 'machine_max_jerk_e': ['2.5'],
 'machine_max_jerk_x': ['5'],
 'machine_max_jerk_y': ['5'],
 'machine_max_jerk_z': ['0.4'],
 'machine_max_speed_e': ['30', '30'],
 'machine_max_speed_x': ['300', '300'],
 'machine_max_speed_y': ['300', '300'],
 'machine_max_speed_z': ['10', '10'],
 'machine_start_gcode': 'M140 S[bed_temperature_initial_layer_single] ;set bed temp\n'
                        'M190 S[bed_temperature_initial_layer_single] ;wait for bed temp\n'
                        'G28\n'
                        'G90\n'
                        'G1 X0 F6000\n'
                        'G1 Y20\n'
                        'G1 Z0.600 F600\n'
                        'G1 Y0 F6000\n'
                        'M400\n'
                        'M104 S[nozzle_temperature_initial_layer] ;set extruder temp\n'
                        'M109 S[nozzle_temperature_initial_layer];wait for extruder temp\n'
                        'G91\n'
                        'M83\n'
                        'G1 E25 F300\n'
                        'G4 P1000\n'
                        'G1 E-0.200 Z5 F600\n'
                        'G1 X23.000 F9000\n'
                        'G1 Z-5.000 F600\n'
                        'G1 X87.000 E20.88 F1800\n'
                        'G1 X87.000 E13.92 F1800\n'
                        'G1 Y1 E0.16 F1800\n'
                        'G1 X-87.000 E13.92 F1800\n'
                        'G1 X-87.000 E20.88 F1800\n'
                        'G1 Y1 E0.24 F1800\n'
                        'G1 X87.000 E20.88 F1800\n'
                        'G1 X87.000 E13.92 F1800\n'
                        'G1 E-0.200 Z1 F600\n'
                        'M400\n'
                        '\n',
 'max_layer_height': ['0.32', '0.32'],
 'name': 'Sovol SV06 0.4 High-Speed nozzle',
 'nozzle_diameter': ['0.4'],
 'printable_area': ['0x0', '220x0', '220x220', '0x220'],
 'printable_height': '250',
 'printer_model': 'Sovol SV06',
 'retract_length_toolchange': ['1', '1'],
 'retract_lift_below': ['248', '248'],
 'retraction_length': ['0.5'],
 'retraction_speed': ['35', '35'],
 'setting_id': 'GM001',
 'thumbnails': ['300x300'],
 'thumbnails_format': 'PNG',
 'type': 'machine',
 'wipe_distance': ['2', '2'],
 'z_hop': ['0.4', '0.4']}
