from __future__ import annotations

# source: profiles/Anycubic/machine/Anycubic Vyper 0.4 nozzle.json
DATA = {'auxiliary_fan': '0',
 'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\n;[layer_z]',
 'change_filament_gcode': 'M600',
 'default_filament_profile': ['Anycubic Generic PLA'],
 'default_print_profile': '0.20mm Standard @Anycubic Vyper',
 'deretraction_speed': ['40'],
 'from': 'system',
 'inherits': 'fdm_machine_common',
 'instantiation': 'true',
 'layer_change_gcode': ';AFTER_LAYER_CHANGE\n;[layer_z]',
 'machine_end_gcode': 'G4 ; wait\n'
                      'G92 E0\n'
                      'G1{if max_layer_z < printable_height} Z{z_offset+min(max_layer_z+30, printable_height)}{endif} '
                      '; move print head up\n'
                      'M104 S0 ; turn off temperature\n'
                      'M140 S0 ; turn off heatbed\n'
                      'M107 ; turn off fan\n'
                      'G1 X0 Y200 F3000 ; home X axis\n'
                      'M84 ; disable motors',
 'machine_max_acceleration_extruding': ['1250', '1250'],
 'machine_max_acceleration_retracting': ['1250', '1250'],
 'machine_max_acceleration_travel': ['1000', '1000'],
 'machine_max_acceleration_x': ['1000', '1000'],
 'machine_max_acceleration_y': ['1000', '1000'],
 'machine_max_acceleration_z': ['200', '200'],
 'machine_max_jerk_e': ['5', '5'],
 'machine_max_jerk_x': ['8', '8'],
 'machine_max_jerk_y': ['8', '8'],
 'machine_max_jerk_z': ['0.4', '0.4'],
 'machine_max_speed_e': ['60', '60'],
 'machine_max_speed_x': ['200', '200'],
 'machine_max_speed_y': ['200', '200'],
 'machine_max_speed_z': ['10', '10'],
 'machine_pause_gcode': 'M601',
 'machine_start_gcode': 'G21 ;metric values\n'
                        'G90 ;absolute positioning\n'
                        'M82 ;set extruder to absolute mode\n'
                        'M107 ;start with the fan off\n'
                        'G28 X0 Y0 ;move X/Y to min endstops\n'
                        'G28 Z0 ;move Z to min endstops\n'
                        'G0 Z0.2 F1800 ; move nozzle to print position\n'
                        'G92 E0 ; specify current extruder position as zero\n'
                        'G1 Y10 X180 E50 F1200 ; extrude a line in front of the printer\n'
                        'G92 E0 ; specify current extruder position as zero\n'
                        'G0 Z20 F6000 ; move head up\n'
                        'G1 E-7 F2400 ; retract\n'
                        'G04 S2 ; wait 2s\n'
                        'G0 X0 F6000 ; wipe from oozed filament\n'
                        'G1 E-1 F2400 ; undo some of the retraction to avoid oozing\n'
                        'G1 F6000 ; set travel speed to move to start printing point\n'
                        'M117',
 'max_layer_height': ['0.32'],
 'min_layer_height': ['0.08'],
 'name': 'Anycubic Vyper 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'undefine',
 'printable_area': ['0x0', '250x0', '250x255', '0x255'],
 'printable_height': '265',
 'printer_model': 'Anycubic Vyper',
 'printer_settings_id': 'Anycubic',
 'retract_before_wipe': ['0%'],
 'retract_length_toolchange': ['10'],
 'retraction_length': ['3'],
 'retraction_minimum_travel': ['1.5'],
 'retraction_speed': ['40'],
 'scan_first_layer': '0',
 'setting_id': 'GM001',
 'single_extruder_multi_material': '1',
 'type': 'machine'}
