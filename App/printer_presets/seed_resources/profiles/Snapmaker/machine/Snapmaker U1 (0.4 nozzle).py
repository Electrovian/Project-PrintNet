from __future__ import annotations

# source: profiles/Snapmaker/machine/Snapmaker U1 (0.4 nozzle).json
DATA = {'auxiliary_fan': '1',
 'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\nTIMELAPSE_TAKE_FRAME',
 'change_filament_gcode': '; Change Tool[previous_extruder] -> Tool[next_extruder] (layer [layer_num])\n'
                          '{\n'
                          'local max_speed_toolchange = 350.0;\n'
                          'local wait_for_extruder_temp = true;\n'
                          'position[2] = position[2] + 2.0;\n'
                          '\n'
                          'local speed_toolchange = max_speed_toolchange;\n'
                          'if travel_speed < max_speed_toolchange then\n'
                          '      speed_toolchange = travel_speed;\n'
                          'endif\n'
                          '"G91\n'
                          'G0 Z1.5 F600\n'
                          'G90\n'
                          '";\n'
                          '"G1 F" + (speed_toolchange * 60) + "\n'
                          '";\n'
                          'if wait_for_extruder_temp and not((layer_num < 0) and (next_extruder == initial_tool)) '
                          'then\n'
                          '      "\n'
                          '";\n'
                          '      "; " + layer_num + "\n'
                          '";\n'
                          '      if layer_num == 0 then\n'
                          '            "M109 S" + first_layer_temperature[next_extruder] + " T" + next_extruder + "\n'
                          '";\n'
                          '      else\n'
                          '            "M109 S" + temperature[next_extruder] + " T" + next_extruder + "\n'
                          '";\n'
                          '      endif\n'
                          'endif\n'
                          '"T" + next_extruder + "\n'
                          '";\n'
                          '}\n'
                          'M400\n'
                          '{if filament_type[next_extruder] == "PVA"}\n'
                          'SET_VELOCITY_LIMIT ACCEL=3000\n'
                          '{else}\n'
                          '{endif}',
 'deretraction_speed': ['35', '35', '35', '35'],
 'enable_filament_ramming': '0',
 'extruder_clearance_height_to_rod': '27.5',
 'extruder_clearance_radius': '72.5',
 'extruder_colour': ['#FCE94F', '#FCE94F', '#FCE94F', '#FCE94F'],
 'extruder_offset': ['0x0', '0x0', '0x0', '0x0'],
 'from': 'system',
 'host_type': 'octoprint',
 'inherits': 'fdm_U1',
 'instantiation': 'true',
 'long_retractions_when_cut': ['0', '0', '0', '0'],
 'machine_end_gcode': ' PRINT_END\nTIMELAPSE_STOP',
 'machine_load_filament_time': '0',
 'machine_max_jerk_z': ['3', '0.4'],
 'machine_max_speed_e': ['30', '25'],
 'machine_max_speed_z': ['20', '12'],
 'machine_pause_gcode': 'M600',
 'machine_tool_change_time': '5',
 'machine_unload_filament_time': '0',
 'max_layer_height': ['0.32', '0.32', '0.32', '0.32'],
 'min_layer_height': ['0.08', '0.08', '0.08', '0.08'],
 'name': 'Snapmaker U1 (0.4 nozzle)',
 'nozzle_diameter': ['0.4', '0.4', '0.4', '0.4'],
 'nozzle_type': 'hardened_steel',
 'printable_area': ['-0.5x-1', '270.5x-1', '270.5x271', '-0.5x271'],
 'printable_height': '270',
 'printer_model': 'Snapmaker U1',
 'printer_notes': '1、修改幅面坐标，原点坐标\n2、修改换头时间，5S',
 'printer_settings_id': 'MyToolChanger 0.4 nozzle - Copy',
 'printer_variant': '0.4',
 'ramming_pressure_advance_value': '0.02',
 'retract_before_wipe': ['0%', '0%', '0%', '0%'],
 'retract_length_toolchange': ['10', '10', '10', '10'],
 'retract_lift_above': ['0', '0', '0', '0'],
 'retract_lift_below': ['269', '269', '269', '269'],
 'retract_lift_enforce': ['All Surfaces', 'All Surfaces', 'All Surfaces', 'All Surfaces'],
 'retract_restart_extra': ['0', '0', '0', '0'],
 'retract_restart_extra_toolchange': ['0', '0', '0', '0'],
 'retract_when_changing_layer': ['1', '1', '1', '1'],
 'retraction_distances_when_cut': ['18', '18', '18', '18'],
 'retraction_length': ['0.8', '0.8', '0.8', '0.8'],
 'retraction_minimum_travel': ['1', '1', '1', '1'],
 'retraction_speed': ['40', '40', '40', '40'],
 'setting_id': '1591507869',
 'thumbnails': '48x48/PNG, 300x300/PNG',
 'tool_change_temprature_wait': '0',
 'travel_slope': ['3', '3', '3', '3'],
 'type': 'machine',
 'wipe': ['1', '1', '1', '1'],
 'wipe_distance': ['2', '2', '2', '2'],
 'z_hop': ['0.4', '0.4', '0.4', '0.4'],
 'z_hop_types': ['Auto Lift', 'Auto Lift', 'Auto Lift', 'Auto Lift'],
 'z_hop_when_prime': ['0', '0', '0', '0']}
