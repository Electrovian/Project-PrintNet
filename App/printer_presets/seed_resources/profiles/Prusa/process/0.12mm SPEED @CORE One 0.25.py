from __future__ import annotations

# source: profiles/Prusa/process/0.12mm SPEED @CORE One 0.25.json
DATA = {'compatible_printers_condition': 'printer_notes=~/.*PRINTER_MODEL_COREONE[^_a-zA-Z0-9].*/ and '
                                  'nozzle_diameter[0]==0.25',
 'default_acceleration': '3000',
 'from': 'system',
 'inherits': '0.12mm SPEED @MK4S 0.25',
 'initial_layer_infill_speed': '45',
 'initial_layer_speed': '25',
 'inner_wall_speed': '150',
 'instantiation': 'true',
 'name': '0.12mm SPEED @CORE One 0.25',
 'outer_wall_speed': '150',
 'small_perimeter_speed': '150',
 'support_interface_top_layers': '3',
 'travel_acceleration': '4000',
 'travel_speed': '350',
 'type': 'process'}
