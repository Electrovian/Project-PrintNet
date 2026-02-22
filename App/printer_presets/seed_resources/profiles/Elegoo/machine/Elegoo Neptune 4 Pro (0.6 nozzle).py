from __future__ import annotations

# source: profiles/Elegoo/machine/Elegoo Neptune 4 Pro (0.6 nozzle).json
DATA = {'auxiliary_fan': '0',
 'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\nG92 E0\n;[layer_z]\n\n',
 'change_filament_gcode': 'M600',
 'default_filament_profile': ['Generic PLA @Elegoo'],
 'default_print_profile': '0.20mm Standard @Elegoo Neptune4Pro (0.6 nozzle)',
 'deretraction_speed': ['45'],
 'from': 'system',
 'gcode_flavor': 'klipper',
 'inherits': 'fdm_neptune_4_common',
 'instantiation': 'true',
 'layer_change_gcode': ';AFTER_LAYER_CHANGE\n;[layer_z]',
 'machine_end_gcode': ';PRINT END\n'
                      'G91 ;Relative positionning\n'
                      'G1 E-2 F2700 ;Retract a bit\n'
                      'G1 E-8 X5 Y5 Z3 F3000 ;Retract\n'
                      'G90 ;Absolute positionning\n'
                      'G1 X10 Y220 F6000;Finish print\n'
                      'M106 S0 ;Turn-off fan\n'
                      'M104 S0 ;Turn-off hotend\n'
                      'M140 S0 ;Turn-off bed\n'
                      'M84 X Y E ;Disable all steppers but Z',
 'machine_pause_gcode': 'PAUSE',
 'machine_start_gcode': ';ELEGOO NEPTUNE 4 PRO\n'
                        'M220 S100 ;Set the feed speed to 100%\n'
                        'M221 S100 ;Set the flow rate to 100%\n'
                        'M104 S140\n'
                        'M190 S[bed_temperature_initial_layer_single]\n'
                        'G90\n'
                        'G28 ;home\n'
                        'G1 Z10 F300\n'
                        'G1 X67.5 Y0 F6000\n'
                        'G1 Z0 F300\n'
                        'M109 S[nozzle_temperature_initial_layer]\n'
                        'G92 E0 ;Reset Extruder\n'
                        'G1 X67.5 Y0 Z0.4 F300 ;Move to start position\n'
                        'G1 X167.5 E30 F400 ;Draw the first line\n'
                        'G1 Z0.6 F120.0 ;Move to side a little\n'
                        'G1 X162.5 F3000\n'
                        'G92 E0 ;Reset Extruder',
 'max_layer_height': ['0.4'],
 'min_layer_height': ['0.08'],
 'name': 'Elegoo Neptune 4 Pro (0.6 nozzle)',
 'nozzle_diameter': ['0.6'],
 'nozzle_type': 'hardened_steel',
 'printable_area': ['0x0', '235x0', '235x230', '0x230'],
 'printable_height': '265',
 'printer_model': 'Elegoo Neptune 4 Pro',
 'printer_settings_id': 'Elegoo',
 'printer_variant': '0.6',
 'retract_before_wipe': ['85%'],
 'retract_length_toolchange': ['2'],
 'retraction_length': ['2.5'],
 'retraction_minimum_travel': ['1'],
 'retraction_speed': ['60'],
 'scan_first_layer': '0',
 'setting_id': 'GM001',
 'single_extruder_multi_material': '1',
 'type': 'machine'}
