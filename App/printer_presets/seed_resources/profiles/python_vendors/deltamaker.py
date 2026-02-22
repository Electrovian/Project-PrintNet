from __future__ import annotations

VENDOR = "DeltaMaker"
INDEX = {
  "description": "DeltaMaker configurations",
  "filament_list": [
    {
      "name": "fdm_filament_common",
      "sub_path": "filament/fdm_filament_common.json"
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
      "name": "fdm_filament_tpu",
      "sub_path": "filament/fdm_filament_tpu.json"
    },
    {
      "name": "DeltaMaker Generic PETG",
      "sub_path": "filament/DeltaMaker Generic PETG.json"
    },
    {
      "name": "DeltaMaker Brand PLA",
      "sub_path": "filament/DeltaMaker Brand PLA.json"
    },
    {
      "name": "DeltaMaker Generic PLA",
      "sub_path": "filament/DeltaMaker Generic PLA.json"
    },
    {
      "name": "DeltaMaker Generic TPU",
      "sub_path": "filament/DeltaMaker Generic TPU.json"
    }
  ],
  "force_update": "0",
  "machine_list": [
    {
      "name": "fdm_machine_common",
      "sub_path": "machine/fdm_machine_common.json"
    },
    {
      "name": "DeltaMaker 2 0.35 nozzle",
      "sub_path": "machine/DeltaMaker 2 0.35 nozzle.json"
    },
    {
      "name": "DeltaMaker 2T 0.5 nozzle",
      "sub_path": "machine/DeltaMaker 2T 0.5 nozzle.json"
    },
    {
      "name": "DeltaMaker 2XT 0.5 nozzle",
      "sub_path": "machine/DeltaMaker 2XT 0.5 nozzle.json"
    },
    {
      "name": "fdm_klipper_common",
      "sub_path": "machine/fdm_klipper_common.json"
    }
  ],
  "machine_model_list": [
    {
      "name": "DeltaMaker 2",
      "sub_path": "machine/DeltaMaker 2.json"
    },
    {
      "name": "DeltaMaker 2T",
      "sub_path": "machine/DeltaMaker 2T.json"
    },
    {
      "name": "DeltaMaker 2XT",
      "sub_path": "machine/DeltaMaker 2XT.json"
    }
  ],
  "name": "DeltaMaker",
  "process_list": [
    {
      "name": "fdm_process_common",
      "sub_path": "process/fdm_process_common.json"
    },
    {
      "name": "0.12mm Fine @DeltaMaker",
      "sub_path": "process/0.12mm Fine @DeltaMaker.json"
    },
    {
      "name": "0.18mm Standard @DeltaMaker",
      "sub_path": "process/0.18mm Standard @DeltaMaker.json"
    },
    {
      "name": "0.25mm Draft @DeltaMaker",
      "sub_path": "process/0.25mm Draft @DeltaMaker.json"
    },
    {
      "name": "fdm_process_klipper_common",
      "sub_path": "process/fdm_process_klipper_common.json"
    }
  ],
  "url": "",
  "version": "02.03.01.11"
}

