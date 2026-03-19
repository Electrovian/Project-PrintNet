from __future__ import annotations

# source: profiles/Tiertime/filament/Tiertime Generic PE@300HS.json
DATA = {'compatible_printers': ['Tiertime UP300 HS 0.4 nozzle',
                         'Tiertime UP600 HS 0.4 nozzle',
                         'Tiertime UP600 HS 0.6 nozzle',
                         'Tiertime UP600 HS 0.8 nozzle'],
 'filament_cost': ['40.99'],
 'filament_density': ['0.95'],
 'filament_id': 'GFP99_01',
 'filament_max_volumetric_speed': ['8'],
 'filament_start_gcode': ['; filament start gcode\n'
                          '{if  (bed_temperature[current_extruder] '
                          '>55)||(bed_temperature_initial_layer[current_extruder] >55)}M106 P3 S200\n'
                          '{elsif(bed_temperature[current_extruder] '
                          '>50)||(bed_temperature_initial_layer[current_extruder] >50)}M106 P3 S150\n'
                          '{elsif(bed_temperature[current_extruder] '
                          '>45)||(bed_temperature_initial_layer[current_extruder] >45)}M106 P3 S50\n'
                          '{endif}\n'
                          '\n'
                          '{if activate_air_filtration[current_extruder] && support_air_filtration}\n'
                          'M106 P3 S{during_print_exhaust_fan_speed_num[current_extruder]} \n'
                          '{endif}'],
 'from': 'system',
 'inherits': 'fdm_filament_pe',
 'instantiation': 'true',
 'name': 'Tiertime Generic PE@300HS',
 'nozzle_temperature': ['210'],
 'nozzle_temperature_initial_layer': ['210'],
 'nozzle_temperature_range_high': ['220'],
 'nozzle_temperature_range_low': ['175'],
 'temperature_vitrification': ['70'],
 'type': 'filament'}
