from __future__ import annotations

# source: profiles/Tiertime/filament/Tiertime PLA-CF.json
DATA = {'additional_cooling_fan_speed': ['0'],
 'compatible_printers': ['Tiertime UP400 Pro 0.4 nozzle',
                         'Tiertime UP400 Pro 0.6 nozzle',
                         'Tiertime UP400 Pro 0.8 nozzle',
                         'Tiertime UP310 Pro 0.4 nozzle'],
 'cool_plate_temp': ['45'],
 'cool_plate_temp_initial_layer': ['45'],
 'filament_cost': ['34.99'],
 'filament_density': ['1.22'],
 'filament_flow_ratio': ['0.98'],
 'filament_id': 'GFA50',
 'filament_max_volumetric_speed': ['15'],
 'filament_start_gcode': ['; filament start gcode\n'
                          '{if  (bed_temperature[current_extruder] '
                          '>55)||(bed_temperature_initial_layer[current_extruder] >55)}M106 P3 S200\n'
                          '{elsif(bed_temperature[current_extruder] '
                          '>50)||(bed_temperature_initial_layer[current_extruder] >50)}M106 P3 S150\n'
                          '{elsif(bed_temperature[current_extruder] '
                          '>45)||(bed_temperature_initial_layer[current_extruder] >45)}M106 P3 S50\n'
                          '{endif}\n'
                          'M142 P1 R35 S40\n'
                          '{if activate_air_filtration[current_extruder] && support_air_filtration}\n'
                          'M106 P3 S{during_print_exhaust_fan_speed_num[current_extruder]} \n'
                          '{endif}'],
 'filament_type': ['PLA-CF'],
 'filament_vendor': ['Tiertime'],
 'from': 'system',
 'inherits': 'fdm_filament_pla',
 'instantiation': 'true',
 'name': 'Tiertime PLA-CF',
 'nozzle_temperature': ['230'],
 'nozzle_temperature_initial_layer': ['230'],
 'nozzle_temperature_range_high': ['250'],
 'nozzle_temperature_range_low': ['210'],
 'required_nozzle_HRC': ['40'],
 'slow_down_layer_time': ['8'],
 'type': 'filament'}
