from __future__ import annotations

# source: profiles/Prusa/process/0.55mm SPEED @CORE One L HF 0.8.json
DATA = {'compatible_printers_condition': 'printer_notes=~/.*PRINTER_MODEL_COREONE_L[^_a-zA-Z0-9].*/ and '
                                  'nozzle_diameter[0]==0.8 and printer_notes=~/.*HF_NOZZLE.*/',
 'default_acceleration': '3000',
 'from': 'system',
 'inherits': '0.55mm SPEED @MK4S HF0.8',
 'initial_layer_infill_speed': '55',
 'initial_layer_speed': '45',
 'instantiation': 'true',
 'internal_solid_infill_acceleration': '5000',
 'name': '0.55mm SPEED @CORE One L HF 0.8',
 'overhang_2_4_speed': '45',
 'sparse_infill_acceleration': '7000',
 'support_interface_top_layers': '3',
 'top_surface_speed': '2000',
 'travel_acceleration': '6000',
 'travel_speed': '500',
 'type': 'process'}
