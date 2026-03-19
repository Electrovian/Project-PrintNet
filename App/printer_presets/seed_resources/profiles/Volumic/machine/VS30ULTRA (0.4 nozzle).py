from __future__ import annotations

# source: profiles/Volumic/machine/VS30ULTRA (0.4 nozzle).json
DATA = {'auxiliary_fan': '0',
 'before_layer_change_gcode': 'G92 E0',
 'default_print_profile': 'Normal speed - 0.15mm',
 'deretraction_speed': ['30'],
 'from': 'system',
 'gcode_flavor': 'marlin',
 'inherits': 'fdm_volumic_common',
 'instantiation': 'true',
 'machine_end_gcode': 'M107\nM104 S0\nM140 S0\nG0 X1 Y199 F5000\nM84\nM300',
 'machine_max_acceleration_x': ['2000'],
 'machine_max_acceleration_y': ['2000'],
 'machine_max_acceleration_z': ['50'],
 'machine_start_gcode': 'M117 Demarrage\n'
                        'M106 S0\n'
                        'M140 S[first_layer_bed_temperature]\n'
                        'M104 T0 S[first_layer_temperature]\n'
                        'G28\n'
                        'G90\n'
                        'M82\n'
                        'G92 E0\n'
                        'G1 Z5 F600\n'
                        'G1 X1 Y199 F6000\n'
                        'M109 T0 S[first_layer_temperature]\n'
                        'M300 P350\n'
                        'G92 E0\n'
                        'M117 Impression',
 'max_layer_height': ['0.3'],
 'min_layer_height': ['0.05'],
 'name': 'VS30ULTRA (0.4 nozzle)',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'undefine',
 'printable_area': ['0x0', '290x0', '290x200', '0x200'],
 'printable_height': '300',
 'printer_model': 'VS30ULTRA',
 'printer_variant': '0.4',
 'retraction_length': ['2.4'],
 'retraction_minimum_travel': ['1'],
 'retraction_speed': ['30'],
 'setting_id': 'GM001',
 'type': 'machine'}
