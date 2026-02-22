from __future__ import annotations

VENDOR = "Kingroon"
INDEX = {
  "description": "Kingroon configuration files",
  "filament_list": [],
  "force_update": "1",
  "machine_list": [
    {
      "name": "fdm_machine_common",
      "sub_path": "machine/fdm_machine_common.json"
    },
    {
      "name": "Kingroon KP3S 3.0 0.4 nozzle",
      "sub_path": "machine/Kingroon KP3S 3.0 0.4 nozzle.json"
    },
    {
      "name": "Kingroon KP3S PRO S1 0.4 nozzle",
      "sub_path": "machine/Kingroon KP3S PRO S1 0.4 nozzle.json"
    },
    {
      "name": "fdm_klipper_common",
      "sub_path": "machine/fdm_klipper_common.json"
    },
    {
      "name": "Kingroon KLP1 0.4 nozzle",
      "sub_path": "machine/Kingroon KLP1 0.4 nozzle.json"
    },
    {
      "name": "Kingroon KP3S PRO V2 0.4 nozzle",
      "sub_path": "machine/Kingroon KP3S PRO V2 0.4 nozzle.json"
    },
    {
      "name": "Kingroon KP3S V1 0.4 nozzle",
      "sub_path": "machine/Kingroon KP3S V1 0.4 nozzle.json"
    }
  ],
  "machine_model_list": [
    {
      "name": "Kingroon KLP1",
      "sub_path": "machine/Kingroon KLP1.json"
    },
    {
      "name": "Kingroon KP3S 3.0",
      "sub_path": "machine/Kingroon KP3S 3.0.json"
    },
    {
      "name": "Kingroon KP3S PRO S1",
      "sub_path": "machine/Kingroon KP3S PRO S1.json"
    },
    {
      "name": "Kingroon KP3S PRO V2",
      "sub_path": "machine/Kingroon KP3S PRO V2.json"
    },
    {
      "name": "Kingroon KP3S V1",
      "sub_path": "machine/Kingroon KP3S V1.json"
    }
  ],
  "name": "Kingroon",
  "process_list": [
    {
      "name": "fdm_process_common",
      "sub_path": "process/fdm_process_common.json"
    },
    {
      "name": "0.08mm Standard @Kingroon KP3S PRO S1",
      "sub_path": "process/0.08mm Standard @Kingroon KP3S PRO S1.json"
    },
    {
      "name": "0.12mm Standard @Kingroon KLP1",
      "sub_path": "process/0.12mm Standard @Kingroon KLP1.json"
    },
    {
      "name": "0.12mm Standard @Kingroon KP3S PRO S1",
      "sub_path": "process/0.12mm Standard @Kingroon KP3S PRO S1.json"
    },
    {
      "name": "0.20mm Standard @Kingroon KLP1",
      "sub_path": "process/0.20mm Standard @Kingroon KLP1.json"
    },
    {
      "name": "0.20mm Standard @Kingroon KP3S PRO S1",
      "sub_path": "process/0.20mm Standard @Kingroon KP3S PRO S1.json"
    },
    {
      "name": "0.20mm Standard @Kingroon KP3S PRO V2",
      "sub_path": "process/0.20mm Standard @Kingroon KP3S PRO V2.json"
    },
    {
      "name": "0.20mm Standard @Kingroon KP3S V1",
      "sub_path": "process/0.20mm Standard @Kingroon KP3S V1.json"
    },
    {
      "name": "0.30mm Standard @Kingroon KP3S 3.0",
      "sub_path": "process/0.30mm Standard @Kingroon KP3S 3.0.json"
    }
  ],
  "url": "https://kingroon.com/",
  "version": "02.03.01.10"
}

