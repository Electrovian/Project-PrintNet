from __future__ import annotations

# source: profiles/EONArena/filament/EONArena Generic PLA-CF @base.json
DATA = {'additional_cooling_fan_speed': ['0'],
 'cool_plate_temp': ['45'],
 'cool_plate_temp_initial_layer': ['45'],
 'filament_flow_ratio': ['0.95'],
 'filament_id': 'GFL98',
 'filament_max_volumetric_speed': ['12'],
 'filament_start_gcode': ['; filament start gcode\n'
                          '{if  (bed_temperature[current_extruder] '
                          '>45)||(bed_temperature_initial_layer[current_extruder] >45)}M106 P3 S255\n'
                          '{elsif(bed_temperature[current_extruder] '
                          '>35)||(bed_temperature_initial_layer[current_extruder] >35)}M106 P3 S180\n'
                          '{endif}'],
 'filament_type': ['PLA-CF'],
 'from': 'system',
 'inherits': 'fdm_filament_pla',
 'instantiation': 'false',
 'name': 'EONArena Generic PLA-CF @base',
 'nozzle_temperature_range_high': ['240'],
 'nozzle_temperature_range_low': ['190'],
 'required_nozzle_HRC': ['40'],
 'slow_down_layer_time': ['7'],
 'temperature_vitrification': ['55'],
 'type': 'filament'}
