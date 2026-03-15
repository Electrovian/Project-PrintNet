from __future__ import annotations

# source: profiles/BBL/process/0.30mm Strength @BBL A1 0.6 nozzle.json
DATA = {'compatible_printers': ['Bambu Lab A1 0.6 nozzle'],
 'default_acceleration': ['6000'],
 'description': 'Compared with the default profile of a 0.6 mm nozzle, it has more wall loops and a higher sparse '
                'infill density. So, it results in higher strength of the prints, but more filament consumption and '
                'longer printing time.',
 'elefant_foot_compensation': '0.075',
 'from': 'system',
 'inherits': 'fdm_process_single_0.30_nozzle_0.6',
 'instantiation': 'true',
 'name': '0.30mm Strength @BBL A1 0.6 nozzle',
 'setting_id': 'GP097',
 'skeleton_infill_density': '25%',
 'skin_infill_density': '25%',
 'sparse_infill_density': '25%',
 'travel_speed': ['700'],
 'type': 'process',
 'wall_loops': '4'}
