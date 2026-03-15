from __future__ import annotations

# source: profiles/Custom/machine/fdm_rrf_common.json
DATA = {'auxiliary_fan': '0',
 'bed_exclude_area': ['0x0'],
 'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n',
 'change_filament_gcode': '',
 'default_filament_profile': ['Generic PLA @System'],
 'default_print_profile': '0.20mm Standard @MyRRF',
 'deretraction_speed': ['30'],
 'extruder_clearance_height_to_lid': '140',
 'extruder_clearance_height_to_rod': '36',
 'extruder_clearance_radius': '65',
 'from': 'system',
 'gcode_flavor': 'reprapfirmware',
 'inherits': 'fdm_machine_common',
 'instantiation': 'false',
 'layer_change_gcode': ';AFTER_LAYER_CHANGE\n;[layer_z]',
 'machine_end_gcode': '{if max_layer_z < max_print_height}G1 Z{z_offset+min(max_layer_z+1, max_print_height)} F720 ; '
                      'Move print head up{endif}\n'
                      'G1 X0 Y200 F3600 ; park\n'
                      '{if max_layer_z < max_print_height}G1 Z{z_offset+min(max_layer_z+49, max_print_height)} F720 ; '
                      'Move print head further up{endif}\n'
                      'M221 S100 ; reset flow\n'
                      'M900 K0 ; reset LA\n'
                      'M104 S0 ; turn off temperature\n'
                      'M140 S0 ; turn off heatbed\n'
                      'M107 ; turn off fan\n'
                      'M84 ; disable motors',
 'machine_max_acceleration_e': ['5000', '5000'],
 'machine_max_acceleration_extruding': ['20000', '20000'],
 'machine_max_acceleration_retracting': ['5000', '5000'],
 'machine_max_acceleration_travel': ['20000', '20000'],
 'machine_max_acceleration_x': ['20000', '20000'],
 'machine_max_acceleration_y': ['20000', '20000'],
 'machine_max_acceleration_z': ['500', '200'],
 'machine_max_jerk_e': ['2.5', '2.5'],
 'machine_max_jerk_x': ['9', '9'],
 'machine_max_jerk_y': ['9', '9'],
 'machine_max_jerk_z': ['0.2', '0.4'],
 'machine_max_speed_e': ['25', '25'],
 'machine_max_speed_x': ['500', '200'],
 'machine_max_speed_y': ['500', '200'],
 'machine_max_speed_z': ['12', '12'],
 'machine_min_extruding_rate': ['0', '0'],
 'machine_min_travel_rate': ['0', '0'],
 'machine_pause_gcode': 'M601',
 'machine_start_gcode': '; Prime Filament Sensor for Runout\n'
                        'M581 P1 T2 S-1 R0\n'
                        'M950 J1 C"nil" ; Input 1 e0 Filament Sensor \n'
                        'M591 D0 P2 C"e0stop" S1 ; Filament Runout Sensor\n'
                        '\n'
                        'M83  ; extruder relative mode\n'
                        '\n'
                        'M140 S[first_layer_bed_temperature] ; set bed temp\n'
                        'M109 S140 ; Set extruder temp 140C before bed level\n'
                        'M190 S[first_layer_bed_temperature] ; wait for bed temp\n'
                        '\n'
                        ';G28 W\n'
                        'G32 ; Levels Z Tilt and probes Z=0\n'
                        'G29 S0 ; mesh bed leveling\n'
                        'G1 X0 Y0 Z2 F2000\n'
                        'M109 S[first_layer_temperature] ; wait for extruder temp\n'
                        '\n'
                        'G1 X10 Y-7 Z0.3 F1000.0 ; go outside print area\n'
                        'G92 E0.0\n'
                        'G1 Z0.2 E8 ; Purge Bubble\n'
                        'G1 X60.0 E9.0  F1000.0 ; intro line\n'
                        'G1 X100.0 E12.5  F1000.0 ; intro line\n'
                        'G92 E0.0',
 'max_layer_height': ['0.32'],
 'min_layer_height': ['0.08'],
 'name': 'fdm_rrf_common',
 'nozzle_type': 'undefine',
 'printable_height': '250',
 'printer_settings_id': '',
 'printer_technology': 'FFF',
 'printer_variant': '0.4',
 'retract_before_wipe': ['70%'],
 'retract_length_toolchange': ['2'],
 'retract_restart_extra': ['0'],
 'retract_restart_extra_toolchange': ['0'],
 'retract_when_changing_layer': ['1'],
 'retraction_length': ['0.8'],
 'retraction_minimum_travel': ['1'],
 'retraction_speed': ['30'],
 'scan_first_layer': '0',
 'silent_mode': '0',
 'single_extruder_multi_material': '1',
 'type': 'machine',
 'wipe': ['1'],
 'z_hop': ['0.4'],
 'z_hop_types': 'Normal Lift'}
