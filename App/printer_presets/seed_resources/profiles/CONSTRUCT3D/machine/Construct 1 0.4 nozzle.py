from __future__ import annotations

# source: profiles/CONSTRUCT3D/machine/Construct 1 0.4 nozzle.json
DATA = {'bed_mesh_max': '200,235',
 'bed_mesh_min': '10,20',
 'default_print_profile': '0.22mm Quality @Construct 1',
 'fan_kickstart': '0.5',
 'fan_speedup_time': '1',
 'from': 'system',
 'inherits': 'fdm_machine_common',
 'instantiation': 'true',
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
 'machine_max_acceleration_e': ['9000'],
 'machine_max_acceleration_extruding': ['9000'],
 'machine_max_acceleration_retracting': ['9000'],
 'machine_max_acceleration_travel': ['9000', '1250'],
 'machine_max_acceleration_x': ['18000'],
 'machine_max_acceleration_y': ['18000'],
 'machine_max_jerk_e': ['6'],
 'machine_max_jerk_x': ['25'],
 'machine_max_jerk_y': ['25'],
 'machine_max_speed_e': ['100'],
 'machine_max_speed_x': ['320'],
 'machine_max_speed_y': ['320'],
 'machine_max_speed_z': ['40'],
 'machine_start_gcode': 'G90 ; use absolute coordinates\n'
                        'M83 ; extruder relative mode\n'
                        'M106 S0 ; Turn Fan off\n'
                        'M204 S[machine_max_acceleration_extruding] T[machine_max_acceleration_retracting]\n'
                        'M190 S[first_layer_bed_temperature] ; set bed temp\n'
                        'M109 S160 ; set extruder temp\n'
                        'M557 P5 X{adaptive_bed_mesh_min[0]}:{adaptive_bed_mesh_max[0]} '
                        'Y{adaptive_bed_mesh_min[1]}:{adaptive_bed_mesh_max[1]} ; dynamic meshing\n'
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
 'max_layer_height': ['0.38'],
 'min_layer_height': ['0.08'],
 'name': 'Construct 1 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'hardened_steel',
 'printable_area': ['0x0', '225x0', '225x260', '0x260'],
 'printable_height': '180',
 'printer_model': 'Construct 1',
 'printer_settings_id': 'CONSTRUCT3D',
 'printer_variant': '0.4',
 'retraction_length': ['0.7'],
 'retraction_speed': ['50'],
 'setting_id': 'GM001',
 'thumbnails_format': 'QOI',
 'type': 'machine',
 'z_hop': ['0.2'],
 'z_hop_types': ['Auto Lift']}
