from __future__ import annotations

VENDOR = "SecKit"
INDEX = {
  "description": "SecKit configurations",
  "filament_list": [
    {
      "name": "fdm_filament_common",
      "sub_path": "filament/fdm_filament_common.json"
    },
    {
      "name": "fdm_filament_abs",
      "sub_path": "filament/fdm_filament_abs.json"
    },
    {
      "name": "fdm_filament_asa",
      "sub_path": "filament/fdm_filament_asa.json"
    },
    {
      "name": "fdm_filament_pa",
      "sub_path": "filament/fdm_filament_pa.json"
    },
    {
      "name": "fdm_filament_pc",
      "sub_path": "filament/fdm_filament_pc.json"
    },
    {
      "name": "fdm_filament_pet",
      "sub_path": "filament/fdm_filament_pet.json"
    },
    {
      "name": "fdm_filament_pla",
      "sub_path": "filament/fdm_filament_pla.json"
    },
    {
      "name": "fdm_filament_pva",
      "sub_path": "filament/fdm_filament_pva.json"
    },
    {
      "name": "fdm_filament_tpu",
      "sub_path": "filament/fdm_filament_tpu.json"
    },
    {
      "name": "SecKit Generic ABS",
      "sub_path": "filament/SecKit Generic ABS.json"
    },
    {
      "name": "SecKit Generic ASA",
      "sub_path": "filament/SecKit Generic ASA.json"
    },
    {
      "name": "SecKit Generic PA",
      "sub_path": "filament/SecKit Generic PA.json"
    },
    {
      "name": "SecKit Generic PA-CF",
      "sub_path": "filament/SecKit Generic PA-CF.json"
    },
    {
      "name": "SecKit Generic PC",
      "sub_path": "filament/SecKit Generic PC.json"
    },
    {
      "name": "SecKit Generic PETG",
      "sub_path": "filament/SecKit Generic PETG.json"
    },
    {
      "name": "SecKit Generic PLA",
      "sub_path": "filament/SecKit Generic PLA.json"
    },
    {
      "name": "SecKit Generic PLA-CF",
      "sub_path": "filament/SecKit Generic PLA-CF.json"
    },
    {
      "name": "SecKit Generic PVA",
      "sub_path": "filament/SecKit Generic PVA.json"
    },
    {
      "name": "SecKit Generic TPU",
      "sub_path": "filament/SecKit Generic TPU.json"
    }
  ],
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
      "name": "SecKit Go3 0.4 nozzle",
      "sub_path": "machine/SecKit Go3 0.4 nozzle.json"
    },
    {
      "name": "SecKit SK-Tank 0.4 nozzle",
      "sub_path": "machine/SecKit SK-Tank 0.4 nozzle.json"
    }
  ],
  "machine_model_list": [
    {
      "name": "SecKit SK-Tank",
      "sub_path": "machine/SecKit SK-Tank.json"
    },
    {
      "name": "Seckit Go3",
      "sub_path": "machine/Seckit Go3.json"
    }
  ],
  "name": "SecKit",
  "process_list": [
    {
      "name": "fdm_process_common",
      "sub_path": "process/fdm_process_common.json"
    },
    {
      "name": "fdm_process_seckit_common",
      "sub_path": "process/fdm_process_seckit_common.json"
    },
    {
      "name": "0.08mm Extra Fine @SecKit",
      "sub_path": "process/0.08mm Extra Fine @SecKit.json"
    },
    {
      "name": "0.12mm Fine @SecKit",
      "sub_path": "process/0.12mm Fine @SecKit.json"
    },
    {
      "name": "0.15mm Optimal @SecKit",
      "sub_path": "process/0.15mm Optimal @SecKit.json"
    },
    {
      "name": "0.20mm Standard @SecKit",
      "sub_path": "process/0.20mm Standard @SecKit.json"
    },
    {
      "name": "0.24mm Draft @SecKit",
      "sub_path": "process/0.24mm Draft @SecKit.json"
    },
    {
      "name": "0.28mm Extra Draft @SecKit",
      "sub_path": "process/0.28mm Extra Draft @SecKit.json"
    },
    {
      "name": "0.30mm Fast @SecKit",
      "sub_path": "process/0.30mm Fast @SecKit.json"
    }
  ],
  "version": "02.03.01.10"
}