MACHINE = {
  "machine/Kingroon KLP1 0.4 nozzle.json": {
    "bed_exclude_area": [
      "0x0"
    ],
    "before_layer_change_gcode": ";BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n",
    "change_filament_gcode": "",
    "default_filament_profile": "Generic PLA @System",
    "default_print_profile": "0.20mm Standard @Kingroon KLP1",
    "deretraction_speed": [
      "90"
    ],
    "enable_filament_ramming": "1",
    "extra_loading_move": "-2",
    "extruder_clearance_height_to_rod": "36",
    "extruder_clearance_radius": "65",
    "extruder_colour": [
      "#FCE94F"
    ],
    "from": "system",
    "high_current_on_filament_swap": "0",
    "inherits": "fdm_klipper_common",
    "instantiation": "true",
    "layer_change_gcode": ";AFTER_LAYER_CHANGE\n;[layer_z]",
    "machine_end_gcode": "G91; relative positioning\n G1 Z1.0 F3000 ; move z up little to prevent scratching of print\n G90; absolute positioning\n G1 X0 Y200 F1000 ; prepare for part removal\n M104 S0; turn off extruder\n M140 S0 ; turn off bed\n G1 X0 Y200 F1000 ; prepare for part removal\n M84 ; disable motors\n M106 S0 ; turn off fan",
    "machine_max_acceleration_e": [
      "5000",
      "5000"
    ],
    "machine_max_acceleration_extruding": [
      "5000",
      "20000"
    ],
    "machine_max_acceleration_retracting": [
      "5000",
      "5000"
    ],
    "machine_max_acceleration_travel": [
      "9000",
      "9000"
    ],
    "machine_max_acceleration_x": [
      "10000",
      "20000"
    ],
    "machine_max_acceleration_y": [
      "10000",
      "20000"
    ],
    "machine_max_acceleration_z": [
      "500",
      "200"
    ],
    "machine_max_jerk_e": [
      "2.5",
      "2.5"
    ],
    "machine_max_jerk_x": [
      "20",
      "9"
    ],
    "machine_max_jerk_y": [
      "20",
      "9"
    ],
    "machine_max_jerk_z": [
      "0.2",
      "0.4"
    ],
    "machine_max_speed_e": [
      "100",
      "25"
    ],
    "machine_max_speed_z": [
      "50",
      "12"
    ],
    "machine_pause_gcode": "PAUSE",
    "machine_start_gcode": "M190 S[bed_temperature_initial_layer_single]\nM109 S[nozzle_temperature_initial_layer]\nG28 ; h1ome all axes\n M117 ;Purge extruder\n G92 E0 ; reset extruder\n G1 Z1.0 F3000 ; move z up little to prevent scratching of surface\n G1 X2 Y20 Z0.3 F5000.0 ; move to start-line position\n G1 X2 Y175.0 Z0.3 F1500.0 E15 ; draw 1st line\n G1 X2 Y175.0 Z0.4 F5000.0 ; move to side a little\n G1 X2 Y20 Z0.4 F1500.0 E30 ; draw 2nd line\n G92 E0 ; reset extruder\n G1 Z1.0 F3000 ; move z up little to prevent scratching of surface",
    "machine_unload_filament_time": "0",
    "max_layer_height": [
      "0.32"
    ],
    "min_layer_height": "0.08",
    "name": "Kingroon KLP1 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "parking_pos_retraction": "92",
    "printable_area": [
      "0x0",
      "230x0",
      "230x230",
      "0x230"
    ],
    "printable_height": "210",
    "printer_model": "Kingroon KLP1",
    "purge_in_prime_tower": "1",
    "retract_lift_above": [
      "0"
    ],
    "retract_lift_below": [
      "0"
    ],
    "retract_lift_enforce": [
      "All Surfaces"
    ],
    "retraction_length": [
      "1"
    ],
    "retraction_speed": [
      "90"
    ],
    "setting_id": "GM003",
    "thumbnails": [
      "100x100"
    ],
    "type": "machine",
    "use_firmware_retraction": "0",
    "wipe": [
      "1"
    ],
    "z_hop": [
      "0"
    ]
  },
  "machine/Kingroon KLP1.json": {
    "default_materials": "Generic ABS @System;Generic PLA @System;Generic PLA-CF @System;Generic PETG @System;Generic TPU @System;Generic ASA @System;Generic PC @System;Generic PVA @System;Generic PA @System;Generic PA-CF @System",
    "family": "Kingroon",
    "hotend_model": "",
    "machine_tech": "FFF",
    "model_id": "Kingroon KLP1",
    "name": "Kingroon KLP1",
    "nozzle_diameter": "0.4",
    "type": "machine_model"
  },
  "machine/Kingroon KP3S 3.0 0.4 nozzle.json": {
    "cooling_tube_length": "0",
    "cooling_tube_retraction": "0",
    "default_print_profile": "0.30mm Standard @Kingroon KP3S 3.0",
    "enable_filament_ramming": "0",
    "extra_loading_move": "0",
    "fan_speedup_overhangs": "0",
    "fan_speedup_time": "1",
    "from": "system",
    "inherits": "fdm_machine_common",
    "instantiation": "true",
    "machine_end_gcode": "G1 E-1.0 F2100 ; retract\nG92 E0.0\nG1{if max_layer_z < max_print_height} Z{z_offset+min(max_layer_z+30, max_print_height)}{endif} E-34.0 F720 ; move print head up & retract filament\nG4 ; wait\nM104 S0 ; turn off temperature\nM140 S0 ; turn off heatbed\nM107 ; turn off fan\nG1 X0 Y105 F3000 ; park print head\nM84 ; disable motors",
    "machine_max_acceleration_e": [
      "10000",
      "5000"
    ],
    "machine_max_acceleration_extruding": [
      "10000",
      "9000"
    ],
    "machine_max_acceleration_retracting": [
      "10000",
      "9000"
    ],
    "machine_max_acceleration_x": [
      "4000",
      "9000"
    ],
    "machine_max_acceleration_y": [
      "4000",
      "9000"
    ],
    "machine_max_acceleration_z": [
      "1100",
      "100"
    ],
    "machine_max_speed_e": [
      "50",
      "60"
    ],
    "machine_max_speed_x": [
      "300",
      "200"
    ],
    "machine_max_speed_y": [
      "300",
      "200"
    ],
    "machine_max_speed_z": [
      "30",
      "12"
    ],
    "machine_start_gcode": "G90 ; use absolute coordinates\nM83 ; extruder relative mode\nM204 S[machine_max_acceleration_extruding] T[machine_max_acceleration_retracting]\nM104 S[first_layer_temperature] ; set extruder temp\nM140 S[first_layer_bed_temperature] ; set bed temp\nG28 ; home all\nG1 Y1.0 Z0.3 F1000 ; move print head up\nM190 S[first_layer_bed_temperature] ; wait for bed temp\nM109 S[first_layer_temperature] ; wait for extruder temp\nG92 E0.0\n; initial load\n M117 Purge extruder\n G1 X2 Y20 Z0.3 F5000.0 ; move to start-line position\n G1 X2 Y175.0 Z0.3 F1500.0 E15 ; draw 1st line\n G1 X2 Y175.0 Z0.4 F5000.0 ; move to side a little\n G1 X2 Y20 Z0.4 F1500.0 E30 ; draw 2nd line\n G92 E0 ; reset extruder\n G1 Z1.0 F3000 ; move z up little to prevent scratching of surface",
    "manual_filament_change": "1",
    "min_layer_height": [
      "0.1"
    ],
    "name": "Kingroon KP3S 3.0 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "nozzle_type": "brass",
    "parking_pos_retraction": "0",
    "printable_area": [
      "0x0",
      "180x0",
      "180x180",
      "0x180"
    ],
    "printable_height": "180",
    "printer_model": "Kingroon KP3S 3.0",
    "purge_in_prime_tower": "0",
    "retract_length_toolchange": [
      "0.5"
    ],
    "retract_when_changing_layer": [
      "1"
    ],
    "retraction_length": [
      "0.3"
    ],
    "retraction_minimum_travel": [
      "3"
    ],
    "retraction_speed": [
      "30"
    ],
    "setting_id": "GM003",
    "support_air_filtration": "0",
    "support_chamber_temp_control": "0",
    "type": "machine",
    "wipe": [
      "1"
    ],
    "z_hop": [
      "0.2"
    ]
  },
  "machine/Kingroon KP3S 3.0.json": {
    "bed_model": "kp3s_bed.stl",
    "bed_texture": "Kingroon_buildplate.png",
    "default_materials": "Generic ABS @System;Generic PLA @System;Generic PLA-CF @System;Generic PETG @System;Generic TPU @System;Generic ASA @System;Generic PC @System;Generic PVA @System;Generic PA @System;Generic PA-CF @System",
    "family": "Kingroon",
    "hotend_model": "",
    "machine_tech": "FFF",
    "model_id": "Kingroon KP3S 3.0",
    "name": "Kingroon KP3S 3.0",
    "nozzle_diameter": "0.4",
    "type": "machine_model"
  },
  "machine/Kingroon KP3S PRO S1 0.4 nozzle.json": {
    "default_print_profile": "0.20mm Standard @Kingroon KP3S PRO S1",
    "inherits": "fdm_machine_common",
    "instantiation": "true",
    "machine_end_gcode": "G1 E-1.0 F2100 ; retract\nG92 E0.0\nG1{if max_layer_z < max_print_height} Z{z_offset+min(max_layer_z+30, max_print_height)}{endif} E-34.0 F720 ; move print head up & retract filament\nG4 ; wait\nM104 S0 ; turn off temperature\nM140 S0 ; turn off heatbed\nM107 ; turn off fan\nG1 X0 Y105 F3000 ; park print head\nM84 ; disable motors",
    "machine_start_gcode": "G90 ; use absolute coordinates\nM83 ; extruder relative mode\nM204 S[machine_max_acceleration_extruding] T[machine_max_acceleration_retracting]\nM104 S[first_layer_temperature] ; set extruder temp\nM140 S[first_layer_bed_temperature] ; set bed temp\nG28 ; home all\nG1 Y1.0 Z0.3 F1000 ; move print head up\nM190 S[first_layer_bed_temperature] ; wait for bed temp\nM109 S[first_layer_temperature] ; wait for extruder temp\nG92 E0.0\n; initial load\n M117 Purge extruder\n G1 X2 Y20 Z0.3 F5000.0 ; move to start-line position\n G1 X2 Y175.0 Z0.3 F1500.0 E15 ; draw 1st line\n G1 X2 Y175.0 Z0.4 F5000.0 ; move to side a little\n G1 X2 Y20 Z0.4 F1500.0 E30 ; draw 2nd line\n G92 E0 ; reset extruder\n G1 Z1.0 F3000 ; move z up little to prevent scratching of surface",
    "name": "Kingroon KP3S PRO S1 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "printer_model": "Kingroon KP3S PRO S1",
    "setting_id": "GM003",
    "type": "machine"
  },
  "machine/Kingroon KP3S PRO S1.json": {
    "bed_model": "kp3s_bed.stl",
    "bed_texture": "Kingroon_buildplate.png",
    "default_materials": "Generic ABS @System;Generic PLA @System;Generic PLA-CF @System;Generic PETG @System;Generic TPU @System;Generic ASA @System;Generic PC @System;Generic PVA @System;Generic PA @System;Generic PA-CF @System",
    "family": "Kingroon",
    "hotend_model": "",
    "machine_tech": "FFF",
    "model_id": "Kingroon-KP3S-PRO-S1",
    "name": "Kingroon KP3S PRO S1",
    "nozzle_diameter": "0.4",
    "type": "machine_model"
  },
  "machine/Kingroon KP3S PRO V2 0.4 nozzle.json": {
    "bed_exclude_area": [
      "0x0"
    ],
    "before_layer_change_gcode": ";BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n",
    "default_filament_profile": "Generic PLA @System",
    "default_print_profile": "0.20mm Standard @Kingroon KP3S PRO V2",
    "deretraction_speed": [
      "45"
    ],
    "extruder_colour": [
      "#FCE94F"
    ],
    "from": "system",
    "inherits": "fdm_klipper_common",
    "instantiation": "true",
    "layer_change_gcode": ";AFTER_LAYER_CHANGE\n;[layer_z]",
    "machine_end_gcode": "{if max_layer_z < max_print_height}G1 Z{z_offset+min(max_layer_z+2, max_print_height)} F600 ; Move print head up{endif}\nG1 X5 Y200 F6000 ; present print\n{if max_layer_z < max_print_height-10}G1 Z{z_offset+min(max_layer_z+20, max_print_height-10)} F600 ; Move print head further up{endif}\n{if max_layer_z < max_print_height*0.6}G1 Z{max_print_height*0.6} F600 ; Move print head further up{endif}\nM140 S0 ; turn off heatbed\nM104 S0 ; turn off temperature\nM107 ; turn off fan\nM84 X Y E ; disable motors\nEND_PRINT",
    "machine_max_acceleration_e": [
      "10000",
      "5000"
    ],
    "machine_max_acceleration_extruding": [
      "10000",
      "9000"
    ],
    "machine_max_acceleration_retracting": [
      "10000",
      "9000"
    ],
    "machine_max_acceleration_x": [
      "10000",
      "9000"
    ],
    "machine_max_acceleration_y": [
      "10000",
      "9000"
    ],
    "machine_max_acceleration_z": [
      "10000",
      "100"
    ],
    "machine_max_jerk_e": [
      "20",
      "5"
    ],
    "machine_max_jerk_x": [
      "20",
      "7"
    ],
    "machine_max_jerk_y": [
      "20",
      "7"
    ],
    "machine_start_gcode": "START_PRINT EXTRUDER_TEMP=[first_layer_temperature] BED_TEMP=[first_layer_bed_temperature]\nCANCEL_POWEROFF\nG90 ; use absolute coordinates\nM83 ; extruder relative mode\nG92 E0",
    "max_layer_height": [
      "0.32"
    ],
    "name": "Kingroon KP3S PRO V2 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "printable_area": [
      "0x0",
      "205x0",
      "205x205",
      "0x205"
    ],
    "printable_height": "200",
    "printer_model": "Kingroon KP3S PRO V2",
    "retraction_length": [
      "0.8"
    ],
    "retraction_speed": [
      "45"
    ],
    "setting_id": "GM003",
    "type": "machine",
    "use_firmware_retraction": "1",
    "wipe": [
      "0"
    ],
    "z_hop": [
      "0"
    ]
  },
  "machine/Kingroon KP3S PRO V2.json": {
    "bed_model": "kp3s_bed.stl",
    "bed_texture": "Kingroon_buildplate.png",
    "default_materials": "Generic ABS @System;Generic PLA @System;Generic PLA-CF @System;Generic PETG @System;Generic TPU @System;Generic ASA @System;Generic PC @System;Generic PVA @System;Generic PA @System;Generic PA-CF @System",
    "family": "Kingroon",
    "hotend_model": "",
    "machine_tech": "FFF",
    "model_id": "Kingroon-KP3S-PRO-V2",
    "name": "Kingroon KP3S PRO V2",
    "nozzle_diameter": "0.4",
    "type": "machine_model"
  },
  "machine/Kingroon KP3S V1 0.4 nozzle.json": {
    "bed_exclude_area": [
      "0x0"
    ],
    "before_layer_change_gcode": ";BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n",
    "best_object_pos": "0.5,0.5",
    "change_extrusion_role_gcode": "",
    "change_filament_gcode": "",
    "cooling_tube_length": "0",
    "cooling_tube_retraction": "0",
    "default_filament_profile": "Generic PLA @System",
    "default_print_profile": "0.20mm Standard @Kingroon KP3S V1",
    "deretraction_speed": [
      "30"
    ],
    "disable_m73": "0",
    "emit_machine_limits_to_gcode": "1",
    "enable_filament_ramming": "0",
    "enable_long_retraction_when_cut": "0",
    "extra_loading_move": "0",
    "extruder_clearance_height_to_rod": "36",
    "extruder_clearance_radius": "65",
    "extruder_colour": [
      "#FCE94F"
    ],
    "from": "system",
    "head_wrap_detect_zone": [],
    "high_current_on_filament_swap": "0",
    "inherits": "fdm_klipper_common",
    "instantiation": "true",
    "layer_change_gcode": ";AFTER_LAYER_CHANGE\n;[layer_z]",
    "long_retractions_when_cut": [
      "0"
    ],
    "machine_end_gcode": "G91; relative positioning\n G1 Z1.0 F3000 ; move z up little to prevent scratching of print\n G90; absolute positioning\n G1 X0 Y180 F1000 ; prepare for part removal\n M104 S0; turn off extruder\n M140 S0 ; turn off bed\n G1 X0 Y180 F1000 ; prepare for part removal\n M84 ; disable motors\n M106 S0 ; turn off fan",
    "machine_max_acceleration_e": [
      "5000",
      "5000"
    ],
    "machine_max_acceleration_extruding": [
      "10000",
      "20000"
    ],
    "machine_max_acceleration_retracting": [
      "5000",
      "5000"
    ],
    "machine_max_acceleration_travel": [
      "20000",
      "20000"
    ],
    "machine_max_acceleration_x": [
      "10000",
      "20000"
    ],
    "machine_max_acceleration_y": [
      "10000",
      "20000"
    ],
    "machine_max_acceleration_z": [
      "500",
      "200"
    ],
    "machine_max_jerk_e": [
      "2.5",
      "2.5"
    ],
    "machine_max_jerk_x": [
      "9",
      "9"
    ],
    "machine_max_jerk_y": [
      "9",
      "9"
    ],
    "machine_max_jerk_z": [
      "0.2",
      "0.4"
    ],
    "machine_max_speed_e": [
      "100",
      "25"
    ],
    "machine_max_speed_z": [
      "12",
      "12"
    ],
    "machine_pause_gcode": "PAUSE",
    "machine_start_gcode": "M104 S{first_layer_temperature[0]} ; set final nozzle temp\nM190 S[bed_temperature_initial_layer_single]\nM109 S[nozzle_temperature_initial_layer]\nM83\nG28 ; h1ome all axes\nG1 Z0.2                                   ; lift nozzle a bit \nG92 E0 \nG1 Y-3 F2400   \nG1 X50 F2400                                  ; zero the extruded length \nG1 X115  E40 F500                       ; Extrude 25mm of filament in a 5cm line. \nG92 E0                                     ; zero the extruded length again \nG1 E-0.2 F3000                                ; Retract a little \nG1 X180 F4000                              ; Quickly wipe away from the filament line\nM117",
    "machine_unload_filament_time": "0",
    "manual_filament_change": "0",
    "max_layer_height": [
      "0.32"
    ],
    "min_layer_height": "0.08",
    "name": "Kingroon KP3S V1 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "nozzle_height": "4",
    "nozzle_type": "brass",
    "parking_pos_retraction": "0",
    "preferred_orientation": "0",
    "printable_area": [
      "0x0",
      "180x0",
      "180x180",
      "0x180"
    ],
    "printable_height": "180",
    "printer_model": "Kingroon KP3S V1",
    "printing_by_object_gcode": "",
    "purge_in_prime_tower": "0",
    "retract_before_wipe": [
      "0%"
    ],
    "retract_lift_above": [
      "0"
    ],
    "retract_lift_below": [
      "0"
    ],
    "retract_lift_enforce": [
      "All Surfaces"
    ],
    "retraction_distances_when_cut": [
      "18"
    ],
    "retraction_length": [
      "0.8"
    ],
    "retraction_speed": [
      "30"
    ],
    "setting_id": "GM003",
    "support_air_filtration": "1",
    "support_chamber_temp_control": "1",
    "support_multi_bed_types": "0",
    "thumbnails": [
      "100x100"
    ],
    "type": "machine",
    "use_firmware_retraction": "0",
    "wipe": [
      "1"
    ],
    "z_hop": [
      "0"
    ],
    "z_offset": "0"
  },
  "machine/Kingroon KP3S V1.json": {
    "default_materials": "Generic ABS @System;Generic PLA @System;Generic PLA-CF @System;Generic PETG @System;Generic TPU @System;Generic ASA @System;Generic PC @System;Generic PVA @System;Generic PA @System;Generic PA-CF @System",
    "family": "Kingroon",
    "hotend_model": "",
    "machine_tech": "FFF",
    "model_id": "Kingroon KP3S V1",
    "name": "Kingroon KP3S V1",
    "nozzle_diameter": "0.4",
    "type": "machine_model"
  },
  "machine/fdm_klipper_common.json": {
    "bed_exclude_area": [
      "0x0"
    ],
    "before_layer_change_gcode": ";BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n",
    "extruder_clearance_height_to_rod": "25",
    "extruder_clearance_radius": "45",
    "from": "system",
    "gcode_flavor": "klipper",
    "inherits": "fdm_machine_common",
    "instantiation": "false",
    "layer_change_gcode": ";AFTER_LAYER_CHANGE\n;[layer_z]",
    "machine_end_gcode": "END_PRINT",
    "machine_max_acceleration_extruding": [
      "9000",
      "9000"
    ],
    "machine_max_acceleration_retracting": [
      "9000",
      "9000"
    ],
    "machine_max_acceleration_x": [
      "9000",
      "9000"
    ],
    "machine_max_acceleration_y": [
      "9000",
      "9000"
    ],
    "machine_max_acceleration_z": [
      "100",
      "100"
    ],
    "machine_max_jerk_e": [
      "5",
      "5"
    ],
    "machine_max_jerk_x": [
      "7",
      "7"
    ],
    "machine_max_jerk_y": [
      "7",
      "7"
    ],
    "machine_max_jerk_z": [
      "0.4",
      "0.4"
    ],
    "machine_max_speed_e": [
      "60",
      "60"
    ],
    "machine_max_speed_x": [
      "500",
      "200"
    ],
    "machine_max_speed_y": [
      "500",
      "200"
    ],
    "machine_max_speed_z": [
      "12",
      "12"
    ],
    "machine_min_extruding_rate": [
      "0",
      "0"
    ],
    "machine_min_travel_rate": [
      "0",
      "0"
    ],
    "machine_pause_gcode": "M601",
    "machine_start_gcode": "START_PRINT EXTRUDER_TEMP=[nozzle_temperature_initial_layer] BED_TEMP=[bed_temperature_initial_layer_single]",
    "min_layer_height": [
      "0.05"
    ],
    "name": "fdm_klipper_common",
    "retract_before_wipe": [
      "70%"
    ],
    "retract_restart_extra": [
      "0"
    ],
    "retract_restart_extra_toolchange": [
      "0"
    ],
    "retract_when_changing_layer": [
      "1"
    ],
    "retraction_length": [
      "1.0"
    ],
    "retraction_minimum_travel": [
      "1"
    ],
    "type": "machine",
    "wipe": [
      "1"
    ],
    "z_hop": [
      "0.4"
    ],
    "z_hop_types": "Normal Lift"
  },
  "machine/fdm_machine_common.json": {
    "auxiliary_fan": "0",
    "before_layer_change_gcode": ";BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n",
    "change_filament_gcode": "M600",
    "deretraction_speed": [
      "30"
    ],
    "extruder_clearance_height_to_lid": "140",
    "extruder_clearance_height_to_rod": "36",
    "extruder_clearance_radius": "65",
    "extruder_colour": [
      "#018001"
    ],
    "extruder_offset": [
      "0x0"
    ],
    "fan_kickstart": "0",
    "fan_speedup_overhangs": "1",
    "fan_speedup_time": "0",
    "from": "system",
    "gcode_flavor": "marlin",
    "instantiation": "false",
    "layer_change_gcode": ";AFTER_LAYER_CHANGE\n;[layer_z]",
    "machine_end_gcode": "",
    "machine_load_filament_time": "0",
    "machine_max_acceleration_e": [
      "5000",
      "5000"
    ],
    "machine_max_acceleration_extruding": [
      "1250",
      "20000"
    ],
    "machine_max_acceleration_retracting": [
      "1250",
      "5000"
    ],
    "machine_max_acceleration_travel": [
      "20000",
      "20000"
    ],
    "machine_max_acceleration_x": [
      "3000",
      "20000"
    ],
    "machine_max_acceleration_y": [
      "3000",
      "20000"
    ],
    "machine_max_acceleration_z": [
      "200",
      "200"
    ],
    "machine_max_jerk_e": [
      "4.5",
      "2.5"
    ],
    "machine_max_jerk_x": [
      "12",
      "9"
    ],
    "machine_max_jerk_y": [
      "12",
      "9"
    ],
    "machine_max_jerk_z": [
      "0.4",
      "0.4"
    ],
    "machine_max_speed_e": [
      "120",
      "25"
    ],
    "machine_max_speed_x": [
      "200",
      "200"
    ],
    "machine_max_speed_y": [
      "200",
      "200"
    ],
    "machine_max_speed_z": [
      "12",
      "12"
    ],
    "machine_min_extruding_rate": [
      "0",
      "0"
    ],
    "machine_min_travel_rate": [
      "0",
      "0"
    ],
    "machine_pause_gcode": "M601",
    "max_layer_height": [
      "0.3"
    ],
    "min_layer_height": [
      "0.08"
    ],
    "name": "fdm_machine_common",
    "nozzle_diameter": [
      "0.4"
    ],
    "nozzle_hrc": "0",
    "nozzle_type": "undefine",
    "nozzle_volume": "0",
    "print_host": "",
    "print_host_webui": "",
    "printable_area": [
      "0x0",
      "200x0",
      "200x200",
      "0x200"
    ],
    "printable_height": "200",
    "printer_settings_id": "",
    "printer_technology": "FFF",
    "printer_variant": "0.4",
    "printhost_apikey": "",
    "printhost_authorization_type": "key",
    "printhost_cafile": "",
    "printhost_password": "",
    "printhost_port": "",
    "printhost_ssl_ignore_revoke": "0",
    "printhost_user": "",
    "retract_before_wipe": [
      "70%"
    ],
    "retract_length_toolchange": [
      "2"
    ],
    "retract_restart_extra": [
      "0"
    ],
    "retract_restart_extra_toolchange": [
      "0"
    ],
    "retract_when_changing_layer": [
      "0"
    ],
    "retraction_length": [
      "1.4"
    ],
    "retraction_minimum_travel": [
      "1"
    ],
    "retraction_speed": [
      "35"
    ],
    "scan_first_layer": "0",
    "silent_mode": "0",
    "single_extruder_multi_material": "1",
    "template_custom_gcode": "",
    "thumbnails": [
      "300x300"
    ],
    "type": "machine",
    "upward_compatible_machine": [],
    "use_firmware_retraction": "0",
    "use_relative_e_distances": "1",
    "wipe": [
      "0"
    ],
    "wipe_distance": [
      "2"
    ],
    "z_hop": [
      "0.3"
    ],
    "z_hop_types": [
      "Auto Lift"
    ]
  }
}

