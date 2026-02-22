from __future__ import annotations

# source: profiles/BBL/filament/Generic PETG @base.json
DATA = {'cool_plate_temp': ['0'],
 'cool_plate_temp_initial_layer': ['0'],
 'eng_plate_temp': ['70'],
 'eng_plate_temp_initial_layer': ['70'],
 'fan_cooling_layer_time': ['30'],
 'fan_max_speed': ['90'],
 'fan_min_speed': ['40'],
 'filament_flow_ratio': ['0.95'],
 'filament_id': 'GFG99',
 'filament_max_volumetric_speed': ['12'],
 'filament_start_gcode': ['; filament start gcode\n'
                          '{if (bed_temperature[current_extruder] '
                          '>80)||(bed_temperature_initial_layer[current_extruder] >80)}M106 P3 S255\n'
                          '{elsif (bed_temperature[current_extruder] '
                          '>60)||(bed_temperature_initial_layer[current_extruder] >60)}M106 P3 S180\n'
                          '{endif}\n'
                          '\n'
                          '{if activate_air_filtration[current_extruder] && support_air_filtration}\n'
                          'M106 P3 S{during_print_exhaust_fan_speed_num[current_extruder]} \n'
                          '{endif}'],
 'from': 'system',
 'hot_plate_temp': ['70'],
 'hot_plate_temp_initial_layer': ['70'],
 'inherits': 'fdm_filament_pet',
 'instantiation': 'false',
 'name': 'Generic PETG @base',
 'nozzle_temperature_range_high': ['270'],
 'overhang_fan_speed': ['90'],
 'overhang_fan_threshold': ['10%'],
 'slow_down_layer_time': ['12'],
 'slow_down_min_speed': ['20'],
 'textured_plate_temp': ['70'],
 'textured_plate_temp_initial_layer': ['70'],
 'type': 'filament'}
