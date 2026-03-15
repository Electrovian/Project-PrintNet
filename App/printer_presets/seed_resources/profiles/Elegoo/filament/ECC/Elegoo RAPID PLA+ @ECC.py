from __future__ import annotations

# source: profiles/Elegoo/filament/ECC/Elegoo RAPID PLA+ @ECC.json
DATA = {'compatible_printers': ['Elegoo Centauri Carbon 0.4 nozzle',
                         'Elegoo Centauri Carbon 0.6 nozzle',
                         'Elegoo Centauri Carbon 0.8 nozzle'],
 'fan_cooling_layer_time': ['80'],
 'fan_max_speed': ['100'],
 'fan_min_speed': ['60'],
 'filament_max_volumetric_speed': ['21'],
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
 'hot_plate_temp': ['60'],
 'hot_plate_temp_initial_layer': ['60'],
 'inherits': 'Elegoo RAPID PLA+ @base',
 'instantiation': 'true',
 'name': 'Elegoo RAPID PLA+ @ECC',
 'pressure_advance': ['0.024'],
 'setting_id': 'ERPLAPLUSECC',
 'slow_down_layer_time': ['4'],
 'textured_plate_temp': ['60'],
 'textured_plate_temp_initial_layer': ['60'],
 'type': 'filament'}
