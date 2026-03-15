from __future__ import annotations

# source: profiles/BBL/filament/Bambu PET-CF @base.json
DATA = {'cool_plate_temp': ['0'],
 'cool_plate_temp_initial_layer': ['0'],
 'description': "When printing this filament, there's a risk of nozzle clogging, oozing, warping and low layer "
                'adhesion strength. To get better results, please refer to this wiki: Printing Tips for High Temp / '
                'Engineering materials.',
 'eng_plate_temp': ['80'],
 'eng_plate_temp_initial_layer': ['80'],
 'fan_cooling_layer_time': ['5'],
 'fan_max_speed': ['30'],
 'fan_min_speed': ['10'],
 'filament_adhesiveness_category': ['800'],
 'filament_cost': ['84.99'],
 'filament_density': ['1.29'],
 'filament_id': 'GFT01',
 'filament_max_volumetric_speed': ['8'],
 'filament_start_gcode': ['; filament start gcode\n'
                          '{if (bed_temperature[current_extruder] '
                          '>80)||(bed_temperature_initial_layer[current_extruder] >80)}M106 P3 S255\n'
                          '{elsif (bed_temperature[current_extruder] '
                          '>60)||(bed_temperature_initial_layer[current_extruder] >60)}M106 P3 S180\n'
                          '{endif}\n'
                          '\n'
                          '{if activate_air_filtration[current_extruder] && support_air_filtration}\n'
                          'M106 P3 S{during_print_exhaust_fan_speed_num[current_extruder]} \n'
                          '{endif}'],
 'filament_type': ['PET-CF'],
 'filament_vendor': ['Bambu Lab'],
 'from': 'system',
 'hot_plate_temp': ['100'],
 'hot_plate_temp_initial_layer': ['100'],
 'impact_strength_z': ['4.5'],
 'inherits': 'fdm_filament_pet',
 'instantiation': 'false',
 'name': 'Bambu PET-CF @base',
 'nozzle_temperature': ['270'],
 'nozzle_temperature_initial_layer': ['270'],
 'nozzle_temperature_range_high': ['290'],
 'nozzle_temperature_range_low': ['260'],
 'overhang_fan_speed': ['40'],
 'overhang_fan_threshold': ['0%'],
 'required_nozzle_HRC': ['40'],
 'slow_down_layer_time': ['2'],
 'supertack_plate_temp': ['80'],
 'supertack_plate_temp_initial_layer': ['80'],
 'temperature_vitrification': ['185'],
 'textured_plate_temp': ['100'],
 'textured_plate_temp_initial_layer': ['100'],
 'type': 'filament'}
