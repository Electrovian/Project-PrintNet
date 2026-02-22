from __future__ import annotations

# source: profiles/Flashforge/machine/Flashforge Adventurer 5M 0.8 Nozzle.json
DATA = {'default_print_profile': '0.40mm Standard @Flashforge AD5M 0.8 Nozzle',
 'from': 'system',
 'inherits': 'fdm_adventurer5m_common',
 'instantiation': 'true',
 'machine_start_gcode': 'M190 S[bed_temperature_initial_layer_single]\n'
                        'M104 S[nozzle_temperature_initial_layer]\n'
                        'G90\n'
                        'M83\n'
                        'G1 Z5 F6000\n'
                        'G1 E-1.5 F600\n'
                        'G1 E12 F800\n'
                        'G1 X85 Y110 Z0.3 F1200\n'
                        'G1 X-110 E30 F2400\n'
                        'G1 Y0 E8 F2400\n'
                        'G1 X-109.6 F2400\n'
                        'G1 Y110 E10 F2400\n'
                        'G92 E0',
 'max_layer_height': ['0.56'],
 'min_layer_height': ['0.24'],
 'name': 'Flashforge Adventurer 5M 0.8 Nozzle',
 'nozzle_diameter': ['0.8'],
 'nozzle_type': 'hardened_steel',
 'printer_model': 'Flashforge Adventurer 5M',
 'printer_variant': '0.8',
 'retraction_length': ['1.5'],
 'setting_id': 'GM005',
 'type': 'machine',
 'z_hop': ['0']}
