from __future__ import annotations

# source: profiles/Creality/machine/Creality Hi 0.4 nozzle.json
DATA = {'auxiliary_fan': '0',
 'change_filament_gcode': 'G2 Z{z_after_toolchange + 0.4} I0.86 J0.86 P1 F10000 ; spiral lift a little from second '
                          'lift\n'
                          'G1 X260 Y180 F30000\n'
                          'G1 Z{z_after_toolchange} F600',
 'default_filament_profile': ['Creality Generic PLA @Hi-all'],
 'default_print_profile': '0.20mm Standard @Creality Hi',
 'deretraction_speed': ['40'],
 'enable_filament_ramming': '0',
 'extruder_clearance_height_to_lid': '301',
 'extruder_clearance_height_to_rod': '27',
 'extruder_clearance_radius': '55',
 'from': 'system',
 'gcode_flavor': 'klipper',
 'inherits': 'fdm_creality_common',
 'instantiation': 'true',
 'machine_end_gcode': 'END_PRINT',
 'machine_load_filament_time': '105',
 'machine_max_acceleration_e': ['5000', '5000'],
 'machine_max_acceleration_extruding': ['12000', '12000'],
 'machine_max_acceleration_retracting': ['5000', '5000'],
 'machine_max_acceleration_travel': ['12000', '12000'],
 'machine_max_acceleration_x': ['12000', '12000'],
 'machine_max_acceleration_y': ['12000', '12000'],
 'machine_max_acceleration_z': ['1000', '1000'],
 'machine_max_jerk_e': ['2.5', '2.5'],
 'machine_max_jerk_x': ['12', '12'],
 'machine_max_jerk_y': ['12', '12'],
 'machine_max_jerk_z': ['2', '2'],
 'machine_max_speed_e': ['50', '50'],
 'machine_max_speed_x': ['500', '500'],
 'machine_max_speed_y': ['500', '500'],
 'machine_max_speed_z': ['30', '30'],
 'machine_pause_gcode': 'PAUSE',
 'machine_start_gcode': 'M140 S0\n'
                        'M104 S0 \n'
                        'START_PRINT EXTRUDER_TEMP=[nozzle_temperature_initial_layer] '
                        'BED_TEMP=[bed_temperature_initial_layer_single]\n'
                        'T[initial_no_support_extruder]\n'
                        'M109 S[nozzle_temperature_initial_layer]\n'
                        'M204 S2000\n'
                        'G1 Z3 F600\n'
                        'M83\n'
                        'G1 Y150 F12000\n'
                        'G1 X0 F12000\n'
                        'G1 Z0.2 F600\n'
                        'G1 X0 Y150 F6000\n'
                        'G1 X0 Y0 E15 F6000\n'
                        'G1 X150 Y0 E15 F6000\n'
                        'G92 E0\n'
                        'G1 Z1 F600',
 'max_layer_height': ['0.32'],
 'min_layer_height': ['0.08'],
 'name': 'Creality Hi 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'hardened_steel',
 'nozzle_volume': '183',
 'printable_area': ['0x0', '260x0', '260x260', '0x260'],
 'printable_height': '300',
 'printer_model': 'Creality Hi',
 'printer_settings_id': 'Creality',
 'printer_structure': 'i3',
 'printer_variant': '0.4',
 'purge_in_prime_tower': '0',
 'retract_before_wipe': ['70%'],
 'retract_length_toolchange': ['0'],
 'retract_lift_below': ['299'],
 'retract_when_changing_layer': ['1'],
 'retraction_length': ['0.8'],
 'retraction_minimum_travel': ['0.5'],
 'retraction_speed': ['40'],
 'scan_first_layer': '0',
 'setting_id': 'GM001',
 'single_extruder_multi_material': '1',
 'support_air_filtration': '0',
 'support_multi_bed_types': '1',
 'thumbnails': ['96x96/PNG, 300x300/PNG'],
 'type': 'machine',
 'wipe_distance': ['2'],
 'z_hop': ['0.4'],
 'z_hop_types': ['Auto Lift']}
