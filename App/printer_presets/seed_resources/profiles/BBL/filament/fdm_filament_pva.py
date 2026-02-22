from __future__ import annotations

# source: profiles/BBL/filament/fdm_filament_pva.json
DATA = {'additional_cooling_fan_speed': ['70'],
 'close_fan_the_first_x_layers': ['1'],
 'cool_plate_temp': ['45'],
 'cool_plate_temp_initial_layer': ['45'],
 'eng_plate_temp': ['0'],
 'eng_plate_temp_initial_layer': ['0'],
 'fan_cooling_layer_time': ['100'],
 'fan_min_speed': ['100'],
 'filament_adhesiveness_category': ['704'],
 'filament_cost': ['20'],
 'filament_density': ['1.24'],
 'filament_end_gcode': ['; filament end gcode \n\n'],
 'filament_is_support': ['1'],
 'filament_max_volumetric_speed': ['15'],
 'filament_soluble': ['1'],
 'filament_start_gcode': ['; filament start gcode\n'
                          '{if  (bed_temperature[current_extruder] '
                          '>45)||(bed_temperature_initial_layer[current_extruder] >45)}M106 P3 S255\n'
                          '{elsif(bed_temperature[current_extruder] '
                          '>35)||(bed_temperature_initial_layer[current_extruder] >35)}M106 P3 S180\n'
                          '{endif}\n'
                          '\n'
                          '{if activate_air_filtration[current_extruder] && support_air_filtration}\n'
                          'M106 P3 S{during_print_exhaust_fan_speed_num[current_extruder]} \n'
                          '{endif}'],
 'filament_type': ['PVA'],
 'from': 'system',
 'hot_plate_temp': ['55'],
 'hot_plate_temp_initial_layer': ['55'],
 'inherits': 'fdm_filament_common',
 'instantiation': 'false',
 'name': 'fdm_filament_pva',
 'nozzle_temperature': ['220'],
 'nozzle_temperature_initial_layer': ['220'],
 'overhang_fan_threshold': ['50%'],
 'reduce_fan_stop_start_freq': ['1'],
 'slow_down_layer_time': ['4'],
 'slow_down_min_speed': ['50'],
 'supertack_plate_temp': ['35'],
 'supertack_plate_temp_initial_layer': ['35'],
 'temperature_vitrification': ['45'],
 'textured_plate_temp': ['55'],
 'textured_plate_temp_initial_layer': ['55'],
 'type': 'filament'}
