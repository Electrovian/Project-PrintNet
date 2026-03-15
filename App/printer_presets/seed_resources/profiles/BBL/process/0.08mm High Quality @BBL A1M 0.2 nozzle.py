from __future__ import annotations

# source: profiles/BBL/process/0.08mm High Quality @BBL A1M 0.2 nozzle.json
DATA = {'compatible_printers': ['Bambu Lab A1 mini 0.2 nozzle'],
 'default_acceleration': ['3000'],
 'description': 'Compared with the default profile of a 0.2 mm nozzle, it has a smaller layer lines, lower speeds and '
                'acceleration, and the sparse infill pattern is Gyroid. So, it results in almost invisible layer lines '
                'and much higher printing quality, but much longer printing time.',
 'from': 'system',
 'inherits': 'fdm_process_single_0.08_nozzle_0.2',
 'initial_layer_infill_speed': ['28'],
 'initial_layer_speed': ['16'],
 'instantiation': 'true',
 'name': '0.08mm High Quality @BBL A1M 0.2 nozzle',
 'outer_wall_acceleration': ['2000'],
 'outer_wall_speed': ['60'],
 'setting_id': 'GP120',
 'sparse_infill_pattern': 'gyroid',
 'travel_speed': ['700'],
 'type': 'process'}
