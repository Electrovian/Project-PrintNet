from __future__ import annotations

# source: profiles/Z-Bolt/process/0.12mm High Quality @Z-Bolt S800.json
DATA = {'compatible_printers': ['Z-Bolt S800 Dual 0.4 nozzle'],
 'default_acceleration': '4000',
 'description': 'Compared with the default profile of a 0.4 mm nozzle, it has a smaller layer height, lower speeds and '
                'acceleration, and the sparse infill pattern is Gyroid. So, it results in almost negligible layer '
                'lines and much higher printing quality, but much longer printing time.',
 'from': 'system',
 'gap_infill_speed': '230',
 'inherits': 'fdm_process_zbolt_0.12',
 'inner_wall_speed': '150',
 'instantiation': 'true',
 'internal_solid_infill_speed': '180',
 'name': '0.12mm High Quality @Z-Bolt S800',
 'outer_wall_acceleration': '2000',
 'outer_wall_speed': '60',
 'overhang_totally_speed': '50',
 'setting_id': 'GP306',
 'smooth_coefficient': '150',
 'sparse_infill_pattern': 'gyroid',
 'sparse_infill_speed': '180',
 'top_surface_speed': '150',
 'type': 'process'}
