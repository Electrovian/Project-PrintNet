from __future__ import annotations

# source: profiles/Creality/filament/Creality Generic ABS @K2-all.json
DATA = {'compatible_printers': ['Creality K2 Plus 0.2 nozzle',
                         'Creality K2 Plus 0.4 nozzle',
                         'Creality K2 Plus 0.6 nozzle',
                         'Creality K2 Plus 0.8 nozzle',
                         'Creality K2 Pro 0.2 nozzle',
                         'Creality K2 Pro 0.4 nozzle',
                         'Creality K2 Pro 0.6 nozzle',
                         'Creality K2 Pro 0.8 nozzle'],
 'filament_flow_ratio': ['0.95'],
 'filament_max_volumetric_speed': ['18'],
 'filament_start_gcode': [';filament start gcode\n'
                          '{if (position[2] > first_layer_height) }\n'
                          'M104 S[nozzle_temperature]\n'
                          '{else} \n'
                          'M104 S[first_layer_temperature]\n'
                          '{endif}'],
 'from': 'system',
 'inherits': 'Creality Generic ABS',
 'instantiation': 'true',
 'name': 'Creality Generic ABS @K2-all',
 'setting_id': 'GFSA04_CREALITY_00',
 'slow_down_layer_time': ['12'],
 'slow_down_min_speed': ['20'],
 'type': 'filament'}