PROCESS = {
  "process/0.08mm Standard @Kingroon KP3S PRO S1.json": {
    "compatible_printers": [
      "Kingroon KP3S PRO S1 0.4 nozzle"
    ],
    "inherits": "fdm_process_common",
    "instantiation": "true",
    "layer_height": "0.08",
    "line_width": "0.4",
    "name": "0.08mm Standard @Kingroon KP3S PRO S1",
    "print_settings_id": "0.08mm Standard @Kingroon KP3S PRO S1",
    "type": "process"
  },
  "process/0.12mm Standard @Kingroon KLP1.json": {
    "compatible_printers": [
      "Kingroon KLP1 0.4 nozzle"
    ],
    "compatible_printers_condition": "",
    "inherits": "fdm_process_common",
    "initial_layer_print_height": "0.2",
    "instantiation": "true",
    "layer_height": "0.12",
    "line_width": "0.4",
    "name": "0.12mm Standard @Kingroon KLP1",
    "type": "process"
  },
  "process/0.12mm Standard @Kingroon KP3S PRO S1.json": {
    "compatible_printers": [
      "Kingroon KP3S PRO S1 0.4 nozzle"
    ],
    "inherits": "fdm_process_common",
    "instantiation": "true",
    "layer_height": "0.12",
    "line_width": "0.4",
    "name": "0.12mm Standard @Kingroon KP3S PRO S1",
    "print_settings_id": "0.12mm Standard @Kingroon KP3S PRO S1",
    "type": "process"
  },
  "process/0.20mm Standard @Kingroon KLP1.json": {
    "compatible_printers": [
      "Kingroon KLP1 0.4 nozzle"
    ],
    "compatible_printers_condition": "",
    "inherits": "fdm_process_common",
    "initial_layer_print_height": "0.2",
    "instantiation": "true",
    "layer_height": "0.2",
    "line_width": "0.42",
    "name": "0.20mm Standard @Kingroon KLP1",
    "type": "process"
  },
  "process/0.20mm Standard @Kingroon KP3S PRO S1.json": {
    "compatible_printers": [
      "Kingroon KP3S PRO S1 0.4 nozzle"
    ],
    "compatible_printers_condition": "",
    "inherits": "fdm_process_common",
    "initial_layer_print_height": "0.2",
    "instantiation": "true",
    "layer_height": "0.2",
    "line_width": "0.42",
    "name": "0.20mm Standard @Kingroon KP3S PRO S1",
    "type": "process"
  },
  "process/0.20mm Standard @Kingroon KP3S PRO V2.json": {
    "compatible_printers": [
      "Kingroon KP3S PRO V2 0.4 nozzle"
    ],
    "inherits": "fdm_process_common",
    "initial_layer_print_height": "0.2",
    "instantiation": "true",
    "layer_height": "0.2",
    "line_width": "0.42",
    "name": "0.20mm Standard @Kingroon KP3S PRO V2",
    "print_settings_id": "0.20mm Standard @Kingroon KP3S PRO V2",
    "type": "process"
  },
  "process/0.20mm Standard @Kingroon KP3S V1.json": {
    "bottom_shell_layers": "2",
    "bridge_speed": "30",
    "brim_type": "no_brim",
    "compatible_printers": [
      "Kingroon KP3S V1 0.4 nozzle"
    ],
    "default_acceleration": "10000",
    "detect_thin_wall": "1",
    "elefant_foot_compensation": "0.15",
    "gap_infill_speed": "60",
    "infill_wall_overlap": "8%",
    "inherits": "fdm_process_common",
    "initial_layer_print_height": "0.25",
    "initial_layer_travel_speed": "200",
    "instantiation": "true",
    "internal_solid_infill_acceleration": "6000",
    "internal_solid_infill_speed": "160",
    "name": "0.20mm Standard @Kingroon KP3S V1",
    "outer_wall_acceleration": "4000",
    "overhang_2_4_speed": "30",
    "overhang_reverse": "1",
    "overhang_reverse_internal_only": "1",
    "overhang_reverse_threshold": "0%",
    "overhang_speed_classic": "1",
    "seam_gap": "0.1",
    "seam_position": "back",
    "slow_down_layers": "2",
    "slowdown_for_curled_perimeters": "1",
    "sparse_infill_acceleration": "6000",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "300",
    "support_type": "normal(manual)",
    "thick_bridges": "1",
    "top_surface_acceleration": "5000",
    "top_surface_speed": "180",
    "travel_acceleration": "10000",
    "type": "process",
    "wall_generator": "classic",
    "wall_loops": "2",
    "wall_transition_angle": "25",
    "xy_hole_compensation": "0.1"
  },
  "process/0.30mm Standard @Kingroon KP3S 3.0.json": {
    "bottom_surface_pattern": "monotonicline",
    "bridge_acceleration": "500",
    "bridge_speed": "30",
    "brim_type": "no_brim",
    "compatible_printers": [
      "Kingroon KP3S 3.0 0.4 nozzle"
    ],
    "default_acceleration": "500",
    "detect_narrow_internal_solid_infill": "0",
    "dont_filter_internal_bridges": "limited",
    "elefant_foot_compensation": "0.2",
    "enable_prime_tower": "1",
    "enable_support": "0",
    "filter_out_gap_fill": "0.9",
    "flush_into_support": "0",
    "from": "User",
    "gap_fill_target": "topbottom",
    "gap_infill_speed": "40",
    "infill_combination": "1",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "500",
    "initial_layer_infill_speed": "50",
    "initial_layer_print_height": "0.3",
    "initial_layer_speed": "20",
    "initial_layer_travel_speed": "250",
    "inner_wall_acceleration": "700",
    "inner_wall_line_width": "0.44",
    "inner_wall_speed": "70",
    "instantiation": "true",
    "internal_bridge_speed": "50",
    "internal_solid_infill_acceleration": "2000",
    "internal_solid_infill_line_width": "0.5",
    "internal_solid_infill_pattern": "monotonicline",
    "internal_solid_infill_speed": "70",
    "layer_height": "0.3",
    "line_width": "0.44",
    "max_travel_detour_distance": "70",
    "max_volumetric_extrusion_rate_slope": "20",
    "name": "0.30mm Standard @Kingroon KP3S 3.0",
    "outer_wall_acceleration": "500",
    "outer_wall_line_width": "0.44",
    "outer_wall_speed": "50",
    "overhang_1_4_speed": "70%",
    "overhang_2_4_speed": "50%",
    "overhang_3_4_speed": "30%",
    "overhang_4_4_speed": "20%",
    "prime_tower_brim_width": "1",
    "prime_tower_width": "20",
    "prime_volume": "30",
    "print_settings_id": "0.30mm Standard @Kingroon KP3S 3.0",
    "raft_first_layer_density": "100%",
    "reduce_crossing_wall": "1",
    "reduce_infill_retraction": "0",
    "scarf_joint_speed": "70",
    "seam_gap": "0",
    "seam_slope_entire_loop": "1",
    "seam_slope_start_height": "0.1",
    "skirt_loops": "1",
    "sparse_infill_acceleration": "1500",
    "sparse_infill_line_width": "0.5",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "70",
    "support_base_pattern": "default",
    "support_interface_pattern": "auto",
    "support_interface_speed": "40",
    "support_line_width": "0.44",
    "support_speed": "70",
    "support_threshold_angle": "30",
    "support_type": "normal(auto)",
    "top_surface_acceleration": "500",
    "top_surface_line_width": "0.44",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "40",
    "travel_acceleration": "4000",
    "travel_speed": "250",
    "tree_support_angle_slow": "35",
    "tree_support_branch_angle_organic": "45",
    "tree_support_branch_diameter_double_wall": "5",
    "tree_support_tip_diameter": "1",
    "tree_support_top_rate": "50%",
    "type": "process",
    "wall_transition_angle": "59",
    "wipe_before_external_loop": "1",
    "wipe_tower_bridging": "2"
  },
  "process/fdm_process_common.json": {
    "accel_to_decel_enable": "0",
    "accel_to_decel_factor": "50%",
    "adaptive_layer_height": "0",
    "bottom_shell_layers": "3",
    "bottom_shell_thickness": "0",
    "bottom_solid_infill_flow_ratio": "1",
    "bottom_surface_pattern": "monotonic",
    "bridge_acceleration": "50%",
    "bridge_angle": "0",
    "bridge_density": "100%",
    "bridge_flow": "0.9",
    "bridge_no_support": "0",
    "bridge_speed": "50",
    "brim_object_gap": "0.1",
    "brim_type": "auto_brim",
    "brim_width": "5",
    "compatible_printers": [],
    "compatible_printers_condition": "",
    "default_acceleration": "3000",
    "default_jerk": "0",
    "detect_narrow_internal_solid_infill": "1",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "0",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0",
    "enable_arc_fitting": "0",
    "enable_overhang_speed": "1",
    "enable_prime_tower": "0",
    "enable_support": "1",
    "enforce_support_layers": "0",
    "ensure_vertical_shell_thickness": "1",
    "exclude_object": "1",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "filter_out_gap_fill": "0",
    "flush_into_infill": "0",
    "flush_into_objects": "0",
    "flush_into_support": "1",
    "from": "system",
    "fuzzy_skin": "none",
    "fuzzy_skin_point_distance": "0.8",
    "fuzzy_skin_thickness": "0.3",
    "gap_infill_speed": "100",
    "gcode_add_line_number": "0",
    "gcode_comments": "0",
    "gcode_label_objects": "1",
    "independent_support_layer_height": "1",
    "infill_anchor": "400%",
    "infill_anchor_max": "20",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_jerk": "9",
    "infill_wall_overlap": "25%",
    "initial_layer_acceleration": "700",
    "initial_layer_infill_speed": "105",
    "initial_layer_jerk": "9",
    "initial_layer_line_width": "0.5",
    "initial_layer_speed": "50",
    "initial_layer_travel_speed": "100%",
    "inner_wall_acceleration": "300",
    "inner_wall_jerk": "9",
    "inner_wall_line_width": "0.45",
    "inner_wall_speed": "100",
    "instantiation": "false",
    "interface_shells": "0",
    "internal_bridge_support_thickness": "0",
    "internal_solid_infill_acceleration": "100%",
    "internal_solid_infill_line_width": "0.42",
    "internal_solid_infill_speed": "100",
    "ironing_flow": "10%",
    "ironing_spacing": "0.15",
    "ironing_speed": "30",
    "ironing_type": "no ironing",
    "max_bridge_length": "30",
    "max_travel_detour_distance": "0",
    "min_bead_width": "85%",
    "min_feature_size": "25%",
    "minimum_sparse_infill_area": "15",
    "name": "fdm_process_common",
    "only_one_wall_first_layer": "0",
    "only_one_wall_top": "0",
    "ooze_prevention": "0",
    "outer_wall_acceleration": "3000",
    "outer_wall_jerk": "9",
    "outer_wall_line_width": "0.42",
    "outer_wall_speed": "80",
    "overhang_1_4_speed": "50",
    "overhang_2_4_speed": "40",
    "overhang_3_4_speed": "20",
    "overhang_4_4_speed": "10",
    "overhang_speed_classic": "0",
    "post_process": [],
    "precise_outer_wall": "0",
    "prime_tower_brim_width": "3",
    "prime_tower_width": "60",
    "prime_volume": "45",
    "print_sequence": "by layer",
    "print_settings_id": "",
    "raft_contact_distance": "0.1",
    "raft_expansion": "1.5",
    "raft_first_layer_density": "90%",
    "raft_first_layer_expansion": "2",
    "raft_layers": "0",
    "reduce_crossing_wall": "0",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "role_based_wipe_speed": "1",
    "seam_gap": "15%",
    "seam_position": "aligned",
    "skirt_distance": "2",
    "skirt_height": "1",
    "skirt_loops": "2",
    "slice_closing_radius": "0.049",
    "slicing_mode": "regular",
    "slow_down_layers": "0",
    "small_perimeter_speed": "50%",
    "small_perimeter_threshold": "0",
    "solid_infill_filament": "1",
    "sparse_infill_acceleration": "100%",
    "sparse_infill_density": "15%",
    "sparse_infill_filament": "1",
    "sparse_infill_line_width": "0.45",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "100",
    "spiral_mode": "0",
    "standby_temperature_delta": "-5",
    "support_angle": "0",
    "support_base_pattern": "rectilinear",
    "support_base_pattern_spacing": "2.5",
    "support_bottom_interface_spacing": "0.5",
    "support_bottom_z_distance": "0.2",
    "support_critical_regions_only": "0",
    "support_expansion": "0",
    "support_filament": "0",
    "support_interface_bottom_layers": "2",
    "support_interface_filament": "0",
    "support_interface_loop_pattern": "0",
    "support_interface_pattern": "rectilinear",
    "support_interface_spacing": "0.5",
    "support_interface_speed": "80",
    "support_interface_top_layers": "2",
    "support_line_width": "0.42",
    "support_object_xy_distance": "0.35",
    "support_on_build_plate_only": "0",
    "support_speed": "150",
    "support_style": "default",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.2",
    "support_type": "tree(auto)",
    "thick_bridges": "0",
    "timelapse_type": "0",
    "top_shell_layers": "4",
    "top_shell_thickness": "0.8",
    "top_solid_infill_flow_ratio": "1",
    "top_surface_acceleration": "3000",
    "top_surface_jerk": "9",
    "top_surface_line_width": "0.42",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "60",
    "travel_acceleration": "3000",
    "travel_jerk": "12",
    "travel_speed": "150",
    "travel_speed_z": "0",
    "tree_support_adaptive_layer_height": "1",
    "tree_support_auto_brim": "1",
    "tree_support_branch_angle": "45",
    "tree_support_branch_diameter": "5",
    "tree_support_branch_distance": "5",
    "tree_support_brim_width": "3",
    "tree_support_wall_count": "0",
    "tree_support_with_infill": "0",
    "type": "process",
    "wall_distribution_count": "1",
    "wall_filament": "1",
    "wall_generator": "arachne",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "3",
    "wall_transition_angle": "10",
    "wall_transition_filter_deviation": "25%",
    "wall_transition_length": "100%",
    "wipe_on_loops": "1",
    "wipe_speed": "80%",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  }
}

FILAMENT = {}

MISC = {}

ASSETS = [
  "Kingroon KLP1_cover.png",
  "Kingroon KP3S 3.0_cover.png",
  "Kingroon KP3S PRO S1_cover.png",
  "Kingroon KP3S PRO V2_cover.png",
  "Kingroon KP3S V1_cover.png",
  "Kingroon_buildplate.png",
  "kp3s_bed.stl",
  "mini_bed.stl"
]

ALL = {
  "vendor": VENDOR,
  "index": INDEX,
  "machine": MACHINE,
  "process": PROCESS,
  "filament": FILAMENT,
  "misc": MISC,
  "assets": ASSETS,
}
