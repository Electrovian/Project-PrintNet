from __future__ import annotations

# source: profiles/Artillery/machine/Artillery M1 Pro 0.4 nozzle.json
DATA = {'adaptive_bed_mesh_margin': '0',
 'auxiliary_fan': '1',
 'bbl_use_printhost': '0',
 'bed_custom_model': '',
 'bed_custom_texture': '',
 'bed_exclude_area': ['0x0'],
 'bed_mesh_max': '99999,99999',
 'bed_mesh_min': '-99999,-99999',
 'bed_mesh_probe_distance': '50,50',
 'before_layer_change_gcode': '\n',
 'best_object_pos': '0.5,0.5',
 'change_extrusion_role_gcode': '',
 'change_filament_gcode': '',
 'cooling_tube_length': '5',
 'cooling_tube_retraction': '91.5',
 'default_filament_profile': ['Artillery PLA Basic'],
 'default_print_profile': '0.20mm Standard @Artillery Genius',
 'deretraction_speed': ['40'],
 'disable_m73': '0',
 'emit_machine_limits_to_gcode': '1',
 'enable_filament_ramming': '1',
 'extra_loading_move': '-2',
 'extruder_clearance_height_to_lid': '140',
 'extruder_clearance_height_to_rod': '36',
 'extruder_clearance_radius': '65',
 'extruder_colour': ['#018001'],
 'extruder_offset': ['0x0'],
 'fan_kickstart': '0',
 'fan_speedup_overhangs': '1',
 'fan_speedup_time': '0',
 'from': 'system',
 'gcode_flavor': 'klipper',
 'head_wrap_detect_zone': [],
 'high_current_on_filament_swap': '0',
 'host_type': 'octoprint',
 'inherits': 'fdm_machine_common',
 'instantiation': 'true',
 'is_artillery': '1',
 'is_custom_defined': '0',
 'layer_change_gcode': 'G92 E0\n'
                       '{if layer_num==2}\n'
                       '\n'
                       ';filter_fan\n'
                       'M106 P3 S{during_print_exhaust_fan_speed[0]*255/100.0};\n'
                       '\n'
                       ';auxiliary_fan\n'
                       'M106 P2 S{additional_cooling_fan_speed[0]*255/100.0}\n'
                       '\n'
                       '{endif}\n'
                       '\n',
 'machine_end_gcode': ';===== G-CODE START =====================\n'
                      ';===== machine: M1 PRO =========================\n'
                      ';===== date: 20250729 =====================\n'
                      '\n'
                      ';===== Raise Z-Axis =====================\n'
                      'M400 ; wait for buffer to clear\n'
                      'G90\n'
                      'G92 E0 ; zero the extruder\n'
                      'G1 E-3 F1800 ; retract\n'
                      '\n'
                      '{if max_layer_z < printable_height}G1 Z{z_offset+min(max_layer_z+2, printable_height)} F300 ; '
                      'Move print head up{endif} \n'
                      'G90\n'
                      'G1 X200 Y260 F21000\n'
                      'G1 X200 Y275 F6000\n'
                      'G1 X160 Y275 F6000\n'
                      'G1 X137 Y275 F3000\n'
                      'M400\n'
                      'TIMELAPSE_TAKE_FRAME\n'
                      '{if max_layer_z < 50}G1 Z50 F300 ; Move print head further up{endif}\n'
                      ';===== Default Settings =====================\n'
                      'M400\n'
                      'M106 S255\n'
                      'M141 S0\n'
                      'M106 P1 S255\n'
                      'M104 S160\n'
                      'G4 P10000\n'
                      'M109 S160\n'
                      'M106 S0  ;turn off cool fan\n'
                      'M141 S0  ;turn off PTC\n'
                      'M106 P2 S0  ;turn off chamber fan\n'
                      'M106 P1 S0  ;turn off PTC fan\n'
                      'M106 P3 S0  ;turn off filter fan\n'
                      'M220 S100 ;Reset Feedrate\n'
                      'M221 S100 ;Reset Flowrate\n'
                      'SET_VELOCITY_LIMIT VELOCITY=500;\n'
                      'SET_VELOCITY_LIMIT ACCEL=6000;\n'
                      'SET_VELOCITY_LIMIT MINIMUM_CRUISE_RATIO=0.2;\n'
                      'SET_VELOCITY_LIMIT SQUARE_CORNER_VELOCITY=5;\n'
                      'G21; set units to millimeters\n'
                      'M104 S0\n'
                      'M140 S0\n'
                      'M400\n'
                      'M84 X Y Z E ; disable motors\n'
                      'M400\n'
                      ';===== G-CODE END =====================',
 'machine_load_filament_time': '0',
 'machine_max_acceleration_e': ['5000', '5000'],
 'machine_max_acceleration_extruding': ['20000', '1250'],
 'machine_max_acceleration_retracting': ['5000', '1250'],
 'machine_max_acceleration_travel': ['1000', '1250'],
 'machine_max_acceleration_x': ['20000', '1000'],
 'machine_max_acceleration_y': ['20000', '1000'],
 'machine_max_acceleration_z': ['500', '200'],
 'machine_max_jerk_e': ['2.5', '2.5'],
 'machine_max_jerk_x': ['9', '10'],
 'machine_max_jerk_y': ['9', '10'],
 'machine_max_jerk_z': ['3', '0.4'],
 'machine_max_speed_e': ['50', '120'],
 'machine_max_speed_x': ['700', '200'],
 'machine_max_speed_y': ['700', '200'],
 'machine_max_speed_z': ['20', '12'],
 'machine_min_extruding_rate': ['0', '0'],
 'machine_min_travel_rate': ['0', '0'],
 'machine_pause_gcode': 'M600',
 'machine_start_gcode': ';===== START G-CODE  =====================\n'
                        ';===== machine: M1 PRO =========================\n'
                        ';===== size: X260 Y260 Z260 =====================\n'
                        ';===== date: 20250708 =====================\n'
                        ';===== Filament Temperature Configuration =====================\n'
                        ';Nozzle_Preheat_Temp:140\n'
                        ';Bed_Preheat_Temp:[bed_temperature_initial_layer_single]\n'
                        '{if (nozzle_temperature_initial_layer[0] '
                        '>250)};Filament_Common_Extrusion_Temp:[nozzle_temperature_initial_layer]{else};Filament_Common_Extrusion_Temp:250{endif}\n'
                        ';Nozzle_Init_Layer_Temp:[nozzle_temperature_initial_layer]\n'
                        ';Filament_Softening_Temp:[nozzle_temperature_range_low]\n'
                        '\n'
                        ';===== Default Settings =====================\n'
                        'M106 S0  ;turn off cool fan\n'
                        'M141 S0  ;turn off PTC\n'
                        'M106 P2 S0  ;turn off chamber fan\n'
                        'M106 P1 S0  ;turn off PTC fan\n'
                        'M106 P3 S0  ;turn off filter fan\n'
                        'M220 S100 ;Reset Feedrate\n'
                        'M221 S100 ;Reset Flowrate\n'
                        'SET_VELOCITY_LIMIT VELOCITY=500;\n'
                        'SET_VELOCITY_LIMIT ACCEL=6000;\n'
                        'SET_VELOCITY_LIMIT MINIMUM_CRUISE_RATIO=0.2;\n'
                        'SET_VELOCITY_LIMIT SQUARE_CORNER_VELOCITY=5;\n'
                        'G21; set units to millimeters\n'
                        'G90\n'
                        '\n'
                        ';===== Preheat While Zeroing =====================\n'
                        'M106 P1 S153\n'
                        '\n'
                        'M140 S[bed_temperature_initial_layer_single];\n'
                        '\n'
                        '{if filament_type[initial_no_support_extruder]=="ABS"}\n'
                        'M106 P1 S255\n'
                        'M106 P2 S60\n'
                        'G4 P5000\n'
                        'M191 S47;\n'
                        'M141 S{chamber_temperature[0]};\n'
                        '{endif}\n'
                        '\n'
                        '{if filament_type[initial_no_support_extruder]=="PC"}\n'
                        'M106 P1 S255\n'
                        'M106 P2 S60\n'
                        'G4 P5000\n'
                        'M191 S47;\n'
                        'M141 S{chamber_temperature[0]};\n'
                        '{endif}\n'
                        '\n'
                        '{if filament_type[initial_no_support_extruder]=="ASA"}\n'
                        'M106 P1 S255\n'
                        'M106 P2 S60\n'
                        'G4 P5000\n'
                        'M191 S47;\n'
                        'M141 S{chamber_temperature[0]};\n'
                        '{endif}\n'
                        '\n'
                        '{if filament_type[initial_no_support_extruder]=="PA"}\n'
                        'M106 P1 S255\n'
                        'M106 P2 S60\n'
                        'G4 P5000\n'
                        'M191 S47;\n'
                        'M141 S{chamber_temperature[0]};\n'
                        '{endif}\n'
                        '\n'
                        '{if filament_type[initial_no_support_extruder]=="PA-CF"}\n'
                        'M106 P1 S255\n'
                        'M106 P2 S60\n'
                        'G4 P5000\n'
                        'M191 S47;\n'
                        'M141 S{chamber_temperature[0]};\n'
                        '{endif}\n'
                        '\n'
                        'M106 P2 S0\n'
                        'M106 S0;\n'
                        'G4 P500\n'
                        '\n'
                        ';===== Wait heating =====================\n'
                        'G28\n'
                        'G1 X20 Y2 Z0  F18000\n'
                        '\n'
                        ';===== Set Print Temperature =====================\n'
                        'M106 S120;\n'
                        'G4 P500\n'
                        'M104 S[first_layer_temperature];\n'
                        '\n'
                        '{if (bed_temperature_initial_layer_single >0)}\n'
                        'M190 S[bed_temperature_initial_layer_single];\n'
                        '{else}\n'
                        'M140 S[bed_temperature_initial_layer_single];\n'
                        '{endif}\n'
                        '\n'
                        'M109 S[first_layer_temperature];\n'
                        'M106 S0;\n'
                        'G4 P500\n'
                        '\n'
                        ';===== Wipe Nozzle Extrude Line =====================\n'
                        'G1 X20 Y2 Z0  F18000\n'
                        'M400\n'
                        '\n'
                        'G92 E0\n'
                        'G0  E4;\n'
                        'M400\n'
                        '\n'
                        'G92 E0\n'
                        'G1 X240 Y2 Z0.2 F1800.0 E11.0;\n'
                        '\n'
                        'G92 E0\n'
                        'G1 X240 Y10 Z0.2 F1800.0 E1;\n'
                        '\n'
                        'G92 E0\n'
                        'G1 X239.5\n'
                        'G0 E0.2\n'
                        '\n'
                        'G92 E0\n'
                        'G0 Y2.5 E0.125\n'
                        '\n'
                        'G92 E0\n'
                        'G1 X20 F1800.0 E11;\n'
                        '\n'
                        'M400\n'
                        'G92 E0\n'
                        'G1 Z0.6 F600\n'
                        'M400\n'
                        '\n'
                        'G1 X{first_layer_print_min[0]} Y{first_layer_print_min[1]} F9000\n'
                        'M400\n'
                        '\n'
                        ';===== END G-CODE  =====================\n'
                        '\n'
                        '\n',
 'machine_unload_filament_time': '0',
 'manual_filament_change': '0',
 'max_layer_height': ['0.32'],
 'min_layer_height': ['0.08'],
 'name': 'Artillery M1 Pro 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_hrc': '0',
 'nozzle_type': 'hardened_steel',
 'nozzle_volume': '0',
 'parking_pos_retraction': '92',
 'preferred_orientation': '0',
 'print_host': '192.168.3.29',
 'print_host_webui': '',
 'printable_area': ['0x0', '260x0', '260x260', '0x260'],
 'printable_height': '260',
 'printer_model': 'Artillery M1 Pro',
 'printer_notes': '',
 'printer_settings_id': 'Artillery M1 Pro 0.4 nozzle',
 'printer_structure': 'undefine',
 'printer_technology': 'FFF',
 'printer_variant': '0.4',
 'printhost_apikey': '',
 'printhost_authorization_type': 'key',
 'printhost_cafile': '',
 'printhost_password': '',
 'printhost_port': '',
 'printhost_ssl_ignore_revoke': '0',
 'printhost_user': '',
 'printing_by_object_gcode': '',
 'purge_in_prime_tower': '1',
 'retract_before_wipe': ['70%'],
 'retract_length_toolchange': ['10'],
 'retract_lift_above': ['0'],
 'retract_lift_below': ['0'],
 'retract_lift_enforce': ['All Surfaces'],
 'retract_restart_extra': ['0'],
 'retract_restart_extra_toolchange': ['0'],
 'retract_when_changing_layer': ['1'],
 'retraction_length': ['1.3'],
 'retraction_minimum_travel': ['1'],
 'retraction_speed': ['40'],
 'scan_first_layer': '0',
 'setting_id': 'GM007',
 'silent_mode': '0',
 'single_extruder_multi_material': '1',
 'support_air_filtration': '1',
 'support_chamber_temp_control': '1',
 'support_multi_bed_types': '1',
 'template_custom_gcode': '',
 'thumbnails': ['300x300'],
 'thumbnails_format': 'PNG',
 'time_cost': '0',
 'time_lapse_gcode': 'TIMELAPSE_TAKE_FRAME',
 'type': 'machine',
 'upward_compatible_machine': [],
 'use_firmware_retraction': '0',
 'use_relative_e_distances': '1',
 'version': '2.1.2.2',
 'wipe': ['1'],
 'wipe_distance': ['2'],
 'z_hop': ['0.6'],
 'z_hop_types': ['Slope Lift'],
 'z_offset': '0'}
