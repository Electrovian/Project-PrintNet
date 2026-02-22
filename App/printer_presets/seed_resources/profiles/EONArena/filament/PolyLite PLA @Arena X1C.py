from __future__ import annotations

# source: profiles/EONArena/filament/PolyLite PLA @Arena X1C.json
DATA = {'compatible_printers': ['EON Arena X1 Carbon 0.4 nozzle',
                         'EON Arena X1 Carbon 0.6 nozzle',
                         'EON Arena X1 Carbon 0.8 nozzle'],
 'filament_max_volumetric_speed': ['15'],
 'filament_start_gcode': ['; filament start gcode\n'
                          '{if  (bed_temperature[current_extruder] '
                          '>45)||(bed_temperature_initial_layer[current_extruder] >45)}M106 P3 S255\n'
                          '{elsif(bed_temperature[current_extruder] '
                          '>35)||(bed_temperature_initial_layer[current_extruder] >35)}M106 P3 S180\n'
                          '{endif}'],
 'from': 'system',
 'inherits': 'PolyLite PLA @base',
 'instantiation': 'true',
 'name': 'PolyLite PLA @Arena X1C',
 'setting_id': 'GFSL19',
 'type': 'filament'}
