from __future__ import annotations

# source: profiles/Creality/filament/Creality Generic ABS @Hi-all.json
DATA = {'compatible_printers': ['Creality Hi 0.4 nozzle', 'Creality Hi 0.6 nozzle'],
 'filament_max_volumetric_speed': ['9'],
 'filament_start_gcode': ['; filament start gcode\n'
                          '{if (position[2] > first_layer_height) }\n'
                          'M104 S[nozzle_temperature]\n'
                          '{else}\n'
                          'M104 S[first_layer_temperature]\n'
                          '{endif}\n'],
 'from': 'system',
 'inherits': 'Creality Generic ABS',
 'instantiation': 'true',
 'name': 'Creality Generic ABS @Hi-all',
 'setting_id': 'GFSA04_CREALITY_00',
 'slow_down_layer_time': ['5'],
 'type': 'filament'}
