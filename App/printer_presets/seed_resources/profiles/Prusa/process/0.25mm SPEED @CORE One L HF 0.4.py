from __future__ import annotations

# source: profiles/Prusa/process/0.25mm SPEED @CORE One L HF 0.4.json
DATA = {'compatible_printers_condition': 'printer_notes=~/.*PRINTER_MODEL_COREONE_L[^_a-zA-Z0-9].*/ and '
                                  'nozzle_diameter[0]==0.4 and printer_notes=~/.*HF_NOZZLE.*/',
 'default_acceleration': '3000',
 'from': 'system',
 'inherits': '0.25mm SPEED @MK4S HF0.4',
 'initial_layer_infill_speed': '100',
 'initial_layer_speed': '45',
 'inner_wall_acceleration': '6000',
 'instantiation': 'true',
 'internal_solid_infill_acceleration': '6000',
 'name': '0.25mm SPEED @CORE One L HF 0.4',
 'outer_wall_acceleration': '3000',
 'overhang_2_4_speed': '50',
 'overhang_3_4_speed': '60%',
 'sparse_infill_acceleration': '7000',
 'sparse_infill_speed': '300',
 'support_interface_top_layers': '3',
 'top_surface_acceleration': '2000',
 'travel_acceleration': '6000',
 'travel_speed': '500',
 'type': 'process'}
