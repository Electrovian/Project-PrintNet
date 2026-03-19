from __future__ import annotations

# source: profiles/EONArena/filament/EONArena Generic PLA Silk @base.json
DATA = {'filament_flow_ratio': ['0.98'],
 'filament_id': 'GFA05',
 'filament_max_volumetric_speed': ['12'],
 'filament_start_gcode': ['; filament start gcode\n'
                          '{if  (bed_temperature[current_extruder] '
                          '>45)||(bed_temperature_initial_layer[current_extruder] >45)}M106 P3 S255\n'
                          '{elsif(bed_temperature[current_extruder] '
                          '>35)||(bed_temperature_initial_layer[current_extruder] >35)}M106 P3 S180\n'
                          '{endif};Prevent PLA from jamming'],
 'from': 'system',
 'inherits': 'fdm_filament_pla',
 'instantiation': 'false',
 'name': 'EONArena Generic PLA Silk @base',
 'slow_down_layer_time': ['8'],
 'type': 'filament'}
