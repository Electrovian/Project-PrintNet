from __future__ import annotations

# source: profiles/Wanhao/machine/Wanhao D12-300 0.4 nozzle.json
DATA = {'auxiliary_fan': '0',
 'default_print_profile': '0.15mm Optimal @Wanhao D12-300',
 'deretraction_speed': ['70'],
 'from': 'system',
 'gcode_flavor': 'marlin',
 'inherits': 'fdm_wanhao_common',
 'instantiation': 'true',
 'machine_end_gcode': '; Wanhao D12-300 Default End Gcode\n'
                      'G91                            ;Relative positioning\n'
                      'G1 E-2 F2700                   ;Retract a bit\n'
                      'G1 E-2 Z0.2 F2400              ;Retract a bit more and raise Z\n'
                      'G1 X5 Y5 F3000                 ;Wipe out\n'
                      'G1 Z10                         ;Raise Z by 10mm\n'
                      'G90                            ;Return to absolute positioning\n'
                      'G1 X0 Y{print_bed_max[1]}         ;TaDaaaa\n'
                      'M106 S0                        ;Turn-off fan\n'
                      'M104 S0                        ;Turn-off hotend\n'
                      'M140 S0                        ;Turn-off bed\n'
                      'M84 X Y E                      ;Disable all steppers but Z',
 'machine_max_acceleration_e': ['10000'],
 'machine_max_acceleration_extruding': ['1000'],
 'machine_max_acceleration_retracting': ['1000'],
 'machine_max_acceleration_x': ['1000'],
 'machine_max_acceleration_y': ['1000'],
 'machine_max_acceleration_z': ['100'],
 'machine_max_jerk_e': ['5'],
 'machine_max_jerk_x': ['10'],
 'machine_max_jerk_y': ['10'],
 'machine_max_jerk_z': ['0.3'],
 'machine_max_speed_e': ['60'],
 'machine_max_speed_x': ['500'],
 'machine_max_speed_y': ['500'],
 'machine_max_speed_z': ['10'],
 'machine_start_gcode': '; Wanhao D12-300 Start G-code\n'
                        '; M117 Initial homing sequence.                         ; Home so that the probe is '
                        'positioned to heat\n'
                        'G28\n'
                        'M117 Probe heating position\n'
                        'G0 X65 Y5 Z1                                                   ; Move the probe to the '
                        'heating position.\n'
                        'M117 Getting the heaters up to temp!\n'
                        'M104 S140                                                          ; Set Extruder '
                        'temperature, no wait\n'
                        'M140 S60                                                            ; Set Heat Bed '
                        'temperature\n'
                        'M190 S60                                                            ; Wait for Heat Bed '
                        'temperature\n'
                        'M117 Waiting for probe to warm!                        ; Wait another 90s for the probe to '
                        'absorb heat.\n'
                        'G4 S90\n'
                        'M117 Post warming re-home\n'
                        'G28                                                                      ; Home all axes '
                        'again after warming\n'
                        'M117 Z-Dance of my people\n'
                        'G34\n'
                        'M117 ABL Probing\n'
                        'G29\n'
                        'M900 K0 L0 T0                                 ;Edit the K and L values if you have calibrated '
                        'a k factor for your filament\n'
                        'M900 T0 S0\n'
                        'G1 Z2.0 F3000                                        ; Move Z Axis up little to prevent '
                        'scratching of Heat Bed\n'
                        'G1 X4.1 Y10 Z0.3 F5000.0                      ; Move to start position\n'
                        'M117 Getting the extruder up to temp\n'
                        'M140 S[first_layer_bed_temperature]      ; Set Heat Bed temperature\n'
                        'M104 S[first_layer_temperature]    ; Set Extruder temperature\n'
                        'M109 S[first_layer_temperature]    ; Wait for Extruder temperature\n'
                        'M190 S[first_layer_bed_temperature]      ; Wait for Heat Bed temperature\n'
                        'G92 E0                                        ; Reset Extruder\n'
                        'M117 Purging\n'
                        'G1 X4.1 Y200.0 Z0.3 F1500.0 E15               ; Draw the first line\n'
                        'G1 X4.4 Y200.0 Z0.3 F5000.0                   ; Move to side a little\n'
                        'G1 X4.4 Y20 Z0.3 F1500.0 E30                  ; Draw the second line\n'
                        'G92 E0                                        ; Reset Extruder\n'
                        'M117 Lets make\n'
                        'G1 X8 Y20 Z0.3 F5000.0                        ; Move over to prevent blob squish',
 'max_layer_height': ['0.32'],
 'min_layer_height': ['0.10'],
 'name': 'Wanhao D12-300 0.4 nozzle',
 'nozzle_diameter': ['0.4'],
 'nozzle_type': 'undefine',
 'printable_area': ['0x0', '300x0', '300x300', '0x300'],
 'printable_height': '400',
 'printer_model': 'Wanhao D12-300',
 'printer_variant': '0.4',
 'retraction_length': ['5'],
 'retraction_minimum_travel': ['1.5'],
 'retraction_speed': ['40'],
 'setting_id': 'GM001',
 'type': 'machine'}
