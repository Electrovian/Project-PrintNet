from __future__ import annotations

# source: profiles/Creality/filament/Creality Generic TPU @K2-all.json
DATA = {'compatible_printers': ['Creality K2 Plus 0.2 nozzle',
                         'Creality K2 Plus 0.4 nozzle',
                         'Creality K2 Plus 0.6 nozzle',
                         'Creality K2 Plus 0.8 nozzle',
                         'Creality K2 Pro 0.2 nozzle',
                         'Creality K2 Pro 0.4 nozzle',
                         'Creality K2 Pro 0.6 nozzle',
                         'Creality K2 Pro 0.8 nozzle'],
 'filament_max_volumetric_speed': ['3'],
 'filament_start_gcode': [';filament start gcode\n'
                          '{if (position[2] > first_layer_height) }\n'
                          'M104 S[nozzle_temperature]\n'
                          '{else} \n'
                          'M104 S[first_layer_temperature]\n'
                          '{endif}'],
 'from': 'system',
 'hot_plate_temp': ['40'],
 'hot_plate_temp_initial_layer': ['40'],
 'inherits': 'Creality Generic TPU',
 'instantiation': 'true',
 'name': 'Creality Generic TPU @K2-all',
 'nozzle_temperature': ['220'],
 'nozzle_temperature_initial_layer': ['220'],
 'reduce_fan_stop_start_freq': ['1'],
 'setting_id': 'GFU99_CREALITY_00',
 'slow_down_layer_time': ['8'],
 'textured_plate_temp': ['40'],
 'textured_plate_temp_initial_layer': ['40'],
 'type': 'filament'}
