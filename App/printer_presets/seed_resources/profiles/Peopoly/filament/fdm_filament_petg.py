from __future__ import annotations

# source: profiles/Peopoly/filament/fdm_filament_petg.json
DATA = {'eng_plate_temp': ['0'],
 'eng_plate_temp_initial_layer': ['0'],
 'fan_cooling_layer_time': ['20'],
 'fan_min_speed': ['20'],
 'filament_cost': ['30'],
 'filament_density': ['1.27'],
 'filament_max_volumetric_speed': ['18'],
 'filament_start_gcode': ['; filament start gcode\n'
                          '{if (bed_temperature[current_extruder] '
                          '>45)||(bed_temperature_initial_layer[current_extruder] >45)}M106 P3 S180\n'
                          '{elsif (bed_temperature[current_extruder] '
                          '>50)||(bed_temperature_initial_layer[current_extruder] >50)}M106 P3 S255\n'
                          '{endif};Prevent PLA from jamming\n'
                          '\n'
                          '{if activate_air_filtration[current_extruder] && support_air_filtration}\n'
                          'M106 P3 S{during_print_exhaust_fan_speed_num[current_extruder]} \n'
                          '{endif}'],
 'filament_type': ['PETG'],
 'from': 'system',
 'hot_plate_temp': ['70'],
 'hot_plate_temp_initial_layer': ['70'],
 'inherits': 'fdm_filament_common',
 'instantiation': 'false',
 'name': 'fdm_filament_petg',
 'nozzle_temperature': ['260'],
 'nozzle_temperature_initial_layer': ['270'],
 'nozzle_temperature_range_high': ['280'],
 'nozzle_temperature_range_low': ['220'],
 'reduce_fan_stop_start_freq': ['1'],
 'temperature_vitrification': ['70'],
 'textured_plate_temp': ['80'],
 'textured_plate_temp_initial_layer': ['80'],
 'type': 'filament'}
