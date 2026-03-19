from __future__ import annotations

# source: profiles/Anker/machine/fdm_marlin_common.json
DATA = {'before_layer_change_gcode': ';BEFORE_LAYER_CHANGE\nG92 E0.0\n;[layer_z]\n\n',
 'change_filament_gcode': 'M600',
 'from': 'system',
 'gcode_flavor': 'marlin2',
 'inherits': 'fdm_machine_common',
 'instantiation': 'false',
 'machine_end_gcode': 'M104 S0\nM140 S0\n;Retract the filament\nG92 E1\nG1 E-1 F300\nG28 X0 Y0\nM18',
 'machine_pause_gcode': 'M601',
 'machine_start_gcode': 'M4899 T3 ; Enable v3 jerk and S-curve acceleration \n'
                        'M104 S150 ; Set hotend temp to 150 degrees to prevent ooze\n'
                        'M190 S{first_layer_bed_temperature[0]} ; set and wait for bed temp to stabilize\n'
                        'M109 S{first_layer_temperature[0]} ; set final nozzle temp to stabilize\n'
                        'G28 ;Home\n'
                        ';LAYER_COUNT:{total_layer_count}',
 'name': 'fdm_marlin_common',
 'type': 'machine'}
