from __future__ import annotations

# source: profiles/Anycubic/machine/Anycubic 4Max Pro 0.4 nozzle.json
DATA = {'auxiliary_fan': '0',
 'bed_exclude_area': ['0x0'],
 'default_print_profile': '0.20mm Standard @Anycubic 4MaxPro',
 'from': 'system',
 'inherits': 'fdm_machine_common',
 'instantiation': 'true',
 'layer_change_gcode': '',
 'machine_end_gcode': 'PRINT_END',
 'machine_start_gcode': 'M190 S[bed_temperature_initial_layer_single]\n'
                        'M109 S[nozzle_temperature_initial_layer]\n'
                        'PRINT_START EXTRUDER=[nozzle_temperature_initial_layer] '
                        'BED=[bed_temperature_initial_layer_single]\n'
                        '; You can use following code instead if your PRINT_START macro support Chamber and print area '
                        'bedmesh\n'
                        '; PRINT_START EXTRUDER=[nozzle_temperature_initial_layer] '
                        'BED=[bed_temperature_initial_layer_single] Chamber=[chamber_temperature] '
                        'PRINT_MIN={first_layer_print_min[0]},{first_layer_print_min[1]} '
                        'PRINT_MAX={first_layer_print_max[0]},{first_layer_print_max[1]}',
 'name': 'Anycubic 4Max Pro 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'hardened_steel',
 'printable_area': ['0x0', '270x0', '270x205', '0x205'],
 'printable_height': '200',
 'printer_model': 'Anycubic 4Max Pro',
 'scan_first_layer': '0',
 'setting_id': 'GM003',
 'type': 'machine'}
