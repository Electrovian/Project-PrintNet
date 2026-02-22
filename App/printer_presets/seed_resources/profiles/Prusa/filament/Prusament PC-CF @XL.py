from __future__ import annotations

# source: profiles/Prusa/filament/Prusament PC-CF @XL.json
DATA = {'close_fan_the_first_x_layers': ['4'],
 'compatible_printers': ['Prusa XL 0.25 nozzle',
                         'Prusa XL 0.3 nozzle',
                         'Prusa XL 0.4 nozzle',
                         'Prusa XL 0.5 nozzle',
                         'Prusa XL 0.6 nozzle',
                         'Prusa XL 0.8 nozzle'],
 'fan_max_speed': ['10'],
 'fan_min_speed': ['10'],
 'filament_cooling_final_speed': '50',
 'filament_cooling_initial_speed': '10',
 'filament_cooling_moves': '5',
 'filament_flow_ratio': ['1.04'],
 'filament_load_time': '15',
 'filament_loading_speed': '14',
 'filament_loading_speed_start': '19',
 'filament_max_volumetric_speed': ['8'],
 'filament_retract_lift_below': '1.5',
 'filament_start_gcode': ['; filament start gcode\n'
                          'M900 K{if nozzle_diameter[0]==0.4}0.07{elsif nozzle_diameter[0]==0.3}0.09{elsif '
                          'nozzle_diameter[0]==0.35}0.08{elsif nozzle_diameter[0]==0.6}0.04{elsif '
                          'nozzle_diameter[0]==0.5}0.05{elsif nozzle_diameter[0]==0.8}0.02{else}0{endif} ; Filament '
                          'gcode\n'
                          '\n'
                          '{if printer_notes=~/.*PRINTER_MODEL_XLIS.*/}\n'
                          'M572 S{if nozzle_diameter[0]==0.4}0.05{elsif nozzle_diameter[0]==0.5}0.035{elsif '
                          'nozzle_diameter[0]==0.6}0.025{elsif nozzle_diameter[0]==0.8}0.016{elsif '
                          'nozzle_diameter[0]==0.25}0.14{elsif nozzle_diameter[0]==0.3}0.09{else}0{endif} ; Filament '
                          'gcode\n'
                          '{endif}\n'
                          '\n'
                          'M142 S45 ; set heatbreak target temp'],
 'filament_unload_time': '12',
 'filament_unloading_speed': '20',
 'filament_unloading_speed_start': '100',
 'from': 'system',
 'hot_plate_temp': '105',
 'hot_plate_temp_initial_layer': '100',
 'inherits': 'fdm_filament_pccf',
 'instantiation': 'true',
 'name': 'Prusament PC-CF @XL',
 'nozzle_temperature': '285',
 'nozzle_temperature_intial_layer': '285',
 'overhang_fan_speed': ['30'],
 'setting_id': 'GFSA04',
 'slow_down_layer_time': ['20'],
 'slow_down_min_speed': ['15'],
 'type': 'filament'}
