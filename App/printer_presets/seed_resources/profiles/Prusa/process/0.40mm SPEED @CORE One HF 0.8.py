from __future__ import annotations

# source: profiles/Prusa/process/0.40mm SPEED @CORE One HF 0.8.json
DATA = {'compatible_printers_condition': 'printer_notes=~/.*PRINTER_MODEL_COREONE[^_a-zA-Z0-9].*/ and nozzle_diameter[0]==0.8 '
                                  'and printer_notes=~/.*HF_NOZZLE.*/',
 'default_acceleration': '3000',
 'from': 'system',
 'inherits': '0.40mm SPEED @MK4S HF0.8',
 'initial_layer_infill_speed': '55',
 'initial_layer_speed': '45',
 'instantiation': 'true',
 'internal_solid_infill_acceleration': '5000',
 'name': '0.40mm SPEED @CORE One HF 0.8',
 'outer_wall_speed': '85',
 'overhang_3_4_speed': '45',
 'small_perimeter_speed': '85',
 'sparse_infill_acceleration': '7000',
 'support_interface_top_layers': '3',
 'top_surface_acceleration': '2000',
 'travel_acceleration': '7000',
 'travel_speed': '350',
 'type': 'process'}
