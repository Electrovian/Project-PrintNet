from __future__ import annotations

# source: profiles/WEMAKE3D/process/fdm_process_tinyBotV1_common.json
DATA = {'default_acceleration': '3000',
 'filename_format': '{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode',
 'from': 'system',
 'inherits': 'fdm_process_common',
 'inner_wall_acceleration': '3500',
 'instantiation': 'false',
 'name': 'fdm_process_tinyBotV1_common',
 'outer_wall_acceleration': '3000',
 'print_sequence': 'by layer',
 'top_surface_acceleration': '3500',
 'travel_acceleration': '5000',
 'type': 'process'}
