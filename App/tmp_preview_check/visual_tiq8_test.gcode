; EON-OpenSlicer slicer_v2 semantic emitter
; firmware=marlin
G21 ; mm units
G90 ; absolute XYZ mode
M82 ; absolute extrusion
G92 E0
;LAYER:0
G0 Z0.050 F9000
G0 X110.000 Y110.000 F9000
G1 E-0.80000 F3600 ; retract
G1 X-140.000 Y-90.000 E9592.70560 F3600
M104 S0
M140 S0
G92 E0
M84
