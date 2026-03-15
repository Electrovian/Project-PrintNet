from __future__ import annotations

# source: profiles/BBL/filament/Bambu PLA Marble @base.json
DATA = {'filament_cost': ['29.99'],
 'filament_density': ['1.22'],
 'filament_flow_ratio': ['0.98'],
 'filament_id': 'GFA07',
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
 'filament_vendor': ['Bambu Lab'],
 'from': 'system',
 'impact_strength_z': ['6.5'],
 'inherits': 'fdm_filament_pla',
 'instantiation': 'false',
 'name': 'Bambu PLA Marble @base',
 'type': 'filament'}
