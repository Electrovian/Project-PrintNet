from __future__ import annotations

# source: profiles/Elegoo/filament/ECC/Elegoo PLA+ @ECC.json
DATA = {'compatible_printers': ['Elegoo Centauri Carbon 0.4 nozzle',
                         'Elegoo Centauri Carbon 0.6 nozzle',
                         'Elegoo Centauri Carbon 0.8 nozzle'],
 'filament_max_volumetric_speed': ['20'],
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
 'inherits': 'Elegoo PLA @base',
 'instantiation': 'true',
 'name': 'Elegoo PLA+ @ECC',
 'pressure_advance': ['0.024'],
 'setting_id': 'EPLAPLUSECC',
 'slow_down_layer_time': ['6'],
 'type': 'filament'}
