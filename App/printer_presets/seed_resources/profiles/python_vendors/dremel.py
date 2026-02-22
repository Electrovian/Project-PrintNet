from __future__ import annotations

VENDOR = "Dremel"
INDEX = {
  "description": "Dremel configurations",
  "filament_list": [
    {
      "name": "fdm_filament_common",
      "sub_path": "filament/fdm_filament_common.json"
    },
    {
      "name": "fdm_filament_pla",
      "sub_path": "filament/fdm_filament_pla.json"
    },
    {
      "name": "Dremel Generic PLA",
      "sub_path": "filament/Dremel Generic PLA.json"
    },
    {
      "name": "Dremel Generic PLA @3D20 all",
      "sub_path": "filament/Dremel Generic PLA @3D20 all.json"
    },
    {
      "name": "Dremel Generic PLA @3D40 all",
      "sub_path": "filament/Dremel Generic PLA @3D40 all.json"
    },
    {
      "name": "Dremel Generic PLA @3D45 all",
      "sub_path": "filament/Dremel Generic PLA @3D45 all.json"
    }
  ],
  "force_update": "0",
  "machine_list": [
    {
      "name": "fdm_machine_common",
      "sub_path": "machine/fdm_machine_common.json"
    },
    {
      "name": "fdm_dremel_common",
      "sub_path": "machine/fdm_dremel_common.json"
    },
    {
      "name": "Dremel 3D20 0.4 nozzle",
      "sub_path": "machine/Dremel 3D20 0.4 nozzle.json"
    },
    {
      "name": "Dremel 3D40 0.4 nozzle",
      "sub_path": "machine/Dremel 3D40 0.4 nozzle.json"
    },
    {
      "name": "Dremel 3D45 0.4 nozzle",
      "sub_path": "machine/Dremel 3D45 0.4 nozzle.json"
    }
  ],
  "machine_model_list": [
    {
      "name": "Dremel 3D20",
      "sub_path": "machine/Dremel 3D20.json"
    },
    {
      "name": "Dremel 3D40",
      "sub_path": "machine/Dremel 3D40.json"
    },
    {
      "name": "Dremel 3D45",
      "sub_path": "machine/Dremel 3D45.json"
    }
  ],
  "name": "Dremel",
  "process_list": [
    {
      "name": "fdm_process_common",
      "sub_path": "process/fdm_process_common.json"
    },
    {
      "name": "fdm_process_dremel_common",
      "sub_path": "process/fdm_process_dremel_common.json"
    },
    {
      "name": ".05mm Super Detail @Dremel 3D40 0.4",
      "sub_path": "process/.05mm Super Detail @Dremel 3D40 0.4.json"
    },
    {
      "name": ".05mm Super Detail @Dremel 3D45 0.4",
      "sub_path": "process/.05mm Super Detail @Dremel 3D45 0.4.json"
    },
    {
      "name": ".10mm Detail @Dremel 3D20 0.4",
      "sub_path": "process/.10mm Detail @Dremel 3D20 0.4.json"
    },
    {
      "name": ".10mm Detail @Dremel 3D40 0.4",
      "sub_path": "process/.10mm Detail @Dremel 3D40 0.4.json"
    },
    {
      "name": ".10mm Detail @Dremel 3D45 0.4",
      "sub_path": "process/.10mm Detail @Dremel 3D45 0.4.json"
    },
    {
      "name": ".20mm Standard @Dremel 3D20 0.4",
      "sub_path": "process/.20mm Standard @Dremel 3D20 0.4.json"
    },
    {
      "name": ".20mm Standard @Dremel 3D40 0.4",
      "sub_path": "process/.20mm Standard @Dremel 3D40 0.4.json"
    },
    {
      "name": ".20mm Standard @Dremel 3D45 0.4",
      "sub_path": "process/.20mm Standard @Dremel 3D45 0.4.json"
    },
    {
      "name": ".30mm Draft @Dremel 3D20 0.4",
      "sub_path": "process/.30mm Draft @Dremel 3D20 0.4.json"
    },
    {
      "name": ".30mm Draft @Dremel 3D40 0.4",
      "sub_path": "process/.30mm Draft @Dremel 3D40 0.4.json"
    },
    {
      "name": ".30mm Draft @Dremel 3D45 0.4",
      "sub_path": "process/.30mm Draft @Dremel 3D45 0.4.json"
    },
    {
      "name": ".34mm SuperDraft @Dremel 3D40 0.4",
      "sub_path": "process/.34mm SuperDraft @Dremel 3D40 0.4.json"
    },
    {
      "name": ".34mm SuperDraft @Dremel 3D45 0.4",
      "sub_path": "process/.34mm SuperDraft @Dremel 3D45 0.4.json"
    }
  ],
  "version": "02.03.01.10"
}

