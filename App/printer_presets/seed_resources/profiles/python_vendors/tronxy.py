from __future__ import annotations

VENDOR = "Tronxy"
INDEX = {
  "description": "Tronxy configurations",
  "filament_list": [],
  "force_update": "0",
  "machine_list": [
    {
      "name": "fdm_machine_common",
      "sub_path": "machine/fdm_machine_common.json"
    },
    {
      "name": "Tronxy X5SA 400 0.4 nozzle",
      "sub_path": "machine/Tronxy X5SA 400 0.4 nozzle.json"
    }
  ],
  "machine_model_list": [
    {
      "name": "Tronxy X5SA 400 Marlin Firmware",
      "sub_path": "machine/Tronxy X5SA 400 Marlin Firmware.json"
    }
  ],
  "name": "Tronxy",
  "process_list": [
    {
      "name": "fdm_process_common",
      "sub_path": "process/fdm_process_common.json"
    },
    {
      "name": "0.08mm Extra Fine @Tronxy",
      "sub_path": "process/0.08mm Extra Fine @Tronxy.json"
    },
    {
      "name": "0.12mm Fine @Tronxy",
      "sub_path": "process/0.12mm Fine @Tronxy.json"
    },
    {
      "name": "0.15mm Optimal @Tronxy",
      "sub_path": "process/0.15mm Optimal @Tronxy.json"
    },
    {
      "name": "0.20mm Standard @Tronxy",
      "sub_path": "process/0.20mm Standard @Tronxy.json"
    },
    {
      "name": "0.24mm Draft @Tronxy",
      "sub_path": "process/0.24mm Draft @Tronxy.json"
    },
    {
      "name": "0.28mm Extra Draft @Tronxy",
      "sub_path": "process/0.28mm Extra Draft @Tronxy.json"
    },
    {
      "name": "fdm_process_tronxy_common",
      "sub_path": "process/fdm_process_tronxy_common.json"
    }
  ],
  "version": "02.03.01.10"
}

MACHINE = {
  "machine/Tronxy X5SA 400 0.4 nozzle.json": {
    "default_filament_profile": "Generic PLA @System",
    "default_print_profile": "0.20mm Standard @Tronxy",
    "from": "system",
    "inherits": "fdm_machine_common",
    "instantiation": "true",
    "machine_start_gcode": "M104 S[nozzle_temperature_initial_layer] ; start heat nozzle\nM140 S[bed_temperature_initial_layer] ; start heat bed\nG90 ; abs coords\nM83 ; extrude relative\nG28 ; home\nM190 S[bed_temperature_initial_layer] ; wait for bed temp\nM109 S[nozzle_temperature_initial_layer] ; wait for nozzle temp\nG1 X10.1 Y20 Z0.28 F5000.0 ; purge line\nG1 X10.1 Y200.0 Z0.28 F1500.0 E15\nG1 X10.4 Y200.0 Z0.28 F5000.0\nG1 X10.4 Y20 Z0.28 F1500.0 E15\nG1 Z5.0 F3000 ; move Z up",
    "name": "Tronxy X5SA 400 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "printable_area": [
      "0x0",
      "400x0",
      "400x400",
      "0x400"
    ],
    "printable_height": "400",
    "printer_model": "Tronxy X5SA 400 Marlin Firmware",
    "setting_id": "GM003",
    "type": "machine"
  },
  "machine/Tronxy X5SA 400 Marlin Firmware.json": {
    "bed_model": "",
    "bed_texture": "tronxy_logo.png",
    "default_materials": "Generic ABS @System;Generic PLA @System;Generic PLA-CF @System;Generic PETG @System;Generic TPU @System;Generic ASA @System;Generic PC @System;Generic PVA @System;Generic PA @System;Generic PA-CF @System",
    "family": "TronxyDesign",
    "hotend_model": "",
    "machine_tech": "FFF",
    "model_id": "Tronxy_X5SA_400_Marlin_Firmware",
    "name": "Tronxy X5SA 400 Marlin Firmware",
    "nozzle_diameter": "0.4",
    "type": "machine_model"
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
    "printable_height": "400",
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
  }
}

