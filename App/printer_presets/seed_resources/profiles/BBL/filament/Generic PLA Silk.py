from __future__ import annotations

# source: profiles/BBL/filament/Generic PLA Silk.json
DATA = {'compatible_printers': ['Bambu Lab X1 Carbon 0.4 nozzle',
                         'Bambu Lab X1 0.4 nozzle',
                         'Bambu Lab X1 Carbon 0.6 nozzle',
                         'Bambu Lab X1 Carbon 0.8 nozzle',
                         'Bambu Lab X1 0.6 nozzle',
                         'Bambu Lab X1 0.8 nozzle',
                         'Bambu Lab P1S 0.4 nozzle',
                         'Bambu Lab P1S 0.6 nozzle',
                         'Bambu Lab P1S 0.8 nozzle',
                         'Bambu Lab X1E 0.4 nozzle',
                         'Bambu Lab X1E 0.6 nozzle',
                         'Bambu Lab X1E 0.8 nozzle'],
 'filament_end_gcode': ['; filament end gcode \n\n'],
 'filament_max_volumetric_speed': ['7.5'],
 'filament_retraction_length': ['0.5'],
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
 'inherits': 'Generic PLA Silk @base',
 'instantiation': 'true',
 'name': 'Generic PLA Silk',
 'setting_id': 'GFSL99_01',
 'type': 'filament'}
