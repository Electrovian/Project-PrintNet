from __future__ import annotations

# source: profiles/Creality/filament/Creality Generic TPU @Hi-all.json
DATA = {'compatible_printers': ['Creality Hi 0.4 nozzle', 'Creality Hi 0.6 nozzle'],
 'filament_max_volumetric_speed': ['3.5'],
 'filament_start_gcode': ['; filament start gcode\n'
                          '{if (position[2] > first_layer_height) }\n'
                          'M104 S[nozzle_temperature]\n'
                          '{else}\n'
                          'M104 S[first_layer_temperature]\n'
                          '{endif}\n'],
 'from': 'system',
 'hot_plate_temp': ['30'],
 'hot_plate_temp_initial_layer': ['30'],
 'inherits': 'Creality Generic TPU',
 'instantiation': 'true',
 'name': 'Creality Generic TPU @Hi-all',
 'nozzle_temperature': ['230'],
 'nozzle_temperature_initial_layer': ['230'],
 'setting_id': 'GFU99_CREALITY_00',
 'slow_down_layer_time': ['5'],
 'textured_plate_temp': ['30'],
 'textured_plate_temp_initial_layer': ['30'],
 'type': 'filament'}
