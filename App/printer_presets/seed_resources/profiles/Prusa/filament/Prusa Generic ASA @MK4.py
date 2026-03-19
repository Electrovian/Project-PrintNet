from __future__ import annotations

# source: profiles/Prusa/filament/Prusa Generic ASA @MK4.json
DATA = {'compatible_printers': ['Prusa MK4 0.25 nozzle',
                         'Prusa MK4 0.4 nozzle',
                         'Prusa MK4 0.6 nozzle',
                         'Prusa MK4 0.8 nozzle'],
 'filament_flow_ratio': ['0.93'],
 'filament_max_volumetric_speed': ['12'],
 'filament_start_gcode': ['; Filament gcode\n'
                          'M900 K{if nozzle_diameter[0]==0.4}0.03{elsif nozzle_diameter[0]==0.25}0.1{elsif '
                          'nozzle_diameter[0]==0.3}0.06{elsif nozzle_diameter[0]==0.35}0.05{elsif '
                          'nozzle_diameter[0]==0.5}0.03{elsif nozzle_diameter[0]==0.6}0.02{elsif '
                          'nozzle_diameter[0]==0.8}0.01{else}0{endif} ; Filament gcode\n'
                          '\n'
                          '{if printer_notes=~/.*PRINTER_MODEL_MK4IS.*/}\n'
                          'M572 S{if nozzle_diameter[0]==0.4}0.02{elsif nozzle_diameter[0]==0.5}0.018{elsif '
                          'nozzle_diameter[0]==0.6}0.012{elsif nozzle_diameter[0]==0.8}0.01{elsif '
                          'nozzle_diameter[0]==0.25}0.09{elsif nozzle_diameter[0]==0.3}0.065{else}0{endif} ; Filament '
                          'gcode\n'
                          '{endif}\n'
                          '\n'
                          'M142 S40 ; set heatbreak target temp'],
 'from': 'system',
 'inherits': 'fdm_filament_asa',
 'instantiation': 'true',
 'name': 'Prusa Generic ASA @MK4',
 'setting_id': 'GFSA04',
 'type': 'filament'}
