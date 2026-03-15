from __future__ import annotations

# source: profiles/Comgrow/machine/Comgrow T300 0.4 nozzle.json
DATA = {'before_layer_change_gcode': '',
 'deretraction_speed': ['50'],
 'from': 'system',
 'inherits': 'fdm_comgrow_common',
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
 'machine_start_gcode': 'G28\n'
                        'G90\n'
                        'G1 X0 F3000\n'
                        'G1 Z0.300 F600\n'
                        'G1 Y0 F3000\n'
                        'G91 \n'
                        'G1 X-2 Y-6 F3000\n'
                        'START_PRINT\n'
                        'M400\n'
                        'G90\n'
                        'M83\n'
                        'G90\n'
                        'G1 X0 F3000\n'
                        'G1 Z0.300 F600\n'
                        'G1 Y0 F3000\n'
                        'G91 \n'
                        'G1 X-2 Y-6 F3000\n'
                        'M140 S[bed_temperature_initial_layer_single] ;set bed temp\n'
                        'M104 S[nozzle_temperature_initial_layer] ;set extruder temp\n'
                        'M190 S[bed_temperature_initial_layer_single] ;wait for bed temp\n'
                        'M109 S[nozzle_temperature_initial_layer];wait for extruder temp\n'
                        'G1 E25 F480\n'
                        'G4 P1000\n'
                        'G1 E-0.200 Z5 F600\n'
                        'G1 X90.000 F6000\n'
                        'G1 Z-5.200 F600\n'
                        'G1 X60.000 E14.4 F3000\n'
                        'G1 X60.000 E9.6 F3000\n'
                        'G1 Y1 E0.16 F3000\n'
                        'G1 X-60.000 E9.6 F3000\n'
                        'G1 X-60.000 E14.4 F3000\n'
                        'G1 Y1 E0.16 F3000\n'
                        'G1 X60.000 E14.4 F3000\n'
                        'G1 X60.000 E9.6 F3000\n'
                        'G1 E-0.100 Z0.5 F600\n'
                        'M400\n'
                        '\n',
 'max_layer_height': ['0.32'],
 'name': 'Comgrow T300 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'printable_area': ['0x0', '300x0', '300x300', '0x300'],
 'printable_height': '350',
 'printer_model': 'Comgrow T300',
 'retract_lift_below': ['348'],
 'retraction_length': ['0.8'],
 'retraction_speed': ['50'],
 'setting_id': 'GM001',
 'thumbnails': ['64x64', '160x160', '176x176'],
 'thumbnails_format': 'JPG',
 'type': 'machine',
 'z_hop': ['0.4']}
