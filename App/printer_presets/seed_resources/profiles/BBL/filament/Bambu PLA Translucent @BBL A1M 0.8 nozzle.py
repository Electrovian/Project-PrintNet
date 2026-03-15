from __future__ import annotations

# source: profiles/BBL/filament/Bambu PLA Translucent @BBL A1M 0.8 nozzle.json
DATA = {'compatible_printers': ['Bambu Lab A1 mini 0.6 nozzle', 'Bambu Lab A1 mini 0.8 nozzle'],
 'fan_cooling_layer_time': ['80'],
 'fan_max_speed': ['80'],
 'fan_min_speed': ['60'],
 'filament_retract_before_wipe': ['0'],
 'filament_start_gcode': ['; filament start gcode\n'
                          '{if  (bed_temperature[current_extruder] '
                          '>45)||(bed_temperature_initial_layer[current_extruder] >45)}M106 P3 S255\n'
                          '{elsif(bed_temperature[current_extruder] '
                          '>35)||(bed_temperature_initial_layer[current_extruder] >35)}M106 P3 S180\n'
                          '{endif};Prevent PLA from jamming\n'
                          '\n'
                          '\n'
                          '{if activate_air_filtration[current_extruder] && support_air_filtration}\n'
                          'M106 P3 S{during_print_exhaust_fan_speed_num[current_extruder]} \n'
                          '{endif}'],
 'from': 'system',
 'hot_plate_temp': ['60'],
 'hot_plate_temp_initial_layer': ['60'],
 'inherits': 'Bambu PLA Translucent @base',
 'instantiation': 'true',
 'name': 'Bambu PLA Translucent @BBL A1M 0.8 nozzle',
 'nozzle_temperature_range_low': ['200'],
 'setting_id': 'GFSA17_10',
 'textured_plate_temp': ['65'],
 'textured_plate_temp_initial_layer': ['65'],
 'type': 'filament'}