MACHINE = {
  "machine/DeltaMaker 2 0.35 nozzle.json": {
    "default_filament_profile": [
      "DeltaMaker Brand PLA",
      "DeltaMaker Generic PLA"
    ],
    "default_print_profile": "0.18mm Standard @DeltaMaker",
    "from": "system",
    "inherits": "fdm_machine_common",
    "instantiation": "true",
    "name": "DeltaMaker 2 0.35 nozzle",
    "nozzle_diameter": [
      "0.35"
    ],
    "printable_area": [
      "-69x-120",
      "-138x0",
      "-69x120",
      "69x120",
      "138x0",
      "69x-120"
    ],
    "printable_height": "260",
    "printer_model": "DeltaMaker 2",
    "printer_variant": "0.35",
    "setting_id": "GM001",
    "type": "machine"
  },
  "machine/DeltaMaker 2.json": {
    "bed_model": "deltamaker_2_buildplate_model.stl",
    "bed_texture": "deltamaker_2_buildplate_texture.svg",
    "default_materials": "DeltaMaker Brand PLA;DeltaMaker Generic PLA",
    "family": "DeltaMaker",
    "machine_tech": "FFF",
    "model_id": "deltamaker-2",
    "name": "DeltaMaker 2",
    "nozzle_diameter": "0.35",
    "type": "machine_model"
  },
  "machine/DeltaMaker 2T 0.5 nozzle.json": {
    "default_filament_profile": [
      "DeltaMaker Brand PLA",
      "DeltaMaker Generic PLA"
    ],
    "default_print_profile": "0.18mm Standard @DeltaMaker",
    "from": "system",
    "inherits": "fdm_machine_common",
    "instantiation": "true",
    "name": "DeltaMaker 2T 0.5 nozzle",
    "nozzle_diameter": [
      "0.5"
    ],
    "printable_area": [
      "-69x-120",
      "-138x0",
      "-69x120",
      "69x120",
      "138x0",
      "69x-120"
    ],
    "printable_height": "460",
    "printer_model": "DeltaMaker 2T",
    "printer_variant": "0.5",
    "setting_id": "GM002",
    "type": "machine"
  },
  "machine/DeltaMaker 2T.json": {
    "bed_model": "deltamaker_2_buildplate_model.stl",
    "bed_texture": "deltamaker_2_buildplate_texture.svg",
    "default_materials": "DeltaMaker Brand PLA;DeltaMaker Generic PLA",
    "family": "DeltaMaker",
    "machine_tech": "FFF",
    "model_id": "deltamaker-2t",
    "name": "DeltaMaker 2T",
    "nozzle_diameter": "0.5",
    "type": "machine_model"
  },
  "machine/DeltaMaker 2XT 0.5 nozzle.json": {
    "default_filament_profile": [
      "DeltaMaker Brand PLA",
      "DeltaMaker Generic PLA"
    ],
    "default_print_profile": "0.25mm Draft @DeltaMaker",
    "from": "system",
    "inherits": "fdm_machine_common",
    "instantiation": "true",
    "name": "DeltaMaker 2XT 0.5 nozzle",
    "nozzle_diameter": [
      "0.5"
    ],
    "printable_area": [
      "-69x-120",
      "-138x0",
      "-69x120",
      "69x120",
      "138x0",
      "69x-120"
    ],
    "printable_height": "565",
    "printer_model": "DeltaMaker 2XT",
    "printer_variant": "0.5",
    "setting_id": "GM003",
    "type": "machine"
  },
  "machine/DeltaMaker 2XT.json": {
    "bed_model": "deltamaker_2_buildplate_model.stl",
    "bed_texture": "deltamaker_2_buildplate_texture.svg",
    "default_materials": "DeltaMaker Brand PLA;DeltaMaker Generic PLA",
    "family": "DeltaMaker",
    "machine_tech": "FFF",
    "model_id": "deltamaker-2xt",
    "name": "DeltaMaker 2XT",
    "nozzle_diameter": "0.5",
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
      "DeltaMaker Generic PLA"
    ],
    "default_print_profile": "0.20mm Standard @DeltaMaker 2 0.35 nozzle",
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
    "machine_end_gcode": "END_PRINT",
    "machine_max_acceleration_e": [
      "5000",
      "5000"
    ],
    "machine_max_acceleration_extruding": [
      "5000",
      "5000"
    ],
    "machine_max_acceleration_retracting": [
      "5000",
      "5000"
    ],
    "machine_max_acceleration_travel": [
      "5000",
      "5000"
    ],
    "machine_max_acceleration_x": [
      "5000",
      "5000"
    ],
    "machine_max_acceleration_y": [
      "5000",
      "5000"
    ],
    "machine_max_acceleration_z": [
      "1000",
      "1000"
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
      "2",
      "2"
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
      "120",
      "120"
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
    "machine_start_gcode": "M190 S[bed_temperature_initial_layer_single]\nM109 S[nozzle_temperature_initial_layer]\nSTART_PRINT EXTRUDER=[nozzle_temperature_initial_layer] BED=[bed_temperature_initial_layer_single]\n",
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
    "printer_variant": "0.5",
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
      "8"
    ],
    "retraction_minimum_travel": [
      "1"
    ],
    "retraction_speed": [
      "60"
    ],
    "scan_first_layer": "0",
    "silent_mode": "1",
    "single_extruder_multi_material": "1",
    "type": "machine",
    "wipe": [
      "1"
    ],
    "z_hop": [
      "0.8"
    ],
    "z_hop_types": "Normal Lift"
  },
  "machine/fdm_machine_common.json": {
    "auxiliary_fan": "0",
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
    "gcode_flavor": "klipper",
    "instantiation": "false",
    "layer_change_gcode": ";AFTER_LAYER_CHANGE\n;[layer_z]",
    "machine_end_gcode": "G28\nM104 S0\nM84 ; disable motors",
    "machine_max_acceleration_e": [
      "5000"
    ],
    "machine_max_acceleration_extruding": [
      "5000"
    ],
    "machine_max_acceleration_retracting": [
      "5000"
    ],
    "machine_max_acceleration_x": [
      "3500"
    ],
    "machine_max_acceleration_y": [
      "3500"
    ],
    "machine_max_acceleration_z": [
      "500"
    ],
    "machine_max_jerk_e": [
      "2.5"
    ],
    "machine_max_jerk_x": [
      "10"
    ],
    "machine_max_jerk_y": [
      "10"
    ],
    "machine_max_jerk_z": [
      "2"
    ],
    "machine_max_speed_e": [
      "120"
    ],
    "machine_max_speed_x": [
      "500"
    ],
    "machine_max_speed_y": [
      "500"
    ],
    "machine_max_speed_z": [
      "150"
    ],
    "machine_min_extruding_rate": [
      "0"
    ],
    "machine_min_travel_rate": [
      "0"
    ],
    "machine_pause_gcode": "",
    "machine_start_gcode": "M104 S[nozzle_temperature_initial_layer] ; set temp\nG28\nM109 S[nozzle_temperature_initial_layer] ; wait for temp\nG28\nG91 ; relative positioning\nG1 Z-40 F4000\nG90 ; absolute positioning\n",
    "max_layer_height": [
      "0.3"
    ],
    "min_layer_height": [
      "0.1"
    ],
    "name": "fdm_machine_common",
    "nozzle_type": "undefine",
    "printer_settings_id": "",
    "printer_technology": "FFF",
    "retract_before_wipe": [
      "0%"
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
      "7"
    ],
    "retraction_minimum_travel": [
      "2"
    ],
    "retraction_speed": [
      "80"
    ],
    "silent_mode": "1",
    "single_extruder_multi_material": "0",
    "type": "machine",
    "z_hop": [
      "0.8"
    ],
    "z_lift_type": "NormalLift"
  }
}

