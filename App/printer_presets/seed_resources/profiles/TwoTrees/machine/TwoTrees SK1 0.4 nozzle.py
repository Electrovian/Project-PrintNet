from __future__ import annotations

# source: profiles/TwoTrees/machine/TwoTrees SK1 0.4 nozzle.json
DATA = {'change_filament_gcode': 'PAUSE',
 'default_print_profile': '0.20mm Standard @SK1',
 'deretraction_speed': ['0'],
 'from': 'system',
 'inherits': 'fdm_klipper_common',
 'instantiation': 'true',
 'machine_end_gcode': ['M104 S0 ; turn off temperature\n'
                       'M140 S0 ; turn off heatbed\n'
                       '\n'
                       'G92 E0.0     ; reset extruder distance position\n'
                       'G1 E-1 F2100 ; retract\n'
                       '\n'
                       'G0 X50 Y250 F12000;\n'
                       'M84    ; disable motors\n'
                       '\n'
                       'M107   ; turn off fan\n'
                       '\n'
                       'SET_VELOCITY_LIMIT ACCEL_TO_DECEL=4000'],
 'machine_max_acceleration_e': ['20000', '5000'],
 'machine_max_acceleration_extruding': ['20000', '1250'],
 'machine_max_acceleration_retracting': ['15000', '1250'],
 'machine_max_acceleration_travel': ['1500', '1250'],
 'machine_max_acceleration_x': ['20000', '1000'],
 'machine_max_acceleration_y': ['20000', '1000'],
 'machine_max_acceleration_z': ['100', '200'],
 'machine_max_jerk_e': ['1', '2.5'],
 'machine_max_jerk_x': ['5', '10'],
 'machine_max_jerk_y': ['5', '10'],
 'machine_max_jerk_z': ['0.2', '0.4'],
 'machine_max_speed_e': ['50', '120'],
 'machine_max_speed_x': ['730', '200'],
 'machine_max_speed_y': ['730', '200'],
 'machine_max_speed_z': ['15', '12'],
 'machine_min_extruding_rate': ['0', '0'],
 'machine_min_travel_rate': ['0', '0'],
 'machine_pause_gcode': 'PAUSE',
 'machine_start_gcode': ['M107 ; Turn off the fan\n'
                         'G21  ; set units to millimeters\n'
                         'G90  ; use absolute coordinates\n'
                         'M83  ; use relative distances for extrusion\n'
                         '\n'
                         'M104 S220     ; set extruder temp\n'
                         'M140 S60  ; set bed temp\n'
                         'M109 S220      ; wait for extruder temp\n'
                         'M190 S60  ; wait for bed temp\n'
                         'G1 E-1.5 F2100 ; retract\n'
                         '\n'
                         ';G32  ;Load bed mesh\n'
                         'G28   ;home\n'
                         'G29   ;bed leveling\n'
                         '\n'
                         'M104 S[first_layer_temperature]      ; set extruder temp\n'
                         'M140 S[first_layer_bed_temperature]  ; set bed temp\n'
                         'M109 S[first_layer_temperature]      ; wait for extruder temp\n'
                         'M190 S[first_layer_bed_temperature]  ; wait for bed temp\n'
                         '\n'
                         'G0 Z2.0 F600;\n'
                         'G0 X50 Y10 F12000;\n'
                         '\n'
                         'G92 E0.0 ; reset extruder distance position\n'
                         'G0 Z0.4 F600;\n'
                         'G1 X100.0 E10 F3000.0 ; intro line\n'
                         'G92 E0.0 ; reset extruder distance position\n'
                         'G1 X200.0 E15 F3000.0 ; intro line\n'
                         'G92 E0.0 ; reset extruder distance position\n'
                         'G0 Z0.8 F600;\n'
                         'G1 X100.0 E15 F3000.0 ; intro line\n'
                         '\n'
                         'G1 Z0.4 F600     ;Wipe\n'
                         'G0 Y12 F6000    ;Wipe\n'
                         'G1 X100 F6000    ;Wipe\n'
                         'G0 Y8 F12000   ;Wipe\n'
                         'G1 X200 F6000    ;Wipe\n'
                         'G1 X190 Y12 F6000 ;Wipe\n'
                         'G1 X180 Y8 F6000 ;Wipe\n'
                         'G1 X170 Y12 F6000 ;Wipe\n'
                         'G1 X160 Y8 F6000 ;Wipe\n'
                         'G1 X150 Y12 F6000 ;Wipe\n'
                         '\n'
                         '\n'
                         ';G0 Z2.0 F600;\n'
                         'G92 E0.0 ; reset extruder distance position\n'
                         '\n'
                         'SET_VELOCITY_LIMIT ACCEL_TO_DECEL=10000'],
 'max_layer_height': '0.32',
 'min_layer_height': '0.08',
 'name': 'TwoTrees SK1 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'hardened_steel',
 'printable_area': ['0x0', '256x0', '256x256', '0x256'],
 'printable_height': '256',
 'printer_model': 'TwoTrees SK1',
 'retract_before_wipe': '100%',
 'retract_length_toolchange': '10',
 'retraction_length': '0.4',
 'retraction_minimum_travel': ['2'],
 'retraction_speed': ['50'],
 'setting_id': 'GM001',
 'support_multi_bed_types': '1',
 'thumbnails': ['300x300'],
 'thumbnails_format': 'PNG',
 'type': 'machine'}
