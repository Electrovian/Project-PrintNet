from __future__ import annotations

# source: profiles/BBL/filament/Generic TPU @BBL A1.json
DATA = {'compatible_printers': ['Bambu Lab A1 0.4 nozzle', 'Bambu Lab A1 0.6 nozzle', 'Bambu Lab A1 0.8 nozzle'],
 'filament_start_gcode': ['; filament start gcode\n'
                          '{if (bed_temperature[current_extruder] '
                          '>35)||(bed_temperature_initial_layer[current_extruder] >35)}M106 P3 S255\n'
                          '{elsif (bed_temperature[current_extruder] '
                          '>30)||(bed_temperature_initial_layer[current_extruder] >30)}M106 P3 S180\n'
                          '{endif} \n'
                          '{if activate_air_filtration[current_extruder] && support_air_filtration}\n'
                          'M106 P3 S{during_print_exhaust_fan_speed_num[current_extruder]} \n'
                          '{endif}'],
 'from': 'system',
 'hot_plate_temp': ['45'],
 'hot_plate_temp_initial_layer': ['45'],
 'inherits': 'Generic TPU',
 'instantiation': 'true',
 'name': 'Generic TPU @BBL A1',
 'setting_id': 'GFSU99_01',
 'textured_plate_temp': ['45'],
 'textured_plate_temp_initial_layer': ['45'],
 'type': 'filament'}
