from __future__ import annotations

# source: profiles/Elegoo/machine/ECC/fdm_machine_ecc.json
DATA = {'auxiliary_fan': '1',
 'bed_exclude_area': ['0x0'],
 'best_object_pos': '0.5x0.5',
 'change_filament_gcode': '',
 'default_filament_profile': ['Elegoo PLA'],
 'default_print_profile': '0.20mm Standard @Elegoo CC 0.4 nozzle',
 'deretraction_speed': ['30'],
 'extruder_clearance_height_to_lid': '90',
 'extruder_clearance_max_radius': '68',
 'extruder_colour': ['#018001'],
 'from': 'system',
 'inherits': 'fdm_machine_ecc_common',
 'instantiation': 'false',
 'layer_change_gcode': ';LAYER:{layer_num+1}\n',
 'machine_end_gcode': ';===== date: 20240510 =====================\n'
                      'M400 ; wait for buffer to clear\n'
                      'G92 E0 ; zero the extruder\n'
                      'G1 E-0.8 F1800 ; retract\n'
                      'G1 Z{max_layer_z + 0.5} F900 ; lower z a little\n'
                      'G1 X65 Y245 F12000 ; move to safe pos \n'
                      'G1 Y245 F3000\n'
                      '\n'
                      'G1 X65 Y245 F12000\n'
                      'G1 Y245 F3000\n'
                      'M140 S0 ; turn off bed\n'
                      'M106 S0 ; turn off fan\n'
                      'M106 P2 S0 ; turn off remote part cooling fan\n'
                      'M106 P3 S0 ; turn off chamber cooling fan\n',
 'machine_max_acceleration_e': ['5000', '5000'],
 'machine_max_acceleration_extruding': ['20000', '20000'],
 'machine_max_acceleration_retracting': ['5000', '5000'],
 'machine_max_acceleration_travel': ['9000', '9000'],
 'machine_max_acceleration_x': ['20000', '20000'],
 'machine_max_acceleration_y': ['20000', '20000'],
 'machine_max_acceleration_z': ['500', '200'],
 'machine_max_jerk_e': ['2.5', '2.5'],
 'machine_max_jerk_x': ['9', '9'],
 'machine_max_jerk_y': ['9', '9'],
 'machine_max_jerk_z': ['3', '3'],
 'machine_max_speed_e': ['30', '30'],
 'machine_max_speed_x': ['500', '200'],
 'machine_max_speed_y': ['500', '200'],
 'machine_max_speed_z': ['20', '20'],
 'machine_min_extruding_rate': ['0', '0'],
 'machine_min_travel_rate': ['0', '0'],
 'machine_pause_gcode': 'M600',
 'name': 'fdm_machine_ecc',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'brass',
 'nozzle_volume': '107',
 'printable_area': ['0x0', '256x0', '256x256', '0x256'],
 'printer_structure': 'corexy',
 'printer_variant': '0.4',
 'retract_before_wipe': ['0%'],
 'retract_length_toolchange': ['2'],
 'retract_lift_below': ['249'],
 'retraction_length': ['0.8'],
 'retraction_minimum_travel': ['0.8'],
 'retraction_speed': ['30'],
 'single_extruder_multi_material': '1',
 'thumbnails': ['320x320', '160x160'],
 'thumbnails_format': 'PNG',
 'type': 'machine',
 'wipe_distance': ['1.2'],
 'z_hop': ['0.4'],
 'z_hop_types': ['Auto Lift']}
