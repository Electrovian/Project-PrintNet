from __future__ import annotations

# source: profiles/CONSTRUCT3D/machine/fdm_machine_common.json
DATA = {'auxiliary_fan': '0',
 'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n',
 'change_filament_gcode': '',
 'default_print_profile': '',
 'deretraction_speed': ['50'],
 'extruder_clearance_height_to_lid': '140',
 'extruder_clearance_height_to_rod': '36',
 'extruder_clearance_radius': '65',
 'extruder_colour': ['#003f87'],
 'extruder_offset': ['0x0'],
 'from': 'system',
 'gcode_flavor': 'reprapfirmware',
 'host_type': 'duet',
 'instantiation': 'false',
 'layer_change_gcode': ';AFTER_LAYER_CHANGE\n;[layer_z]',
 'machine_end_gcode': ';Retract the filament\n'
                      'G92 E1\n'
                      'G1 E-5 F900\n'
                      ';Move nozzle fast\n'
                      'G1 X5 Y258 F15000\n'
                      ';Move Bed Down\n'
                      'G1 Z180 F6000\n'
                      '\n'
                      ';Set machine to idle\n'
                      'M104 S0\n'
                      'M104 S0 ; turn off temperature\n'
                      'M140 S0 ; turn off heatbed\n'
                      'M107 ; turn off fan\n'
                      'M84 ; disable motors',
 'machine_max_acceleration_e': ['8000'],
 'machine_max_acceleration_extruding': ['9000'],
 'machine_max_acceleration_retracting': ['9000'],
 'machine_max_acceleration_x': ['9000'],
 'machine_max_acceleration_y': ['9000'],
 'machine_max_acceleration_z': ['400'],
 'machine_max_jerk_e': ['10'],
 'machine_max_jerk_x': ['20'],
 'machine_max_jerk_y': ['20'],
 'machine_max_jerk_z': ['0.2'],
 'machine_max_speed_e': ['100'],
 'machine_max_speed_x': ['320'],
 'machine_max_speed_y': ['320'],
 'machine_max_speed_z': ['30'],
 'machine_min_extruding_rate': ['0'],
 'machine_min_travel_rate': ['0'],
 'machine_start_gcode': 'G90 ; use absolute coordinates\n'
                        'M83 ; extruder relative mode\n'
                        'M106 S0 ; Turn Fan off\n'
                        'M204 S[machine_max_acceleration_extruding] T[machine_max_acceleration_retracting]\n'
                        'M190 S[first_layer_bed_temperature] ; set bed temp\n'
                        'M109 S160 ; set extruder temp\n'
                        'G28 ; home all\n'
                        'G1 Z15 F6000 ; move the printer down 15mm\n'
                        'G1 Y1.0 Z0.3 F4000 ; move print head up\n'
                        'M109 S[first_layer_temperature] ; set extruder temp\n'
                        '\n'
                        'M190 S[first_layer_bed_temperature] ; wait for bed temp\n'
                        'M109 S[first_layer_temperature] ; wait for extruder temp\n'
                        ';prime the extruder\n'
                        'G1 X5 Y2 Z0.3 F6000; go to edge of build volume\n'
                        'G1 X60 E10 F1000 ;gentle purge start\n'
                        'G1 X110 E25 F1000; heavy purge\n'
                        'G1 X60;',
 'max_layer_height': ['0.80'],
 'min_layer_height': ['0.08'],
 'name': 'fdm_machine_common',
 'nozzle_diameter': ['0.6'],
 'printable_height': '180',
 'printer_settings_id': '',
 'printer_technology': 'FFF',
 'printhost_apikey': '',
 'printhost_authorization_type': 'key',
 'printhost_cafile': '',
 'printhost_password': '',
 'printhost_port': '',
 'printhost_ssl_ignore_revoke': '0',
 'printhost_user': '',
 'retract_before_wipe': ['70%'],
 'retract_length_toolchange': ['1'],
 'retract_restart_extra': ['0'],
 'retract_restart_extra_toolchange': ['0'],
 'retract_when_changing_layer': ['1'],
 'retraction_length': ['1'],
 'retraction_minimum_travel': ['2.6'],
 'retraction_speed': ['50'],
 'silent_mode': '0',
 'single_extruder_multi_material': '1',
 'thumbnails': ['160x160'],
 'thumbnails_format': 'QOI',
 'type': 'machine',
 'wipe': ['1'],
 'z_hop': ['0.2'],
 'z_lift_type': 'Auto Lift'}
