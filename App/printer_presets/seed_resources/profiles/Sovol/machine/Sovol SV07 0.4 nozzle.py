from __future__ import annotations

# source: profiles/Sovol/machine/Sovol SV07 0.4 nozzle.json
DATA = {'before_layer_change_gcode': 'TIMELAPSE_TAKE_FRAME\nG92 E0',
 'default_print_profile': '0.20mm Standard @Sovol SV07',
 'deretraction_speed': ['50'],
 'from': 'system',
 'inherits': 'fdm_machine_common',
 'instantiation': 'true',
 'machine_end_gcode': 'END_PRINT\n',
 'machine_max_acceleration_e': ['5000'],
 'machine_max_acceleration_extruding': ['20000'],
 'machine_max_acceleration_retracting': ['5000'],
 'machine_max_acceleration_x': ['12000'],
 'machine_max_acceleration_y': ['12000'],
 'machine_max_acceleration_z': ['500'],
 'machine_max_jerk_e': ['3'],
 'machine_max_jerk_x': ['9'],
 'machine_max_jerk_y': ['9'],
 'machine_max_jerk_z': ['0.25'],
 'machine_max_speed_e': ['50'],
 'machine_max_speed_x': ['500'],
 'machine_max_speed_y': ['500'],
 'machine_max_speed_z': ['20'],
 'machine_pause_gcode': 'PAUSE',
 'machine_start_gcode': 'G28\n'
                        'G90\n'
                        'G1 X0 F9000\n'
                        'G1 Y20 F9000\n'
                        'G1 Z0.300 F600\n'
                        'G1 Y0 F9000\n'
                        'G91\n'
                        'M83\n'
                        'M140 S[bed_temperature_initial_layer_single] ;set bed temp\n'
                        'M104 S[nozzle_temperature_initial_layer] ;set extruder temp\n'
                        'M190 S[bed_temperature_initial_layer_single] ;wait for bed temp\n'
                        'M109 S[nozzle_temperature_initial_layer];wait for extruder temp\n'
                        'G1 E25 F480\n'
                        'G4 P1000\n'
                        'G1 E-0.200 Z5 F600\n'
                        'G1 X55.000 Y0.000 F6000\n'
                        'G1 Z-4.800 F600\n'
                        'G1 X55.000 E13.2 F3000\n'
                        'G1 X55.000 E8.8 F3000\n'
                        'G1 Y1 E0.16 F3000\n'
                        'G1 X-55.000 E8.8 F3000\n'
                        'G1 X-55.000 E13.2 F3000\n'
                        'G1 Y1 E0.24 F3000\n'
                        'G1 X55.000 E13.2 F3000\n'
                        'G1 X55.000 E8.8 F3000\n'
                        'G1 E-0.200 Z1 F600\n'
                        'M400\n'
                        '\n',
 'max_layer_height': ['0.32'],
 'name': 'Sovol SV07 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'printable_area': ['0x0', '220x0', '220x220', '0x220'],
 'printable_height': '250',
 'printer_model': 'Sovol SV07',
 'retract_lift_below': ['348'],
 'retraction_length': ['0.8'],
 'retraction_speed': ['50'],
 'setting_id': 'GM001',
 'thumbnails': ['300x300'],
 'thumbnails_format': 'PNG',
 'type': 'machine',
 'z_hop': ['0.4']}
