from __future__ import annotations

VENDOR = "Vivedino"
INDEX = {
  "description": "Vivedino configurations",
  "filament_list": [],
  "force_update": "0",
  "machine_list": [
    {
      "name": "fdm_machine_common",
      "sub_path": "machine/fdm_machine_common.json"
    },
    {
      "name": "fdm_klipper_common",
      "sub_path": "machine/fdm_klipper_common.json"
    },
    {
      "name": "fdm_rrf_common",
      "sub_path": "machine/fdm_rrf_common.json"
    },
    {
      "name": "Troodon 2.0 Klipper 0.4 nozzle",
      "sub_path": "machine/Troodon 2.0 Klipper 0.4 nozzle.json"
    },
    {
      "name": "Troodon 2.0 RRF 0.4 nozzle",
      "sub_path": "machine/Troodon 2.0 RRF 0.4 nozzle.json"
    }
  ],
  "machine_model_list": [
    {
      "name": "Troodon 2.0 - Klipper",
      "sub_path": "machine/Troodon2Klipper.json"
    },
    {
      "name": "Troodon 2.0 - RRF",
      "sub_path": "machine/Troodon2RRF.json"
    }
  ],
  "name": "Vivedino",
  "process_list": [
    {
      "name": "fdm_process_common",
      "sub_path": "process/fdm_process_common.json"
    },
    {
      "name": "fdm_process_klipper_common",
      "sub_path": "process/fdm_process_klipper_common.json"
    },
    {
      "name": "0.08mm Extra Fine @Troodon2",
      "sub_path": "process/0.08mm Extra Fine @Troodon2.json"
    },
    {
      "name": "0.12mm Fine @Troodon2",
      "sub_path": "process/0.12mm Fine @Troodon2.json"
    },
    {
      "name": "0.15mm Optimal @Troodon2",
      "sub_path": "process/0.15mm Optimal @Troodon2.json"
    },
    {
      "name": "0.20mm Standard @Troodon2",
      "sub_path": "process/0.20mm Standard @Troodon2.json"
    },
    {
      "name": "0.24mm Draft @Troodon2",
      "sub_path": "process/0.24mm Draft @Troodon2.json"
    },
    {
      "name": "0.28mm Extra Draft @Troodon2",
      "sub_path": "process/0.28mm Extra Draft @Troodon2.json"
    }
  ],
  "version": "02.03.01.10"
}

