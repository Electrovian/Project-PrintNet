from __future__ import annotations

# source: profiles/Creality/filament/Creality Generic PA-CF @K2-all.json
DATA = {'compatible_printers': ['Creality K2 Plus 0.2 nozzle',
                         'Creality K2 Plus 0.4 nozzle',
                         'Creality K2 Plus 0.6 nozzle',
                         'Creality K2 Plus 0.8 nozzle',
                         'Creality K2 Pro 0.2 nozzle',
                         'Creality K2 Pro 0.4 nozzle',
                         'Creality K2 Pro 0.6 nozzle',
                         'Creality K2 Pro 0.8 nozzle'],
 'fan_min_speed': ['30'],
 'filament_start_gcode': [';filament start gcode\n'
                          '{if (position[2] > first_layer_height) }\n'
                          'M104 S[nozzle_temperature]\n'
                          '{else} \n'
                          'M104 S[first_layer_temperature]\n'
                          '{endif}'],
 'from': 'system',
 'inherits': 'Creality Generic PA-CF',
 'instantiation': 'true',
 'name': 'Creality Generic PA-CF @K2-all',
 'nozzle_temperature': ['280'],
 'nozzle_temperature_initial_layer': ['280'],
 'setting_id': 'GFSN99_01',
 'type': 'filament'}
