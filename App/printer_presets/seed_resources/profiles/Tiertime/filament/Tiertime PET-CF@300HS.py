from __future__ import annotations

# source: profiles/Tiertime/filament/Tiertime PET-CF@300HS.json
DATA = {'compatible_printers': ['Tiertime UP300 HS 0.4 nozzle',
                         'Tiertime UP600 HS 0.4 nozzle',
                         'Tiertime UP600 HS 0.6 nozzle',
                         'Tiertime UP600 HS 0.8 nozzle'],
 'cool_plate_temp': ['0'],
 'cool_plate_temp_initial_layer': ['0'],
 'eng_plate_temp': ['80'],
 'eng_plate_temp_initial_layer': ['80'],
 'fan_cooling_layer_time': ['5'],
 'fan_max_speed': ['30'],
 'fan_min_speed': ['10'],
 'filament_cost': ['84.99'],
 'filament_density': ['1.29'],
 'filament_id': 'GFT01_01',
 'filament_max_volumetric_speed': ['8'],
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
 'filament_type': ['PET-CF'],
 'filament_vendor': ['Tiertime'],
 'from': 'system',
 'hot_plate_temp': ['100'],
 'hot_plate_temp_initial_layer': ['100'],
 'inherits': 'fdm_filament_pet',
 'instantiation': 'true',
 'name': 'Tiertime PET-CF@300HS',
 'nozzle_temperature': ['270'],
 'nozzle_temperature_initial_layer': ['270'],
 'nozzle_temperature_range_high': ['290'],
 'nozzle_temperature_range_low': ['260'],
 'overhang_fan_speed': ['40'],
 'overhang_fan_threshold': ['0%'],
 'reduce_fan_stop_start_freq': ['0'],
 'required_nozzle_HRC': ['40'],
 'slow_down_layer_time': ['2'],
 'slow_down_min_speed': ['20'],
 'temperature_vitrification': ['185'],
 'textured_plate_temp': ['100'],
 'textured_plate_temp_initial_layer': ['100'],
 'type': 'filament'}
