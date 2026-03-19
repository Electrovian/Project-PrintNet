from __future__ import annotations

# source: profiles/Artillery/machine/Artillery Sidewinder X2 0.4 nozzle.json
DATA = {'auxiliary_fan': '0',
 'bed_exclude_area': ['0x0'],
 'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\nG92 E0\n;[layer_z]\n\n',
 'change_filament_gcode': '',
 'default_filament_profile': ['Artillery Generic PLA'],
 'default_print_profile': '0.20mm Standard @Artillery X2',
 'deretraction_speed': ['0'],
 'from': 'system',
 'inherits': 'fdm_machine_common',
 'instantiation': 'true',
 'layer_change_gcode': ';AFTER_LAYER_CHANGE\n;[layer_z]',
 'machine_end_gcode': 'G4 ; wait\n'
                      'G92 E0 ; prepare to retract\n'
                      'G1 E-0.5 F3000; retract to avoid stringing\n'
                      '\n'
                      '; Anti-stringing end wiggle\n'
                      'G91 ; use relative coordinates\n'
                      'G1 X1 Y1 F1200\n'
                      '\n'
                      '; Raise nozzle and present bed\n'
                      '{if layer_z < printable_height}G1 Z{z_offset+min(layer_z+120, printable_height)}{endif} ; Move '
                      'print head up\n'
                      'G90 ; use absolute coordinates\n'
                      '\n'
                      '; Reset print setting overrides\n'
                      'M200 D0 ; disable volumetric e\n'
                      'M220 S100 ; reset speed factor to 100%\n'
                      'M221 S100 ; reset extrusion rate to 100%\n'
                      '\n'
                      '; Shut down printer\n'
                      'M106 S0 ; turn-off fan\n'
                      'M104 S0 ; turn-off hotend\n'
                      'M140 S0 ; turn-off bed\n'
                      'M150 P0 ; turn off led\n'
                      'M85 S0 ; deactivate idle timeout\n'
                      'M84 ; disable motors\n',
 'machine_max_acceleration_extruding': ['1250', '1250'],
 'machine_max_acceleration_retracting': ['1250', '1250'],
 'machine_max_acceleration_travel': ['1000', '1000'],
 'machine_max_acceleration_x': ['1000', '960'],
 'machine_max_acceleration_y': ['1000', '960'],
 'machine_max_acceleration_z': ['1000', '1000'],
 'machine_max_jerk_e': ['1.5', '1.5'],
 'machine_max_jerk_x': ['8', '8'],
 'machine_max_jerk_y': ['8', '8'],
 'machine_max_jerk_z': ['0.4', '0.4'],
 'machine_max_speed_e': ['120', '120'],
 'machine_max_speed_x': ['200', '100'],
 'machine_max_speed_y': ['200', '100'],
 'machine_max_speed_z': ['12', '12'],
 'machine_pause_gcode': 'M0',
 'machine_start_gcode': '; Initial setups\n'
                        'G90 ; use absolute coordinates\n'
                        'M83 ; extruder relative mode\n'
                        'M900 K0.12 ; K factor\n'
                        'M900 W[line_width] H[layer_height] D[filament_diameter]\n'
                        'M200 D0 ; disable volumetric e\n'
                        'M220 S100 ; reset speed factor to 100%\n'
                        'M221 S100 ; reset extrusion rate to 100%\n'
                        '\n'
                        '; Set the heating\n'
                        'M190 S[bed_temperature_initial_layer_single] ; wait for bed to heat up\n'
                        "M104 S[nozzle_temperature_initial_layer] ; start nozzle heating but don't wait\n"
                        '\n'
                        '; Home\n'
                        'G1 Z3 F3000 ; move z up little to prevent scratching of surface\n'
                        'G28 ; home all axes\n'
                        'G1 X3 Y3 F5000 ; move to corner of the bed to avoid ooze over centre\n'
                        '\n'
                        '; Wait for final heating\n'
                        'M109 S[nozzle_temperature_initial_layer] ; wait for the nozzle to heat up\n'
                        'M190 S[bed_temperature_initial_layer_single] ; wait for the bed to heat up\n'
                        '\n'
                        ';Auto bed Leveling\n'
                        '@BEDLEVELVISUALIZER\n'
                        'G29 ; ABL T\n'
                        'M420 S1 Z3 ; reload and fade mesh bed leveling until it reach 3mm Z\n'
                        '\n'
                        '; Return to prime position, Prime line routine\n'
                        'G92 E0 ; Reset Extruder\n'
                        'G1 Z3 F3000 ; move z up little to prevent scratching of surface\n'
                        'G1 X10 Y.5 Z0.25 F5000.0 ; Move to start position\n'
                        'G1 X100 Y.5 Z0.25 F1500.0 E15 ; Draw the first line\n'
                        'G1 X100 Y.2 Z0.25 F5000.0 ; Move to side a little\n'
                        'G1 X10 Y.2 Z0.25 F1500.0 E30 ; Draw the second line\n'
                        'G92 E0 ; Reset Extruder\n'
                        'M221 S{if layer_height<0.075}100{else}95{endif}',
 'max_layer_height': ['0.32'],
 'min_layer_height': ['0.08'],
 'name': 'Artillery Sidewinder X2 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'brass',
 'printable_area': ['0x0', '300x0', '300x300', '0x300'],
 'printable_height': '400',
 'printer_model': 'Artillery Sidewinder X2',
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
