from __future__ import annotations

# source: profiles/Geeetech/machine/Geeetech Thunder 0.8 nozzle.json
DATA = {'auxiliary_fan': '1',
 'default_filament_profile': ['Generic PLA @System'],
 'default_print_profile': '0.44mm Draft @Geeetech Thunder 0.8 nozzle',
 'extruder_type': ['Bowden'],
 'from': 'system',
 'inherits': 'fdm_geeetech_common',
 'instantiation': 'true',
 'machine_end_gcode': 'G91 ;Switch to relative positioning\n'
                      'G1 E-2.5 F2700 ;Retract filament\n'
                      'G1 E-1.5 Z0.2 F2400 ;Retract and raise Z\n'
                      'G1 X5 Y5 F3000 ;Move away\n'
                      'G1 Z10 ;lift print head\n'
                      'G90 ;Switch to absolute positioning\n'
                      'G28 X Y ;homing XY\n'
                      'M106 S0 ;off Fan\n'
                      'M104 S0 ;Cooldown hotend\n'
                      'M140 S0 ;Cooldown bed\n'
                      'M84 X Y E ;Disable steppers',
 'machine_max_acceleration_extruding': ['3500', '3500'],
 'machine_max_acceleration_retracting': ['3500', '3500'],
 'machine_max_acceleration_travel': ['5000', '5000'],
 'machine_max_acceleration_x': ['5000', '5000'],
 'machine_max_acceleration_y': ['4000', '4000'],
 'machine_max_acceleration_z': ['50', '50'],
 'machine_max_jerk_e': ['8', '8'],
 'machine_max_jerk_x': ['45', '45'],
 'machine_max_jerk_y': ['45', '45'],
 'machine_max_jerk_z': ['0.8', '0.8'],
 'machine_max_speed_e': ['35', '35'],
 'machine_max_speed_x': ['300', '300'],
 'machine_max_speed_y': ['300', '300'],
 'machine_max_speed_z': ['10', '10'],
 'machine_start_gcode': ';Official viki homepage for '
                        'Thunder:https://www.geeetech.com/wiki/index.php/Geeetech_Thunder_3D_printer\n'
                        '\n'
                        'M104 S[first_layer_temperature] ; Set Hotend Temp.\n'
                        'M140 S[first_layer_bed_temperature] ; Set bed Temp.\n'
                        'M190 S[first_layer_bed_temperature] ; Wait for Bed Temp.\n'
                        'M109 S[first_layer_temperature] ; Wait for Hotend Temp.\n'
                        'M220 S100 ;Reset Feedrate\n'
                        'M221 S100 ;Reset Flowrate\n'
                        'G92 E0 ; Reset Extruder\n'
                        'G28 ; Home all axes\n'
                        'M107 P0 ;Off Main Fan\n'
                        'M107 P1 ;Off Aux Fan\n'
                        'M2012 P8 S1 F100 ; ON Light\n'
                        'G1 Z5.0 F3000 ;Move the Z-axis slightly up to prevent scratching the heatbed\n'
                        'G1 X0.1 Y20 Z0.8 F5000 ; Move to start position\n'
                        'G1 X0.1 Y200.0 Z1.2 F1500 E30 ; Draw the first line\n'
                        'G92 E0 ; Reset Extruder\n'
                        'G1 X0.4 Y200.0 Z1.2 F3000 ; Move to side a little\n'
                        'G1 X0.4 Y20 Z1.2 F1500 E25 ; Draw the second line\n'
                        'G92 E0 ; Reset Extruder\n'
                        'G1 Z2.0 F3000 ; Move the Z-axis slightly up to prevent scratching the heatbed\n'
                        'G1 X5 Y20 Z0.4 F3000.0 ; Scrape off nozzle residue\n'
                        'G92 E0\n'
                        ';---------------------------------------\n'
                        ';M106 P0 S383 ; ON MainFan 150% if need\n'
                        ';M106 P1 S255 ; ON Aux Fan 100% if need\n'
                        ';---------------------------------------',
 'max_layer_height': ['0.56'],
 'min_layer_height': ['0.16'],
 'name': 'Geeetech Thunder 0.8 nozzle',
 'nozzle_diameter': ['0.8'],
 'nozzle_type': 'brass',
 'printable_area': ['0x0', '250x0', '250x250', '0x250'],
 'printable_height': '260',
 'printer_model': 'Geeetech Thunder',
 'printer_variant': '0.8',
 'retract_lift_below': ['259'],
 'setting_id': 'GM_GEEETECH_004',
 'type': 'machine'}
