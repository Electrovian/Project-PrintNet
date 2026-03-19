from __future__ import annotations

# source: profiles/Prusa/process/0.25mm SPEED @CORE One 0.5.json
DATA = {'compatible_printers_condition': 'printer_notes=~/.*PRINTER_MODEL_COREONE[^_a-zA-Z0-9].*/ and nozzle_diameter[0]==0.5 '
                                  'and printer_notes!~/.*HF_NOZZLE.*/',
 'default_acceleration': '3000',
 'from': 'system',
 'inherits': '0.25mm SPEED @MK4S 0.5',
 'initial_layer_infill_speed': '100',
 'initial_layer_speed': '45',
 'inner_wall_acceleration': '6000',
 'instantiation': 'true',
 'internal_solid_infill_acceleration': '6000',
 'name': '0.25mm SPEED @CORE One 0.5',
 'outer_wall_acceleration': '3000',
 'overhang_3_4_speed': '50',
 'sparse_infill_acceleration': '7000',
 'support_interface_top_layers': '3',
 'top_surface_acceleration': '2000',
 'travel_acceleration': '7000',
 'travel_speed': '350',
 'type': 'process'}