MACHINE = {
  "machine/Troodon 2.0 Klipper 0.4 nozzle.json": {
    "from": "system",
    "inherits": "fdm_klipper_common",
    "instantiation": "true",
    "name": "Troodon 2.0 Klipper 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "printable_area": [
      "0x0",
      "350x0",
      "350x350",
      "0x350"
    ],
    "printable_height": "330",
    "printer_model": "Troodon 2.0 - Klipper",
    "setting_id": "GM001",
    "type": "machine"
  },
  "machine/Troodon 2.0 RRF 0.4 nozzle.json": {
    "from": "system",
    "inherits": "fdm_rrf_common",
    "instantiation": "true",
    "name": "Troodon 2.0 RRF 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "printable_area": [
      "0x0",
      "350x0",
      "350x350",
      "0x350"
    ],
    "printable_height": "330",
    "printer_model": "Troodon 2.0 - RRF",
    "setting_id": "GM002",
    "type": "machine"
  },
  "machine/Troodon2Klipper.json": {
    "bed_model": "",
    "bed_texture": "EONSlicer-Troodon2-Bed-Texture.png",
    "default_materials": "Generic ABS @System;Generic PLA @System;Generic PLA-CF @System;Generic PETG @System;Generic TPU @System;Generic ASA @System;Generic PC @System;Generic PVA @System;Generic PA @System;Generic PA-CF @System",
    "family": "Vivedino",
    "hotend_model": "",
    "machine_tech": "FFF",
    "model_id": "Troodon2Klipper",
    "name": "Troodon 2.0 - Klipper",
    "nozzle_diameter": "0.4",
    "type": "machine_model"
  },
  "machine/Troodon2RRF.json": {
    "bed_model": "",
    "bed_texture": "EONSlicer-Troodon2-Bed-Texture.png",
    "default_materials": "Generic ABS @System;Generic PLA @System;Generic PLA-CF @System;Generic PETG @System;Generic TPU @System;Generic ASA @System;Generic PC @System;Generic PVA @System;Generic PA @System;Generic PA-CF @System",
    "family": "Vivedino",
    "hotend_model": "",
    "machine_tech": "FFF",
    "model_id": "Troodon2RRF",
    "name": "Troodon 2.0 - RRF",
    "nozzle_diameter": "0.4",
    "type": "machine_model"
  },
  "machine/fdm_klipper_common.json": {
    "auxiliary_fan": "0",
    "bed_exclude_area": [
      "0x0"
    ],
    "before_layer_change_gcode": ";BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n",
    "change_filament_gcode": "",
    "default_filament_profile": [
      "Generic ABS @System"
    ],
    "default_print_profile": "0.20mm Standard @Troodon2",
    "deretraction_speed": [
      "30"
    ],
    "extruder_clearance_height_to_lid": "140",
    "extruder_clearance_height_to_rod": "36",
    "extruder_clearance_radius": "65",
    "from": "system",
    "gcode_flavor": "klipper",
    "inherits": "fdm_machine_common",
    "instantiation": "false",
    "layer_change_gcode": ";AFTER_LAYER_CHANGE\n;[layer_z]",
    "machine_end_gcode": "PRINT_END",
    "machine_max_acceleration_e": [
      "5000",
      "5000"
    ],
    "machine_max_acceleration_extruding": [
      "20000",
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
      "20000",
      "20000"
    ],
    "machine_max_acceleration_y": [
      "20000",
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
      "25",
      "25"
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
    "machine_pause_gcode": "PAUSE",
    "machine_start_gcode": "M190 S[bed_temperature_initial_layer_single]\nM109 S[nozzle_temperature_initial_layer]\nPRINT_START EXTRUDER=[nozzle_temperature_initial_layer] BED=[bed_temperature_initial_layer_single]\n",
    "max_layer_height": [
      "0.32"
    ],
    "min_layer_height": [
      "0.08"
    ],
    "name": "fdm_klipper_common",
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
      "0.8"
    ],
    "retraction_minimum_travel": [
      "1"
    ],
    "retraction_speed": [
      "30"
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
    ],
    "z_hop_types": "Normal Lift"
  },
  "machine/fdm_machine_common.json": {
    "before_layer_change_gcode": ";BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n",
    "change_filament_gcode": "",
    "default_print_profile": "",
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
    "layer_change_gcode": ";AFTER_LAYER_CHANGE\n;[layer_z]",
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
      "100"
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
    "machine_pause_gcode": "M601",
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
    "type": "machine",
    "wipe": [
      "1"
    ],
    "z_hop": [
      "0"
    ]
  },
  "machine/fdm_rrf_common.json": {
    "auxiliary_fan": "0",
    "bed_exclude_area": [
      "0x0"
    ],
    "before_layer_change_gcode": ";BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n",
    "change_filament_gcode": "",
    "default_filament_profile": [
      "Generic ABS @System"
    ],
    "default_print_profile": "0.20mm Standard @Troodon2",
    "deretraction_speed": [
      "30"
    ],
    "extruder_clearance_height_to_lid": "140",
    "extruder_clearance_height_to_rod": "36",
    "extruder_clearance_radius": "65",
    "from": "system",
    "gcode_flavor": "reprapfirmware",
    "inherits": "fdm_machine_common",
    "instantiation": "false",
    "layer_change_gcode": ";AFTER_LAYER_CHANGE\n;[layer_z]",
    "machine_end_gcode": "M0",
    "machine_max_acceleration_e": [
      "5000",
      "5000"
    ],
    "machine_max_acceleration_extruding": [
      "20000",
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
      "20000",
      "20000"
    ],
    "machine_max_acceleration_y": [
      "20000",
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
      "25",
      "25"
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
    "machine_pause_gcode": "PAUSE\n",
    "machine_start_gcode": "M104 S0\nM190 S0\nM98 P\"start_print.g\" A[first_layer_bed_temperature] B\"[filament_type]\" C[first_layer_temperature] D[nozzle_diameter] E{first_layer_print_min[0]} F{first_layer_print_max[0]} H{first_layer_print_min[1]} J{first_layer_print_max[1]}",
    "max_layer_height": [
      "0.32"
    ],
    "min_layer_height": [
      "0.08"
    ],
    "name": "fdm_rrf_common",
    "nozzle_type": "undefine",
    "printable_height": "330",
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
      "0.8"
    ],
    "retraction_minimum_travel": [
      "1"
    ],
    "retraction_speed": [
      "30"
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
    ],
    "z_hop_types": "Normal Lift"
  }
}

