from __future__ import annotations

# source: profiles/BBL/process/0.20mm Strength @BBL A1.json
DATA = {'compatible_printers': ['Bambu Lab A1 0.4 nozzle'],
 'default_acceleration': ['6000'],
 'description': 'Compared with the default profile of a 0.4 mm nozzle, it has more wall loops and a higher sparse '
                'infill density. So, it results in higher strength of the prints, but more filament consumption and '
                'longer printing time.',
 'elefant_foot_compensation': '0.075',
 'from': 'system',
 'inherits': 'fdm_process_single_0.20',
 'instantiation': 'true',
 'name': '0.20mm Strength @BBL A1',
 'outer_wall_speed': ['60'],
 'setting_id': 'GP080',
 'skeleton_infill_density': '25%',
 'skin_infill_density': '25%',
 'sparse_infill_density': '25%',
 'travel_speed': ['700'],
 'type': 'process',
 'wall_loops': '6'}
