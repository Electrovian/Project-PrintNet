from __future__ import annotations

# source: profiles/Qidi/machine/Qidi X-Plus 0.4 nozzle.json
DATA = {'auxiliary_fan': '0',
 'change_filament_gcode': '',
 'default_filament_profile': ['Qidi Generic PLA'],
 'default_print_profile': '0.20mm Standard @Qidi XPlus',
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
                        'G92 E0\n'
                        'G0 X270 Y5 Z50 F3600\n'
                        'M190 S[bed_temperature_initial_layer_single]\n'
                        'M109 S[first_layer_temperature]\n'
                        'G92 E-16\n',
 'max_layer_height': ['0.32'],
 'min_layer_height': ['0.07'],
 'name': 'Qidi X-Plus 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'hardened_steel',
 'printable_area': ['0x0', '270x0', '270x200', '0x200'],
 'printable_height': '200',
 'printer_model': 'Qidi X-Plus',
 'printer_settings_id': 'Qidi',
 'retract_length_toolchange': ['2'],
 'retraction_length': ['2'],
 'retraction_minimum_travel': ['2'],
 'scan_first_layer': '0',
 'setting_id': 'GM001',
 'single_extruder_multi_material': '0',
 'type': 'machine'}
