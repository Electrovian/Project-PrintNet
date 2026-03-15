from __future__ import annotations

# source: profiles/Prusa/filament/Prusament PETG @XL.json
DATA = {'close_fan_the_first_x_layers': ['3'],
 'compatible_printers': ['Prusa XL 0.25 nozzle',
                         'Prusa XL 0.3 nozzle',
                         'Prusa XL 0.4 nozzle',
                         'Prusa XL 0.5 nozzle',
                         'Prusa XL 0.6 nozzle',
                         'Prusa XL 0.8 nozzle'],
 'fan_max_speed': ['50'],
 'fan_min_speed': ['30'],
 'filament_cooling_final_speed': '2.5',
 'filament_cooling_initial_speed': '5',
 'filament_cooling_moves': '3',
 'filament_flow_ratio': ['1'],
 'filament_load_time': '10.5',
 'filament_loading_speed': '10',
 'filament_loading_speed_start': '50',
 'filament_max_volumetric_speed': ['9.5'],
 'filament_retract_before_wipe': '20%',
 'filament_retract_lift_below': '1.5',
 'filament_start_gcode': ['; filament start gcode\n'
                          'M900 K{if nozzle_diameter[0]==0.4}0.07{elsif nozzle_diameter[0]==0.25}0.12{elsif '
                          'nozzle_diameter[0]==0.3}0.09{elsif nozzle_diameter[0]==0.35}0.08{elsif '
                          'nozzle_diameter[0]==0.6}0.04{elsif nozzle_diameter[0]==0.5}0.05{elsif '
                          'nozzle_diameter[0]==0.8}0.02{else}0{endif} ; Filament gcode\n'
                          '\n'
                          '{if printer_notes=~/.*PRINTER_MODEL_XLIS.*/}\n'
                          'M572 S{if nozzle_diameter[0]==0.4}0.053{elsif nozzle_diameter[0]==0.5}0.042{elsif '
                          'nozzle_diameter[0]==0.6}0.032{elsif nozzle_diameter[0]==0.8}0.018{elsif '
                          'nozzle_diameter[0]==0.25}0.18{elsif nozzle_diameter[0]==0.3}0.1{else}0{endif} ; Filament '
                          'gcode\n'
                          '{endif}\n'
                          '\n'
                          'M142 S36 ; set heatbreak target temp'],
 'filament_unload_time': '8.5',
 'filament_unloading_speed': '100',
 'filament_unloading_speed_start': '100',
 'filament_wipe': '1',
 'from': 'system',
 'full_fan_speed_layer': '5',
 'hot_plate_temp': '80',
 'hot_plate_temp_initial_layer': '80',
 'inherits': 'fdm_filament_pet',
 'instantiation': 'true',
 'name': 'Prusament PETG @XL',
 'nozzle_temperature': '250',
 'nozzle_temperature_intial_layer': '240',
 'overhang_fan_speed': ['50'],
 'setting_id': 'GFSA04',
 'slow_down_layer_time': ['9'],
 'slow_down_min_speed': '15',
 'type': 'filament'}