MACHINE = {
  "machine/Dremel 3D20 0.4 nozzle.json": {
    "auxiliary_fan": "0",
    "default_filament_profile": [
      "Dremel Generic PLA @3D20 all"
    ],
    "default_print_profile": ".20mm Standard @Dremel 3D20 0.4",
    "deretraction_speed": [
      "40"
    ],
    "emit_machine_limits_to_gcode": "1",
    "extruder_clearance_height_to_lid": "101",
    "extruder_clearance_height_to_rod": "45",
    "extruder_clearance_radius": "45",
    "from": "system",
    "gcode_flavor": "marlin",
    "inherits": "fdm_dremel_common",
    "instantiation": "true",
    "machine_end_gcode": "M104 S0 T0\nG1 Z140 F3300\nG28 X0 Y0\nM132 X Y Z A\nG91\nM18",
    "machine_max_acceleration_e": [
      "6200",
      "5000"
    ],
    "machine_max_acceleration_extruding": [
      "6200",
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
      "6200",
      "20000"
    ],
    "machine_max_acceleration_y": [
      "6200",
      "20000"
    ],
    "machine_max_acceleration_z": [
      "500",
      "500"
    ],
    "machine_max_jerk_e": [
      "2.5",
      "2.5"
    ],
    "machine_max_jerk_x": [
      "12",
      "12"
    ],
    "machine_max_jerk_y": [
      "12",
      "12"
    ],
    "machine_max_jerk_z": [
      "2",
      "2"
    ],
    "machine_max_speed_e": [
      "3000",
      "100"
    ],
    "machine_max_speed_x": [
      "1000",
      "1000"
    ],
    "machine_max_speed_y": [
      "1000",
      "1000"
    ],
    "machine_max_speed_z": [
      "30",
      "30"
    ],
    "machine_start_gcode": "G90\nG28\nM132 X Y Z A\nG1 Z100 F3300\nG1 X-110.5 Y-74 F6000\nM6 T0\nM907 X100 Y100 Z60 A100\nG1 Z0.6 F3300\nG4 P2000\nM108 T0",
    "max_layer_height": [
      "0.3"
    ],
    "min_layer_height": [
      "0.08"
    ],
    "name": "Dremel 3D20 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "nozzle_type": "undefine",
    "printable_area": [
      "0x0",
      "230x0",
      "230x150",
      "0x150"
    ],
    "printable_height": "140",
    "printer_model": "Dremel 3D20",
    "printer_settings_id": "Dremel",
    "printer_structure": "hbot",
    "printer_variant": "0.4",
    "retract_before_wipe": [
      "70%"
    ],
    "retract_length_toolchange": [
      "1"
    ],
    "retract_lift_above": [
      "0"
    ],
    "retract_lift_below": [
      "0"
    ],
    "retract_lift_enforce": [
      "Top Only"
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
      "0.5"
    ],
    "retraction_minimum_travel": [
      "2"
    ],
    "retraction_speed": [
      "40"
    ],
    "setting_id": "GM001",
    "thumbnails": [
      "96x96",
      "300x300"
    ],
    "thumbnails_format": "PNG",
    "type": "machine",
    "wipe": [
      "1"
    ],
    "wipe_distance": [
      "1"
    ],
    "z_hop": [
      "0.2"
    ],
    "z_hop_types": [
      "Normal Lift"
    ]
  },
  "machine/Dremel 3D20.json": {
    "bed_model": "dremel_3d20_buildplate_model.stl",
    "bed_texture": "",
    "default_materials": "Dremel Generic PLA @3D20 all",
    "family": "Dremel",
    "hotend_model": "",
    "machine_tech": "FFF",
    "model_id": "Dremel_3D20",
    "name": "Dremel 3D20",
    "nozzle_diameter": "0.4",
    "type": "machine_model"
  },
  "machine/Dremel 3D40 0.4 nozzle.json": {
    "auxiliary_fan": "0",
    "default_filament_profile": [
      "Dremel Generic PLA @3D40 all"
    ],
    "default_print_profile": ".20mm Standard @Dremel 3D40 0.4",
    "deretraction_speed": [
      "40"
    ],
    "emit_machine_limits_to_gcode": "1",
    "enable_filament_ramming": "1",
    "extra_loading_move": "-2",
    "extruder_clearance_height_to_lid": "101",
    "extruder_clearance_height_to_rod": "45",
    "extruder_clearance_radius": "45",
    "fan_speedup_overhangs": "1",
    "from": "system",
    "gcode_flavor": "marlin",
    "inherits": "fdm_dremel_common",
    "instantiation": "true",
    "machine_end_gcode": "M104 S0\nM140 S0\nG92 E1\nG1 E-1 F300\nG162 Z F600\nG162 X Y F2000\nM84",
    "machine_max_acceleration_e": [
      "6200",
      "5000"
    ],
    "machine_max_acceleration_extruding": [
      "6200",
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
      "6200",
      "20000"
    ],
    "machine_max_acceleration_y": [
      "6200",
      "20000"
    ],
    "machine_max_acceleration_z": [
      "500",
      "500"
    ],
    "machine_max_jerk_e": [
      "2.5",
      "2.5"
    ],
    "machine_max_jerk_x": [
      "12",
      "12"
    ],
    "machine_max_jerk_y": [
      "12",
      "12"
    ],
    "machine_max_jerk_z": [
      "2",
      "2"
    ],
    "machine_max_speed_e": [
      "3000",
      "100"
    ],
    "machine_max_speed_x": [
      "1000",
      "1000"
    ],
    "machine_max_speed_y": [
      "1000",
      "1000"
    ],
    "machine_max_speed_z": [
      "30",
      "30"
    ],
    "machine_min_extruding_rate": [
      "0",
      "0"
    ],
    "machine_min_travel_rate": [
      "0",
      "0"
    ],
    "machine_start_gcode": "G90\nG28\nM132 X Y Z A\nG1 Z100 F3300\nG1 X-110.5 Y-74 F6000\nM6 T0\nM907 X100 Y100 Z60 A100\nG1 Z0.6 F3300\nG4 P2000\nM108 T0",
    "max_layer_height": [
      "0.34"
    ],
    "min_layer_height": [
      "0.05"
    ],
    "name": "Dremel 3D40 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "nozzle_type": "undefine",
    "printable_area": [
      "-127.5x-77.5",
      "97.5x-77.5",
      "97.5x77.5",
      "-127.5x77.5"
    ],
    "printable_height": "170",
    "printer_model": "Dremel 3D40",
    "printer_settings_id": "Dremel",
    "printer_structure": "hbot",
    "printer_variant": "0.4",
    "retract_before_wipe": [
      "70%"
    ],
    "retract_length_toolchange": [
      "1"
    ],
    "retract_lift_enforce": [
      "Top Only"
    ],
    "retract_when_changing_layer": [
      "1"
    ],
    "retraction_length": [
      "3"
    ],
    "retraction_minimum_travel": [
      "5"
    ],
    "retraction_speed": [
      "60"
    ],
    "setting_id": "GM001",
    "thumbnails": [
      "96x96",
      "300x300"
    ],
    "thumbnails_format": "PNG",
    "type": "machine",
    "use_relative_e_distances": "0",
    "wipe": [
      "1"
    ],
    "wipe_distance": [
      "1"
    ],
    "z_hop": [
      "0.5"
    ],
    "z_hop_types": [
      "Normal Lift"
    ]
  },
  "machine/Dremel 3D40.json": {
    "bed_model": "dremel_3d40_3d45_buildplate_model.stl",
    "bed_texture": "",
    "default_materials": "Dremel Generic PLA @3D40 all",
    "family": "Dremel",
    "hotend_model": "",
    "machine_tech": "FFF",
    "model_id": "Dremel_3D40",
    "name": "Dremel 3D40",
    "nozzle_diameter": "0.4",
    "type": "machine_model"
  },
  "machine/Dremel 3D45 0.4 nozzle.json": {
    "change_filament_gcode": "G5",
    "default_filament_profile": [
      "Dremel Generic PLA @3D45 all"
    ],
    "default_print_profile": ".20mm Standard @Dremel 3D45 0.4",
    "deretraction_speed": [
      "40"
    ],
    "emit_machine_limits_to_gcode": "1",
    "enable_filament_ramming": "1",
    "extra_loading_move": "-2",
    "from": "system",
    "gcode_flavor": "marlin",
    "inherits": "fdm_dremel_common",
    "instantiation": "true",
    "machine_end_gcode": "M104 S0; turn off nozzle\nM140 S0; turn off bed\nG92 E1; return print head to home\nG1 E-1 F300\nG162 Z F600\nG162 X Y F2000\nM84; disable stepper motors",
    "machine_max_acceleration_e": [
      "10000",
      "10000"
    ],
    "machine_max_acceleration_extruding": [
      "1500",
      "1500"
    ],
    "machine_max_acceleration_retracting": [
      "1500",
      "1500"
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
      "500",
      "500"
    ],
    "machine_max_jerk_e": [
      "2.5",
      "2.5"
    ],
    "machine_max_jerk_x": [
      "10",
      "10"
    ],
    "machine_max_jerk_y": [
      "10",
      "10"
    ],
    "machine_max_jerk_z": [
      "0.2",
      "0.2"
    ],
    "machine_max_speed_e": [
      "120",
      "120"
    ],
    "machine_max_speed_x": [
      "500",
      "500"
    ],
    "machine_max_speed_y": [
      "500",
      "500"
    ],
    "machine_max_speed_z": [
      "12",
      "12"
    ],
    "machine_pause_gcode": "G5",
    "machine_start_gcode": "G28; home printer\nG1 Z50.00 F400; pruge line\nG1 F200 E3\nM132 X Y Z A; prepare printer\nM907 X100 Y100 Z50 A100",
    "max_layer_height": [
      "0.34"
    ],
    "min_layer_height": [
      "0.07"
    ],
    "name": "Dremel 3D45 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "printable_area": [
      "-127.5x-77.5",
      "97.5x-77.5",
      "97.5x77.5",
      "-127.5x77.5"
    ],
    "printable_height": "170",
    "printer_model": "Dremel 3D45",
    "printer_settings_id": "Dremel",
    "printer_variant": "0.4",
    "retraction_length": [
      "1"
    ],
    "retraction_minimum_travel": [
      "2"
    ],
    "retraction_speed": [
      "40"
    ],
    "setting_id": "GM001",
    "type": "machine",
    "use_relative_e_distances": "0",
    "wipe": [
      "1"
    ],
    "wipe_distance": [
      "1"
    ],
    "z_hop": [
      "0.5"
    ]
  },
  "machine/Dremel 3D45.json": {
    "bed_model": "dremel_3d45.stl",
    "bed_texture": "",
    "default_materials": "Dremel Generic PLA @3D45 all",
    "family": "Dremel",
    "hotend_model": "",
    "machine_tech": "FFF",
    "model_id": "Dremel_3D45",
    "name": "Dremel 3D45",
    "nozzle_diameter": "0.4",
    "type": "machine_model"
  },
  "machine/fdm_dremel_common.json": {
    "auxiliary_fan": "0",
    "bed_exclude_area": [
      "0x0"
    ],
    "change_filament_gcode": "",
    "default_filament_profile": [
      "Dremel Generic PLA"
    ],
    "deretraction_speed": [
      "40"
    ],
    "extruder_clearance_height_to_lid": "34",
    "extruder_clearance_height_to_rod": "34",
    "extruder_clearance_radius": "47",
    "from": "system",
    "gcode_flavor": "marlin",
    "inherits": "fdm_machine_common",
    "instantiation": "false",
    "layer_change_gcode": "",
    "machine_end_gcode": "{if max_layer_z < printable_height}G1 Z{min(max_layer_z+2, printable_height)} F600 ; Move print head up{endif}\nG1 X5 Y{print_bed_max[1]*0.8} F{travel_speed*60} ; present print\n{if max_layer_z < printable_height-10}G1 Z{min(max_layer_z+70, printable_height-10)} F600 ; Move print head further up{endif}\n{if max_layer_z < printable_height*0.6}G1 Z{printable_height*0.6} F600 ; Move print head further up{endif}\nM140 S0 ; turn off heatbed\nM104 S0 ; turn off temperature\nM107 ; turn off fan\nM84 X Y E ; disable motors",
    "machine_max_acceleration_e": [
      "5000",
      "5000"
    ],
    "machine_max_acceleration_extruding": [
      "500",
      "500"
    ],
    "machine_max_acceleration_retracting": [
      "1000",
      "1000"
    ],
    "machine_max_acceleration_travel": [
      "500",
      "500"
    ],
    "machine_max_acceleration_x": [
      "500",
      "500"
    ],
    "machine_max_acceleration_y": [
      "500",
      "500"
    ],
    "machine_max_acceleration_z": [
      "500",
      "500"
    ],
    "machine_max_jerk_e": [
      "5",
      "5"
    ],
    "machine_max_jerk_x": [
      "8",
      "8"
    ],
    "machine_max_jerk_y": [
      "8",
      "8"
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
      "500"
    ],
    "machine_max_speed_y": [
      "500",
      "500"
    ],
    "machine_max_speed_z": [
      "10",
      "10"
    ],
    "machine_min_extruding_rate": [
      "0",
      "0"
    ],
    "machine_min_travel_rate": [
      "0",
      "0"
    ],
    "machine_pause_gcode": "M25 ;pause print",
    "machine_start_gcode": "G90 ; use absolute coordinates\nM83 ; extruder relative mode\nM140 S[bed_temperature_initial_layer] ; set final bed temp\nM104 S150 ; set temporary nozzle temp to prevent oozing during homing\nG4 S10 ; allow partial nozzle warmup\nG28 ; home all axis\nG1 Z50 F240\nG1 X2 Y10 F3000\nM104 S[nozzle_temperature_initial_layer] ; set final nozzle temp\nM190 S[bed_temperature_initial_layer] ; wait for bed temp to stabilize\nM109 S[nozzle_temperature_initial_layer] ; wait for nozzle temp to stabilize\nG1 Z0.28 F240\nG92 E0\nG1 Y140 E10 F1500 ; prime the nozzle\nG1 X2.3 F5000\nG92 E0\nG1 Y10 E10 F1200 ; prime the nozzle\nG92 E0",
    "max_layer_height": [
      "0.32"
    ],
    "min_layer_height": [
      "0.08"
    ],
    "name": "fdm_dremel_common",
    "nozzle_type": "undefine",
    "printable_height": "250",
    "printer_settings_id": "",
    "printer_technology": "FFF",
    "printer_variant": "0.4",
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
      "1"
    ],
    "retraction_length": [
      "5"
    ],
    "retraction_minimum_travel": [
      "2"
    ],
    "retraction_speed": [
      "60"
    ],
    "scan_first_layer": "0",
    "silent_mode": "0",
    "single_extruder_multi_material": "1",
    "type": "machine",
    "wipe": [
      "1"
    ],
    "z_hop": [
      "0.4"
    ]
  },
  "machine/fdm_machine_common.json": {
    "before_layer_change_gcode": ";BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n",
    "change_filament_gcode": "",
    "default_print_profile": "0.16mm Optimal @Bambu Lab X1 Carbon 0.4 nozzle",
    "deretraction_speed": [
      "40"
    ],
    "extruder_clearance_height_to_lid": "140",
    "extruder_clearance_height_to_rod": "36",
    "extruder_clearance_radius": "65",
    "extruder_colour": [
      "#FCE94F"
    ],
    "extruder_offset": [
      "0x0"
    ],
    "from": "system",
    "gcode_flavor": "marlin",
    "instantiation": "false",
    "machine_end_gcode": "M400 ; wait for buffer to clear\nG92 E0 ; zero the extruder\nG1 E-4.0 F3600; retract \nG91\nG1 Z3;\nM104 S0 ; turn off hotend\nM140 S0 ; turn off bed\nM106 S0 ; turn off fan\nG90 \nG0 X110 Y200 F3600 \nprint_end",
    "machine_max_acceleration_e": [
      "5000"
    ],
    "machine_max_acceleration_extruding": [
      "10000"
    ],
    "machine_max_acceleration_retracting": [
      "1000"
    ],
    "machine_max_acceleration_x": [
      "10000"
    ],
    "machine_max_acceleration_y": [
      "10000"
    ],
    "machine_max_acceleration_z": [
      "500"
    ],
    "machine_max_jerk_e": [
      "5"
    ],
    "machine_max_jerk_x": [
      "8"
    ],
    "machine_max_jerk_y": [
      "8"
    ],
    "machine_max_jerk_z": [
      "0.4"
    ],
    "machine_max_speed_e": [
      "60"
    ],
    "machine_max_speed_x": [
      "500"
    ],
    "machine_max_speed_y": [
      "500"
    ],
    "machine_max_speed_z": [
      "10"
    ],
    "machine_min_extruding_rate": [
      "0"
    ],
    "machine_min_travel_rate": [
      "0"
    ],
    "machine_start_gcode": "G0 Z20 F9000\nG92 E0; G1 E-10 F1200\nG28\nM970 Q1 A10 B10 C130 K0\nM970 Q1 A10 B131 C250 K1\nM974 Q1 S1 P0\nM970 Q0 A10 B10 C130 H20 K0\nM970 Q0 A10 B131 C250 K1\nM974 Q0 S1 P0\nM220 S100 ;Reset Feedrate\nM221 S100 ;Reset Flowrate\nG29 ;Home\nG90;\nG92 E0 ;Reset Extruder \nG1 Z2.0 F3000 ;Move Z Axis up \nG1 X10.1 Y20 Z0.28 F5000.0 ;Move to start position\nM109 S205;\nG1 X10.1 Y200.0 Z0.28 F1500.0 E15 ;Draw the first line\nG1 X10.4 Y200.0 Z0.28 F5000.0 ;Move to side a little\nG1 X10.4 Y20 Z0.28 F1500.0 E30 ;Draw the second line\nG92 E0 ;Reset Extruder \nG1 X110 Y110 Z2.0 F3000 ;Move Z Axis up",
    "max_layer_height": [
      "0.32"
    ],
    "min_layer_height": [
      "0.08"
    ],
    "name": "fdm_machine_common",
    "nozzle_diameter": [
      "0.4"
    ],
    "printable_height": "250",
    "printer_settings_id": "",
    "printer_technology": "FFF",
    "printer_variant": "0.4",
    "retract_before_wipe": [
      "70%"
    ],
    "retract_length_toolchange": [
      "1"
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
      "1"
    ],
    "retraction_minimum_travel": [
      "2"
    ],
    "retraction_speed": [
      "60"
    ],
    "silent_mode": "0",
    "single_extruder_multi_material": "1",
    "support_air_filtration": "0",
    "support_chamber_temp_control": "0",
    "type": "machine",
    "wipe": [
      "1"
    ],
    "z_hop": [
      "0"
    ],
    "z_hop_types": "Normal Lift"
  }
}

