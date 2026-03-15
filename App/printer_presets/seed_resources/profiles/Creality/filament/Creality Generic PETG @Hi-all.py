from __future__ import annotations

# source: profiles/Creality/filament/Creality Generic PETG @Hi-all.json
DATA = {'compatible_printers': ['Creality Hi 0.4 nozzle', 'Creality Hi 0.6 nozzle'],
 'cool_plate_temp': ['70'],
 'cool_plate_temp_initial_layer': ['70'],
 'eng_plate_temp': ['70'],
 'eng_plate_temp_initial_layer': ['70'],
 'filament_max_volumetric_speed': ['9'],
 'filament_start_gcode': ['; filament start gcode\n'
                          '{if (position[2] > first_layer_height) }\n'
                          'M104 S[nozzle_temperature]\n'
                          '{else}\n'
                          'M104 S[first_layer_temperature]\n'
                          '{endif}\n'],
 'from': 'system',
 'hot_plate_temp': ['70'],
 'hot_plate_temp_initial_layer': ['70'],
 'inherits': 'Creality Generic PETG',
 'instantiation': 'true',
 'name': 'Creality Generic PETG @Hi-all',
 'nozzle_temperature': ['250'],
 'nozzle_temperature_initial_layer': ['250'],
 'setting_id': 'GFSG99_00',
 'slow_down_layer_time': ['5'],
 'textured_plate_temp': ['70'],
 'textured_plate_temp_initial_layer': ['70'],
 'type': 'filament'}
