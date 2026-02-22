from __future__ import annotations

# source: profiles/Creality/machine/Creality Ender-3 V3 SE 0.6 nozzle.json
DATA = {'auxiliary_fan': '0',
 'change_filament_gcode': 'M600',
 'default_filament_profile': ['Creality Generic PLA @Ender-3V3-all'],
 'default_print_profile': '0.20mm Standard @Creality Ender3V3SE 0.6',
 'deretraction_speed': ['30'],
 'disable_m73': '1',
 'extruder_clearance_height_to_rod': '47',
 'extruder_clearance_radius': '90',
 'from': 'system',
 'gcode_flavor': 'marlin2',
 'inherits': 'fdm_creality_common',
 'instantiation': 'true',
 'machine_end_gcode': 'G91 ;Relative positionning \n'
                      'G1 E-2 F2700 ;Retract a bit \n'
                      'G1 E-2 Z0.2 F2400 ;Retract and raise Z \n'
                      'G1 X5 Y5 F3000 ;Wipe out \n'
                      'G1 Z10 ;Raise Z more \n'
                      'G90 ;Absolute positionning \n'
                      ' \n'
                      'G1 X0 Y220 ;Present print \n'
                      'M106 S0 ;Turn-off fan \n'
                      'M104 S0 ;Turn-off hotend \n'
                      'M140 S0 ;Turn-off bed \n'
                      ' \n'
                      'M84 X Y E ;Disable all steppers but Z',
 'machine_load_filament_time': '11',
 'machine_max_acceleration_extruding': ['2500', '2500'],
 'machine_max_acceleration_retracting': ['500', '500'],
 'machine_max_acceleration_travel': ['2500', '2500'],
 'machine_max_acceleration_x': ['2500', '2500'],
 'machine_max_acceleration_y': ['2500', '2500'],
 'machine_max_acceleration_z': ['500', '500'],
 'machine_max_jerk_e': ['5', '5'],
 'machine_max_jerk_x': ['10', '10'],
 'machine_max_jerk_y': ['10', '10'],
 'machine_max_jerk_z': ['0.4', '0.4'],
 'machine_max_speed_e': ['40', '40'],
 'machine_max_speed_x': ['250', '250'],
 'machine_max_speed_y': ['250', '250'],
 'machine_max_speed_z': ['5', '5'],
 'machine_pause_gcode': 'M25',
 'machine_start_gcode': 'M220 S100 ;Reset Feedrate \n'
                        'M221 S100 ;Reset Flowrate \n'
                        ' \n'
                        'M104 S[nozzle_temperature_initial_layer] ;Set final nozzle temp \n'
                        'M190 S[bed_temperature_initial_layer_single] ;Set and wait for bed temp to stabilize \n'
                        'G28 ;Home \n'
                        'G92 E0 ;Reset Extruder \n'
                        'G1 Z2.0 F3000 ;Move Z Axis up \n'
                        'G1 X-2.1 Y20 Z0.28 F5000.0 ;Move to start position \n'
                        'M109 S[nozzle_temperature_initial_layer] ;Wait for nozzle temp to stabilize \n'
                        'G1 X-2.1 Y145.0 Z0.28 F1500.0 E15 ;Draw the first line \n'
                        'G1 X-2.4 Y145.0 Z0.28 F5000.0 ;Move to side a little \n'
                        'G1 X-2.4 Y20 Z0.28 F1500.0 E30 ;Draw the second line \n'
                        'G92 E0  ;Reset Extruder \n'
                        'G1 E-1.0000 F1800 ;Retract a bit \n'
                        'G1 Z2.0 F3000 ;Move Z Axis up \n'
                        'G1 E0.0000 F1800',
 'manual_filament_change': '1',
 'max_layer_height': ['0.48'],
 'min_layer_height': ['0.12'],
 'name': 'Creality Ender-3 V3 SE 0.6 nozzle',
 'nozzle_diameter': ['0.6'],
 'nozzle_type': 'brass',
 'printable_area': ['0x0', '220x0', '220x220', '0x220'],
 'printable_height': '250',
 'printer_model': 'Creality Ender-3 V3 SE',
 'printer_settings_id': 'Creality',
 'printer_structure': 'i3',
 'printer_variant': '0.6',
 'retract_before_wipe': ['70%'],
 'retract_length_toolchange': ['1'],
 'retraction_length': ['1.2'],
 'retraction_minimum_travel': ['2'],
 'retraction_speed': ['40'],
 'scan_first_layer': '0',
 'setting_id': 'GM001',
 'single_extruder_multi_material': '1',
 'thumbnails': [],
 'type': 'machine',
 'z_hop_types': ['Spiral Lift']}