PROCESS = {
  "process/0.12mm Fine @DeltaMaker.json": {
    "bottom_shell_layers": "6",
    "detect_thin_wall": "1",
    "from": "system",
    "infill_wall_overlap": "35%",
    "inherits": "fdm_process_common",
    "instantiation": "true",
    "ironing_flow": "15%",
    "ironing_spacing": "0.1",
    "layer_height": "0.12",
    "name": "0.12mm Fine @DeltaMaker",
    "setting_id": "GP004",
    "skirt_distance": "3",
    "skirt_height": "1",
    "sparse_infill_density": "15%",
    "top_shell_layers": "8",
    "travel_speed": "150",
    "tree_support_branch_angle": "40",
    "type": "process"
  },
  "process/0.18mm Standard @DeltaMaker.json": {
    "detect_thin_wall": "1",
    "from": "system",
    "infill_wall_overlap": "35%",
    "inherits": "fdm_process_common",
    "initial_layer_print_height": "0.25",
    "inner_wall_speed": "40",
    "instantiation": "true",
    "ironing_flow": "15%",
    "ironing_spacing": "0.1",
    "ironing_speed": "15",
    "layer_height": "0.18",
    "name": "0.18mm Standard @DeltaMaker",
    "overhang_2_4_speed": "20",
    "overhang_3_4_speed": "15",
    "setting_id": "GP004",
    "skirt_distance": "3",
    "skirt_height": "1",
    "skirt_loops": "2",
    "sparse_infill_density": "15%",
    "sparse_infill_speed": "40",
    "top_surface_speed": "15",
    "type": "process",
    "wall_loops": "3"
  },
  "process/0.25mm Draft @DeltaMaker.json": {
    "adaptive_layer_height": "1",
    "bottom_shell_layers": "3",
    "bridge_speed": "60",
    "detect_thin_wall": "1",
    "from": "system",
    "infill_wall_overlap": "35%",
    "inherits": "fdm_process_common",
    "instantiation": "true",
    "ironing_flow": "15%",
    "layer_height": "0.25",
    "name": "0.25mm Draft @DeltaMaker",
    "overhang_2_4_speed": "20",
    "overhang_3_4_speed": "15",
    "print_settings_id": "",
    "setting_id": "GP004",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.40",
    "standby_temperature_delta": "-5",
    "top_shell_layers": "4",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "2"
  },
  "process/fdm_process_common.json": {
    "adaptive_layer_height": "0",
    "bottom_shell_layers": "4",
    "bottom_shell_thickness": "0.8",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.98",
    "bridge_no_support": "0",
    "bridge_speed": "100",
    "brim_object_gap": "0.1",
    "brim_type": "no_brim",
    "brim_width": "4",
    "compatible_printers": [
      "DeltaMaker 2 0.35 nozzle",
      "DeltaMaker 2T 0.5 nozzle",
      "DeltaMaker 2XT 0.5 nozzle"
    ],
    "default_acceleration": "1000",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "0",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "filename_format": "{input_filename_base}_{layer_height}mm_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "30",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "25%",
    "initial_layer_acceleration": "500",
    "initial_layer_infill_speed": "20",
    "initial_layer_line_width": "120%",
    "initial_layer_print_height": "0.25",
    "initial_layer_speed": "20",
    "initial_layer_travel_speed": "50%",
    "inner_wall_acceleration": "1000",
    "inner_wall_line_width": "110%",
    "inner_wall_speed": "80",
    "instantiation": "false",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "120%",
    "internal_solid_infill_speed": "75",
    "ironing_flow": "10%",
    "ironing_spacing": "0.15",
    "ironing_speed": "30",
    "ironing_type": "no ironing",
    "layer_height": "0.2",
    "line_width": "120%",
    "max_travel_detour_distance": "20.0",
    "min_skirt_length": "4",
    "minimum_sparse_infill_area": "15",
    "name": "fdm_process_common",
    "outer_wall_acceleration": "700",
    "outer_wall_line_width": "100%",
    "outer_wall_speed": "50",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "50",
    "overhang_3_4_speed": "30",
    "overhang_4_4_speed": "10",
    "prime_tower_width": "12.0",
    "print_sequence": "by layer",
    "print_settings_id": "",
    "raft_layers": "0",
    "reduce_crossing_wall": "0",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "seam_position": "aligned",
    "skirt_distance": "3.0",
    "skirt_height": "2",
    "skirt_loops": "3",
    "slow_down_layers": "2",
    "slowdown_for_curled_perimeters": "1",
    "sparse_infill_density": "50%",
    "sparse_infill_line_width": "100%",
    "sparse_infill_pattern": "gyroid",
    "sparse_infill_speed": "80",
    "spiral_mode": "0",
    "standby_temperature_delta": "-5",
    "support_base_pattern": "default",
    "support_base_pattern_spacing": "2.5",
    "support_bottom_z_distance": "0.25",
    "support_filament": "0",
    "support_interface_bottom_layers": "0",
    "support_interface_filament": "0",
    "support_interface_loop_pattern": "0",
    "support_interface_spacing": "0.25",
    "support_interface_speed": "80",
    "support_interface_top_layers": "1",
    "support_line_width": "110%",
    "support_object_xy_distance": "0.8",
    "support_on_build_plate_only": "0",
    "support_speed": "75",
    "support_threshold_angle": "25",
    "support_top_z_distance": "0.25",
    "support_type": "tree(auto)",
    "top_shell_layers": "4",
    "top_shell_thickness": "0.8",
    "top_surface_acceleration": "1000",
    "top_surface_line_width": "100%",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "50",
    "travel_acceleration": "1000",
    "travel_speed": "150",
    "tree_support_branch_angle": "45",
    "tree_support_wall_count": "0",
    "tree_support_with_infill": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "2",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/fdm_process_klipper_common.json": {
    "default_acceleration": "5000",
    "exclude_object": "1",
    "from": "system",
    "gap_infill_speed": "100",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "500",
    "initial_layer_infill_speed": "105",
    "initial_layer_speed": "50",
    "inner_wall_acceleration": "5000",
    "inner_wall_speed": "120",
    "instantiation": "false",
    "internal_solid_infill_speed": "120",
    "name": "fdm_process_klipper_common",
    "outer_wall_acceleration": "3000",
    "outer_wall_speed": "120",
    "sparse_infill_speed": "120",
    "top_surface_acceleration": "3000",
    "top_surface_speed": "100",
    "travel_acceleration": "6000",
    "travel_speed": "250",
    "type": "process"
  }
}