PROCESS = {
  "process/0.08mm Extra Fine @Troodon2.json": {
    "bottom_shell_layers": "7",
    "from": "system",
    "inherits": "fdm_process_klipper_common",
    "instantiation": "true",
    "layer_height": "0.08",
    "name": "0.08mm Extra Fine @Troodon2",
    "setting_id": "GP004",
    "top_shell_layers": "9",
    "type": "process"
  },
  "process/0.12mm Fine @Troodon2.json": {
    "bottom_shell_layers": "5",
    "from": "system",
    "inherits": "fdm_process_klipper_common",
    "instantiation": "true",
    "layer_height": "0.12",
    "name": "0.12mm Fine @Troodon2",
    "setting_id": "GP004",
    "top_shell_layers": "6",
    "type": "process"
  },
  "process/0.15mm Optimal @Troodon2.json": {
    "bottom_shell_layers": "4",
    "from": "system",
    "inherits": "fdm_process_klipper_common",
    "instantiation": "true",
    "layer_height": "0.15",
    "name": "0.15mm Optimal @Troodon2",
    "setting_id": "GP004",
    "top_shell_layers": "5",
    "type": "process"
  },
  "process/0.20mm Standard @Troodon2.json": {
    "bottom_shell_layers": "3",
    "from": "system",
    "inherits": "fdm_process_klipper_common",
    "instantiation": "true",
    "layer_height": "0.2",
    "name": "0.20mm Standard @Troodon2",
    "setting_id": "GP004",
    "top_shell_layers": "4",
    "type": "process"
  },
  "process/0.24mm Draft @Troodon2.json": {
    "bottom_shell_layers": "3",
    "from": "system",
    "inherits": "fdm_process_klipper_common",
    "instantiation": "true",
    "layer_height": "0.24",
    "name": "0.24mm Draft @Troodon2",
    "setting_id": "GP004",
    "top_shell_layers": "4",
    "top_surface_line_width": "0.45",
    "type": "process"
  },
  "process/0.28mm Extra Draft @Troodon2.json": {
    "bottom_shell_layers": "3",
    "from": "system",
    "inherits": "fdm_process_klipper_common",
    "instantiation": "true",
    "layer_height": "0.28",
    "name": "0.28mm Extra Draft @Troodon2",
    "setting_id": "GP004",
    "top_shell_layers": "4",
    "top_surface_line_width": "0.45",
    "type": "process"
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
  "process/fdm_process_klipper_common.json": {
    "adaptive_layer_height": "0",
    "bottom_shell_layers": "3",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.95",
    "bridge_no_support": "0",
    "bridge_speed": "50",
    "brim_object_gap": "0.1",
    "brim_width": "5",
    "compatible_printers": [
      "Troodon 2.0 Klipper 0.4 nozzle",
      "Troodon 2.0 RRF 0.4 nozzle"
    ],
    "compatible_printers_condition": "",
    "default_acceleration": "5000",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "0",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "exclude_object": "1",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "100",
    "ineternal_bridge_speed": "70",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "25%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "500",
    "initial_layer_infill_speed": "80",
    "initial_layer_line_width": "0.5",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "50",
    "inner_wall_acceleration": "5000",
    "inner_wall_line_width": "0.45",
    "inner_wall_speed": "200",
    "instantiation": "false",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0.4",
    "internal_solid_infill_speed": "200",
    "ironing_flow": "10%",
    "ironing_spacing": "0.15",
    "ironing_speed": "30",
    "ironing_type": "no ironing",
    "layer_height": "0.2",
    "line_width": "0.4",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "15",
    "name": "fdm_process_klipper_common",
    "outer_wall_acceleration": "3000",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "120",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "50",
    "overhang_3_4_speed": "30",
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
    "skirt_loops": "0",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.45",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "200",
    "spiral_mode": "0",
    "standby_temperature_delta": "-5",
    "support_base_pattern": "rectilinear",
    "support_base_pattern_spacing": "2.5",
    "support_filament": "0",
    "support_interface_bottom_layers": "2",
    "support_interface_filament": "0",
    "support_interface_loop_pattern": "0",
    "support_interface_spacing": "0.5",
    "support_interface_speed": "60",
    "support_interface_top_layers": "2",
    "support_line_width": "0.4",
    "support_object_xy_distance": "0.35",
    "support_on_build_plate_only": "0",
    "support_speed": "80",
    "support_style": "default",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.2",
    "support_type": "normal(auto)",
    "top_shell_layers": "3",
    "top_shell_thickness": "0.8",
    "top_surface_acceleration": "3000",
    "top_surface_line_width": "0.4",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "100",
    "travel_acceleration": "7000",
    "travel_speed": "350",
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

FILAMENT = {}

MISC = {}

ASSETS = [
  "OrcaSlicer-Troodon2-Bed-Texture.png",
  "Troodon 2.0 - Klipper_cover.png",
  "Troodon 2.0 - RRF_cover.png"
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