MACHINE = {
  "machine/SecKit Go3 0.4 nozzle.json": {
    "auxiliary_fan": "0",
    "from": "system",
    "inherits": "fdm_klipper_common",
    "instantiation": "true",
    "machine_load_filament_time": "0",
    "machine_unload_filament_time": "0",
    "name": "SecKit Go3 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "nozzle_type": "hardened_steel",
    "printable_area": [
      "0x0",
      "300x0",
      "300x300",
      "0x300"
    ],
    "printable_height": "275",
    "printer_model": "Seckit Go3",
    "scan_first_layer": "0",
    "setting_id": "GM002",
    "type": "machine"
  },
  "machine/SecKit SK-Tank 0.4 nozzle.json": {
    "from": "system",
    "inherits": "fdm_klipper_common",
    "instantiation": "true",
    "name": "SecKit SK-Tank 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "printable_area": [
      "0x0",
      "350x0",
      "350x350",
      "0x350"
    ],
    "printable_height": "400",
    "printer_model": "SecKit SK-Tank",
    "setting_id": "GM001",
    "type": "machine"
  },
  "machine/SecKit SK-Tank.json": {
    "bed_model": "SK-Tank_Bed.stl",
    "bed_texture": "seckit_logo.svg",
    "default_materials": "SecKit Generic ABS;SecKit Generic PLA;SecKit Generic PLA-CF;SecKit Generic PETG;SecKit Generic TPU;SecKit Generic ASA;SecKit Generic PC;SecKit Generic PVA;SecKit Generic PA;SecKit Generic PA-CF",
    "family": "SecKit",
    "hotend_model": "hotend.stl",
    "machine_tech": "FFF",
    "model_id": "SK-Tank",
    "name": "SecKit SK-Tank",
    "nozzle_diameter": "0.4",
    "type": "machine_model",
    "url": "https://seckit3dp.design"
  },
  "machine/Seckit Go3.json": {
    "bed_model": "SK-Go3_Bed.stl",
    "bed_texture": "seckit_logo.svg",
    "default_materials": "SecKit Generic ABS;SecKit Generic PLA;SecKit Generic PLA-CF;SecKit Generic PETG;SecKit Generic TPU;SecKit Generic ASA;SecKit Generic PC;SecKit Generic PVA;SecKit Generic PA;SecKit Generic PA-CF",
    "family": "SecKit",
    "hotend_model": "seckit-hotend.stl",
    "machine_tech": "FFF",
    "model_id": "SK-Go3",
    "name": "Seckit Go3",
    "nozzle_diameter": "0.4",
    "type": "machine_model",
    "url": "https://seckit3dp.design"
  },
  "machine/fdm_klipper_common.json": {
    "auxiliary_fan": "0",
    "bed_exclude_area": [
      "0x0"
    ],
    "before_layer_change_gcode": ";BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n",
    "change_filament_gcode": "M600",
    "default_filament_profile": [
      "SecKit Generic PETG"
    ],
    "default_print_profile": "0.20mm Standard @SecKit",
    "deretraction_speed": [
      "120"
    ],
    "extruder_clearance_height_to_lid": "140",
    "extruder_clearance_height_to_rod": "44",
    "extruder_clearance_radius": "46",
    "from": "system",
    "gcode_flavor": "klipper",
    "inherits": "fdm_machine_common",
    "instantiation": "false",
    "layer_change_gcode": ";AFTER_LAYER_CHANGE\n;[layer_z]",
    "machine_end_gcode": "END_PRINT",
    "machine_max_acceleration_e": [
      "8000",
      "8000"
    ],
    "machine_max_acceleration_extruding": [
      "3500",
      "3500"
    ],
    "machine_max_acceleration_retracting": [
      "3500",
      "3500"
    ],
    "machine_max_acceleration_travel": [
      "3500",
      "3500"
    ],
    "machine_max_acceleration_x": [
      "3500",
      "3500"
    ],
    "machine_max_acceleration_y": [
      "3500",
      "3500"
    ],
    "machine_max_acceleration_z": [
      "200",
      "200"
    ],
    "machine_max_jerk_e": [
      "8",
      "8"
    ],
    "machine_max_jerk_x": [
      "14.14",
      "14.14"
    ],
    "machine_max_jerk_y": [
      "14.14",
      "14.14"
    ],
    "machine_max_jerk_z": [
      "2",
      "2"
    ],
    "machine_max_speed_e": [
      "180",
      "180"
    ],
    "machine_max_speed_x": [
      "300",
      "300"
    ],
    "machine_max_speed_y": [
      "300",
      "300"
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
    "machine_start_gcode": "START_PRINT EXTRUDER_TEMP=[nozzle_temperature_initial_layer] BED_TEMP=[bed_temperature_initial_layer_single]\nG90\nG92 E0",
    "max_layer_height": [
      "0.35"
    ],
    "min_layer_height": [
      "0.05"
    ],
    "name": "fdm_klipper_common",
    "nozzle_type": "undefine",
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
      "1.2"
    ],
    "retraction_minimum_travel": [
      "2"
    ],
    "retraction_speed": [
      "120"
    ],
    "scan_first_layer": "0",
    "silent_mode": "0",
    "single_extruder_multi_material": "1",
    "type": "machine",
    "wipe": [
      "1"
    ],
    "z_hop": [
      "0.25"
    ],
    "z_hop_types": "Normal Lift"
  },
  "machine/fdm_machine_common.json": {
    "change_filament_gcode": "",
    "deretraction_speed": [
      "40"
    ],
    "extruder_clearance_height_to_lid": "140",
    "extruder_clearance_height_to_rod": "44",
    "extruder_clearance_radius": "46",
    "extruder_colour": [
      "#FCE94F"
    ],
    "extruder_offset": [
      "0x0"
    ],
    "from": "system",
    "gcode_flavor": "marlin",
    "instantiation": "false",
    "machine_max_acceleration_e": [
      "8000"
    ],
    "machine_max_acceleration_extruding": [
      "3500"
    ],
    "machine_max_acceleration_retracting": [
      "3500"
    ],
    "machine_max_acceleration_travel": [
      "3500"
    ],
    "machine_max_acceleration_x": [
      "3500"
    ],
    "machine_max_acceleration_y": [
      "3500"
    ],
    "machine_max_acceleration_z": [
      "200"
    ],
    "machine_max_jerk_e": [
      "8"
    ],
    "machine_max_jerk_x": [
      "14.14"
    ],
    "machine_max_jerk_y": [
      "14.14"
    ],
    "machine_max_jerk_z": [
      "2"
    ],
    "machine_max_speed_e": [
      "180"
    ],
    "machine_max_speed_x": [
      "300"
    ],
    "machine_max_speed_y": [
      "300"
    ],
    "machine_max_speed_z": [
      "12"
    ],
    "machine_min_extruding_rate": [
      "0"
    ],
    "machine_min_travel_rate": [
      "0"
    ],
    "max_layer_height": [
      "0.35"
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
      "0"
    ],
    "retraction_length": [
      "1.2"
    ],
    "retraction_minimum_travel": [
      "2"
    ],
    "retraction_speed": [
      "120"
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
  "process/0.08mm Extra Fine @SecKit.json": {
    "bottom_shell_layers": "7",
    "from": "system",
    "inherits": "fdm_process_seckit_common",
    "instantiation": "true",
    "layer_height": "0.08",
    "name": "0.08mm Extra Fine @SecKit",
    "setting_id": "GP001",
    "top_shell_layers": "9",
    "type": "process"
  },
  "process/0.12mm Fine @SecKit.json": {
    "bottom_shell_layers": "5",
    "from": "system",
    "inherits": "fdm_process_seckit_common",
    "instantiation": "true",
    "layer_height": "0.12",
    "name": "0.12mm Fine @SecKit",
    "setting_id": "GP002",
    "top_shell_layers": "6",
    "type": "process"
  },
  "process/0.15mm Optimal @SecKit.json": {
    "bottom_shell_layers": "4",
    "from": "system",
    "inherits": "fdm_process_seckit_common",
    "instantiation": "true",
    "layer_height": "0.15",
    "name": "0.15mm Optimal @SecKit",
    "setting_id": "GP003",
    "top_shell_layers": "5",
    "type": "process"
  },
  "process/0.20mm Standard @SecKit.json": {
    "bottom_shell_layers": "3",
    "from": "system",
    "inherits": "fdm_process_seckit_common",
    "instantiation": "true",
    "layer_height": "0.2",
    "name": "0.20mm Standard @SecKit",
    "setting_id": "GP005",
    "top_shell_layers": "4",
    "type": "process"
  },
  "process/0.24mm Draft @SecKit.json": {
    "bottom_shell_layers": "3",
    "from": "system",
    "inherits": "fdm_process_seckit_common",
    "instantiation": "true",
    "layer_height": "0.24",
    "name": "0.24mm Draft @SecKit",
    "setting_id": "GP006",
    "top_shell_layers": "4",
    "top_surface_line_width": "0.45",
    "type": "process"
  },
  "process/0.28mm Extra Draft @SecKit.json": {
    "bottom_shell_layers": "3",
    "from": "system",
    "inherits": "fdm_process_seckit_common",
    "instantiation": "true",
    "layer_height": "0.28",
    "name": "0.28mm Extra Draft @SecKit",
    "setting_id": "GP007",
    "top_shell_layers": "4",
    "top_surface_line_width": "0.45",
    "type": "process"
  },
  "process/0.30mm Fast @SecKit.json": {
    "bottom_shell_layers": "3",
    "from": "system",
    "inherits": "fdm_process_seckit_common",
    "instantiation": "true",
    "layer_height": "0.3",
    "name": "0.30mm Fast @SecKit",
    "setting_id": "GP008",
    "top_shell_layers": "4",
    "top_surface_line_width": "0.5",
    "type": "process"
  },
  "process/fdm_process_common.json": {
    "adaptive_layer_height": "0",
    "bridge_flow": "0.95",
    "bridge_no_support": "0",
    "bridge_speed": "25",
    "brim_width": "5",
    "compatible_printers": [],
    "default_acceleration": "3500",
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
    "travel_speed": "235",
    "type": "process",
    "wall_loops": "3",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/fdm_process_seckit_common.json": {
    "adaptive_layer_height": "0",
    "bottom_shell_layers": "3",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.80",
    "bridge_no_support": "0",
    "bridge_speed": "50",
    "brim_object_gap": "0.1",
    "brim_width": "5",
    "compatible_printers": [
      "SecKit SK-Tank 0.4 nozzle",
      "SecKit Go3 0.4 nozzle"
    ],
    "compatible_printers_condition": "",
    "default_acceleration": "3500",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "0",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "filename_format": "{input_filename_base}_{layer_height}mm_{filament_type[0]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "100",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "25%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "500",
    "initial_layer_infill_speed": "105",
    "initial_layer_line_width": "0.45",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "50",
    "inner_wall_acceleration": "3500",
    "inner_wall_line_width": "0.40",
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
    "name": "fdm_process_seckit_common",
    "outer_wall_acceleration": "3000",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "120",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "60",
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
    "sparse_infill_line_width": "0.4",
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
    "travel_acceleration": "3500",
    "travel_speed": "235",
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
  "filament/SecKit Generic ABS.json": {
    "close_fan_the_first_x_layers": [
      "2"
    ],
    "compatible_printers": [
      "SecKit SK-Tank 0.4 nozzle",
      "SecKit Go3 0.4 nozzle"
    ],
    "enable_pressure_advance": [
      "1"
    ],
    "fan_cooling_layer_time": [
      "10"
    ],
    "fan_max_speed": [
      "30"
    ],
    "fan_min_speed": [
      "10"
    ],
    "filament_flow_ratio": [
      "0.980"
    ],
    "filament_id": "GFB99",
    "filament_max_volumetric_speed": [
      "18"
    ],
    "filament_z_hop": [
      "0"
    ],
    "from": "system",
    "hot_plate_temp_initial_layer": [
      "108"
    ],
    "inherits": "fdm_filament_abs",
    "instantiation": "true",
    "name": "SecKit Generic ABS",
    "nozzle_temperature": [
      "243"
    ],
    "nozzle_temperature_initial_layer": [
      "248"
    ],
    "overhang_fan_speed": [
      "30"
    ],
    "pressure_advance": [
      "0.03"
    ],
    "setting_id": "GFSA04",
    "type": "filament"
  },
  "filament/SecKit Generic ASA.json": {
    "close_fan_the_first_x_layers": [
      "2"
    ],
    "compatible_printers": [
      "SecKit SK-Tank 0.4 nozzle",
      "SecKit Go3 0.4 nozzle"
    ],
    "enable_pressure_advance": [
      "1"
    ],
    "fan_cooling_layer_time": [
      "10"
    ],
    "fan_max_speed": [
      "30"
    ],
    "fan_min_speed": [
      "10"
    ],
    "filament_density": [
      "1.1"
    ],
    "filament_flow_ratio": [
      "0.93"
    ],
    "filament_id": "GFB98",
    "filament_max_volumetric_speed": [
      "19"
    ],
    "filament_z_hop": [
      "0"
    ],
    "from": "system",
    "inherits": "fdm_filament_asa",
    "instantiation": "true",
    "name": "SecKit Generic ASA",
    "overhang_fan_speed": [
      "25"
    ],
    "pressure_advance": [
      "0.033"
    ],
    "setting_id": "GFSA04",
    "type": "filament"
  },
  "filament/SecKit Generic PA-CF.json": {
    "compatible_printers": [
      "SecKit SK-Tank 0.4 nozzle",
      "SecKit Go3 0.4 nozzle"
    ],
    "enable_pressure_advance": [
      "1"
    ],
    "filament_density": [
      "1.24"
    ],
    "filament_id": "GFN98",
    "filament_type": [
      "PA-CF"
    ],
    "filament_z_hop": [
      "0"
    ],
    "from": "system",
    "hot_plate_temp": [
      "80"
    ],
    "hot_plate_temp_initial_layer": [
      "80"
    ],
    "inherits": "fdm_filament_pa",
    "instantiation": "true",
    "name": "SecKit Generic PA-CF",
    "nozzle_temperature": [
      "270"
    ],
    "nozzle_temperature_initial_layer": [
      "270"
    ],
    "nozzle_temperature_range_high": [
      "280"
    ],
    "overhang_fan_speed": [
      "50"
    ],
    "pressure_advance": [
      "0.045"
    ],
    "setting_id": "GFSA04",
    "type": "filament"
  },
  "filament/SecKit Generic PA.json": {
    "compatible_printers": [
      "SecKit SK-Tank 0.4 nozzle",
      "SecKit Go3 0.4 nozzle"
    ],
    "enable_pressure_advance": [
      "1"
    ],
    "filament_density": [
      "1.24"
    ],
    "filament_id": "GFN99",
    "filament_z_hop": [
      "0"
    ],
    "from": "system",
    "hot_plate_temp": [
      "80"
    ],
    "hot_plate_temp_initial_layer": [
      "80"
    ],
    "inherits": "fdm_filament_pa",
    "instantiation": "true",
    "name": "SecKit Generic PA",
    "nozzle_temperature": [
      "270"
    ],
    "nozzle_temperature_initial_layer": [
      "270"
    ],
    "nozzle_temperature_range_high": [
      "280"
    ],
    "overhang_fan_speed": [
      "50"
    ],
    "pressure_advance": [
      "0.045"
    ],
    "setting_id": "GFSA04",
    "type": "filament"
  },
  "filament/SecKit Generic PC.json": {
    "compatible_printers": [
      "SecKit SK-Tank 0.4 nozzle",
      "SecKit Go3 0.4 nozzle"
    ],
    "enable_pressure_advance": [
      "1"
    ],
    "filament_flow_ratio": [
      "0.93"
    ],
    "filament_id": "GFC99",
    "filament_max_volumetric_speed": [
      "12"
    ],
    "filament_z_hop": [
      "0"
    ],
    "from": "system",
    "hot_plate_temp": [
      "100"
    ],
    "hot_plate_temp_initial_layer": [
      "100"
    ],
    "inherits": "fdm_filament_pc",
    "instantiation": "true",
    "name": "SecKit Generic PC",
    "nozzle_temperature_initial_layer": [
      "280"
    ],
    "nozzle_temperature_range_high": [
      "290"
    ],
    "pressure_advance": [
      "0.045"
    ],
    "setting_id": "GFSA04",
    "type": "filament"
  },
  "filament/SecKit Generic PETG.json": {
    "compatible_printers": [
      "SecKit SK-Tank 0.4 nozzle",
      "SecKit Go3 0.4 nozzle"
    ],
    "enable_pressure_advance": [
      "1"
    ],
    "fan_cooling_layer_time": [
      "10"
    ],
    "fan_max_speed": [
      "100"
    ],
    "fan_min_speed": [
      "40"
    ],
    "filament_flow_ratio": [
      "0.94"
    ],
    "filament_id": "GFG99",
    "filament_max_volumetric_speed": [
      "11"
    ],
    "filament_z_hop": [
      "0"
    ],
    "from": "system",
    "inherits": "fdm_filament_pet",
    "instantiation": "true",
    "name": "SecKit Generic PETG",
    "nozzle_temperature": [
      "235"
    ],
    "nozzle_temperature_initial_layer": [
      "240"
    ],
    "nozzle_temperature_range_high": [
      "250"
    ],
    "overhang_fan_speed": [
      "100"
    ],
    "overhang_fan_threshold": [
      "25%"
    ],
    "pressure_advance": [
      "0.045"
    ],
    "reduce_fan_stop_start_freq": [
      "1"
    ],
    "setting_id": "GFSA04",
    "slow_down_for_layer_cooling": [
      "1"
    ],
    "slow_down_layer_time": [
      "8"
    ],
    "slow_down_min_speed": [
      "10"
    ],
    "type": "filament"
  },
  "filament/SecKit Generic PLA-CF.json": {
    "compatible_printers": [
      "SecKit SK-Tank 0.4 nozzle",
      "SecKit Go3 0.4 nozzle"
    ],
    "enable_pressure_advance": [
      "1"
    ],
    "filament_flow_ratio": [
      "0.92"
    ],
    "filament_id": "GFL98",
    "filament_max_volumetric_speed": [
      "12"
    ],
    "filament_type": [
      "PLA-CF"
    ],
    "filament_z_hop": [
      "0"
    ],
    "from": "system",
    "inherits": "fdm_filament_pla",
    "instantiation": "true",
    "name": "SecKit Generic PLA-CF",
    "nozzle_temperature": [
      "205"
    ],
    "nozzle_temperature_initial_layer": [
      "210"
    ],
    "pressure_advance": [
      "0.05"
    ],
    "setting_id": "GFSA04",
    "slow_down_layer_time": [
      "7"
    ],
    "type": "filament"
  },
  "filament/SecKit Generic PLA.json": {
    "compatible_printers": [
      "SecKit SK-Tank 0.4 nozzle",
      "SecKit Go3 0.4 nozzle"
    ],
    "enable_pressure_advance": [
      "1"
    ],
    "filament_flow_ratio": [
      "0.92"
    ],
    "filament_id": "GFL99",
    "filament_max_volumetric_speed": [
      "20"
    ],
    "filament_z_hop": [
      "0"
    ],
    "from": "system",
    "inherits": "fdm_filament_pla",
    "instantiation": "true",
    "name": "SecKit Generic PLA",
    "nozzle_temperature": [
      "200"
    ],
    "nozzle_temperature_initial_layer": [
      "205"
    ],
    "pressure_advance": [
      "0.05"
    ],
    "setting_id": "GFSA04",
    "slow_down_layer_time": [
      "8"
    ],
    "type": "filament"
  },
  "filament/SecKit Generic PVA.json": {
    "compatible_printers": [
      "SecKit SK-Tank 0.4 nozzle",
      "SecKit Go3 0.4 nozzle"
    ],
    "enable_pressure_advance": [
      "1"
    ],
    "filament_flow_ratio": [
      "0.95"
    ],
    "filament_id": "GFS99",
    "filament_max_volumetric_speed": [
      "12"
    ],
    "filament_z_hop": [
      "0"
    ],
    "from": "system",
    "inherits": "fdm_filament_pva",
    "instantiation": "true",
    "name": "SecKit Generic PVA",
    "pressure_advance": [
      "0.03"
    ],
    "setting_id": "GFSA04",
    "slow_down_layer_time": [
      "7"
    ],
    "slow_down_min_speed": [
      "10"
    ],
    "type": "filament"
  },
  "filament/SecKit Generic TPU.json": {
    "compatible_printers": [
      "SecKit SK-Tank 0.4 nozzle",
      "SecKit Go3 0.4 nozzle"
    ],
    "enable_pressure_advance": [
      "1"
    ],
    "filament_id": "GFU99",
    "filament_max_volumetric_speed": [
      "5"
    ],
    "filament_z_hop": [
      "0"
    ],
    "from": "system",
    "inherits": "fdm_filament_tpu",
    "instantiation": "true",
    "name": "SecKit Generic TPU",
    "nozzle_temperature": [
      "220"
    ],
    "nozzle_temperature_initial_layer": [
      "220"
    ],
    "pressure_advance": [
      "0.1"
    ],
    "setting_id": "GFSA04",
    "type": "filament"
  },
  "filament/fdm_filament_abs.json": {
    "close_fan_the_first_x_layers": [
      "3"
    ],
    "cool_plate_temp": [
      "105"
    ],
    "cool_plate_temp_initial_layer": [
      "105"
    ],
    "eng_plate_temp": [
      "105"
    ],
    "eng_plate_temp_initial_layer": [
      "105"
    ],
    "fan_cooling_layer_time": [
      "30"
    ],
    "fan_max_speed": [
      "80"
    ],
    "fan_min_speed": [
      "10"
    ],
    "filament_cost": [
      "20"
    ],
    "filament_density": [
      "1.04"
    ],
    "filament_max_volumetric_speed": [
      "28.6"
    ],
    "filament_type": [
      "ABS"
    ],
    "from": "system",
    "hot_plate_temp": [
      "105"
    ],
    "hot_plate_temp_initial_layer": [
      "105"
    ],
    "inherits": "fdm_filament_common",
    "instantiation": "false",
    "name": "fdm_filament_abs",
    "nozzle_temperature": [
      "260"
    ],
    "nozzle_temperature_initial_layer": [
      "260"
    ],
    "nozzle_temperature_range_high": [
      "270"
    ],
    "nozzle_temperature_range_low": [
      "240"
    ],
    "overhang_fan_speed": [
      "80"
    ],
    "overhang_fan_threshold": [
      "25%"
    ],
    "reduce_fan_stop_start_freq": [
      "1"
    ],
    "slow_down_for_layer_cooling": [
      "1"
    ],
    "slow_down_layer_time": [
      "3"
    ],
    "slow_down_min_speed": [
      "10"
    ],
    "temperature_vitrification": [
      "110"
    ],
    "textured_plate_temp": [
      "105"
    ],
    "textured_plate_temp_initial_layer": [
      "105"
    ],
    "type": "filament"
  },
  "filament/fdm_filament_asa.json": {
    "close_fan_the_first_x_layers": [
      "3"
    ],
    "cool_plate_temp": [
      "105"
    ],
    "cool_plate_temp_initial_layer": [
      "105"
    ],
    "eng_plate_temp": [
      "105"
    ],
    "eng_plate_temp_initial_layer": [
      "105"
    ],
    "fan_cooling_layer_time": [
      "35"
    ],
    "fan_max_speed": [
      "80"
    ],
    "fan_min_speed": [
      "10"
    ],
    "filament_cost": [
      "20"
    ],
    "filament_density": [
      "1.04"
    ],
    "filament_max_volumetric_speed": [
      "28.6"
    ],
    "filament_type": [
      "ASA"
    ],
    "from": "system",
    "hot_plate_temp": [
      "105"
    ],
    "hot_plate_temp_initial_layer": [
      "105"
    ],
    "inherits": "fdm_filament_common",
    "instantiation": "false",
    "name": "fdm_filament_asa",
    "nozzle_temperature": [
      "260"
    ],
    "nozzle_temperature_initial_layer": [
      "260"
    ],
    "nozzle_temperature_range_high": [
      "270"
    ],
    "nozzle_temperature_range_low": [
      "240"
    ],
    "overhang_fan_speed": [
      "80"
    ],
    "overhang_fan_threshold": [
      "25%"
    ],
    "reduce_fan_stop_start_freq": [
      "1"
    ],
    "slow_down_for_layer_cooling": [
      "1"
    ],
    "slow_down_layer_time": [
      "3"
    ],
    "slow_down_min_speed": [
      "10"
    ],
    "temperature_vitrification": [
      "110"
    ],
    "textured_plate_temp": [
      "105"
    ],
    "textured_plate_temp_initial_layer": [
      "105"
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
    "cool_plate_temp": [
      "60"
    ],
    "cool_plate_temp_initial_layer": [
      "60"
    ],
    "eng_plate_temp": [
      "60"
    ],
    "eng_plate_temp_initial_layer": [
      "60"
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
    "from": "system",
    "full_fan_speed_layer": [
      "0"
    ],
    "hot_plate_temp": [
      "60"
    ],
    "hot_plate_temp_initial_layer": [
      "60"
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
    "textured_plate_temp": [
      "60"
    ],
    "textured_plate_temp_initial_layer": [
      "60"
    ],
    "type": "filament"
  },
  "filament/fdm_filament_pa.json": {
    "close_fan_the_first_x_layers": [
      "3"
    ],
    "cool_plate_temp": [
      "0"
    ],
    "cool_plate_temp_initial_layer": [
      "0"
    ],
    "eng_plate_temp": [
      "100"
    ],
    "eng_plate_temp_initial_layer": [
      "100"
    ],
    "fan_cooling_layer_time": [
      "4"
    ],
    "fan_max_speed": [
      "60"
    ],
    "fan_min_speed": [
      "0"
    ],
    "filament_cost": [
      "20"
    ],
    "filament_density": [
      "1.04"
    ],
    "filament_max_volumetric_speed": [
      "8"
    ],
    "filament_type": [
      "PA"
    ],
    "from": "system",
    "hot_plate_temp": [
      "100"
    ],
    "hot_plate_temp_initial_layer": [
      "100"
    ],
    "inherits": "fdm_filament_common",
    "instantiation": "false",
    "name": "fdm_filament_pa",
    "nozzle_temperature": [
      "290"
    ],
    "nozzle_temperature_initial_layer": [
      "290"
    ],
    "nozzle_temperature_range_high": [
      "300"
    ],
    "nozzle_temperature_range_low": [
      "270"
    ],
    "overhang_fan_speed": [
      "30"
    ],
    "reduce_fan_stop_start_freq": [
      "0"
    ],
    "slow_down_for_layer_cooling": [
      "1"
    ],
    "slow_down_layer_time": [
      "2"
    ],
    "slow_down_min_speed": [
      "10"
    ],
    "temperature_vitrification": [
      "108"
    ],
    "textured_plate_temp": [
      "100"
    ],
    "textured_plate_temp_initial_layer": [
      "100"
    ],
    "type": "filament"
  },
  "filament/fdm_filament_pc.json": {
    "close_fan_the_first_x_layers": [
      "3"
    ],
    "cool_plate_temp": [
      "0"
    ],
    "cool_plate_temp_initial_layer": [
      "0"
    ],
    "eng_plate_temp": [
      "110"
    ],
    "eng_plate_temp_initial_layer": [
      "110"
    ],
    "fan_cooling_layer_time": [
      "30"
    ],
    "fan_max_speed": [
      "60"
    ],
    "fan_min_speed": [
      "10"
    ],
    "filament_cost": [
      "20"
    ],
    "filament_density": [
      "1.04"
    ],
    "filament_max_volumetric_speed": [
      "23.2"
    ],
    "filament_type": [
      "PC"
    ],
    "from": "system",
    "hot_plate_temp": [
      "110"
    ],
    "hot_plate_temp_initial_layer": [
      "110"
    ],
    "inherits": "fdm_filament_common",
    "instantiation": "false",
    "name": "fdm_filament_pc",
    "nozzle_temperature": [
      "280"
    ],
    "nozzle_temperature_initial_layer": [
      "270"
    ],
    "nozzle_temperature_range_high": [
      "280"
    ],
    "nozzle_temperature_range_low": [
      "260"
    ],
    "overhang_fan_speed": [
      "60"
    ],
    "overhang_fan_threshold": [
      "25%"
    ],
    "reduce_fan_stop_start_freq": [
      "1"
    ],
    "slow_down_for_layer_cooling": [
      "1"
    ],
    "slow_down_layer_time": [
      "2"
    ],
    "slow_down_min_speed": [
      "10"
    ],
    "temperature_vitrification": [
      "140"
    ],
    "textured_plate_temp": [
      "110"
    ],
    "textured_plate_temp_initial_layer": [
      "110"
    ],
    "type": "filament"
  },
  "filament/fdm_filament_pet.json": {
    "close_fan_the_first_x_layers": [
      "3"
    ],
    "cool_plate_temp": [
      "60"
    ],
    "cool_plate_temp_initial_layer": [
      "60"
    ],
    "eng_plate_temp": [
      "0"
    ],
    "eng_plate_temp_initial_layer": [
      "0"
    ],
    "fan_cooling_layer_time": [
      "20"
    ],
    "fan_max_speed": [
      "100"
    ],
    "fan_min_speed": [
      "20"
    ],
    "filament_cost": [
      "30"
    ],
    "filament_density": [
      "1.27"
    ],
    "filament_max_volumetric_speed": [
      "25"
    ],
    "filament_start_gcode": [
      "; filament start gcode\n"
    ],
    "filament_type": [
      "PETG"
    ],
    "from": "system",
    "hot_plate_temp": [
      "80"
    ],
    "hot_plate_temp_initial_layer": [
      "80"
    ],
    "inherits": "fdm_filament_common",
    "instantiation": "false",
    "name": "fdm_filament_pet",
    "nozzle_temperature": [
      "255"
    ],
    "nozzle_temperature_initial_layer": [
      "255"
    ],
    "nozzle_temperature_range_high": [
      "260"
    ],
    "nozzle_temperature_range_low": [
      "220"
    ],
    "overhang_fan_speed": [
      "100"
    ],
    "reduce_fan_stop_start_freq": [
      "1"
    ],
    "slow_down_for_layer_cooling": [
      "1"
    ],
    "temperature_vitrification": [
      "80"
    ],
    "textured_plate_temp": [
      "80"
    ],
    "textured_plate_temp_initial_layer": [
      "80"
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
    "cool_plate_temp": [
      "60"
    ],
    "cool_plate_temp_initial_layer": [
      "60"
    ],
    "eng_plate_temp": [
      "60"
    ],
    "eng_plate_temp_initial_layer": [
      "60"
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
    "hot_plate_temp": [
      "60"
    ],
    "hot_plate_temp_initial_layer": [
      "60"
    ],
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
    "textured_plate_temp": [
      "60"
    ],
    "textured_plate_temp_initial_layer": [
      "60"
    ],
    "type": "filament"
  },
  "filament/fdm_filament_pva.json": {
    "additional_cooling_fan_speed": [
      "70"
    ],
    "close_fan_the_first_x_layers": [
      "1"
    ],
    "cool_plate_temp": [
      "35"
    ],
    "cool_plate_temp_initial_layer": [
      "35"
    ],
    "eng_plate_temp": [
      "0"
    ],
    "eng_plate_temp_initial_layer": [
      "0"
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
    "filament_is_support": [
      "1"
    ],
    "filament_max_volumetric_speed": [
      "15"
    ],
    "filament_soluble": [
      "1"
    ],
    "filament_start_gcode": [
      "; filament start gcode\n"
    ],
    "filament_type": [
      "PVA"
    ],
    "from": "system",
    "hot_plate_temp": [
      "45"
    ],
    "hot_plate_temp_initial_layer": [
      "45"
    ],
    "inherits": "fdm_filament_common",
    "instantiation": "false",
    "name": "fdm_filament_pva",
    "nozzle_temperature": [
      "220"
    ],
    "nozzle_temperature_initial_layer": [
      "220"
    ],
    "nozzle_temperature_range_high": [
      "250"
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
      "50"
    ],
    "textured_plate_temp": [
      "45"
    ],
    "textured_plate_temp_initial_layer": [
      "45"
    ],
    "type": "filament"
  },
  "filament/fdm_filament_tpu.json": {
    "additional_cooling_fan_speed": [
      "70"
    ],
    "close_fan_the_first_x_layers": [
      "1"
    ],
    "cool_plate_temp": [
      "30"
    ],
    "cool_plate_temp_initial_layer": [
      "30"
    ],
    "eng_plate_temp": [
      "30"
    ],
    "eng_plate_temp_initial_layer": [
      "30"
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
      "15"
    ],
    "filament_retraction_length": [
      "0.4"
    ],
    "filament_start_gcode": [
      "; filament start gcode\n"
    ],
    "filament_type": [
      "TPU"
    ],
    "from": "system",
    "hot_plate_temp": [
      "35"
    ],
    "hot_plate_temp_initial_layer": [
      "35"
    ],
    "inherits": "fdm_filament_common",
    "instantiation": "false",
    "name": "fdm_filament_tpu",
    "nozzle_temperature": [
      "240"
    ],
    "nozzle_temperature_initial_layer": [
      "240"
    ],
    "nozzle_temperature_range_high": [
      "250"
    ],
    "nozzle_temperature_range_low": [
      "200"
    ],
    "overhang_fan_speed": [
      "100"
    ],
    "reduce_fan_stop_start_freq": [
      "1"
    ],
    "slow_down_for_layer_cooling": [
      "1"
    ],
    "temperature_vitrification": [
      "60"
    ],
    "textured_plate_temp": [
      "35"
    ],
    "textured_plate_temp_initial_layer": [
      "35"
    ],
    "type": "filament"
  }
}

MISC = {}

ASSETS = [
  "Seckit Go3_cover.png",
  "SecKit SK-Tank_cover.png",
  "seckit-hotend.stl",
  "seckit_logo.svg",
  "SK-Go3_Bed.stl",
  "SK-Tank_Bed.stl"
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
