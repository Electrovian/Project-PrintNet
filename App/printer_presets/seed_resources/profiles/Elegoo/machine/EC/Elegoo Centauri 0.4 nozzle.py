from __future__ import annotations

# source: profiles/Elegoo/machine/EC/Elegoo Centauri 0.4 nozzle.json
DATA = {'auxiliary_fan': '1',
 'bed_exclude_area': ['246x0', '256x0', '256x20', '246x20'],
 'change_filament_gcode': 'M600',
 'default_bed_type': '4',
 'default_filament_profile': ['Elegoo PLA @EC'],
 'default_print_profile': '0.20mm Standard @Elegoo C 0.4 nozzle',
 'extruder_offset': ['0x0'],
 'fan_speedup_time': '0.5',
 'from': 'system',
 'gcode_flavor': 'klipper',
 'inherits': 'fdm_machine_ecc',
 'instantiation': 'true',
 'layer_change_gcode': 'SET_PRINT_STATS_INFO CURRENT_LAYER={layer_num + 1}',
 'machine_end_gcode': ';===== date: 20250109 =====================\n'
                      'M400 ; wait for buffer to clear\n'
                      'M140 S0 ;Turn-off bed\n'
                      'M106 S255 ;Cooling nozzle\n'
                      'M83\n'
                      'G92 E0 ; zero the extruder\n'
                      'G2 I1 J0 Z{max_layer_z+0.5} E-1 F3000 ; lower z a little\n'
                      'G90\n'
                      '{if max_layer_z > 50}G1 Z{min(max_layer_z+50, printable_height+0.5)} F20000{else}G1 Z100 F20000 '
                      '{endif}; Move print head up \n'
                      'M204 S5000\n'
                      'M400\n'
                      'M83\n'
                      'G1 X202 F20000\n'
                      'M400\n'
                      'G1 Y250 F20000\n'
                      'G1 Y264.5 F1200\n'
                      'M400\n'
                      'G92 E0\n'
                      'M104 S0 ;Turn-off hotend\n'
                      'M140 S0 ;Turn-off bed\n'
                      'M106 S0 ; turn off fan\n'
                      'M106 P2 S0 ; turn off remote part cooling fan\n'
                      'M106 P3 S0 ; turn off chamber cooling fan\n'
                      'M84 ;Disable all steppers',
 'machine_load_filament_time': '29',
 'machine_max_acceleration_travel': ['20000', '20000'],
 'machine_pause_gcode': 'M600',
 'machine_start_gcode': ';;===== date: 20240520 =====================\n'
                        ';printer_model:[printer_model]\n'
                        ';initial_filament:{filament_type[initial_extruder]}\n'
                        ';curr_bed_type:{curr_bed_type}\n'
                        'M400 ; wait for buffer to clear\n'
                        'M220 S100 ;Set the feed speed to 100%\n'
                        'M221 S100 ;Set the flow rate to 100%\n'
                        'M104 S140\n'
                        'M140 S[bed_temperature_initial_layer_single]\n'
                        'G90\n'
                        'G28 ;home\n'
                        'M729 ;Clean Nozzle\n'
                        'M106 P2 S255\n'
                        'M190 S[bed_temperature_initial_layer_single]\n'
                        'M106 P2 S0\n'
                        '\n'
                        '\n'
                        ';=============turn on fans to prevent PLA jamming=================\n'
                        '{if filament_type[initial_no_support_extruder]=="PLA"}\n'
                        '    {if (bed_temperature[initial_no_support_extruder] '
                        '>50)||(bed_temperature_initial_layer[initial_no_support_extruder] >50)}\n'
                        '    M106 P3 S255\n'
                        '    {elsif (bed_temperature[initial_no_support_extruder] '
                        '>45)||(bed_temperature_initial_layer[initial_no_support_extruder] >45)}\n'
                        '    M106 P3 S180\n'
                        '    {endif};Prevent PLA from jamming\n'
                        '{endif}\n'
                        '\n'
                        ';enable_pressure_advance:{enable_pressure_advance[initial_extruder]}\n'
                        ';This value is called if pressure advance is enabled\n'
                        '{if enable_pressure_advance[initial_extruder] == "true"}\n'
                        'SET_PRESSURE_ADVANCE ADVANCE=[pressure_advance] ;\n'
                        'M400\n'
                        '{endif}\n'
                        'M204 S{min(20000,max(1000,outer_wall_acceleration))} ;Call exterior wall print acceleration\n'
                        '\n'
                        '\n'
                        'G1 X{print_bed_max[0]*0.5} Y-1.2 F20000\n'
                        'G1 Z0.3 F900\n'
                        'M109 S[nozzle_temperature_initial_layer]\n'
                        'M83\n'
                        'G92 E0 ;Reset Extruder\n'
                        'G1 F{min(6000, max(900, '
                        'filament_max_volumetric_speed[initial_no_support_extruder]/0.5/0.3*60))} \n'
                        'G1 X-1.2 E10.156 ;Draw the first line\n'
                        'G1 Y98.8 E7.934\n'
                        'G1 X-0.5 Y100 E0.1\n'
                        'G1 Y-0.3 E7.934\n'
                        'G1 X{print_bed_max[0]*0.5-50} E6.284\n'
                        'G1 F{0.2*min(12000, max(1200, '
                        'filament_max_volumetric_speed[initial_no_support_extruder]/0.5/0.3*60))} \n'
                        'G1 X{print_bed_max[0]*0.5-30} E2\n'
                        'G1 F{min(12000, max(1200, '
                        'filament_max_volumetric_speed[initial_no_support_extruder]/0.5/0.3*60))} \n'
                        'G1 X{print_bed_max[0]*0.5-10} E2\n'
                        'G1 F{0.2*min(12000, max(1200, '
                        'filament_max_volumetric_speed[initial_no_support_extruder]/0.5/0.3*60))} \n'
                        'G1 X{print_bed_max[0]*0.5+10} E2\n'
                        'G1 F{min(12000, max(1200, '
                        'filament_max_volumetric_speed[initial_no_support_extruder]/0.5/0.3*60))} \n'
                        'G1 X{print_bed_max[0]*0.5+30} E2\n'
                        'G1 F{min(12000, max(1200, '
                        'filament_max_volumetric_speed[initial_no_support_extruder]/0.5/0.3*60))} \n'
                        'G1 X{print_bed_max[0]*0.5+50} E2\n'
                        ';End PA test.\n'
                        '\n'
                        '\n'
                        'G3 I-1 J0 Z0.6 F1200.0 ;Move to side a little\n'
                        'G1 F20000\n'
                        'G92 E0 ;Reset Extruder\n'
                        'SET_PRINT_STATS_INFO TOTAL_LAYER=[total_layer_count]\n'
                        ';LAYER_COUNT:[total_layer_count]\n'
                        ';LAYER:0',
 'machine_unload_filament_time': '28',
 'name': 'Elegoo Centauri 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'hardened_steel',
 'printable_area': ['0x0', '257x0', '257x257', '0x257'],
 'printable_height': '257',
 'printer_model': 'Elegoo Centauri',
 'printer_variant': '0.4',
 'retract_lift_below': ['255'],
 'scan_first_layer': '1',
 'setting_id': 'EC04',
 'thumbnails': ['144x144'],
 'type': 'machine',
 'upward_compatible_machine': []}
