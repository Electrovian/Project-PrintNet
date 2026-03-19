from __future__ import annotations

# source: profiles/Prusa/process/0.20mm SPEED @CORE One 0.3.json
DATA = {'compatible_printers_condition': 'printer_notes=~/.*PRINTER_MODEL_COREONE[^_a-zA-Z0-9].*/ and nozzle_diameter[0]==0.3',
 'default_acceleration': '3000',
 'from': 'system',
 'inherits': '0.20mm SPEED @MK4S 0.3',
 'initial_layer_infill_speed': '60',
 'initial_layer_speed': '45',
 'inner_wall_acceleration': '3000',
 'inner_wall_speed': '160',
 'instantiation': 'true',
 'name': '0.20mm SPEED @CORE One 0.3',
 'outer_wall_speed': '160',
 'small_perimeter_speed': '160',
 'sparse_infill_acceleration': '6000',
 'support_interface_top_layers': '3',
 'top_surface_acceleration': '1500',
 'travel_acceleration': '7000',
 'travel_speed': '350',
 'type': 'process'}
