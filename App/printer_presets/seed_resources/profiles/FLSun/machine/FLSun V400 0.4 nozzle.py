from __future__ import annotations

# source: profiles/FLSun/machine/FLSun V400 0.4 nozzle.json
DATA = {'auxiliary_fan': '0',
 'bed_exclude_area': ['0x0'],
 'default_print_profile': '0.20mm Standard @FLSun V400',
 'from': 'system',
 'gcode_flavor': 'klipper',
 'inherits': 'fdm_machine_common',
 'instantiation': 'true',
 'layer_change_gcode': '',
 'machine_end_gcode': 'M107 T0\n'
                      'M104 S0\n'
                      'M104 S0 T1\n'
                      'M140 S0\n'
                      'G92 E0\n'
                      'G91\n'
                      'G1 E-1 F300\n'
                      'G1 Z+0.5  F6000\n'
                      'G28 \n'
                      'G90 ;absolute positioning',
 'machine_pause_gcode': 'PAUSE',
 'machine_start_gcode': 'G21\n'
                        'G90\n'
                        'M82\n'
                        'M107 T0\n'
                        'M140 S[bed_temperature_initial_layer_single]\n'
                        'M104 S[nozzle_temperature_initial_layer] T0\n'
                        'M190 S[bed_temperature_initial_layer_single]\n'
                        'M109 S[nozzle_temperature_initial_layer] T0\n'
                        'G28\n'
                        'G1 F3000 Z1\n'
                        'G1 X-150 Y0 Z0.4\n'
                        'G92 E0\n'
                        'G3 X0 Y-130 I150 Z0.3 E30 F2000\n'
                        'G92 E0',
 'name': 'FLSun V400 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'hardened_steel',
 'printable_area': ['149.429x13.0734',
                    '147.721x26.0472',
                    '144.889x38.8229',
                    '140.954x51.303',
                    '135.946x63.3927',
                    '129.904x75',
                    '122.873x86.0365',
                    '114.907x96.4181',
                    '106.066x106.066',
                    '96.4181x114.907',
                    '86.0365x122.873',
                    '75x129.904',
                    '63.3927x135.946',
                    '51.303x140.954',
                    '38.8229x144.889',
                    '26.0472x147.721',
                    '13.0734x149.429',
                    '9.18485e-15x150',
                    '-13.0734x149.429',
                    '-26.0472x147.721',
                    '-38.8229x144.889',
                    '-51.303x140.954',
                    '-63.3927x135.946',
                    '-75x129.904',
                    '-86.0365x122.873',
                    '-96.4181x114.907',
                    '-106.066x106.066',
                    '-114.907x96.4181',
                    '-122.873x86.0365',
                    '-129.904x75',
                    '-135.946x63.3927',
                    '-140.954x51.303',
                    '-144.889x38.8229',
                    '-147.721x26.0472',
                    '-149.429x13.0734',
                    '-150x1.83697e-14',
                    '-149.429x-13.0734',
                    '-147.721x-26.0472',
                    '-144.889x-38.8229',
                    '-140.954x-51.303',
                    '-135.946x-63.3927',
                    '-129.904x-75',
                    '-122.873x-86.0365',
                    '-114.907x-96.4181',
                    '-106.066x-106.066',
                    '-96.4181x-114.907',
                    '-86.0365x-122.873',
                    '-75x-129.904',
                    '-63.3927x-135.946',
                    '-51.303x-140.954',
                    '-38.8229x-144.889',
                    '-26.0472x-147.721',
                    '-13.0734x-149.429',
                    '-2.75546e-14x-150',
                    '13.0734x-149.429',
                    '26.0472x-147.721',
                    '38.8229x-144.889',
                    '51.303x-140.954',
                    '63.3927x-135.946',
                    '75x-129.904',
                    '86.0365x-122.873',
                    '96.4181x-114.907',
                    '106.066x-106.066',
                    '114.907x-96.4181',
                    '122.873x-86.0365',
                    '129.904x-75',
                    '135.946x-63.3927',
                    '140.954x-51.303',
                    '144.889x-38.8229',
                    '147.721x-26.0472',
                    '149.429x-13.0734',
                    '150x-3.67394e-14'],
 'printable_height': '410',
 'printer_model': 'FLSun V400',
 'scan_first_layer': '0',
 'setting_id': 'GM003',
 'type': 'machine'}
