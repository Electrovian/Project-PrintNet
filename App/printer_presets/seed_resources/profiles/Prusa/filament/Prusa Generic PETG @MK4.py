from __future__ import annotations

# source: profiles/Prusa/filament/Prusa Generic PETG @MK4.json
DATA = {'compatible_printers': ['Prusa MK4 0.25 nozzle',
                         'Prusa MK4 0.4 nozzle',
                         'Prusa MK4 0.6 nozzle',
                         'Prusa MK4 0.8 nozzle'],
 'fan_cooling_layer_time': ['30'],
 'fan_max_speed': ['90'],
 'fan_min_speed': ['40'],
 'filament_flow_ratio': ['0.95'],
 'filament_max_volumetric_speed': ['10'],
 'filament_ramming_parameters': ['250 100 42.4 42.4 42.4 42.4 42.4 | 0.05 42.4 0.45 42.4 0.95 42.4 1.45 42.4 1.95 42.4 '
                                 '2.45 42.4 2.95 42.4 3.45 42.4 3.95 42.4 4.45 42.4 4.95 42.4'],
 'filament_start_gcode': ['; filament start gcode\n'
                          'M900 K{if nozzle_diameter[0]==0.4}0.035{elsif nozzle_diameter[0]==0.25}0.12{elsif '
                          'nozzle_diameter[0]==0.3}0.09{elsif nozzle_diameter[0]==0.35}0.08{elsif '
                          'nozzle_diameter[0]==0.6}0.04{elsif nozzle_diameter[0]==0.5}0.05{elsif '
                          'nozzle_diameter[0]==0.8}0.02{else}0{endif} ; Filament gcode\n'
                          '\n'
                          '{if printer_notes=~/.*PRINTER_MODEL_MK4IS.*/}\n'
                          'M572 S{if nozzle_diameter[0]==0.4}0.055{elsif nozzle_diameter[0]==0.5}0.042{elsif '
                          'nozzle_diameter[0]==0.6}0.025{elsif nozzle_diameter[0]==0.8}0.018{elsif '
                          'nozzle_diameter[0]==0.25}0.18{elsif nozzle_diameter[0]==0.3}0.1{else}0{endif} ; Filament '
                          'gcode\n'
                          '{endif}\n'
                          '\n'
                          'M142 S36 ; set heatbreak target temp'],
 'from': 'system',
 'inherits': 'fdm_filament_pet',
 'instantiation': 'true',
 'name': 'Prusa Generic PETG @MK4',
 'overhang_fan_speed': ['90'],
 'overhang_fan_threshold': ['25%'],
 'reduce_fan_stop_start_freq': ['1'],
 'setting_id': 'GFSA04',
 'slow_down_for_layer_cooling': ['1'],
 'slow_down_layer_time': ['8'],
 'slow_down_min_speed': ['10'],
 'type': 'filament'}
