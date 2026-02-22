from __future__ import annotations

# source: profiles/Qidi/machine/Qidi X-CF Pro 0.4 nozzle.json
DATA = {'auxiliary_fan': '0',
 'change_filament_gcode': '',
 'default_filament_profile': ['Qidi Generic PLA'],
 'default_print_profile': '0.20mm Standard @Qidi XCFPro',
 'deretraction_speed': ['0'],
 'from': 'system',
 'inherits': 'fdm_qidi_common',
 'instantiation': 'true',
 'machine_end_gcode': 'M104 S0\nM140 S0\n;Retract the filament\nG92 E0\nG1 E-3 F300\nG28\nM84\n',
 'machine_max_acceleration_extruding': ['1500', '1250'],
 'machine_max_acceleration_retracting': ['1500', '1250'],
 'machine_max_acceleration_travel': ['1500', '1250'],
 'machine_max_acceleration_x': ['9000', '1000'],
 'machine_max_acceleration_y': ['9000', '1000'],
 'machine_max_acceleration_z': ['500', '200'],
 'machine_max_jerk_e': ['2.5', '2.5'],
 'machine_max_jerk_x': ['10', '10'],
 'machine_max_jerk_y': ['10', '10'],
 'machine_max_jerk_z': ['0.2', '0.4'],
 'machine_max_speed_e': ['120', '120'],
 'machine_max_speed_x': ['500', '200'],
 'machine_max_speed_y': ['500', '200'],
 'machine_max_speed_z': ['12', '12'],
 'machine_pause_gcode': 'M0',
 'machine_start_gcode': 'G28\n'
                        'M140 S[hot_plate_temp_initial_layer]\n'
                        'M190 S[hot_plate_temp_initial_layer]\n'
                        'M109 S[nozzle_temperature_initial_layer]\n'
                        'G92 E-19\n'
                        'G0 Y5 Z0.3 F3600\n'
                        'G1 X5 E0 F2400\n',
 'max_layer_height': ['0.32'],
 'min_layer_height': ['0.07'],
 'name': 'Qidi X-CF Pro 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'hardened_steel',
 'printable_area': ['0x0', '300x0', '300x250', '0x250'],
 'printable_height': '300',
 'printer_model': 'Qidi X-CF Pro',
 'printer_settings_id': 'Qidi',
 'retract_length_toolchange': ['2'],
 'retraction_length': ['2'],
 'retraction_minimum_travel': ['2'],
 'scan_first_layer': '0',
 'setting_id': 'GM001',
 'single_extruder_multi_material': '1',
 'type': 'machine'}
