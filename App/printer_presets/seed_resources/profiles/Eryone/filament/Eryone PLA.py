from __future__ import annotations

# source: profiles/Eryone/filament/Eryone PLA.json
DATA = {'compatible_printers': ['Thinker X400 0.4 nozzle'],
 'fan_min_speed': ['90'],
 'filament_end_gcode': ['; filament end gcode \nSET_FAN_SPEED FAN=filter_fan SPEED=0'],
 'filament_id': 'EFL90',
 'filament_max_volumetric_speed': ['20'],
 'filament_settings_id': ['Eryone PLA'],
 'filament_start_gcode': ['; filament start gcode\nSET_FAN_SPEED FAN=filter_fan SPEED=1'],
 'from': 'system',
 'hot_plate_temp': ['60'],
 'hot_plate_temp_initial_layer': ['60'],
 'inherits': 'Eryone Standard PLA',
 'instantiation': 'true',
 'name': 'Eryone PLA',
 'setting_id': 'EFSA00',
 'slow_down_layer_time': ['4'],
 'slow_down_min_speed': ['15'],
 'type': 'filament'}
