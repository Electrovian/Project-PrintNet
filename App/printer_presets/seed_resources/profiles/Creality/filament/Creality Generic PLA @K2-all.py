from __future__ import annotations

# source: profiles/Creality/filament/Creality Generic PLA @K2-all.json
DATA = {'compatible_printers': ['Creality K2 Plus 0.2 nozzle',
                         'Creality K2 Plus 0.4 nozzle',
                         'Creality K2 Plus 0.6 nozzle',
                         'Creality K2 Plus 0.8 nozzle',
                         'Creality K2 Pro 0.2 nozzle',
                         'Creality K2 Pro 0.4 nozzle',
                         'Creality K2 Pro 0.6 nozzle',
                         'Creality K2 Pro 0.8 nozzle'],
 'cool_plate_temp': ['50'],
 'cool_plate_temp_initial_layer': ['50'],
 'eng_plate_temp': ['50'],
 'eng_plate_temp_initial_layer': ['50'],
 'filament_flow_ratio': ['0.95'],
 'filament_max_volumetric_speed': ['18'],
 'filament_start_gcode': [';filament start gcode\n'
                          '{if (position[2] > first_layer_height) }\n'
                          'M104 S[nozzle_temperature]\n'
                          '{else} \n'
                          'M104 S[first_layer_temperature]\n'
                          '{endif}'],
 'from': 'system',
 'hot_plate_temp': ['50'],
 'hot_plate_temp_initial_layer': ['50'],
 'inherits': 'Creality Generic PLA',
 'instantiation': 'true',
 'name': 'Creality Generic PLA @K2-all',
 'reduce_fan_stop_start_freq': ['1'],
 'setting_id': 'GFSL99_00',
 'slow_down_layer_time': ['4'],
 'slow_down_min_speed': ['20'],
 'textured_plate_temp': ['50'],
 'textured_plate_temp_initial_layer': ['50'],
 'type': 'filament'}