PROCESS = {
  "process/0.08mm Extra Fine @Tronxy.json": {
    "bottom_shell_layers": "7",
    "from": "system",
    "inherits": "fdm_process_common",
    "instantiation": "true",
    "layer_height": "0.08",
    "name": "0.08mm Extra Fine @Tronxy",
    "setting_id": "GP001",
    "top_shell_layers": "9",
    "type": "process"
  },
  "process/0.12mm Fine @Tronxy.json": {
    "bottom_shell_layers": "5",
    "from": "system",
    "inherits": "fdm_process_common",
    "instantiation": "true",
    "layer_height": "0.12",
    "name": "0.12mm Fine @Tronxy",
    "setting_id": "GP002",
    "top_shell_layers": "6",
    "type": "process"
  },
  "process/0.15mm Optimal @Tronxy.json": {
    "bottom_shell_layers": "4",
    "from": "system",
    "inherits": "fdm_process_common",
    "instantiation": "true",
    "layer_height": "0.15",
    "name": "0.15mm Optimal @Tronxy",
    "setting_id": "GP003",
    "top_shell_layers": "5",
    "type": "process"
  },
  "process/0.20mm Standard @Tronxy.json": {
    "bottom_shell_layers": "3",
    "from": "system",
    "inherits": "fdm_process_common",
    "instantiation": "true",
    "layer_height": "0.2",
    "name": "0.20mm Standard @Tronxy",
    "setting_id": "GP004",
    "top_shell_layers": "4",
    "type": "process"
  },
  "process/0.24mm Draft @Tronxy.json": {
    "bottom_shell_layers": "3",
    "from": "system",
    "inherits": "fdm_process_common",
    "instantiation": "true",
    "layer_height": "0.24",
    "name": "0.24mm Draft @Tronxy",
    "setting_id": "GP005",
    "top_shell_layers": "4",
    "top_surface_line_width": "0.45",
    "type": "process"
  },
  "process/0.28mm Extra Draft @Tronxy.json": {
    "bottom_shell_layers": "3",
    "from": "system",
    "inherits": "fdm_process_common",
    "instantiation": "true",
    "layer_height": "0.28",
    "name": "0.28mm Extra Draft @Tronxy",
    "setting_id": "GP006",
    "top_shell_layers": "4",
    "top_surface_line_width": "0.45",
    "type": "process"
  },
  "process/fdm_process_common.json": {
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
      "Tronxy X5SA 400 0.4 nozzle"
    ],
    "compatible_printers_condition": "",
    "default_acceleration": "7000",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "0",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "filename_format": "{input_filename_base}_{filament_type[0]}_{print_time}.gcode_[total_weight] g weight.gcode",
    "from": "system",
    "gap_infill_speed": "100",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "25%",
    "initial_layer_acceleration": "500",
    "initial_layer_infill_speed": "105",
    "initial_layer_line_width": "0.5",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "50",
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
    "name": "fdm_process_common",
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
    "support_interface_speed": "80",
    "support_interface_top_layers": "2",
    "support_line_width": "0.4",
    "support_object_xy_distance": "0.35",
    "support_on_build_plate_only": "0",
    "support_speed": "150",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.2",
    "support_type": "normal(auto)",
    "top_shell_layers": "3",
    "top_shell_thickness": "0.8",
    "top_surface_acceleration": "3000",
    "top_surface_line_width": "0.4",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "100",
    "travel_speed": "350",
    "tree_support_branch_angle": "45",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "2",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/fdm_process_tronxy_common.json": {
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
      "Tronxy X5SA 400 0.4 nozzle"
    ],
    "compatible_printers_condition": "",
    "default_acceleration": "7000",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "0",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "filename_format": "{input_filename_base}_{filament_type[0]}_{print_time}.gcode_[total_weight] g weight.gcode",
    "from": "system",
    "gap_infill_speed": "100",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "25%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "500",
    "initial_layer_infill_speed": "105",
    "initial_layer_line_width": "0.5",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "50",
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
    "name": "fdm_process_tronxy_common",
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
    "support_interface_speed": "80",
    "support_interface_top_layers": "2",
    "support_line_width": "0.4",
    "support_object_xy_distance": "0.35",
    "support_on_build_plate_only": "0",
    "support_speed": "150",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.2",
    "support_type": "normal(auto)",
    "top_shell_layers": "3",
    "top_shell_thickness": "0.8",
    "top_surface_acceleration": "3000",
    "top_surface_line_width": "0.4",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "100",
    "travel_speed": "350",
    "tree_support_branch_angle": "45",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "2",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  }
}

FILAMENT = {}

MISC = {}

ASSETS = [
  "Tronxy X5SA 400 Marlin Firmware_cover.png",
  "tronxy_logo.png",
  "tronxy_v0_logo.png"
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
