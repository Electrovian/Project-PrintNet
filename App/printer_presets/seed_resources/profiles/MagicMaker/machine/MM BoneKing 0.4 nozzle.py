from __future__ import annotations

# source: profiles/MagicMaker/machine/MM BoneKing 0.4 nozzle.json
DATA = {'auxiliary_fan': '0',
 'change_filament_gcode': '',
 'cooling_tube_length': '20',
 'cooling_tube_retraction': '60',
 'default_filament_profile': ['MM Generic PLA'],
 'default_print_profile': '0.10mm Fine @MM BoneKing',
 'deretraction_speed': ['30'],
 'extruder_clearance_height_to_lid': '100',
 'extruder_clearance_height_to_rod': '32',
 'extruder_clearance_radius': '50',
 'from': 'system',
 'gcode_flavor': 'klipper',
 'inherits': 'fdm_machine_common',
 'instantiation': 'true',
 'machine_end_gcode': 'M104 S0 ;extruder heater off\n'
                      'M140 S0 ;heated bed heater off (if you have it)\n'
                      'G91 ;relative positioning\n'
                      'M83\n'
                      'G1 E-1 F1200  ;retract the filament a bit before lifting the nozzle, to release some of the '
                      'pressure\n'
                      'G1 Z+1 F300 \n'
                      'G90 ;absolute positioning\n'
                      'G1 X100 Y0 F6000\n'
                      'G1 E-4 F1200\n'
                      'M84 ;steppers off\n'
                      'M107 ; turn off fan\n'
                      'PRINT_END',
 'machine_max_acceleration_e': ['10000'],
 'machine_max_acceleration_extruding': ['10000', '1500'],
 'machine_max_acceleration_retracting': ['10000', '1500'],
 'machine_max_acceleration_travel': ['3000', '3000'],
 'machine_max_acceleration_x': ['100000', '3000'],
 'machine_max_acceleration_y': ['100000', '3000'],
 'machine_max_acceleration_z': ['500', '500'],
 'machine_max_jerk_e': ['2.5', '2.5'],
 'machine_max_jerk_x': ['9', '20'],
 'machine_max_jerk_y': ['9', '20'],
 'machine_max_jerk_z': ['0.5', '0.4'],
 'machine_max_speed_e': ['100', '120'],
 'machine_max_speed_x': ['1000', '500'],
 'machine_max_speed_y': ['1000', '500'],
 'machine_max_speed_z': ['12', '12'],
 'machine_pause_gcode': 'PAUSE',
 'machine_start_gcode': 'G0 Z3 F300\n'
                        'M190 S[bed_temperature_initial_layer_single]\n'
                        'M109 S[nozzle_temperature_initial_layer]\n'
                        'PRINT_START EXTRUDER=[nozzle_temperature_initial_layer] '
                        'BED=[bed_temperature_initial_layer_single]\n'
                        'G21 ;metric values\n'
                        'G90 ;absolute positioning\n'
                        'M82 ;set extruder to absolute mode\n'
                        'M107 ;start with the fan off\n'
                        'G28 ;Home\n'
                        'G0 Z5 F300\n'
                        'G1 X0 Y100 F6000\n'
                        'G92 E0\n'
                        'G0 Z0.5 F300\n'
                        'G1 F1000 Y0 E15\n'
                        'G1 F1000 X100 E25\n'
                        'G92 E0 ;zero the extruded length again\n'
                        'G1 F9000\n'
                        'M117 Printing...',
 'max_layer_height': ['0.3'],
 'min_layer_height': ['0.05'],
 'name': 'MM BoneKing 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'brass',
 'parking_pos_retraction': '22',
 'printable_area': ['0x0', '310x0', '310x306', '0x306'],
 'printable_height': '300',
 'printer_model': 'MM BoneKing',
 'printer_settings_id': 'MM',
 'retract_before_wipe': ['70%'],
 'retract_length_toolchange': ['5'],
 'retraction_length': ['1'],
 'retraction_minimum_travel': ['1'],
 'retraction_speed': ['30'],
 'scan_first_layer': '0',
 'setting_id': 'GM001',
 'single_extruder_multi_material': '1',
 'thumbnails': ['310x310'],
 'type': 'machine',
 'wipe_distance': ['1'],
 'z_hop': ['0.2'],
 'z_hop_types': ['Slope Lift']}