PROCESS = {
  "process/.05mm Super Detail @Dremel 3D40 0.4.json": {
    "adaptive_layer_height": "0",
    "bottom_shell_layers": "10",
    "bottom_shell_thickness": "1",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "1",
    "bridge_no_support": "0",
    "bridge_speed": "50",
    "brim_object_gap": "0.1",
    "brim_width": "5",
    "compatible_printers": [
      "Dremel 3D40 0.4 nozzle"
    ],
    "default_acceleration": "2000",
    "detect_overhang_wall": "1",
    "enable_support": "1",
    "filename_format": "{input_filename_base}_{filament_type[0]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "30",
    "infill_combination": "1",
    "infill_direction": "45",
    "infill_wall_overlap": "15%",
    "inherits": "fdm_process_dremel_common",
    "initial_layer_acceleration": "2000",
    "initial_layer_infill_speed": "15",
    "initial_layer_line_width": "0.5",
    "initial_layer_print_height": "0.05",
    "initial_layer_speed": "22",
    "inner_wall_acceleration": "2000",
    "inner_wall_line_width": "0.45",
    "inner_wall_speed": "40",
    "instantiation": "true",
    "internal_bridge_support_thickness": "0.8",
    "internal_solid_infill_line_width": "0.42",
    "internal_solid_infill_speed": "40",
    "ironing_flow": "10%",
    "ironing_spacing": "0.15",
    "ironing_speed": "30",
    "ironing_type": "top",
    "layer_height": "0.05",
    "line_width": "0.42",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "15",
    "name": ".05mm Super Detail @Dremel 3D40 0.4",
    "only_one_wall_top": "1",
    "outer_wall_acceleration": "2000",
    "outer_wall_line_width": "0.42",
    "outer_wall_speed": "30",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "50",
    "overhang_3_4_speed": "30",
    "overhang_4_4_speed": "10",
    "print_sequence": "by layer",
    "raft_first_layer_density": "100%",
    "raft_first_layer_expansion": "1.5",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "seam_position": "aligned",
    "skirt_distance": "2",
    "skirt_height": "1",
    "skirt_loops": "7",
    "slow_down_layers": "2",
    "sparse_infill_density": "20%",
    "sparse_infill_line_width": "0.45",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "45",
    "support_base_pattern": "default",
    "support_base_pattern_spacing": "2.5",
    "support_bottom_z_distance": "0.1",
    "support_expansion": "1.5",
    "support_interface_bottom_layers": "2",
    "support_interface_pattern": "auto",
    "support_interface_spacing": "0.5",
    "support_interface_speed": "40",
    "support_interface_top_layers": "2",
    "support_line_width": "0.42",
    "support_object_xy_distance": "1.4",
    "support_speed": "45",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.1",
    "top_shell_layers": "10",
    "top_shell_thickness": "1",
    "top_surface_acceleration": "2000",
    "top_surface_line_width": "0.42",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "15",
    "travel_acceleration": "2000",
    "travel_speed": "100",
    "type": "process",
    "wall_generator": "arachne",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "3"
  },
  "process/.05mm Super Detail @Dremel 3D45 0.4.json": {
    "adaptive_layer_height": "0",
    "bottom_shell_layers": "20",
    "bottom_shell_thickness": "1",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "1",
    "bridge_no_support": "0",
    "bridge_speed": "50",
    "brim_object_gap": "0.1",
    "brim_width": "5",
    "compatible_printers": [
      "Dremel 3D45 0.4 nozzle"
    ],
    "default_acceleration": "2000",
    "detect_overhang_wall": "1",
    "enable_support": "1",
    "filename_format": "{input_filename_base}_{filament_type[0]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "35",
    "infill_combination": "1",
    "infill_direction": "45",
    "infill_wall_overlap": "12%",
    "inherits": "fdm_process_dremel_common",
    "initial_layer_acceleration": "2000",
    "initial_layer_infill_speed": "25",
    "initial_layer_line_width": "0.4",
    "initial_layer_print_height": "0.05",
    "initial_layer_speed": "25",
    "inner_wall_acceleration": "2000",
    "inner_wall_line_width": "0.4",
    "inner_wall_speed": "50",
    "instantiation": "true",
    "internal_bridge_support_thickness": "0.8",
    "internal_solid_infill_line_width": "0.4",
    "internal_solid_infill_speed": "40",
    "ironing_flow": "10%",
    "ironing_spacing": "0.15",
    "ironing_speed": "30",
    "ironing_type": "top",
    "layer_height": "0.05",
    "line_width": "0.4",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "15",
    "name": ".05mm Super Detail @Dremel 3D45 0.4",
    "only_one_wall_top": "1",
    "outer_wall_acceleration": "2000",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "35",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "50",
    "overhang_3_4_speed": "30",
    "overhang_4_4_speed": "10",
    "print_sequence": "by layer",
    "raft_first_layer_density": "100%",
    "raft_first_layer_expansion": "1.5",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "seam_position": "aligned",
    "skirt_distance": "2",
    "skirt_height": "1",
    "skirt_loops": "5",
    "slow_down_layers": "2",
    "sparse_infill_density": "20%",
    "sparse_infill_line_width": "0.4",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "50",
    "support_base_pattern": "default",
    "support_base_pattern_spacing": "2.5",
    "support_bottom_z_distance": "0.4",
    "support_expansion": "1.5",
    "support_interface_bottom_layers": "2",
    "support_interface_pattern": "auto",
    "support_interface_spacing": "0.5",
    "support_interface_speed": "50",
    "support_interface_top_layers": "2",
    "support_line_width": "0.4",
    "support_object_xy_distance": "1",
    "support_speed": "50",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.4",
    "top_shell_layers": "20",
    "top_shell_thickness": "1",
    "top_surface_acceleration": "2000",
    "top_surface_line_width": "0.4",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "35",
    "travel_acceleration": "2000",
    "travel_speed": "100",
    "type": "process",
    "wall_generator": "arachne",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "3"
  },
  "process/.10mm Detail @Dremel 3D20 0.4.json": {
    "adaptive_layer_height": "0",
    "bottom_shell_layers": "6",
    "bottom_shell_thickness": "1",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "1",
    "bridge_no_support": "0",
    "bridge_speed": "50",
    "brim_object_gap": "0.1",
    "brim_width": "5",
    "compatible_printers": [
      "Dremel 3D20 0.4 nozzle"
    ],
    "default_acceleration": "5000",
    "detect_overhang_wall": "1",
    "enable_support": "1",
    "filename_format": "{input_filename_base}_{filament_type[0]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "45",
    "infill_combination": "1",
    "infill_direction": "45",
    "infill_wall_overlap": "18%",
    "inherits": "fdm_process_dremel_common",
    "initial_layer_acceleration": "2000",
    "initial_layer_infill_speed": "20",
    "initial_layer_line_width": "0.4",
    "initial_layer_print_height": "0.1",
    "initial_layer_speed": "20",
    "inner_wall_acceleration": "5000",
    "inner_wall_line_width": "0.4",
    "inner_wall_speed": "50",
    "instantiation": "true",
    "internal_bridge_support_thickness": "0.8",
    "internal_solid_infill_line_width": "0.4",
    "internal_solid_infill_speed": "45",
    "ironing_flow": "10%",
    "ironing_spacing": "0.15",
    "ironing_speed": "30",
    "ironing_type": "top",
    "layer_height": "0.1",
    "line_width": "0.4",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "15",
    "name": ".10mm Detail @Dremel 3D20 0.4",
    "only_one_wall_top": "1",
    "outer_wall_acceleration": "2500",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "30",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "50",
    "overhang_3_4_speed": "30",
    "overhang_4_4_speed": "10",
    "print_sequence": "by layer",
    "raft_first_layer_density": "10%",
    "raft_first_layer_expansion": "1.5",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "seam_position": "aligned",
    "skirt_distance": "2",
    "skirt_height": "1",
    "skirt_loops": "3",
    "slow_down_layers": "2",
    "sparse_infill_density": "30%",
    "sparse_infill_line_width": "0.4",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "45",
    "support_base_pattern": "default",
    "support_base_pattern_spacing": "3.5",
    "support_bottom_z_distance": "0.4",
    "support_expansion": "1.5",
    "support_interface_bottom_layers": "2",
    "support_interface_pattern": "auto",
    "support_interface_spacing": "0.5",
    "support_interface_speed": "50",
    "support_interface_top_layers": "2",
    "support_line_width": "0.4",
    "support_object_xy_distance": "1",
    "support_speed": "45",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.4",
    "top_shell_layers": "6",
    "top_shell_thickness": "1",
    "top_surface_acceleration": "1000",
    "top_surface_line_width": "0.4",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "45",
    "travel_acceleration": "5000",
    "travel_speed": "90",
    "type": "process",
    "wall_distribution_count": "2",
    "wall_generator": "arachne",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "3"
  },
  "process/.10mm Detail @Dremel 3D40 0.4.json": {
    "adaptive_layer_height": "0",
    "bottom_shell_layers": "10",
    "bottom_shell_thickness": "1",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "1",
    "bridge_no_support": "0",
    "bridge_speed": "50",
    "brim_object_gap": "0.1",
    "brim_width": "5",
    "compatible_printers": [
      "Dremel 3D40 0.4 nozzle"
    ],
    "default_acceleration": "2000",
    "detect_overhang_wall": "1",
    "enable_support": "1",
    "filename_format": "{input_filename_base}_{filament_type[0]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "55",
    "infill_combination": "1",
    "infill_direction": "45",
    "infill_wall_overlap": "12%",
    "inherits": "fdm_process_dremel_common",
    "initial_layer_acceleration": "2000",
    "initial_layer_infill_speed": "25",
    "initial_layer_line_width": "0.5",
    "initial_layer_print_height": "0.1",
    "initial_layer_speed": "25",
    "inner_wall_acceleration": "2000",
    "inner_wall_line_width": "0.45",
    "inner_wall_speed": "60",
    "instantiation": "true",
    "internal_bridge_support_thickness": "0.8",
    "internal_solid_infill_line_width": "0.42",
    "internal_solid_infill_speed": "60",
    "ironing_flow": "10%",
    "ironing_spacing": "0.15",
    "ironing_speed": "30",
    "ironing_type": "top",
    "layer_height": "0.1",
    "line_width": "0.42",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "15",
    "name": ".10mm Detail @Dremel 3D40 0.4",
    "only_one_wall_top": "1",
    "outer_wall_acceleration": "2000",
    "outer_wall_line_width": "0.42",
    "outer_wall_speed": "35",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "50",
    "overhang_3_4_speed": "30",
    "overhang_4_4_speed": "10",
    "print_sequence": "by layer",
    "raft_first_layer_density": "100%",
    "raft_first_layer_expansion": "1.5",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "seam_position": "aligned",
    "skirt_distance": "2",
    "skirt_height": "1",
    "skirt_loops": "5",
    "slow_down_layers": "2",
    "sparse_infill_density": "20%",
    "sparse_infill_line_width": "0.45",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "55",
    "support_base_pattern": "default",
    "support_base_pattern_spacing": "2.5",
    "support_bottom_z_distance": "0.1",
    "support_expansion": "1.5",
    "support_interface_bottom_layers": "2",
    "support_interface_pattern": "auto",
    "support_interface_spacing": "0.68",
    "support_interface_speed": "55",
    "support_interface_top_layers": "2",
    "support_line_width": "0.42",
    "support_object_xy_distance": "1",
    "support_speed": "60",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.1",
    "top_shell_layers": "10",
    "top_shell_thickness": "1",
    "top_surface_acceleration": "2000",
    "top_surface_line_width": "0.42",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "35",
    "travel_acceleration": "2000",
    "travel_speed": "120",
    "type": "process",
    "wall_generator": "arachne",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "3"
  },
  "process/.10mm Detail @Dremel 3D45 0.4.json": {
    "adaptive_layer_height": "0",
    "bottom_shell_layers": "10",
    "bottom_shell_thickness": "1",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "1",
    "bridge_no_support": "0",
    "bridge_speed": "50",
    "brim_object_gap": "0.1",
    "brim_width": "5",
    "compatible_printers": [
      "Dremel 3D45 0.4 nozzle"
    ],
    "default_acceleration": "2000",
    "detect_overhang_wall": "1",
    "enable_support": "1",
    "filename_format": "{input_filename_base}_{filament_type[0]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "35",
    "infill_combination": "1",
    "infill_direction": "45",
    "infill_wall_overlap": "12%",
    "inherits": "fdm_process_dremel_common",
    "initial_layer_acceleration": "2000",
    "initial_layer_infill_speed": "25",
    "initial_layer_line_width": "0.4",
    "initial_layer_print_height": "0.1",
    "initial_layer_speed": "25",
    "inner_wall_acceleration": "2000",
    "inner_wall_line_width": "0.4",
    "inner_wall_speed": "50",
    "instantiation": "true",
    "internal_bridge_support_thickness": "0.8",
    "internal_solid_infill_line_width": "0.4",
    "internal_solid_infill_speed": "40",
    "ironing_flow": "10%",
    "ironing_spacing": "0.15",
    "ironing_speed": "30",
    "ironing_type": "top",
    "layer_height": "0.1",
    "line_width": "0.4",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "15",
    "name": ".10mm Detail @Dremel 3D45 0.4",
    "only_one_wall_top": "1",
    "outer_wall_acceleration": "2000",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "35",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "50",
    "overhang_3_4_speed": "30",
    "overhang_4_4_speed": "10",
    "print_sequence": "by layer",
    "raft_first_layer_density": "100%",
    "raft_first_layer_expansion": "1.5",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "seam_position": "aligned",
    "skirt_distance": "2",
    "skirt_height": "1",
    "skirt_loops": "5",
    "slow_down_layers": "2",
    "sparse_infill_density": "20%",
    "sparse_infill_line_width": "0.4",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "50",
    "support_base_pattern": "default",
    "support_base_pattern_spacing": "2.5",
    "support_bottom_z_distance": "0.4",
    "support_expansion": "1.5",
    "support_interface_bottom_layers": "2",
    "support_interface_pattern": "auto",
    "support_interface_spacing": "0.5",
    "support_interface_speed": "50",
    "support_interface_top_layers": "2",
    "support_line_width": "0.4",
    "support_object_xy_distance": "1",
    "support_speed": "50",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.4",
    "top_shell_layers": "10",
    "top_shell_thickness": "1",
    "top_surface_acceleration": "2000",
    "top_surface_line_width": "0.4",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "35",
    "travel_acceleration": "2000",
    "travel_speed": "100",
    "type": "process",
    "wall_generator": "arachne",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "3"
  },
  "process/.20mm Standard @Dremel 3D20 0.4.json": {
    "adaptive_layer_height": "0",
    "bottom_shell_layers": "4",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.95",
    "bridge_no_support": "0",
    "bridge_speed": "25",
    "brim_object_gap": "0.1",
    "brim_width": "5",
    "compatible_printers": [
      "Dremel 3D20 0.4 nozzle"
    ],
    "default_acceleration": "5000",
    "detect_overhang_wall": "1",
    "enable_support": "1",
    "filename_format": "{input_filename_base}_{filament_type[0]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "50",
    "infill_combination": "1",
    "infill_direction": "45",
    "infill_wall_overlap": "25%",
    "inherits": "fdm_process_dremel_common",
    "initial_layer_acceleration": "2000",
    "initial_layer_infill_speed": "35%",
    "initial_layer_line_width": "0.42",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "50",
    "inner_wall_acceleration": "5000",
    "inner_wall_line_width": "0.45",
    "inner_wall_speed": "60",
    "instantiation": "true",
    "internal_bridge_support_thickness": "0.8",
    "internal_solid_infill_line_width": "0.4",
    "internal_solid_infill_speed": "60",
    "ironing_flow": "15%",
    "ironing_spacing": "0.1",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.2",
    "line_width": "0.45",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": ".20mm Standard @Dremel 3D20 0.4",
    "only_one_wall_top": "1",
    "outer_wall_acceleration": "2500",
    "outer_wall_line_width": "0.45",
    "outer_wall_speed": "60",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "20",
    "overhang_3_4_speed": "15",
    "overhang_4_4_speed": "10",
    "print_sequence": "by layer",
    "raft_first_layer_density": "10%",
    "raft_first_layer_expansion": "1.5",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "seam_position": "aligned",
    "skirt_distance": "2",
    "skirt_height": "1",
    "skirt_loops": "3",
    "slow_down_layers": "2",
    "sparse_infill_density": "18%",
    "sparse_infill_line_width": "0.45",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "60",
    "support_base_pattern": "default",
    "support_base_pattern_spacing": "3.5",
    "support_bottom_z_distance": "0.4",
    "support_expansion": "1.5",
    "support_interface_bottom_layers": "1",
    "support_interface_pattern": "auto",
    "support_interface_spacing": "0.2",
    "support_interface_speed": "100%",
    "support_interface_top_layers": "3",
    "support_line_width": "0.38",
    "support_object_xy_distance": "60%",
    "support_speed": "50",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.3",
    "top_shell_layers": "4",
    "top_shell_thickness": "0.8",
    "top_surface_acceleration": "1000",
    "top_surface_line_width": "0.4",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "50",
    "travel_acceleration": "5000",
    "travel_speed": "100",
    "type": "process",
    "wall_distribution_count": "2",
    "wall_generator": "arachne",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "3"
  },
  "process/.20mm Standard @Dremel 3D40 0.4.json": {
    "adaptive_layer_height": "0",
    "bottom_shell_layers": "4",
    "bottom_shell_thickness": "1",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "1",
    "bridge_no_support": "0",
    "bridge_speed": "50",
    "brim_object_gap": "0.1",
    "brim_width": "5",
    "compatible_printers": [
      "Dremel 3D40 0.4 nozzle"
    ],
    "default_acceleration": "2000",
    "detect_overhang_wall": "1",
    "enable_support": "1",
    "filename_format": "{input_filename_base}_{filament_type[0]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "55",
    "infill_combination": "1",
    "infill_direction": "45",
    "infill_wall_overlap": "12%",
    "inherits": "fdm_process_dremel_common",
    "initial_layer_acceleration": "2000",
    "initial_layer_infill_speed": "25",
    "initial_layer_line_width": "0.5",
    "initial_layer_print_height": "0.1",
    "initial_layer_speed": "25",
    "inner_wall_acceleration": "2000",
    "inner_wall_line_width": "0.45",
    "inner_wall_speed": "60",
    "instantiation": "true",
    "internal_bridge_support_thickness": "0.8",
    "internal_solid_infill_line_width": "0.42",
    "internal_solid_infill_speed": "60",
    "ironing_flow": "10%",
    "ironing_spacing": "0.15",
    "ironing_speed": "30",
    "ironing_type": "top",
    "layer_height": "0.2",
    "line_width": "0.42",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "15",
    "name": ".20mm Standard @Dremel 3D40 0.4",
    "only_one_wall_top": "1",
    "outer_wall_acceleration": "2000",
    "outer_wall_line_width": "0.42",
    "outer_wall_speed": "30",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "50",
    "overhang_3_4_speed": "30",
    "overhang_4_4_speed": "10",
    "print_sequence": "by layer",
    "raft_first_layer_density": "100%",
    "raft_first_layer_expansion": "1.5",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "seam_position": "aligned",
    "skirt_distance": "2",
    "skirt_height": "1",
    "skirt_loops": "5",
    "slow_down_layers": "2",
    "sparse_infill_density": "20%",
    "sparse_infill_line_width": "0.45",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "55",
    "support_base_pattern": "default",
    "support_base_pattern_spacing": "2.5",
    "support_bottom_z_distance": "0.4",
    "support_expansion": "1.5",
    "support_interface_bottom_layers": "2",
    "support_interface_pattern": "auto",
    "support_interface_spacing": "0.68",
    "support_interface_speed": "55",
    "support_interface_top_layers": "2",
    "support_line_width": "0.42",
    "support_object_xy_distance": "1",
    "support_speed": "60",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.4",
    "top_shell_layers": "4",
    "top_shell_thickness": "1",
    "top_surface_acceleration": "2000",
    "top_surface_line_width": "0.42",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "35",
    "travel_acceleration": "2000",
    "travel_speed": "120",
    "type": "process",
    "wall_generator": "arachne",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "3"
  },
  "process/.20mm Standard @Dremel 3D45 0.4.json": {
    "adaptive_layer_height": "0",
    "bottom_shell_layers": "4",
    "bottom_shell_thickness": "1",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "1",
    "bridge_no_support": "0",
    "bridge_speed": "50",
    "brim_object_gap": "0.1",
    "brim_width": "5",
    "compatible_printers": [
      "Dremel 3D45 0.4 nozzle"
    ],
    "default_acceleration": "2000",
    "detect_overhang_wall": "1",
    "enable_support": "1",
    "filename_format": "{input_filename_base}_{filament_type[0]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "35",
    "infill_combination": "1",
    "infill_direction": "45",
    "infill_wall_overlap": "12%",
    "inherits": "fdm_process_dremel_common",
    "initial_layer_acceleration": "2000",
    "initial_layer_infill_speed": "25",
    "initial_layer_line_width": "0.4",
    "initial_layer_print_height": "0.1",
    "initial_layer_speed": "25",
    "inner_wall_acceleration": "2000",
    "inner_wall_line_width": "0.4",
    "inner_wall_speed": "60",
    "instantiation": "true",
    "internal_bridge_support_thickness": "0.8",
    "internal_solid_infill_line_width": "0.4",
    "internal_solid_infill_speed": "50",
    "ironing_flow": "10%",
    "ironing_spacing": "0.15",
    "ironing_speed": "30",
    "ironing_type": "top",
    "layer_height": "0.2",
    "line_width": "0.4",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "15",
    "name": ".20mm Standard @Dremel 3D45 0.4",
    "only_one_wall_top": "1",
    "outer_wall_acceleration": "2000",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "30",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "50",
    "overhang_3_4_speed": "30",
    "overhang_4_4_speed": "10",
    "print_sequence": "by layer",
    "raft_first_layer_density": "100%",
    "raft_first_layer_expansion": "1.5",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "seam_position": "aligned",
    "skirt_distance": "2",
    "skirt_height": "1",
    "skirt_loops": "5",
    "slow_down_layers": "2",
    "sparse_infill_density": "20%",
    "sparse_infill_line_width": "0.4",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "55",
    "support_base_pattern": "default",
    "support_base_pattern_spacing": "2.5",
    "support_bottom_z_distance": "0.4",
    "support_expansion": "1.5",
    "support_interface_bottom_layers": "2",
    "support_interface_pattern": "auto",
    "support_interface_spacing": "0.5",
    "support_interface_speed": "50",
    "support_interface_top_layers": "2",
    "support_line_width": "0.4",
    "support_object_xy_distance": "1",
    "support_speed": "55",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.4",
    "top_shell_layers": "4",
    "top_shell_thickness": "1",
    "top_surface_acceleration": "2000",
    "top_surface_line_width": "0.4",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "35",
    "travel_acceleration": "2000",
    "travel_speed": "100",
    "type": "process",
    "wall_generator": "arachne",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "3"
  },
  "process/.30mm Draft @Dremel 3D20 0.4.json": {
    "adaptive_layer_height": "0",
    "bottom_shell_layers": "6",
    "bottom_shell_thickness": "1",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "1",
    "bridge_no_support": "0",
    "bridge_speed": "50",
    "brim_object_gap": "0.1",
    "brim_width": "5",
    "compatible_printers": [
      "Dremel 3D20 0.4 nozzle"
    ],
    "default_acceleration": "5000",
    "detect_overhang_wall": "1",
    "enable_support": "1",
    "filename_format": "{input_filename_base}_{filament_type[0]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "50",
    "infill_combination": "1",
    "infill_direction": "45",
    "infill_wall_overlap": "18%",
    "inherits": "fdm_process_dremel_common",
    "initial_layer_acceleration": "2000",
    "initial_layer_infill_speed": "50",
    "initial_layer_line_width": "0.4",
    "initial_layer_print_height": "0.3",
    "initial_layer_speed": "20",
    "inner_wall_acceleration": "5000",
    "inner_wall_line_width": "0.4",
    "inner_wall_speed": "60",
    "instantiation": "true",
    "internal_bridge_support_thickness": "0.8",
    "internal_solid_infill_line_width": "0.4",
    "internal_solid_infill_speed": "60",
    "ironing_flow": "10%",
    "ironing_spacing": "0.15",
    "ironing_speed": "30",
    "ironing_type": "top",
    "layer_height": "0.3",
    "line_width": "0.4",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "15",
    "name": ".30mm Draft @Dremel 3D20 0.4",
    "only_one_wall_top": "1",
    "outer_wall_acceleration": "2500",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "60",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "50",
    "overhang_3_4_speed": "30",
    "overhang_4_4_speed": "10",
    "print_sequence": "by layer",
    "raft_first_layer_density": "10%",
    "raft_first_layer_expansion": "1.5",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "seam_position": "aligned",
    "skirt_distance": "2",
    "skirt_height": "1",
    "skirt_loops": "3",
    "slow_down_layers": "2",
    "sparse_infill_density": "18%",
    "sparse_infill_line_width": "0.4",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "60",
    "support_base_pattern": "default",
    "support_base_pattern_spacing": "3.5",
    "support_bottom_z_distance": "0.4",
    "support_expansion": "1.5",
    "support_interface_bottom_layers": "2",
    "support_interface_pattern": "auto",
    "support_interface_spacing": "0.5",
    "support_interface_speed": "50",
    "support_interface_top_layers": "2",
    "support_line_width": "0.4",
    "support_object_xy_distance": "1",
    "support_speed": "50",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.3",
    "top_shell_layers": "3",
    "top_shell_thickness": "1",
    "top_surface_acceleration": "1000",
    "top_surface_line_width": "0.4",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "50",
    "travel_acceleration": "5000",
    "travel_speed": "100",
    "type": "process",
    "wall_distribution_count": "2",
    "wall_generator": "arachne",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "3"
  },
  "process/.30mm Draft @Dremel 3D40 0.4.json": {
    "adaptive_layer_height": "0",
    "bottom_shell_layers": "10",
    "bottom_shell_thickness": "1",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "1",
    "bridge_no_support": "0",
    "bridge_speed": "50",
    "brim_object_gap": "0.1",
    "brim_width": "5",
    "compatible_printers": [
      "Dremel 3D40 0.4 nozzle"
    ],
    "default_acceleration": "2000",
    "detect_overhang_wall": "1",
    "enable_support": "1",
    "filename_format": "{input_filename_base}_{filament_type[0]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "55",
    "infill_combination": "1",
    "infill_direction": "45",
    "infill_wall_overlap": "12%",
    "inherits": "fdm_process_dremel_common",
    "initial_layer_acceleration": "2000",
    "initial_layer_infill_speed": "25",
    "initial_layer_line_width": "0.5",
    "initial_layer_print_height": "0.3",
    "initial_layer_speed": "25",
    "inner_wall_acceleration": "2000",
    "inner_wall_line_width": "0.45",
    "inner_wall_speed": "60",
    "instantiation": "true",
    "internal_bridge_support_thickness": "0.8",
    "internal_solid_infill_line_width": "0.42",
    "internal_solid_infill_speed": "60",
    "ironing_flow": "10%",
    "ironing_spacing": "0.15",
    "ironing_speed": "30",
    "ironing_type": "top",
    "layer_height": "0.3",
    "line_width": "0.42",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "15",
    "name": ".30mm Draft @Dremel 3D40 0.4",
    "only_one_wall_top": "1",
    "outer_wall_acceleration": "2000",
    "outer_wall_line_width": "0.42",
    "outer_wall_speed": "60",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "50",
    "overhang_3_4_speed": "30",
    "overhang_4_4_speed": "10",
    "print_sequence": "by layer",
    "raft_first_layer_density": "100%",
    "raft_first_layer_expansion": "1.5",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "seam_position": "aligned",
    "skirt_distance": "2",
    "skirt_height": "1",
    "skirt_loops": "5",
    "slow_down_layers": "2",
    "sparse_infill_density": "20%",
    "sparse_infill_line_width": "0.45",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "55",
    "support_base_pattern": "default",
    "support_base_pattern_spacing": "2.5",
    "support_bottom_z_distance": "0.3",
    "support_expansion": "1.5",
    "support_interface_bottom_layers": "2",
    "support_interface_pattern": "auto",
    "support_interface_spacing": "0.68",
    "support_interface_speed": "55",
    "support_interface_top_layers": "2",
    "support_line_width": "0.42",
    "support_object_xy_distance": "1",
    "support_speed": "60",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.3",
    "top_shell_layers": "3",
    "top_shell_thickness": "1",
    "top_surface_acceleration": "2000",
    "top_surface_line_width": "0.42",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "55",
    "travel_acceleration": "2000",
    "travel_speed": "120",
    "type": "process",
    "wall_generator": "arachne",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "3"
  },
  "process/.30mm Draft @Dremel 3D45 0.4.json": {
    "adaptive_layer_height": "0",
    "bottom_shell_layers": "10",
    "bottom_shell_thickness": "1",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "1",
    "bridge_no_support": "0",
    "bridge_speed": "50",
    "brim_object_gap": "0.1",
    "brim_width": "5",
    "compatible_printers": [
      "Dremel 3D45 0.4 nozzle"
    ],
    "default_acceleration": "2000",
    "detect_overhang_wall": "1",
    "enable_support": "1",
    "filename_format": "{input_filename_base}_{filament_type[0]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "35",
    "infill_combination": "1",
    "infill_direction": "45",
    "infill_wall_overlap": "12%",
    "inherits": "fdm_process_dremel_common",
    "initial_layer_acceleration": "2000",
    "initial_layer_infill_speed": "25",
    "initial_layer_line_width": "0.4",
    "initial_layer_print_height": "0.3",
    "initial_layer_speed": "25",
    "inner_wall_acceleration": "2000",
    "inner_wall_line_width": "0.4",
    "inner_wall_speed": "60",
    "instantiation": "true",
    "internal_bridge_support_thickness": "0.8",
    "internal_solid_infill_line_width": "0.4",
    "internal_solid_infill_speed": "50",
    "ironing_flow": "10%",
    "ironing_spacing": "0.15",
    "ironing_speed": "30",
    "ironing_type": "top",
    "layer_height": "0.3",
    "line_width": "0.4",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "15",
    "name": ".30mm Draft @Dremel 3D45 0.4",
    "only_one_wall_top": "1",
    "outer_wall_acceleration": "2000",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "30",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "50",
    "overhang_3_4_speed": "30",
    "overhang_4_4_speed": "10",
    "print_sequence": "by layer",
    "raft_first_layer_density": "100%",
    "raft_first_layer_expansion": "1.5",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "seam_position": "aligned",
    "skirt_distance": "2",
    "skirt_height": "1",
    "skirt_loops": "5",
    "slow_down_layers": "2",
    "sparse_infill_density": "20%",
    "sparse_infill_line_width": "0.4",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "55",
    "support_base_pattern": "default",
    "support_base_pattern_spacing": "2.5",
    "support_bottom_z_distance": "0.6",
    "support_expansion": "1.5",
    "support_interface_bottom_layers": "2",
    "support_interface_pattern": "auto",
    "support_interface_spacing": "0.5",
    "support_interface_speed": "50",
    "support_interface_top_layers": "2",
    "support_line_width": "0.4",
    "support_object_xy_distance": "1",
    "support_speed": "55",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.6",
    "top_shell_layers": "3",
    "top_shell_thickness": "1",
    "top_surface_acceleration": "2000",
    "top_surface_line_width": "0.4",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "35",
    "travel_acceleration": "2000",
    "travel_speed": "100",
    "type": "process",
    "wall_generator": "arachne",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "3"
  },
  "process/.34mm SuperDraft @Dremel 3D40 0.4.json": {
    "adaptive_layer_height": "0",
    "bottom_shell_layers": "10",
    "bottom_shell_thickness": "1",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "1",
    "bridge_no_support": "0",
    "bridge_speed": "50",
    "brim_object_gap": "0.1",
    "brim_width": "5",
    "compatible_printers": [
      "Dremel 3D40 0.4 nozzle"
    ],
    "default_acceleration": "2000",
    "detect_overhang_wall": "1",
    "enable_support": "1",
    "filename_format": "{input_filename_base}_{filament_type[0]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "55",
    "infill_combination": "1",
    "infill_direction": "45",
    "infill_wall_overlap": "12%",
    "inherits": "fdm_process_dremel_common",
    "initial_layer_acceleration": "2000",
    "initial_layer_infill_speed": "30",
    "initial_layer_line_width": "0.5",
    "initial_layer_print_height": "0.34",
    "initial_layer_speed": "30",
    "inner_wall_acceleration": "2000",
    "inner_wall_line_width": "0.45",
    "inner_wall_speed": "70",
    "instantiation": "true",
    "internal_bridge_support_thickness": "0.8",
    "internal_solid_infill_line_width": "0.42",
    "internal_solid_infill_speed": "60",
    "ironing_flow": "10%",
    "ironing_spacing": "0.15",
    "ironing_speed": "30",
    "ironing_type": "top",
    "layer_height": "0.34",
    "line_width": "0.42",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "15",
    "name": ".34mm SuperDraft @Dremel 3D40 0.4",
    "only_one_wall_top": "1",
    "outer_wall_acceleration": "2000",
    "outer_wall_line_width": "0.42",
    "outer_wall_speed": "70",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "50",
    "overhang_3_4_speed": "30",
    "overhang_4_4_speed": "10",
    "print_sequence": "by layer",
    "raft_first_layer_density": "100%",
    "raft_first_layer_expansion": "1.5",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "seam_position": "aligned",
    "skirt_distance": "2",
    "skirt_height": "1",
    "skirt_loops": "5",
    "slow_down_layers": "2",
    "sparse_infill_density": "10%",
    "sparse_infill_line_width": "0.45",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "65",
    "support_base_pattern": "default",
    "support_base_pattern_spacing": "2.5",
    "support_bottom_z_distance": "0.34",
    "support_expansion": "1.5",
    "support_interface_bottom_layers": "2",
    "support_interface_pattern": "auto",
    "support_interface_spacing": "0.68",
    "support_interface_speed": "55",
    "support_interface_top_layers": "2",
    "support_line_width": "0.42",
    "support_object_xy_distance": "0.34",
    "support_speed": "60",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.34",
    "top_shell_layers": "3",
    "top_shell_thickness": "1",
    "top_surface_acceleration": "2000",
    "top_surface_line_width": "0.42",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "55",
    "travel_acceleration": "2000",
    "travel_speed": "120",
    "type": "process",
    "wall_generator": "arachne",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "3"
  },
  "process/.34mm SuperDraft @Dremel 3D45 0.4.json": {
    "adaptive_layer_height": "0",
    "bottom_shell_layers": "10",
    "bottom_shell_thickness": "1",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "1",
    "bridge_no_support": "0",
    "bridge_speed": "50",
    "brim_object_gap": "0.1",
    "brim_width": "5",
    "compatible_printers": [
      "Dremel 3D45 0.4 nozzle"
    ],
    "default_acceleration": "2000",
    "detect_overhang_wall": "1",
    "enable_support": "1",
    "filename_format": "{input_filename_base}_{filament_type[0]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "35",
    "infill_combination": "1",
    "infill_direction": "45",
    "infill_wall_overlap": "12%",
    "inherits": "fdm_process_dremel_common",
    "initial_layer_acceleration": "2000",
    "initial_layer_infill_speed": "35",
    "initial_layer_line_width": "0.48",
    "initial_layer_print_height": "0.34",
    "initial_layer_speed": "35",
    "inner_wall_acceleration": "2000",
    "inner_wall_line_width": "0.48",
    "inner_wall_speed": "70",
    "instantiation": "true",
    "internal_bridge_support_thickness": "0.8",
    "internal_solid_infill_line_width": "0.56",
    "internal_solid_infill_speed": "50",
    "ironing_flow": "10%",
    "ironing_spacing": "0.15",
    "ironing_speed": "30",
    "ironing_type": "top",
    "layer_height": "0.34",
    "line_width": "0.48",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "15",
    "name": ".34mm SuperDraft @Dremel 3D45 0.4",
    "only_one_wall_top": "1",
    "outer_wall_acceleration": "2000",
    "outer_wall_line_width": "0.48",
    "outer_wall_speed": "35",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "50",
    "overhang_3_4_speed": "30",
    "overhang_4_4_speed": "10",
    "print_sequence": "by layer",
    "raft_first_layer_density": "100%",
    "raft_first_layer_expansion": "1.5",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "seam_position": "aligned",
    "skirt_distance": "2",
    "skirt_height": "1",
    "skirt_loops": "5",
    "slow_down_layers": "2",
    "sparse_infill_density": "10%",
    "sparse_infill_line_width": "0.56",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "70",
    "support_base_pattern": "default",
    "support_base_pattern_spacing": "2.5",
    "support_bottom_z_distance": "0.68",
    "support_expansion": "1.5",
    "support_interface_bottom_layers": "2",
    "support_interface_pattern": "auto",
    "support_interface_spacing": "0.5",
    "support_interface_speed": "55",
    "support_interface_top_layers": "2",
    "support_line_width": "0.48",
    "support_object_xy_distance": "1",
    "support_speed": "60",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.68",
    "top_shell_layers": "3",
    "top_shell_thickness": "1",
    "top_surface_acceleration": "2000",
    "top_surface_line_width": "0.48",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "35",
    "travel_acceleration": "2000",
    "travel_speed": "100",
    "type": "process",
    "wall_generator": "arachne",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "3"
  },
  "process/fdm_process_common.json": {
    "adaptive_layer_height": "0",
    "bridge_flow": "0.95",
    "bridge_no_support": "0",
    "bridge_speed": "25",
    "brim_width": "5",
    "compatible_printers": [],
    "default_acceleration": "10000",
    "detect_overhang_wall": "0",
    "detect_thin_wall": "0",
    "elefant_foot_compensation": "0.1",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "filename_format": "{input_filename_base}.gcode",
    "from": "system",
    "gap_infill_speed": "30",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "25%",
    "initial_layer_line_width": "0.42",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "20",
    "inner_wall_line_width": "0.45",
    "inner_wall_speed": "40",
    "instantiation": "false",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0.45",
    "internal_solid_infill_speed": "40",
    "line_width": "0.45",
    "minimum_sparse_infill_area": "0",
    "name": "fdm_process_common",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "120",
    "prime_tower_width": "60",
    "print_sequence": "by layer",
    "print_settings_id": "",
    "raft_layers": "0",
    "reduce_crossing_wall": "0",
    "reduce_infill_retraction": "0",
    "seam_position": "nearest",
    "skirt_distance": "2",
    "skirt_height": "2",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.45",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "50",
    "spiral_mode": "0",
    "standby_temperature_delta": "-5",
    "support_base_pattern": "rectilinear",
    "support_base_pattern_spacing": "2",
    "support_filament": "0",
    "support_interface_filament": "0",
    "support_interface_loop_pattern": "0",
    "support_interface_spacing": "0",
    "support_interface_speed": "80",
    "support_interface_top_layers": "2",
    "support_line_width": "0.42",
    "support_object_xy_distance": "0.5",
    "support_on_build_plate_only": "0",
    "support_speed": "40",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.15",
    "top_surface_line_width": "0.4",
    "top_surface_speed": "30",
    "travel_speed": "400",
    "type": "process",
    "wall_loops": "3",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/fdm_process_dremel_common.json": {
    "adaptive_layer_height": "0",
    "bottom_shell_layers": "3",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.95",
    "bridge_no_support": "0",
    "bridge_speed": "25",
    "brim_object_gap": "0.1",
    "brim_width": "5",
    "compatible_printers_condition": "",
    "default_acceleration": "500",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "0",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "30",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "23%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "500",
    "initial_layer_infill_speed": "20",
    "initial_layer_line_width": "0.5",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "15",
    "inner_wall_acceleration": "500",
    "inner_wall_line_width": "0.45",
    "inner_wall_speed": "40",
    "instantiation": "false",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0.4",
    "internal_solid_infill_speed": "40",
    "ironing_flow": "15%",
    "ironing_spacing": "0.1",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.2",
    "line_width": "0.4",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "15",
    "name": "fdm_process_dremel_common",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "25",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "20",
    "overhang_3_4_speed": "15",
    "overhang_4_4_speed": "10",
    "prime_tower_width": "60",
    "print_sequence": "by layer",
    "print_settings_id": "",
    "raft_layers": "0",
    "reduce_crossing_wall": "0",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "seam_position": "aligned",
    "skirt_distance": "2",
    "skirt_height": "1",
    "skirt_loops": "1",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.45",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "50",
    "spiral_mode": "0",
    "standby_temperature_delta": "-5",
    "support_base_pattern": "rectilinear",
    "support_base_pattern_spacing": "2.5",
    "support_filament": "0",
    "support_interface_bottom_layers": "2",
    "support_interface_filament": "0",
    "support_interface_loop_pattern": "0",
    "support_interface_spacing": "0.5",
    "support_interface_speed": "80",
    "support_interface_top_layers": "2",
    "support_line_width": "0.4",
    "support_object_xy_distance": "0.35",
    "support_on_build_plate_only": "0",
    "support_speed": "150",
    "support_style": "default",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.2",
    "support_type": "normal(auto)",
    "top_shell_layers": "3",
    "top_shell_thickness": "0.8",
    "top_surface_acceleration": "500",
    "top_surface_line_width": "0.4",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "30",
    "travel_acceleration": "700",
    "travel_speed": "150",
    "tree_support_branch_angle": "45",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "3",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  }
}

