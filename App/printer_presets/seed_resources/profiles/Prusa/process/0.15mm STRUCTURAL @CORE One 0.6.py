from __future__ import annotations

# source: profiles/Prusa/process/0.15mm STRUCTURAL @CORE One 0.6.json
DATA = {'compatible_printers_condition': 'printer_notes=~/.*PRINTER_MODEL_COREONE[^_a-zA-Z0-9].*/ and nozzle_diameter[0]==0.6',
 'default_acceleration': '3000',
 'from': 'system',
 'gap_infill_speed': '70',
 'inherits': '0.15mm STRUCTURAL @MK4S 0.6',
 'initial_layer_infill_speed': '70',
 'initial_layer_speed': '45',
 'inner_wall_acceleration': '2500',
 'inner_wall_speed': '70',
 'instantiation': 'true',
 'internal_solid_infill_acceleration': '4000',
 'name': '0.15mm STRUCTURAL @CORE One 0.6',
 'outer_wall_acceleration': '1500',
 'overhang_3_4_speed': '30',
 'overhang_4_4_speed': '70%',
 'sparse_infill_acceleration': '6000',
 'support_interface_top_layers': '3',
 'top_surface_acceleration': '2000',
 'travel_acceleration': '7000',
 'travel_speed': '350',
 'type': 'process'}
