from __future__ import annotations

# source: profiles/UltiMaker/machine/UltiMaker 2 0.4 nozzle.json
DATA = {'auxiliary_fan': '0',
 'change_filament_gcode': '',
 'default_filament_profile': ['Generic PLA @System'],
 'default_print_profile': '0.18mm Standard @UltiMaker 2',
 'deretraction_speed': ['0'],
 'from': 'system',
 'inherits': 'fdm_machine_common',
 'instantiation': 'true',
 'machine_end_gcode': '; # # # # # # START Footer\n'
                      'G91; relative coordinates\n'
                      ';G1 E-1 F1200; retract the filament\n'
                      'G1 Z+15  X-10 Y-10 E-7  F6000; move Z a bit\n'
                      '; G1 X-10 Y-10 F6000; move XY a bit\n'
                      'G1 E-5.5 F300; retract the filament\n'
                      'G28 X0 Y0; move X/Y to min endstops, so the head is out of the way\n'
                      'M104 S0; extruder heater off\n'
                      'M140 S0; heated bed heater off (if you have it)\n'
                      'M84; disable motors\n'
                      '; # # # # # # END Footer\n',
 'machine_max_acceleration_extruding': ['1500', '1500'],
 'machine_max_acceleration_retracting': ['1500', '1500'],
 'machine_max_acceleration_travel': ['3000', '3000'],
 'machine_max_acceleration_x': ['3000', '3000'],
 'machine_max_acceleration_y': ['3000', '3000'],
 'machine_max_acceleration_z': ['500', '500'],
 'machine_max_jerk_e': ['2.5', '2.5'],
 'machine_max_jerk_x': ['20', '20'],
 'machine_max_jerk_y': ['20', '20'],
 'machine_max_jerk_z': ['0.4', '0.4'],
 'machine_max_speed_e': ['120', '120'],
 'machine_max_speed_x': ['500', '500'],
 'machine_max_speed_y': ['500', '500'],
 'machine_max_speed_z': ['12', '12'],
 'machine_pause_gcode': 'M0',
 'machine_start_gcode': '; # # # # # # START Header\n'
                        'G21; metric values\n'
                        'G90; absolute positioning\n'
                        'M82 ; set extruder to absolute mode\n'
                        'M107; start with the fan off\n'
                        '\n'
                        'M140 S[bed_temperature_initial_layer_single]; start bed heating\n'
                        '\n'
                        'G28 X0 Y0 Z0; move X/Y/Z to endstops\n'
                        'G1 X1 Y6 F15000; move X/Y to start position\n'
                        'G1 Z35 F9000; move Z to start position\n'
                        '\n'
                        '; Wait for bed and nozzle temperatures\n'
                        'M190 S{hot_plate_temp_initial_layer[0] - 5}; wait for bed temperature - 5\n'
                        'M140 S[bed_temperature_initial_layer_single]; continue bed heating\n'
                        'M109 S[nozzle_temperature_initial_layer]; wait for nozzle temperature\n'
                        '\n'
                        '; Purge and prime\n'
                        'M83; set extruder to relative mode\n'
                        'G92 E0; reset extrusion distance\n'
                        'G0 X0 Y1 F10000\n'
                        'G1 F150 E20 ; compress the bowden tube\n'
                        'G1 E-8 F1200\n'
                        'G0 X30 Y1 F5000\n'
                        'G0 F1200 Z{initial_layer_print_height/2}; Cut the connection to priming blob\n'
                        'G0 X100 F10000; disconnect with the prime blob\n'
                        'G0 X50; Avoid the metal clip holding the Ultimaker glass plate\n'
                        'G0 Z0.2 F720\n'
                        'G1 E8 F1200\n'
                        'G1 X80 E3 F1000; intro line 1\n'
                        'G1 X110 E4 F1000 ; intro line 2\n'
                        'G1 X140 F600; drag filament to decompress bowden tube\n'
                        'G1 X100 F3200; wipe backwards a bit\n'
                        'G1 X150 F3200; back to where there is no plastic: avoid dragging\n'
                        'G92 E0; reset extruder reference\n'
                        'M82; set extruder to absolute mode\n'
                        '\n'
                        '; # # # # # # END Header',
 'max_layer_height': ['0.3'],
 'min_layer_height': ['0.08'],
 'name': 'UltiMaker 2 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'undefine',
 'printable_area': ['0x0', '224x0', '224x225', '0x225'],
 'printable_height': '212',
 'printer_model': 'UltiMaker 2',
 'printer_settings_id': 'Qidi',
 'retract_before_wipe': ['70%'],
 'retract_length_toolchange': ['10'],
 'retraction_length': ['4.5'],
 'retraction_minimum_travel': ['5'],
 'retraction_speed': ['35'],
 'scan_first_layer': '0',
 'setting_id': 'GM001',
 'single_extruder_multi_material': '1',
 'type': 'machine',
 'wipe_distance': ['0.2']}
