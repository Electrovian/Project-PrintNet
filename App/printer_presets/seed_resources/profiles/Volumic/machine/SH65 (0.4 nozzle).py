from __future__ import annotations

# source: profiles/Volumic/machine/SH65 (0.4 nozzle).json
DATA = {'auxiliary_fan': '0',
 'before_layer_change_gcode': 'G92 E0',
 'default_print_profile': 'Normal speed - 0.15mm',
 'deretraction_speed': ['30'],
 'from': 'system',
 'gcode_flavor': 'marlin',
 'host_type': 'esp3d',
 'inherits': 'fdm_volumic_common',
 'instantiation': 'true',
 'machine_end_gcode': 'G90\n'
                      'G0 X1 Y419 F5000\n'
                      'G0 X1 Y419 F5000\n'
                      'M107\n'
                      'G91\n'
                      'T0\n'
                      'G1 E-1\n'
                      'M104 T0 S0\n'
                      'G92 E0\n'
                      'M140 S0\n'
                      'M84\n'
                      'M300',
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
                        'G1 X1 Y299 F6000\n'
                        'M109 T0 S[first_layer_temperature]\n'
                        'M300 P350\n'
                        'G92 E0\n'
                        'M117 Impression',
 'max_layer_height': ['0.3'],
 'min_layer_height': ['0.025'],
 'name': 'SH65 (0.4 nozzle)',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'undefine',
 'print_host': '192.168.0.60',
 'printable_area': ['0x0', '650x0', '650x300', '0x300'],
 'printable_height': '300',
 'printer_model': 'SH65',
 'printer_variant': '0.4',
 'retraction_length': ['2.4'],
 'retraction_minimum_travel': ['1'],
 'retraction_speed': ['30'],
 'setting_id': 'GM001',
 'type': 'machine'}
