from __future__ import annotations

# source: profiles/Geeetech/machine/Geeetech A30 Pro 0.4 nozzle.json
DATA = {'auxiliary_fan': '0',
 'default_filament_profile': ['Generic PLA @System'],
 'default_print_profile': '0.20mm Standard @Geeetech common',
 'extruder_type': ['Bowden'],
 'from': 'system',
 'inherits': 'fdm_geeetech_common',
 'instantiation': 'true',
 'machine_end_gcode': 'G1 E-2.5 F2100 ; Retract filament\n'
                      'G92 E0.0\n'
                      'G1{if max_layer_z < printable_height} Z{z_offset+min(max_layer_z+30, '
                      'printable_height+0.2)}{endif} E-1.5 F720 ; Retract and raise Z\n'
                      'G4 ; wait\n'
                      'M104 S0 ; Cooldown hotend\n'
                      'M140 S0 ; Cooldown bed\n'
                      'M107 ; off fan\n'
                      'G1 X0 Y100 F3000 ; park print head\n'
                      'M84 ; disable motors',
 'machine_start_gcode': ';Geeetech official wiki homepage for A30: '
                        'https://www.geeetech.com/wiki/index.php/Geeetech_A30_3D_Printer \n'
                        'M104 S[first_layer_temperature] ; set extruder temp\n'
                        'M140 S[first_layer_bed_temperature] ; set bed temp\n'
                        'M190 S[first_layer_bed_temperature] ; wait for bed temp\n'
                        'M109 S[first_layer_temperature] ; wait for extruder temp\n'
                        'M220 S100 ;Reset Feedrate\n'
                        'M221 S100 ;Reset Flowrate\n'
                        'G92 E0 ; Reset Extruder\n'
                        'G28 ; Home all axes\n'
                        'M107 ;Off Fan\n'
                        'G1 Z5.0 F3000 ;Move Z Axis up little to prevent scratching of Heat Bed\n'
                        'G1 X0.1 Y20 Z1.4 F6000 ; Move to start position\n'
                        'G1 X0.1 Y80.0 Z1.4 F1000 E25 ; Draw the first line\n'
                        'G92 E0 ; Reset Extruder\n'
                        'G1 X0.4 Y80.0 Z1.4 F6000 ; Move to side a little\n'
                        'G1 X1.4 Y20 Z1.4 F1000 E20 ; Draw the second line\n'
                        'G92 E0 ; Reset Extruder\n'
                        'G1 Z2.0 F3000 ; Move Z Axis up little to prevent scratching of Heat Bed\n'
                        'G1 X5 Y20 Z0.28 F3000.0 ; Move over to prevent blob squish\n'
                        'G92 E0',
 'max_layer_height': ['0.3'],
 'min_layer_height': ['0.07'],
 'name': 'Geeetech A30 Pro 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'brass',
 'printable_area': ['0x0', '320x0', '320x320', '0x320'],
 'printable_height': '420',
 'printer_model': 'Geeetech A30 Pro',
 'printer_variant': '0.4',
 'retract_lift_below': ['419'],
 'setting_id': 'GM_GEEETECH_034',
 'type': 'machine'}
