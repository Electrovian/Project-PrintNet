from __future__ import annotations

# source: profiles/Tiertime/filament/Tiertime Generic TPU.json
DATA = {'compatible_printers': ['Tiertime UP400 Pro 0.4 nozzle',
                         'Tiertime UP400 Pro 0.6 nozzle',
                         'Tiertime UP400 Pro 0.8 nozzle',
                         'Tiertime UP310 Pro 0.4 nozzle'],
 'filament_id': 'GFU99',
 'filament_max_volumetric_speed': ['3.2'],
 'filament_start_gcode': ['; filament start gcode\n'
                          '{if (bed_temperature[current_extruder] '
                          '>35)||(bed_temperature_initial_layer[current_extruder] >35)}M106 P3 S255\n'
                          '{elsif (bed_temperature[current_extruder] '
                          '>30)||(bed_temperature_initial_layer[current_extruder] >30)}M106 P3 S180\n'
                          '{endif} \n'
                          '\n'
                          '{if activate_air_filtration[current_extruder] && support_air_filtration}\n'
                          'M106 P3 S{during_print_exhaust_fan_speed_num[current_extruder]} \n'
                          '{endif}'],
 'from': 'system',
 'inherits': 'fdm_filament_tpu',
 'instantiation': 'true',
 'name': 'Tiertime Generic TPU',
 'setting_id': 'GFSR99',
 'type': 'filament'}
