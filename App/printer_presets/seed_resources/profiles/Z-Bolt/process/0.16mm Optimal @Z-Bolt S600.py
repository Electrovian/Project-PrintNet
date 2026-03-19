from __future__ import annotations

# source: profiles/Z-Bolt/process/0.16mm Optimal @Z-Bolt S600.json
DATA = {'compatible_printers': ['Z-Bolt S600 0.4 nozzle',
                         'Z-Bolt S600 Dual 0.4 nozzle',
                         'Z-Bolt S1000 0.4 nozzle',
                         'Z-Bolt S1000 Dual 0.4 nozzle'],
 'description': 'Compared with the default profile of a 0.4 mm nozzle, it has a smaller layer height, and results in '
                'less apparent layer lines and higher printing quality, but longer printing time.',
 'from': 'system',
 'inherits': 'fdm_process_zbolt_0.16',
 'instantiation': 'true',
 'name': '0.16mm Optimal @Z-Bolt S600',
 'overhang_totally_speed': '50',
 'setting_id': 'GP209',
 'smooth_coefficient': '150',
 'type': 'process'}
