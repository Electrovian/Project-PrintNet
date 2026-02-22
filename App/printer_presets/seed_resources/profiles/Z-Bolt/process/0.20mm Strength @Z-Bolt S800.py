from __future__ import annotations

# source: profiles/Z-Bolt/process/0.20mm Strength @Z-Bolt S800.json
DATA = {'compatible_printers': ['Z-Bolt S800 Dual 0.4 nozzle'],
 'description': 'Compared with the default profile of a 0.4 mm nozzle, it has more wall loops and a higher sparse '
                'infill density. So, it results in higher strength of the prints, but more filament consumption and '
                'longer printing time.',
 'from': 'system',
 'inherits': 'fdm_process_zbolt_0.20',
 'instantiation': 'true',
 'name': '0.20mm Strength @Z-Bolt S800',
 'outer_wall_speed': '60',
 'overhang_totally_speed': '50',
 'setting_id': 'GP312',
 'smooth_coefficient': '150',
 'sparse_infill_density': '25%',
 'type': 'process',
 'wall_loops': '6'}