FILAMENT = {
  "filament/DeltaMaker Brand PLA.json": {
    "compatible_printers": [
      "DeltaMaker 2 0.35 nozzle",
      "DeltaMaker 2T 0.5 nozzle",
      "DeltaMaker 2XT 0.5 nozzle"
    ],
    "filament_flow_ratio": [
      "0.987"
    ],
    "filament_id": "GFL99",
    "filament_max_volumetric_speed": [
      "12"
    ],
    "filament_vendor": [
      "DeltaMaker"
    ],
    "from": "system",
    "inherits": "fdm_filament_pla",
    "instantiation": "true",
    "name": "DeltaMaker Brand PLA",
    "nozzle_temperature": [
      "230"
    ],
    "nozzle_temperature_initial_layer": [
      "235"
    ],
    "nozzle_temperature_range_high": [
      "235"
    ],
    "nozzle_temperature_range_low": [
      "210"
    ],
    "setting_id": "GFSL99",
    "slow_down_layer_time": [
      "8"
    ],
    "type": "filament"
  },
  "filament/DeltaMaker Generic PETG.json": {
    "compatible_printers": [
      "DeltaMaker 2 0.35 nozzle",
      "DeltaMaker 2T 0.5 nozzle",
      "DeltaMaker 2XT 0.5 nozzle"
    ],
    "fan_cooling_layer_time": [
      "30"
    ],
    "fan_max_speed": [
      "40"
    ],
    "fan_min_speed": [
      "20"
    ],
    "filament_flow_ratio": [
      "0.95"
    ],
    "filament_id": "GFG99",
    "filament_max_volumetric_speed": [
      "2"
    ],
    "filament_start_gcode": [
      "; filament start gcode\n"
    ],
    "from": "system",
    "inherits": "fdm_filament_pet",
    "instantiation": "true",
    "name": "DeltaMaker Generic PETG",
    "overhang_fan_speed": [
      "90"
    ],
    "reduce_fan_stop_start_freq": [
      "1"
    ],
    "setting_id": "GFSG99",
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
  "filament/DeltaMaker Generic PLA.json": {
    "compatible_printers": [
      "DeltaMaker 2 0.35 nozzle",
      "DeltaMaker 2T 0.5 nozzle",
      "DeltaMaker 2XT 0.5 nozzle"
    ],
    "filament_flow_ratio": [
      "0.987"
    ],
    "filament_id": "GFL99",
    "filament_max_volumetric_speed": [
      "10"
    ],
    "from": "system",
    "inherits": "fdm_filament_pla",
    "instantiation": "true",
    "name": "DeltaMaker Generic PLA",
    "setting_id": "GFSA04",
    "slow_down_layer_time": [
      "8"
    ],
    "type": "filament"
  },
  "filament/DeltaMaker Generic TPU.json": {
    "compatible_printers": [
      "DeltaMaker 2 0.35 nozzle",
      "DeltaMaker 2T 0.5 nozzle",
      "DeltaMaker 2XT 0.5 nozzle"
    ],
    "filament_flow_ratio": [
      "0.94"
    ],
    "filament_id": "GFB99",
    "filament_max_volumetric_speed": [
      "4.5"
    ],
    "from": "system",
    "inherits": "fdm_filament_tpu",
    "instantiation": "true",
    "name": "DeltaMaker Generic TPU",
    "setting_id": "GFSA04",
    "type": "filament"
  },
  "filament/fdm_filament_common.json": {
    "bed_type": [
      "Cool Plate"
    ],
    "close_fan_the_first_x_layers": [
      "1"
    ],
    "cool_plate_temp": [
      "0"
    ],
    "cool_plate_temp_initial_layer": [
      "0"
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
      "38"
    ],
    "filament_density": [
      "1.25"
    ],
    "filament_deretraction_speed": [
      "150"
    ],
    "filament_diameter": [
      "1.75"
    ],
    "filament_end_gcode": [
      "; filament end gcode \n"
    ],
    "filament_flow_ratio": [
      "1.0"
    ],
    "filament_max_volumetric_speed": [
      "15"
    ],
    "filament_minimal_purge_on_wipe_tower": [
      "15"
    ],
    "filament_retract_before_wipe": [
      "1"
    ],
    "filament_retract_restart_extra": [
      "0.0"
    ],
    "filament_retract_when_changing_layer": [
      "0"
    ],
    "filament_retraction_length": [
      "8.0"
    ],
    "filament_retraction_minimum_travel": [
      "3.0"
    ],
    "filament_retraction_speed": [
      "150"
    ],
    "filament_settings_id": [
      ""
    ],
    "filament_soluble": [
      "0"
    ],
    "filament_start_gcode": [
      "; filament start gcode\n"
    ],
    "filament_type": [
      "PLA"
    ],
    "filament_vendor": [
      "Generic"
    ],
    "filament_wipe": [
      "1"
    ],
    "filament_wipe_distance": [
      "8.0"
    ],
    "filament_z_hop": [
      "0.8"
    ],
    "filament_z_hop_types": [
      "nil"
    ],
    "from": "system",
    "full_fan_speed_layer": [
      "0"
    ],
    "hot_plate_temp": [
      "0"
    ],
    "hot_plate_temp_initial_layer": [
      "0"
    ],
    "instantiation": "false",
    "name": "fdm_filament_common",
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
      "8"
    ],
    "slow_down_min_speed": [
      "10"
    ],
    "temperature_vitrification": [
      "60"
    ],
    "textured_plate_temp": [
      "0"
    ],
    "textured_plate_temp_initial_layer": [
      "0"
    ],
    "type": "filament"
  },
  "filament/fdm_filament_pet.json": {
    "close_fan_the_first_x_layers": [
      "3"
    ],
    "fan_cooling_layer_time": [
      "15"
    ],
    "fan_max_speed": [
      "40"
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
      "0"
    ],
    "filament_start_gcode": [
      "; filament start gcode\n"
    ],
    "filament_type": [
      "PETG"
    ],
    "from": "system",
    "inherits": "fdm_filament_common",
    "instantiation": "false",
    "name": "fdm_filament_pet",
    "nozzle_temperature": [
      "250"
    ],
    "nozzle_temperature_initial_layer": [
      "240"
    ],
    "nozzle_temperature_range_high": [
      "255"
    ],
    "nozzle_temperature_range_low": [
      "235"
    ],
    "overhang_fan_speed": [
      "50"
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
    "type": "filament"
  },
  "filament/fdm_filament_pla.json": {
    "close_fan_the_first_x_layers": [
      "1"
    ],
    "fan_cooling_layer_time": "100",
    "fan_max_speed": [
      "100"
    ],
    "fan_min_speed": [
      "100"
    ],
    "filament_cost": [
      "29"
    ],
    "filament_density": [
      "1.24"
    ],
    "filament_max_volumetric_speed": [
      "0"
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
      "210"
    ],
    "nozzle_temperature_initial_layer": [
      "205"
    ],
    "nozzle_temperature_range_high": [
      "210"
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
  },
  "filament/fdm_filament_tpu.json": {
    "close_fan_the_first_x_layers": [
      "3"
    ],
    "fan_cooling_layer_time": [
      "30"
    ],
    "fan_max_speed": [
      "5"
    ],
    "fan_min_speed": [
      "5"
    ],
    "filament_cost": [
      "20"
    ],
    "filament_density": [
      "1.10"
    ],
    "filament_max_volumetric_speed": [
      "0"
    ],
    "filament_type": [
      "TPU"
    ],
    "from": "system",
    "inherits": "fdm_filament_common",
    "instantiation": "false",
    "name": "fdm_filament_tpu",
    "nozzle_temperature": [
      "235"
    ],
    "nozzle_temperature_initial_layer": [
      "240"
    ],
    "nozzle_temperature_range_high": [
      "240"
    ],
    "nozzle_temperature_range_low": [
      "235"
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
      "15"
    ],
    "slow_down_min_speed": [
      "10"
    ],
    "temperature_vitrification": [
      "110"
    ],
    "type": "filament"
  }
}

MISC = {}

ASSETS = [
  "DeltaMaker 2_cover.png",
  "DeltaMaker 2T_cover.png",
  "DeltaMaker 2XT_cover.png",
  "deltamaker_2_buildplate_model.stl",
  "deltamaker_2_buildplate_texture.svg"
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
