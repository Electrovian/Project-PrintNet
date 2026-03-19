from __future__ import annotations

# source: profiles/Prusa/process/0.20mm STRUCTURAL @CORE One L 0.3.json
DATA = {'compatible_printers_condition': 'printer_notes=~/.*PRINTER_MODEL_COREONE_L[^_a-zA-Z0-9].*/ and '
                                  'nozzle_diameter[0]==0.3',
 'default_acceleration': '3000',
 'from': 'system',
 'inherits': '0.20mm STRUCTURAL @MK4S 0.3',
 'initial_layer_infill_speed': '60',
 'initial_layer_speed': '45',
 'instantiation': 'true',
 'name': '0.20mm STRUCTURAL @CORE One L 0.3',
 'sparse_infill_acceleration': '6000',
 'support_interface_top_layers': '3',
 'top_surface_acceleration': '1500',
 'travel_acceleration': '6000',
 'travel_speed': '500',
 'type': 'process'}
