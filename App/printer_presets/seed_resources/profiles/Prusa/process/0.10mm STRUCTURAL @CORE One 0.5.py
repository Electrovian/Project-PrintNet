from __future__ import annotations

# source: profiles/Prusa/process/0.10mm STRUCTURAL @CORE One 0.5.json
DATA = {'compatible_printers_condition': 'printer_notes=~/.*PRINTER_MODEL_COREONE[^_a-zA-Z0-9].*/ and nozzle_diameter[0]==0.5',
 'default_acceleration': '3000',
 'from': 'system',
 'inherits': '0.10mm STRUCTURAL @MK4S 0.5',
 'initial_layer_infill_speed': '100',
 'initial_layer_speed': '45',
 'inner_wall_speed': '70',
 'instantiation': 'true',
 'name': '0.10mm STRUCTURAL @CORE One 0.5',
 'outer_wall_speed': '50',
 'small_perimeter_speed': '50',
 'support_interface_top_layers': '3',
 'travel_acceleration': '7000',
 'travel_speed': '350',
 'type': 'process'}
