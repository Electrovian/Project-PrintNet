from __future__ import annotations

# source: profiles/Anycubic/machine/Anycubic 4Max Pro 2 0.4 nozzle.json
DATA = {'auxiliary_fan': '0',
 'change_filament_gcode': 'M600',
 'default_filament_profile': ['Anycubic Generic PLA'],
 'default_print_profile': '0.20mm Standard @Anycubic 4MaxPro2',
 'deretraction_speed': ['25'],
 'from': 'system',
 'inherits': 'fdm_machine_common',
 'instantiation': 'true',
 'machine_end_gcode': 'M104 S0 ; turn off extruder heating\n'
                      'M140 S0 ; turn off bed heating\n'
                      'M107 ; turn off fans\n'
                      'G91 ; relative positioning\n'
                      'G0 Z+0.5 ; move Z up a tiny bit\n'
                      'G90 ; absolute positioning\n'
                      'G0 X135 Y105 F{machine_max_speed_x[0]*60} ; move extruder to center position\n'
                      'G0 Z190.5 F{machine_max_speed_z[0]*60} ; lower the plattform to Z min\n'
                      'M84 ; steppers off\n'
                      'G90 ; absolute positioning\n',
 'machine_max_acceleration_extruding': ['1250', '1250'],
 'machine_max_acceleration_retracting': ['1250', '1250'],
 'machine_max_acceleration_travel': ['1500', '1500'],
 'machine_max_acceleration_x': ['900', '900'],
 'machine_max_acceleration_y': ['900', '900'],
 'machine_max_acceleration_z': ['100', '100'],
 'machine_max_jerk_e': ['5', '5'],
 'machine_max_jerk_x': ['6', '6'],
 'machine_max_jerk_y': ['6', '6'],
 'machine_max_jerk_z': ['0.2', '0.2'],
 'machine_max_speed_e': ['120', '120'],
 'machine_max_speed_x': ['200', '200'],
 'machine_max_speed_y': ['200', '200'],
 'machine_max_speed_z': ['16', '16'],
 'machine_pause_gcode': 'M601',
 'machine_start_gcode': 'G21 ; metric values\n'
                        'G90 ; absolute positioning\n'
                        'M82 ; set extruder to absolute mode\n'
                        'M140 S[first_layer_bed_temperature] ; set bed temp\n'
                        'G28 X0 Y0 ; home X and Y\n'
                        'G28 Z0 ; home Z\n'
                        'G1 Z30 F{machine_max_speed_z[0]*60} ; move Z a bit down to not blow on the bed edge while '
                        'heating\n'
                        'G1 X10 F3900 ; let some space on x to prevent the filament cooling exhaust from beeing '
                        'blocked by the servo motor\n'
                        'M190 S[bed_temperature_initial_layer_single] ; wait for bed temp\n'
                        'M104 S[nozzle_temperature_initial_layer] ; set extruder temp\n'
                        'M106 S80 ; turn on fan to prevent air nozzle melt while heating up\n'
                        'M109 S[nozzle_temperature_initial_layer] ; wait for extruder temp\n'
                        'M107 ; start with the fan off\n'
                        'G28 X0 ; goto X home again\n'
                        'G92 E0 ; zero the extruded length\n'
                        'G1 Z0.2 F360 ; move plattform upwards\n'
                        '; extrude material next to the plattform (comment or remove following lines to disable)\n'
                        'G1 F180 E20 ; extrude some material next to the plattform\n'
                        'G92 E0 ; zero the extruded length\n'
                        'G1 E-[retraction_length] F{retraction_speed[0]*60} ; do a filament retract\n'
                        'G92 E0 ; zero the extruded length again\n'
                        'G1 X5 F3900 ; move sideways to get rid of that string\n'
                        'G1 E[retraction_length] F{retraction_speed[0]*60} ; do a filament deretract with retract '
                        'parameters\n'
                        'G92 E0 ; zero the extruded length again\n'
                        '; draw intro line (comment or remove following lines to disable)\n'
                        'G1 X30 E5 F700 ; draw intro line\n'
                        'G92 E0 ; zero the extruded length\n'
                        'G1 E-[retraction_length] F{retraction_speed[0]*60} ; do a filament retract\n'
                        'G1 X40 Z2.0 ; move away from the introline\n'
                        'G92 E0 ; zero the extruded length again\n'
                        'G1 E[retraction_length] F{retraction_speed[0]*60} ; do a filament deretract with retract '
                        'parameters\n'
                        '; end of intro line code\n'
                        'M117 Printing...\n'
                        'G5',
 'max_layer_height': ['0.3'],
 'min_layer_height': ['0.07'],
 'name': 'Anycubic 4Max Pro 2 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'undefine',
 'printable_area': ['0x0', '270x0', '270x210', '0x210'],
 'printable_height': '190',
 'printer_model': 'Anycubic 4Max Pro 2',
 'printer_settings_id': 'Anycubic',
 'retract_before_wipe': ['0%'],
 'retract_length_toolchange': ['10'],
 'retraction_length': ['2.5'],
 'retraction_minimum_travel': ['2'],
 'retraction_speed': ['35'],
 'scan_first_layer': '0',
 'setting_id': 'GM001',
 'single_extruder_multi_material': '1',
 'type': 'machine'}
