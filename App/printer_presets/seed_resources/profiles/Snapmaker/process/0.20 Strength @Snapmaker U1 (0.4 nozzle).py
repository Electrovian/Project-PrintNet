from __future__ import annotations

# source: profiles/Snapmaker/process/0.20 Strength @Snapmaker U1 (0.4 nozzle).json
DATA = {'compatible_printers': ['Snapmaker U1 (0.4 nozzle)'],
 'description': 'Compared with the default profile of a 0.4 mm nozzle, it has more wall loops and a higher sparse '
                'infill density. So, it results in higher strength of the prints, but more filament consumption and '
                'longer printing time.',
 'from': 'system',
 'inherits': 'fdm_process_U1_0.20',
 'instantiation': 'true',
 'name': '0.20 Strength @Snapmaker U1 (0.4 nozzle)',
 'ooze_prevention': '1',
 'outer_wall_speed': '60',
 'overhang_totally_speed': '50',
 'setting_id': 'GP013',
 'slowdown_for_curled_perimeters': '0',
 'smooth_coefficient': '150',
 'sparse_infill_density': '25%',
 'standby_temperature_delta': '-150',
 'type': 'process',
 'wall_loops': '6',
 'wipe_tower_filament': '1'}