FILAMENT = {
  "filament/Dremel Generic PLA @3D20 all.json": {
    "compatible_printers": [
      "Dremel 3D20 0.4 nozzle"
    ],
    "filament_max_volumetric_speed": [
      "9"
    ],
    "filament_retraction_length": [
      "3"
    ],
    "filament_retraction_speed": [
      "60"
    ],
    "from": "system",
    "inherits": "Dremel Generic PLA",
    "instantiation": "true",
    "name": "Dremel Generic PLA @3D20 all",
    "nozzle_temperature": [
      "225"
    ],
    "nozzle_temperature_initial_layer": [
      "230"
    ],
    "nozzle_temperature_range_high": [
      "230"
    ],
    "setting_id": "GFSL99_00",
    "slow_down_layer_time": [
      "10"
    ],
    "type": "filament"
  },
  "filament/Dremel Generic PLA @3D40 all.json": {
    "compatible_printers": [
      "Dremel 3D40 0.4 nozzle"
    ],
    "filament_max_volumetric_speed": [
      "9"
    ],
    "filament_retraction_length": [
      "3"
    ],
    "filament_retraction_speed": [
      "60"
    ],
    "from": "system",
    "hot_plate_temp": [
      "60"
    ],
    "hot_plate_temp_initial_layer": [
      "60"
    ],
    "inherits": "Dremel Generic PLA",
    "instantiation": "true",
    "name": "Dremel Generic PLA @3D40 all",
    "nozzle_temperature": [
      "225"
    ],
    "nozzle_temperature_initial_layer": [
      "225"
    ],
    "nozzle_temperature_range_high": [
      "230"
    ],
    "setting_id": "GFSL99_00",
    "slow_down_layer_time": [
      "10"
    ],
    "type": "filament"
  },
  "filament/Dremel Generic PLA @3D45 all.json": {
    "close_fan_the_first_x_layers": "3",
    "compatible_printers": [
      "Dremel 3D45 0.4 nozzle"
    ],
    "filament_cooling_final_speed": "3.4",
    "filament_cooling_initial_speed": "2.2",
    "filament_cooling_moves": "4",
    "filament_loading_speed": "28",
    "filament_loading_speed_start": "3",
    "filament_retraction_length": [
      "3"
    ],
    "filament_retraction_speed": [
      "60"
    ],
    "filament_unloading_speed": "90",
    "filament_unloading_speed_start": "100",
    "from": "system",
    "inherits": "Dremel Generic PLA",
    "instantiation": "true",
    "name": "Dremel Generic PLA @3D45 all",
    "nozzle_temperature": [
      "200"
    ],
    "nozzle_temperature_initial_layer": [
      "200"
    ],
    "setting_id": "GFSL99_00",
    "slow_down_min_speed": "10",
    "type": "filament"
  },
  "filament/Dremel Generic PLA.json": {
    "compatible_printers": [
      "Dremel 3D45 0.4 nozzle",
      "Dremel 3D40 0.4 nozzle",
      "Dremel 3D20 0.4 nozzle"
    ],
    "filament_flow_ratio": [
      "0.98"
    ],
    "filament_id": "GFL99",
    "filament_max_volumetric_speed": [
      "12"
    ],
    "from": "system",
    "inherits": "fdm_filament_pla",
    "instantiation": "true",
    "name": "Dremel Generic PLA",
    "setting_id": "GFSA04",
    "slow_down_layer_time": [
      "8"
    ],
    "type": "filament"
  },
  "filament/fdm_filament_common.json": {
    "bed_type": [
      "Cool Plate"
    ],
    "close_fan_the_first_x_layers": [
      "3"
    ],
    "fan_cooling_layer_time": [
      "60"
    ],
    "fan_max_speed": [
      "100"
    ],
    "fan_min_speed": [
      "35"
    ],
    "filament_cost": [
      "0"
    ],
    "filament_density": [
      "0"
    ],
    "filament_deretraction_speed": [
      "nil"
    ],
    "filament_diameter": [
      "1.75"
    ],
    "filament_end_gcode": [
      "; filament end gcode \n"
    ],
    "filament_flow_ratio": [
      "1"
    ],
    "filament_max_volumetric_speed": [
      "0"
    ],
    "filament_minimal_purge_on_wipe_tower": [
      "15"
    ],
    "filament_retract_before_wipe": [
      "nil"
    ],
    "filament_retract_restart_extra": [
      "nil"
    ],
    "filament_retract_when_changing_layer": [
      "nil"
    ],
    "filament_retraction_length": [
      "nil"
    ],
    "filament_retraction_minimum_travel": [
      "nil"
    ],
    "filament_retraction_speed": [
      "nil"
    ],
    "filament_settings_id": [
      ""
    ],
    "filament_soluble": [
      "0"
    ],
    "filament_start_gcode": [
      "; Filament gcode\n"
    ],
    "filament_type": [
      "PLA"
    ],
    "filament_vendor": [
      "Generic"
    ],
    "filament_wipe": [
      "nil"
    ],
    "filament_wipe_distance": [
      "nil"
    ],
    "filament_z_hop": [
      "nil"
    ],
    "filament_z_hop_types": [
      "nil"
    ],
    "from": "system",
    "full_fan_speed_layer": [
      "0"
    ],
    "instantiation": "false",
    "name": "fdm_filament_common",
    "nozzle_temperature": [
      "200"
    ],
    "nozzle_temperature_initial_layer": [
      "200"
    ],
    "overhang_fan_speed": [
      "100"
    ],
    "overhang_fan_threshold": [
      "95%"
    ],
    "reduce_fan_stop_start_freq": [
      "0"
    ],
    "slow_down_for_layer_cooling": [
      "1"
    ],
    "slow_down_layer_time": [
      "8"
    ],
    "slow_down_min_speed": [
      "10"
    ],
    "temperature_vitrification": [
      "100"
    ],
    "type": "filament"
  },
  "filament/fdm_filament_pla.json": {
    "additional_cooling_fan_speed": [
      "70"
    ],
    "close_fan_the_first_x_layers": [
      "1"
    ],
    "fan_cooling_layer_time": [
      "100"
    ],
    "fan_max_speed": [
      "100"
    ],
    "fan_min_speed": [
      "100"
    ],
    "filament_cost": [
      "20"
    ],
    "filament_density": [
      "1.24"
    ],
    "filament_max_volumetric_speed": [
      "12"
    ],
    "filament_start_gcode": [
      "; filament start gcode\n"
    ],
    "filament_type": [
      "PLA"
    ],
    "from": "system",
    "inherits": "fdm_filament_common",
    "instantiation": "false",
    "name": "fdm_filament_pla",
    "nozzle_temperature": [
      "220"
    ],
    "nozzle_temperature_initial_layer": [
      "220"
    ],
    "nozzle_temperature_range_high": [
      "230"
    ],
    "nozzle_temperature_range_low": [
      "190"
    ],
    "overhang_fan_speed": [
      "100"
    ],
    "overhang_fan_threshold": [
      "50%"
    ],
    "reduce_fan_stop_start_freq": [
      "1"
    ],
    "slow_down_for_layer_cooling": [
      "1"
    ],
    "slow_down_layer_time": [
      "4"
    ],
    "slow_down_min_speed": [
      "10"
    ],
    "temperature_vitrification": [
      "60"
    ],
    "type": "filament"
  }
}

MISC = {}

ASSETS = [
  "Dremel 3D20_cover.png",
  "Dremel 3D40_cover.png",
  "Dremel 3D45_cover.png",
  "dremel_3d20_buildplate_model.stl",
  "dremel_3d40_3d45_buildplate_model.stl",
  "dremel_3d45.stl"
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
