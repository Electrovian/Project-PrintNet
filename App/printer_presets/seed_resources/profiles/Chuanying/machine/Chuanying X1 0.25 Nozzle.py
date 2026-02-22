from __future__ import annotations

# source: profiles/Chuanying/machine/Chuanying X1 0.25 Nozzle.json
DATA = {'default_print_profile': '0.12mm Standard @Chuanying X1 0.25 Nozzle',
 'from': 'system',
 'inherits': 'fdm_x1_common',
 'instantiation': 'true',
 'machine_start_gcode': 'M190 S[bed_temperature_initial_layer_single]\n'
                        'M104 S[nozzle_temperature_initial_layer]\n'
                        'G1 Z5 F6000\n'
                        'G90 E0\n'
                        'M83\n'
                        'G1 E-1 F600\n'
                        'G1 E8 F300\n'
                        'G1 X85 Y110 Z0.2 F1200\n'
                        'G1 X-110 E15 F2400\n'
                        'G1 Y0 E4 F2400\n'
                        'G1 X-109.6 F2400\n'
                        'G1 Y110 E5 F2400\n'
                        'G92 E0',
 'max_layer_height': ['0.14'],
 'min_layer_height': ['0.08'],
 'name': 'Chuanying X1 0.25 Nozzle',
 'nozzle_diameter': ['0.25'],
 'nozzle_type': 'stainless_steel',
 'printer_model': 'Chuanying X1',
 'printer_variant': '0.25',
 'retraction_length': ['1'],
 'setting_id': 'GM006',
 'type': 'machine',
 'z_hop': ['0.3']}
