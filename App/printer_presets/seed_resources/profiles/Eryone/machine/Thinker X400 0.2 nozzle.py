from __future__ import annotations

# source: profiles/Eryone/machine/Thinker X400 0.2 nozzle.json
DATA = {'default_filament_profile': 'Eryone PLA @0.2 nozzle;Eryone ABS @0.2 nozzle;Eryone ASA @0.2 nozzle;Eryone PETG @0.2 '
                             'nozzle;Eryone Silk PLA @0.2 nozzle;Eryone TPU @0.2 nozzle;Eryone ABS-CF @0.2 '
                             'nozzle;Eryone ASA-CF @0.2 nozzle;Eryone PA @0.2 nozzle;Eryone PA-CF @0.2 nozzle;Eryone '
                             'PA-GF @0.2 nozzle;Eryone PETG-CF @0.2 nozzle;Eryone PLA-CF @0.2 nozzle;Eryone PP @0.2 '
                             'nozzle;Eryone PP-CF @0.2 nozzle;',
 'default_print_profile': '0.10mm Standard @Thinker X400 0.2 nozzle',
 'from': 'system',
 'inherits': 'Thinker X400 0.4 nozzle',
 'instantiation': 'true',
 'machine_start_gcode': 'M117 Heating\n'
                        'M104 S[first_layer_temperature] ; set extruder temp\n'
                        'M109 S[first_layer_temperature] ; wait for extruder temp\n'
                        'PRINT_START \n'
                        'G90 ; use absolute coordinates\n'
                        'M83 ; extruder relative mode\n'
                        'M204 S[machine_max_acceleration_extruding] T[machine_max_acceleration_retracting]\n'
                        'M104 S0\n'
                        'M140 S[bed_temperature_initial_layer_single] ; set bed temp\n'
                        'M117 Heating\n'
                        'M190 S[bed_temperature_initial_layer_single]\n'
                        'M104 S[first_layer_temperature] ; set extruder temp\n'
                        'M109 S[first_layer_temperature] ; wait for extruder temp\n'
                        ';QUAD_GANTRY_LEVEL\n'
                        'CLEAN_N S=[first_layer_temperature] X=240 Y=-3 A=0 D=0.4\n'
                        'M117 Quad Level\n'
                        '_QUAD_GANTRY_LEVEL  horizontal_move_z=10 retry_tolerance=1 LIFT_SPEED=5\n'
                        'G28 Z\n'
                        'M117 Quad Level\n'
                        '_QUAD_GANTRY_LEVEL  horizontal_move_z=5 retry_tolerance=0.05 LIFT_SPEED=5\n'
                        'M117 Bed Mesh Level\n'
                        'G1 X132.5 Y197.5\n'
                        'G28 N\n'
                        'BED_MESH_CALIBRATE\n'
                        'M117 Heating\n'
                        'G1 X275.0 Y0.0 Z0.3 F1500 ; move print head up\n'
                        'M104 S[first_layer_temperature] ; set extruder temp\n'
                        'M109 S[first_layer_temperature] ; wait for extruder temp\n'
                        'M117 .\n'
                        'INTRO_LINE D=0.2 ;intro line with 0.2 mm nozzle',
 'max_layer_height': ['0.14'],
 'min_layer_height': ['0.04'],
 'name': 'Thinker X400 0.2 nozzle',
 'nozzle_diameter': ['0.2'],
 'printer_model': 'Thinker X400',
 'retraction_length': ['0.5'],
 'setting_id': 'GM0032',
 'type': 'machine'}
