from __future__ import annotations

# source: profiles/BBL/filament/Generic PLA @0.2 nozzle.json
DATA = {'compatible_printers': ['Bambu Lab X1 Carbon 0.2 nozzle',
                         'Bambu Lab X1 0.2 nozzle',
                         'Bambu Lab P1S 0.2 nozzle',
                         'Bambu Lab X1E 0.2 nozzle'],
 'filament_end_gcode': ['; filament end gcode \n\n'],
 'filament_max_volumetric_speed': ['1.6'],
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
 'inherits': 'Generic PLA @base',
 'instantiation': 'true',
 'name': 'Generic PLA @0.2 nozzle',
 'setting_id': 'GFSL99_00',
 'type': 'filament'}
