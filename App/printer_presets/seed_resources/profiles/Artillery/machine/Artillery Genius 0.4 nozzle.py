from __future__ import annotations

# source: profiles/Artillery/machine/Artillery Genius 0.4 nozzle.json
DATA = {'auxiliary_fan': '0',
 'bed_exclude_area': ['0x0'],
 'change_filament_gcode': '',
 'default_filament_profile': ['Artillery Generic PLA'],
 'default_print_profile': '0.20mm Standard @Artillery Genius',
 'deretraction_speed': ['0'],
 'from': 'system',
 'inherits': 'fdm_machine_common',
 'instantiation': 'true',
 'layer_change_gcode': '',
 'machine_end_gcode': 'G91; Relative positionning\n'
                      'G1 E-2 Z0.2 F2400; Retract and raise Z\n'
                      'G1 X5 Y5 F3000; Wipe out\n'
                      'G1 Z10; Raise Z more\n'
                      'G90; Absolute positionning\n'
                      'G1 X0 Y100; Present print\n'
                      'M106 S0; Turn-off fan\n'
                      'M104 S0; Turn-off hotend\n'
                      'M140 S0; Turn-off bed\n'
                      'M84 X Y E; Disable all steppers but Z',
 'machine_max_acceleration_extruding': ['1000', '1250'],
 'machine_max_acceleration_retracting': ['1000', '1250'],
 'machine_max_acceleration_travel': ['1000', '1250'],
 'machine_max_acceleration_x': ['2000', '1000'],
 'machine_max_acceleration_y': ['2000', '1000'],
 'machine_max_acceleration_z': ['500', '200'],
 'machine_max_jerk_e': ['3', '2.5'],
 'machine_max_jerk_x': ['7', '10'],
 'machine_max_jerk_y': ['7', '10'],
 'machine_max_jerk_z': ['0.2', '0.4'],
 'machine_max_speed_e': ['120', '120'],
 'machine_max_speed_x': ['500', '200'],
 'machine_max_speed_y': ['500', '200'],
 'machine_max_speed_z': ['12', '12'],
 'machine_pause_gcode': 'M0',
 'machine_start_gcode': 'M83; extruder relative mode\n'
                        'G28; home all axes\n'
                        'M109 S[nozzle_temperature_initial_layer]; hotend temperature\n'
                        'M140 S[bed_temperature_initial_layer_single]; heatbed temperature\n'
                        'M190 S[bed_temperature_initial_layer_single]; wait for the bed to heat up\n'
                        'M109 S[nozzle_temperature_initial_layer]; wait for the extruder to heat up\n'
                        'G92 E0; reset extruder\n'
                        'G1 X20 Y5 Z0.3 F5000.0; move to start-line position\n'
                        'G1 Z0.3 F1000; print height\n'
                        'G1 X200 Y5 F1500.0 E15; draw 1st line\n'
                        'G1 X200 Y5.3 Z0.3 F5000.0; move to side a little\n'
                        'G1 X5.3  Y5.3 Z0.3 F1500.0 E30; draw 2nd line\n'
                        'G1 Z3 F3000; move z up little to prevent scratching of surface',
 'max_layer_height': ['0.32'],
 'min_layer_height': ['0.08'],
 'name': 'Artillery Genius 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'brass',
 'printable_area': ['0x0', '220x0', '220x220', '0x220'],
 'printable_height': '250',
 'printer_model': 'Artillery Genius',
 'printer_settings_id': 'Artillery',
 'retract_before_wipe': ['0%'],
 'retract_length_toolchange': ['4'],
 'retraction_length': ['1'],
 'retraction_minimum_travel': ['1'],
 'retraction_speed': ['35'],
 'scan_first_layer': '0',
 'setting_id': 'GM003',
 'single_extruder_multi_material': '1',
 'type': 'machine'}
