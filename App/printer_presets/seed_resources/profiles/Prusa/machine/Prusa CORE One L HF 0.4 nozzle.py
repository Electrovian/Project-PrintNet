from __future__ import annotations

# source: profiles/Prusa/machine/Prusa CORE One L HF 0.4 nozzle.json
DATA = {'before_layer_change_gcode': [';BEFORE_LAYER_CHANGE\n'
                               'G92 E0.0\n'
                               ';[layer_z]\n'
                               '{if layer_z > 150}\n'
                               'M201 X{interpolate_table(layer_z, (0,6000), (150,6000), (200,4000), (331,2000))} '
                               'Y{interpolate_table(layer_z, (0,6000), (150,6000), (200,4000), (331,2000))}\n'
                               '{endif}\n'],
 'change_filament_gcode': ['M600\nG1 E0.3 F1500 ; prime after color change'],
 'default_filament_profile': 'Prusament PLA @CORE One HF 0.4',
 'default_print_profile': '0.20mm SPEED @CORE One L 0.4',
 'deretraction_speed': '25',
 'emit_machine_limits_to_gcode': '1',
 'extruder_clearance_height_to_lid': '50',
 'extruder_clearance_height_to_rod': '33',
 'extruder_clearance_radius': '75',
 'from': 'system',
 'gcode_flavor': 'marlin2',
 'host_type': 'prusalink',
 'inherits': 'fdm_machine_common',
 'instantiation': 'true',
 'layer_change_gcode': [';AFTER_LAYER_CHANGE\n;[layer_z]'],
 'machine_end_gcode': ['{if layer_z < max_print_height}G1 Z{z_offset+min(max_layer_z+1, max_print_height)} F720 ; Move '
                       'print head up{endif}\n'
                       'M104 S0 ; turn off temperature\n'
                       'M140 S0 ; turn off heatbed\n'
                       'M141 S0 ; disable chamber control\n'
                       'M107 ; turn off fan\n'
                       'M107 P3\n'
                       'M107 P5\n'
                       'G1 X242 Y211 F10200 ; park\n'
                       'G4 ; wait\n'
                       'M572 S0 ; reset PA\n'
                       'M84 X Y E ; disable motors\n'
                       '; max_layer_z = [max_layer_z]'],
 'machine_max_acceleration_e': ['5000', '2500'],
 'machine_max_acceleration_extruding': ['7000', '2500'],
 'machine_max_acceleration_retracting': ['2500', '1200'],
 'machine_max_acceleration_travel': ['6000', '2500'],
 'machine_max_acceleration_x': ['10000', '2500'],
 'machine_max_acceleration_y': ['10000', '2500'],
 'machine_max_acceleration_z': ['400', '200'],
 'machine_max_jerk_e': ['10', '10'],
 'machine_max_jerk_x': ['10', '8'],
 'machine_max_jerk_y': ['10', '8'],
 'machine_max_jerk_z': ['2', '2'],
 'machine_max_speed_e': ['100', '100'],
 'machine_max_speed_x': ['350', '160'],
 'machine_max_speed_y': ['350', '160'],
 'machine_max_speed_z': ['12', '12'],
 'machine_pause_gcode': 'M601',
 'machine_start_gcode': ['M17 ; enable steppers\n'
                         'M862.1 P[nozzle_diameter] A{(printer_notes=~/.*ABRASIVE_NOZZLE.*/ ? 1 : 0)} '
                         'F{(printer_notes=~/.*HF_NOZZLE.*/ ? 1 : 0)} ; nozzle check\n'
                         'M862.3 P "COREONEL" ; printer model check\n'
                         'M862.5 P2 ; g-code level check\n'
                         'M862.6 P"Input shaper" ; FW feature check\n'
                         'M115 U6.3.0+10073\n'
                         '\n'
                         'M555 X{(min(print_bed_max[0], first_layer_print_min[0] + 32) - 32)} Y{(max(0, '
                         'first_layer_print_min[1]) - 4)} W{((min(print_bed_max[0], max(first_layer_print_min[0] + 32, '
                         'first_layer_print_max[0])))) - ((min(print_bed_max[0], first_layer_print_min[0] + 32) - '
                         '32))} H{((first_layer_print_max[1])) - ((max(0, first_layer_print_min[1]) - 4))}\n'
                         '\n'
                         'G90 ; use absolute coordinates\n'
                         'M83 ; extruder relative mode\n'
                         '\n'
                         'M140 S[first_layer_bed_temperature] ; set bed temp\n'
                         '{if chamber_temperature[initial_tool] > 35}\n'
                         'M106 P5 R A125 B10 C5 ;turn on bed fans with fade for chamber or bed\n'
                         '{else}\n'
                         'M106 P5 R A125 B10 ;turn on bed fans with fade for bed\n'
                         '{endif}\n'
                         '\n'
                         'M109 R{((filament_notes[0]=~/.*MBL160.*/) ? 160 : (filament_notes[0]=~/.*HT_MBL10.*/) ? '
                         '(first_layer_temperature[0] - 10) : (filament_type[0] == "PC" or filament_type[0] == "PA") ? '
                         '(first_layer_temperature[0] - 25) : (filament_type[0] == "FLEX") ? 210 : 170)} ; wait for '
                         'temp\n'
                         '\n'
                         'M84 E ; turn off E motor\n'
                         '\n'
                         'G28 Q ;home all without mesh bed level\n'
                         '\n'
                         'G1 Z20 F720 ;lift bed to optimal bed fan height\n'
                         '\n'
                         '{if chamber_temperature[initial_tool] > 35}\n'
                         '; Min chamber temp section\n'
                         'M104 S170 ; set idle temp\n'
                         'G1 X292 Y-5 F4800 ; set print head position\n'
                         'M191 S{chamber_temperature[initial_tool]}\n'
                         'M141 S{chamber_temperature[initial_tool]} ; set nominal chamber temp\n'
                         'M104 S{((filament_notes[0]=~/.*MBL160.*/) ? 160 : (filament_notes[0]=~/.*HT_MBL10.*/) ? '
                         '(first_layer_temperature[0] - 10) : (filament_type[0] == "PC" or filament_type[0] == "PA") ? '
                         '(first_layer_temperature[0] - 25) : (filament_type[0] == "FLEX") ? 210 : 170)} ; set MBL '
                         'temp\n'
                         'M106 P3 N25 G5\n'
                         '{else}\n'
                         'M141 S{chamber_temperature[initial_tool]} ; set nominal chamber temp\n'
                         '{if chamber_temperature[initial_tool]<30}\n'
                         'M106 P3 N76 G3\n'
                         '{else}\n'
                         'M106 P3 N51 G1\n'
                         '{endif}\n'
                         '{endif}\n'
                         '\n'
                         '{if first_layer_bed_temperature[initial_tool]<=60}M106 S70{endif}\n'
                         'M190 R[first_layer_bed_temperature] ; wait for bed temp\n'
                         'M107\n'
                         '{if chamber_temperature[initial_tool]<50} \n'
                         '; turn off bed fans for chamber temps < 50C\n'
                         'M107 P5\n'
                         '{endif}\n'
                         'M109 R{((filament_notes[0]=~/.*MBL160.*/) ? 160 : (filament_notes[0]=~/.*HT_MBL10.*/) ? '
                         '(first_layer_temperature[0] - 10) : (filament_type[0] == "PC" or filament_type[0] == "PA") ? '
                         '(first_layer_temperature[0] - 25) : (filament_type[0] == "FLEX") ? 210 : 170)} ; wait for '
                         'MBL temp\n'
                         '\n'
                         'M302 S155 ; lower cold extrusion limit to 155C\n'
                         '\n'
                         '{if filament_type[initial_tool]=="FLEX"}\n'
                         'G1 E-4 F2400 ; retraction\n'
                         '{else}\n'
                         'G1 E-2 F2400 ; retraction\n'
                         '{endif}\n'
                         '\n'
                         'M84 E ; turn off E motor\n'
                         '\n'
                         'G29 P9 X208 Y-2.5 W32 H4\n'
                         '\n'
                         ';\n'
                         '; MBL\n'
                         ';\n'
                         '\n'
                         'M84 E ; turn off E motor\n'
                         'G29 P1 ; invalidate mbl & probe print area\n'
                         'G29 P1 X150 Y0 W100 H20 C ; probe near purge place\n'
                         'G29 P3.2 ; interpolate mbl probes\n'
                         'G29 P3.13 ; extrapolate mbl outside probe area\n'
                         'G29 A ; activate mbl\n'
                         '\n'
                         '; prepare for purge\n'
                         'M104 S{first_layer_temperature[0]}\n'
                         'G0 X249 Y-2.5 Z15 F4800 ; move away and ready for the purge\n'
                         'M109 S{first_layer_temperature[0]}\n'
                         '\n'
                         'G92 E0\n'
                         'M569 S0 E ; set spreadcycle mode for extruder\n'
                         '\n'
                         'M591 S0 ; disable stuck detection\n'
                         '\n'
                         ';\n'
                         '; Extrude purge line\n'
                         ';\n'
                         'G92 E0 ; reset extruder position\n'
                         'G1 E{(filament_type[0] == "FLEX" ? 4 : 2)} F2400 ; deretraction after the initial one\n'
                         'G0 E5 X235 Z0.2 F500 ; purge\n'
                         'G0 X225 E4 F500 ; purge\n'
                         'G0 X215 E4 F650 ; purge\n'
                         'G0 X205 E4 F800 ; purge\n'
                         'G0 X202 Z0.05 F8000 ; wipe, move close to the bed\n'
                         'G0 X199 Z0.2 F8000 ; wipe, move quickly away from the bed\n'
                         '\n'
                         'M591 R ; restore stuck detection\n'
                         '\n'
                         'G92 E0\n'
                         'M221 S100 ; set flow to 100%'],
 'max_layer_height': '0.30',
 'min_layer_height': '0.07',
 'name': 'Prusa CORE One L HF 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'printable_area': ['0x0', '300x0', '300x300', '0x300'],
 'printable_height': '331',
 'printer_model': 'Prusa CORE One L HF',
 'printer_notes': ['Don\'t remove the following keywords! These keywords are used in the "compatible printer" '
                   'condition of the print and filament profiles to link the particular print and filament profiles to '
                   'this printer profile.\n'
                   'PRINTER_MODEL_COREONE_L\n'
                   'HF_NOZZLE\n'
                   'PG\n'
                   'NO_TEMPLATES\n'
                   'SEQ_ARRANGE_MODEL_COREONEL'],
 'printer_structure': 'corexy',
 'printer_variant': '0.4',
 'retract_before_wipe': '80',
 'retract_length_toolchange': '0',
 'retract_lift_above': '0',
 'retract_lift_below': '329',
 'retract_when_changing_layer': '1',
 'retraction_length': '0.7',
 'retraction_minimum_travel': '1.5',
 'retraction_speed': '45',
 'single_extruder_multi_material': '0',
 'thumbnails': ['16x16/QOI', '313x173/QOI', '440x240/QOI', '480x240/QOI', '640x480/PNG'],
 'travel_slope': '1',
 'type': 'machine',
 'use_firmware_retraction': '0',
 'use_relative_e_distances': '1',
 'wipe': '0',
 'z_hop': '0.2',
 'z_hop_types': 'Normal Lift'}
