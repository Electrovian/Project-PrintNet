from __future__ import annotations

# source: profiles/Prusa/process/0.20mm STRUCTURAL @CORE One 0.4.json
DATA = {'compatible_printers_condition': 'printer_notes=~/.*PRINTER_MODEL_COREONE[^_a-zA-Z0-9].*/ and nozzle_diameter[0]==0.4',
 'default_acceleration': '3000',
 'from': 'system',
 'inherits': '0.20mm STRUCTURAL @MK4S 0.4',
 'initial_layer_infill_speed': '100',
 'initial_layer_speed': '45',
 'inner_wall_acceleration': '2500',
 'instantiation': 'true',
 'internal_solid_infill_acceleration': '4000',
 'name': '0.20mm STRUCTURAL @CORE One 0.4',
 'outer_wall_acceleration': '1500',
 'overhang_3_4_speed': '45',
 'sparse_infill_acceleration': '6000',
 'support_interface_top_layers': '3',
 'top_surface_acceleration': '2000',
 'travel_acceleration': '7000',
 'travel_speed': '350',
 'type': 'process'}
