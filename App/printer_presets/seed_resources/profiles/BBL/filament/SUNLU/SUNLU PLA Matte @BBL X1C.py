from __future__ import annotations

# source: profiles/BBL/filament/SUNLU/SUNLU PLA Matte @BBL X1C.json
DATA = {'compatible_printers': ['Bambu Lab X1 Carbon 0.4 nozzle',
                         'Bambu Lab X1 Carbon 0.6 nozzle',
                         'Bambu Lab X1 Carbon 0.8 nozzle',
                         'Bambu Lab P1S 0.4 nozzle',
                         'Bambu Lab P1S 0.6 nozzle',
                         'Bambu Lab P1S 0.8 nozzle',
                         'Bambu Lab X1E 0.4 nozzle',
                         'Bambu Lab X1E 0.6 nozzle',
                         'Bambu Lab X1E 0.8 nozzle'],
 'filament_adaptive_volumetric_speed': ['0', '0'],
 'filament_deretraction_speed': ['nil', 'nil'],
 'filament_extruder_variant': ['Direct Drive Standard', 'Direct Drive High Flow'],
 'filament_flow_ratio': ['0.98', '0.98'],
 'filament_flush_temp': ['0', '0'],
 'filament_flush_volumetric_speed': ['0', '0'],
 'filament_long_retractions_when_cut': ['1', '1'],
 'filament_max_volumetric_speed': ['21', '21'],
 'filament_pre_cooling_temperature': ['0', '0'],
 'filament_ramming_travel_time': ['0', '0'],
 'filament_ramming_volumetric_speed': ['-1', '-1'],
 'filament_retract_before_wipe': ['nil', 'nil'],
 'filament_retract_restart_extra': ['nil', 'nil'],
 'filament_retract_when_changing_layer': ['nil', 'nil'],
 'filament_retraction_distances_when_cut': ['18', '18'],
 'filament_retraction_length': ['nil', 'nil'],
 'filament_retraction_minimum_travel': ['nil', 'nil'],
 'filament_retraction_speed': ['nil', 'nil'],
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
 'filament_wipe': ['nil', 'nil'],
 'filament_wipe_distance': ['nil', 'nil'],
 'filament_z_hop': ['nil', 'nil'],
 'filament_z_hop_types': ['nil', 'nil'],
 'from': 'system',
 'inherits': 'SUNLU PLA Matte @base',
 'instantiation': 'true',
 'long_retractions_when_ec': ['0', '0'],
 'name': 'SUNLU PLA Matte @BBL X1C',
 'nozzle_temperature': ['220', '220'],
 'nozzle_temperature_initial_layer': ['220', '220'],
 'retraction_distances_when_ec': ['0', '0'],
 'setting_id': 'GFSNLS02',
 'type': 'filament',
 'volumetric_speed_coefficients': ['0 0 0 0 0 0', '0 0 0 0 0 0']}
