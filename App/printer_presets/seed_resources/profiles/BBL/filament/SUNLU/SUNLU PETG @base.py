from __future__ import annotations

# source: profiles/BBL/filament/SUNLU/SUNLU PETG @base.json
DATA = {'cool_plate_temp': ['0'],
 'cool_plate_temp_initial_layer': ['0'],
 'description': 'To get better transparent or translucent results with the corresponding filament, please refer to '
                'this wiki: Printing tips for transparent PETG.',
 'eng_plate_temp': ['60'],
 'eng_plate_temp_initial_layer': ['60'],
 'fan_cooling_layer_time': ['30'],
 'fan_max_speed': ['30'],
 'fan_min_speed': ['10'],
 'filament_cost': ['22.99'],
 'filament_density': ['1.27'],
 'filament_flow_ratio': ['0.95'],
 'filament_id': 'GFSNL08',
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
 'filament_vendor': ['SUNLU'],
 'from': 'system',
 'hot_plate_temp': ['60'],
 'hot_plate_temp_initial_layer': ['60'],
 'inherits': 'fdm_filament_pet',
 'instantiation': 'false',
 'name': 'SUNLU PETG @base',
 'nozzle_temperature': ['245'],
 'nozzle_temperature_initial_layer': ['250'],
 'nozzle_temperature_range_high': ['280'],
 'nozzle_temperature_range_low': ['230'],
 'overhang_fan_speed': ['90'],
 'overhang_fan_threshold': ['10%'],
 'slow_down_layer_time': ['12'],
 'temperature_vitrification': ['68'],
 'textured_plate_temp': ['60'],
 'textured_plate_temp_initial_layer': ['60'],
 'type': 'filament'}
