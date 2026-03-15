from __future__ import annotations

# source: profiles/Sovol/machine/Sovol SV08 0.8 nozzle.json
DATA = {'before_layer_change_gcode': 'TIMELAPSE_TAKE_FRAME\nG92 E0',
 'default_filament_profile': ['Sovol SV08 PLA'],
 'default_print_profile': '0.20mm Standard @Sovol SV08 0.8 nozzle',
 'deretraction_speed': ['30'],
 'from': 'system',
 'gcode_flavor': 'klipper',
 'inherits': 'fdm_machine_common',
 'instantiation': 'true',
 'machine_end_gcode': 'END_PRINT\n',
 'machine_max_acceleration_e': ['5000'],
 'machine_max_acceleration_extruding': ['20000'],
 'machine_max_acceleration_retracting': ['5000'],
 'machine_max_acceleration_travel': ['40000'],
 'machine_max_acceleration_x': ['40000'],
 'machine_max_acceleration_y': ['40000'],
 'machine_max_acceleration_z': ['500'],
 'machine_max_jerk_e': ['5'],
 'machine_max_jerk_x': ['20'],
 'machine_max_jerk_y': ['20'],
 'machine_max_jerk_z': ['0.5'],
 'machine_max_speed_e': ['50'],
 'machine_max_speed_x': ['700'],
 'machine_max_speed_y': ['700'],
 'machine_max_speed_z': ['20'],
 'machine_pause_gcode': 'PAUSE',
 'machine_start_gcode': 'G28\n'
                        'G90\n'
                        'G1 X0 F9000\n'
                        'G1 Y20\n'
                        'G1 Z0.600 F600\n'
                        'G1 Y0 F9000\n'
                        'START_PRINT\n'
                        'G90\n'
                        'G1 X0 F9000\n'
                        'G1 Y20\n'
                        'G1 Z0.600 F600\n'
                        'G1 Y0 F9000\n'
                        'M400\n'
                        'G91\n'
                        'M83\n'
                        'M140 S[bed_temperature_initial_layer_single] ;set bed temp\n'
                        'M104 S[nozzle_temperature_initial_layer] ;set extruder temp\n'
                        'M190 S[bed_temperature_initial_layer_single] ;wait for bed temp\n'
                        'M109 S[nozzle_temperature_initial_layer];wait for extruder temp\n'
                        'G1 E25 F300\n'
                        'G4 P1000\n'
                        'G1 E-0.200 Z5 F600\n'
                        'G1 X88.000 F9000\n'
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
                        'M400\n',
 'max_layer_height': ['0.56'],
 'min_layer_height': ['0.16'],
 'name': 'Sovol SV08 0.8 nozzle',
 'nozzle_diameter': ['0.8'],
 'printable_area': ['0x0', '350x0', '350x350', '0x350'],
 'printable_height': '345',
 'printer_model': 'Sovol SV08',
 'printer_variant': '0.8',
 'retract_before_wipe': ['0%'],
 'retract_length_toolchange': ['2'],
 'retract_lift_below': ['343'],
 'retraction_length': ['0.5'],
 'retraction_minimum_travel': ['1'],
 'retraction_speed': ['30'],
 'setting_id': 'GM001',
 'thumbnails': ['300x300', '400x300', '32x32'],
 'thumbnails_format': 'PNG',
 'type': 'machine',
 'wipe_distance': ['2'],
 'z_hop': ['0.4']}
