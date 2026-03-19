from __future__ import annotations

VENDOR = "RH3D"
INDEX = {
  "description": "RH3D - printer profiles",
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
      "name": "fdm_filament_pccf",
      "sub_path": "filament/fdm_filament_pccf.json"
    },
    {
      "name": "fdm_filament_petg",
      "sub_path": "filament/fdm_filament_petg.json"
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
      "name": "Generic ABS @E3NG v1.2S",
      "sub_path": "filament/Generic ABS @E3NG v1.2S.json"
    },
    {
      "name": "Generic ASA @E3NG v1.2S",
      "sub_path": "filament/Generic ASA @E3NG v1.2S.json"
    },
    {
      "name": "Generic PCCF @E3NG v1.2S",
      "sub_path": "filament/Generic PCCF @E3NG v1.2S.json"
    },
    {
      "name": "Generic PETG @E3NG v1.2S",
      "sub_path": "filament/Generic PETG @E3NG v1.2S.json"
    },
    {
      "name": "Generic PLA @E3NG v1.2S",
      "sub_path": "filament/Generic PLA @E3NG v1.2S.json"
    },
    {
      "name": "Generic TPU @E3NG v1.2S",
      "sub_path": "filament/Generic TPU @E3NG v1.2S.json"
    }
  ],
  "force_update": "0",
  "machine_list": [
    {
      "name": "fdm_machine_common",
      "sub_path": "machine/fdm_machine_common.json"
    },
    {
      "name": "fdm_common_E3NG v1.2S",
      "sub_path": "machine/fdm_common_E3NG v1.2S.json"
    },
    {
      "name": "E3NG v1.2S - 0.2 nozzle",
      "sub_path": "machine/E3NG v1.2S - 0.2 nozzle.json"
    },
    {
      "name": "E3NG v1.2S - 0.3 nozzle",
      "sub_path": "machine/E3NG v1.2S - 0.3 nozzle.json"
    },
    {
      "name": "E3NG v1.2S - 0.4 nozzle",
      "sub_path": "machine/E3NG v1.2S - 0.4 nozzle.json"
    },
    {
      "name": "E3NG v1.2S - 0.5 nozzle",
      "sub_path": "machine/E3NG v1.2S - 0.5 nozzle.json"
    },
    {
      "name": "E3NG v1.2S - 0.6 nozzle",
      "sub_path": "machine/E3NG v1.2S - 0.6 nozzle.json"
    }
  ],
  "machine_model_list": [
    {
      "name": "E3NG v1.2S",
      "sub_path": "machine/E3NG v1.2S.json"
    }
  ],
  "name": "RH3D",
  "process_list": [
    {
      "name": "fdm_process_common",
      "sub_path": "process/fdm_process_common.json"
    },
    {
      "name": "process_common_E3NG v1.2S",
      "sub_path": "process/process_common_E3NG v1.2S.json"
    },
    {
      "name": "0.20mm Slow @E3NG v1.2S",
      "sub_path": "process/0.20mm Slow @E3NG v1.2S.json"
    },
    {
      "name": "0.10mm Standard @E3NG v1.2S",
      "sub_path": "process/0.10mm Standard @E3NG v1.2S.json"
    },
    {
      "name": "0.15mm Standard @E3NG v1.2S",
      "sub_path": "process/0.15mm Standard @E3NG v1.2S.json"
    },
    {
      "name": "0.20mm Standard @E3NG v1.2S",
      "sub_path": "process/0.20mm Standard @E3NG v1.2S.json"
    },
    {
      "name": "0.25mm Standard @E3NG v1.2S",
      "sub_path": "process/0.25mm Standard @E3NG v1.2S.json"
    },
    {
      "name": "0.20mm Fast @E3NG v1.2S",
      "sub_path": "process/0.20mm Fast @E3NG v1.2S.json"
    },
    {
      "name": "0.25mm Fast @E3NG v1.2S",
      "sub_path": "process/0.25mm Fast @E3NG v1.2S.json"
    }
  ],
  "version": "00.06.10.25"
}

MACHINE = {
  "machine/E3NG v1.2S - 0.2 nozzle.json": {
    "default_print_profile": "0.10mm Standard @E3NG v1.2S",
    "from": "system",
    "inherits": "fdm_common_E3NG v1.2S",
    "instantiation": "true",
    "name": "E3NG v1.2S - 0.2 nozzle",
    "nozzle_diameter": [
      "0.2"
    ],
    "printer_model": "E3NG v1.2S",
    "printer_variant": "0.2",
    "type": "machine"
  },
  "machine/E3NG v1.2S - 0.3 nozzle.json": {
    "default_print_profile": "0.15mm Standard @E3NG v1.2S",
    "from": "system",
    "inherits": "fdm_common_E3NG v1.2S",
    "instantiation": "true",
    "name": "E3NG v1.2S - 0.3 nozzle",
    "nozzle_diameter": [
      "0.3"
    ],
    "printer_model": "E3NG v1.2S",
    "printer_variant": "0.3",
    "type": "machine"
  },
  "machine/E3NG v1.2S - 0.4 nozzle.json": {
    "default_print_profile": "0.20mm Standard @E3NG v1.2S",
    "from": "system",
    "inherits": "fdm_common_E3NG v1.2S",
    "instantiation": "true",
    "name": "E3NG v1.2S - 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "printer_model": "E3NG v1.2S",
    "printer_variant": "0.4",
    "type": "machine"
  },
  "machine/E3NG v1.2S - 0.5 nozzle.json": {
    "default_print_profile": "0.20mm Standard @E3NG v1.2S",
    "from": "system",
    "inherits": "fdm_common_E3NG v1.2S",
    "instantiation": "true",
    "name": "E3NG v1.2S - 0.5 nozzle",
    "nozzle_diameter": [
      "0.5"
    ],
    "printer_model": "E3NG v1.2S",
    "printer_variant": "0.5",
    "type": "machine"
  },
  "machine/E3NG v1.2S - 0.6 nozzle.json": {
    "default_print_profile": "0.25mm Standard @E3NG v1.2S",
    "from": "system",
    "inherits": "fdm_common_E3NG v1.2S",
    "instantiation": "true",
    "name": "E3NG v1.2S - 0.6 nozzle",
    "nozzle_diameter": [
      "0.6"
    ],
    "printer_model": "E3NG v1.2S",
    "printer_variant": "0.6",
    "type": "machine"
  },
  "machine/E3NG v1.2S.json": {
    "bed_model": "E3NG-bed.stl",
    "bed_texture": "E3NG-bed-texture.svg",
    "default_materials": "Generic ABS @E3NG v1.2S;Generic ASA @E3NG v1.2S;Generic PCCF @E3NG v1.2S;Generic PETG @E3NG v1.2S;Generic PLA @E3NG v1.2S;Generic TPU @E3NG v1.2S",
    "family": "RH3D",
    "hotend_model": "",
    "machine_tech": "FFF",
    "model_id": "E3NGV12S",
    "name": "E3NG v1.2S",
    "nozzle_diameter": "0.2;0.3;0.4;0.5;0.6",
    "type": "machine_model"
  },
  "machine/fdm_common_E3NG v1.2S.json": {
    "extruder_clearance_height_to_lid": "140",
    "extruder_clearance_height_to_rod": "36",
    "extruder_clearance_radius": "65",
    "from": "system",
    "inherits": "fdm_machine_common",
    "instantiation": "false",
    "machine_max_acceleration_e": [
      "7500",
      "7500"
    ],
    "machine_max_acceleration_extruding": [
      "20000",
      "20000"
    ],
    "machine_max_acceleration_retracting": [
      "20000",
      "20000"
    ],
    "machine_max_acceleration_travel": [
      "10000",
      "10000"
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
      "500"
    ],
    "machine_max_speed_e": [
      "25",
      "25"
    ],
    "machine_max_speed_x": [
      "400",
      "400"
    ],
    "machine_max_speed_y": [
      "400",
      "400"
    ],
    "machine_max_speed_z": [
      "12",
      "12"
    ],
    "name": "fdm_common_E3NG v1.2S",
    "printable_area": [
      "0x0",
      "232x0",
      "232x232",
      "0x232"
    ],
    "printable_height": "245",
    "printer_model": "E3NG v1.2S",
    "printer_notes": [
      "Design by RH3D"
    ],
    "retract_before_wipe": "80%",
    "retract_length_toolchange": "0",
    "retract_lift_below": "240",
    "retraction_minimum_travel": "1.5",
    "travel_slope": "1",
    "type": "machine"
  },
  "machine/fdm_machine_common.json": {
    "before_layer_change_gcode": ";BEFORE_LAYER_CHANGE\nG92 E0",
    "change_filament_gcode": "PAUSE\nG1 E1.0 F300 ; prime after color change",
    "default_filament_profile": "Generic PLA @E3NG v1.2S",
    "deretraction_speed": "60",
    "emit_machine_limits_to_gcode": "0",
    "extruder_colour": "#02aba2",
    "extruder_offset": "0x0",
    "from": "system",
    "gcode_flavor": "klipper",
    "instantiation": "false",
    "layer_change_gcode": ";AFTER_LAYER_CHANGE",
    "machine_end_gcode": "PRINT_END",
    "machine_min_extruding_rate": [
      "0",
      "0"
    ],
    "machine_min_travel_rate": [
      "0",
      "0"
    ],
    "machine_pause_gcode": "PAUSE\n",
    "machine_start_gcode": "M104 S0 ; Stops EONSlicer from sending temp waits separately\nM140 S0\nPRINT_START EXTRUDER=[first_layer_temperature] BED=[first_layer_bed_temperature]\n; Start of actual GCode for the print",
    "max_layer_height": "0.30",
    "min_layer_height": "0.10",
    "name": "fdm_machine_common",
    "nozzle_diameter": "0.4",
    "printer_settings_id": "",
    "printer_structure": "corexy",
    "printer_technology": "FFF",
    "printer_variant": "0.4",
    "retract_length_toolchange": "2",
    "retract_restart_extra": "0",
    "retract_restart_extra_toolchange": "0",
    "retract_when_changing_layer": "1",
    "retraction_length": "0.6",
    "retraction_minimum_travel": "1",
    "retraction_speed": "40",
    "single_extruder_multi_material": "0",
    "thumbnails": [
      "16x16/QOI",
      "313x173/QOI",
      "440x240/QOI",
      "480x240/QOI",
      "32x32/PNG",
      "320x240/PNG",
      "640x480/PNG"
    ],
    "type": "machine",
    "use_firmware_retraction": "1",
    "use_relative_e_distances": "1",
    "wipe": "1",
    "z_hop": "0.0",
    "z_hop_types": "Slope Lift"
  }
}

PROCESS = {
  "process/0.10mm Standard @E3NG v1.2S.json": {
    "compatible_printers": [
      "E3NG v1.2S - 0.2 nozzle",
      "E3NG v1.2S - 0.3 nozzle",
      "E3NG v1.2S - 0.4 nozzle"
    ],
    "from": "system",
    "inherits": "process_common_E3NG v1.2S",
    "initial_layer_print_height": "0.15",
    "instantiation": "true",
    "layer_height": "0.1",
    "name": "0.10mm Standard @E3NG v1.2S",
    "setting_id": "NG2010",
    "type": "process"
  },
  "process/0.15mm Standard @E3NG v1.2S.json": {
    "compatible_printers": [
      "E3NG v1.2S - 0.2 nozzle",
      "E3NG v1.2S - 0.3 nozzle",
      "E3NG v1.2S - 0.4 nozzle",
      "E3NG v1.2S - 0.5 nozzle"
    ],
    "from": "system",
    "inherits": "process_common_E3NG v1.2S",
    "initial_layer_print_height": "0.2",
    "instantiation": "true",
    "layer_height": "0.15",
    "name": "0.15mm Standard @E3NG v1.2S",
    "setting_id": "NG2015",
    "type": "process"
  },
  "process/0.20mm Fast @E3NG v1.2S.json": {
    "bridge_acceleration": "5000",
    "bridge_speed": "75",
    "compatible_printers": [
      "E3NG v1.2S - 0.4 nozzle",
      "E3NG v1.2S - 0.5 nozzle",
      "E3NG v1.2S - 0.6 nozzle"
    ],
    "default_acceleration": "10000",
    "from": "system",
    "gap_infill_speed": "300",
    "infill_combination": "1",
    "inherits": "process_common_E3NG v1.2S",
    "initial_layer_acceleration": "7500",
    "initial_layer_infill_speed": "150",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "100",
    "inner_wall_acceleration": "10000",
    "inner_wall_speed": "340",
    "instantiation": "true",
    "internal_solid_infill_acceleration": "10000",
    "internal_solid_infill_line_width": "125%",
    "internal_solid_infill_speed": "340",
    "ironing_speed": "150",
    "layer_height": "0.2",
    "name": "0.20mm Fast @E3NG v1.2S",
    "only_one_wall_first_layer": "0",
    "only_one_wall_top": "0",
    "outer_wall_acceleration": "7500",
    "outer_wall_speed": "300",
    "overhang_1_4_speed": "100",
    "overhang_2_4_speed": "50",
    "overhang_3_4_speed": "30",
    "overhang_4_4_speed": "15",
    "reduce_crossing_wall": "0",
    "seam_position": "nearest",
    "setting_id": "NG3020",
    "small_perimeter_speed": "300",
    "sparse_infill_acceleration": "12500",
    "sparse_infill_line_width": "125%",
    "sparse_infill_speed": "400",
    "support_interface_speed": "120",
    "top_surface_acceleration": "7500",
    "top_surface_line_width": "100%",
    "top_surface_speed": "300",
    "travel_acceleration": "10000",
    "travel_speed": "400",
    "type": "process"
  },
  "process/0.20mm Slow @E3NG v1.2S.json": {
    "bridge_acceleration": "2000",
    "bridge_speed": "40",
    "compatible_printers": [
      "E3NG v1.2S - 0.4 nozzle",
      "E3NG v1.2S - 0.5 nozzle",
      "E3NG v1.2S - 0.6 nozzle"
    ],
    "default_acceleration": "3000",
    "from": "system",
    "gap_infill_speed": "140",
    "infill_combination": "0",
    "inherits": "process_common_E3NG v1.2S",
    "initial_layer_acceleration": "3000",
    "initial_layer_infill_speed": "75",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "60",
    "inner_wall_acceleration": "3000",
    "inner_wall_speed": "140",
    "instantiation": "true",
    "internal_solid_infill_acceleration": "3000",
    "internal_solid_infill_line_width": "125%",
    "internal_solid_infill_speed": "140",
    "ironing_speed": "80",
    "layer_height": "0.2",
    "name": "0.20mm Slow @E3NG v1.2S",
    "only_one_wall_first_layer": "1",
    "only_one_wall_top": "1",
    "outer_wall_acceleration": "3000",
    "outer_wall_speed": "140",
    "overhang_1_4_speed": "60",
    "overhang_2_4_speed": "35",
    "overhang_3_4_speed": "20",
    "overhang_4_4_speed": "8",
    "reduce_crossing_wall": "1",
    "seam_position": "aligned",
    "setting_id": "NG1020",
    "small_perimeter_speed": "140",
    "sparse_infill_acceleration": "4000",
    "sparse_infill_line_width": "125%",
    "sparse_infill_speed": "140",
    "support_interface_speed": "60",
    "top_surface_acceleration": "2000",
    "top_surface_line_width": "100%",
    "top_surface_speed": "140",
    "travel_acceleration": "3000",
    "travel_speed": "400",
    "type": "process"
  },
  "process/0.20mm Standard @E3NG v1.2S.json": {
    "compatible_printers": [
      "E3NG v1.2S - 0.3 nozzle",
      "E3NG v1.2S - 0.4 nozzle",
      "E3NG v1.2S - 0.5 nozzle",
      "E3NG v1.2S - 0.6 nozzle"
    ],
    "from": "system",
    "inherits": "process_common_E3NG v1.2S",
    "instantiation": "true",
    "name": "0.20mm Standard @E3NG v1.2S",
    "setting_id": "NG2020",
    "type": "process"
  },
  "process/0.25mm Fast @E3NG v1.2S.json": {
    "bridge_acceleration": "5000",
    "bridge_speed": "75",
    "compatible_printers": [
      "E3NG v1.2S - 0.4 nozzle",
      "E3NG v1.2S - 0.5 nozzle",
      "E3NG v1.2S - 0.6 nozzle"
    ],
    "default_acceleration": "10000",
    "from": "system",
    "gap_infill_speed": "300",
    "infill_combination": "1",
    "inherits": "process_common_E3NG v1.2S",
    "initial_layer_acceleration": "7500",
    "initial_layer_infill_speed": "150",
    "initial_layer_print_height": "0.25",
    "initial_layer_speed": "100",
    "inner_wall_acceleration": "10000",
    "inner_wall_speed": "340",
    "instantiation": "true",
    "internal_solid_infill_acceleration": "10000",
    "internal_solid_infill_line_width": "125%",
    "internal_solid_infill_speed": "340",
    "ironing_speed": "150",
    "layer_height": "0.25",
    "name": "0.25mm Fast @E3NG v1.2S",
    "only_one_wall_first_layer": "0",
    "only_one_wall_top": "0",
    "outer_wall_acceleration": "7500",
    "outer_wall_speed": "300",
    "overhang_1_4_speed": "100",
    "overhang_2_4_speed": "50",
    "overhang_3_4_speed": "30",
    "overhang_4_4_speed": "15",
    "reduce_crossing_wall": "0",
    "seam_position": "nearest",
    "setting_id": "NG3025",
    "small_perimeter_speed": "300",
    "sparse_infill_acceleration": "12500",
    "sparse_infill_line_width": "125%",
    "sparse_infill_speed": "400",
    "support_interface_speed": "120",
    "top_surface_acceleration": "7500",
    "top_surface_line_width": "100%",
    "top_surface_speed": "300",
    "travel_acceleration": "10000",
    "travel_speed": "400",
    "type": "process"
  },
  "process/0.25mm Standard @E3NG v1.2S.json": {
    "compatible_printers": [
      "E3NG v1.2S - 0.4 nozzle",
      "E3NG v1.2S - 0.5 nozzle",
      "E3NG v1.2S - 0.6 nozzle"
    ],
    "from": "system",
    "inherits": "process_common_E3NG v1.2S",
    "initial_layer_print_height": "0.25",
    "instantiation": "true",
    "layer_height": "0.25",
    "name": "0.25mm Standard @E3NG v1.2S",
    "setting_id": "NG2025",
    "type": "process"
  },
  "process/fdm_process_common.json": {
    "adaptive_layer_height": "0",
    "bottom_shell_layers": "4",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonicline",
    "bridge_acceleration": "2500",
    "bridge_flow": "1",
    "bridge_no_support": "0",
    "bridge_speed": "50",
    "brim_object_gap": "0.1",
    "brim_width": "0",
    "compatible_printers": [],
    "compatible_printers_condition": "",
    "default_acceleration": "5000",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "0",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "exclude_object": "1",
    "filename_format": "{input_filename_base}_{filament_type[0]}_{print_time}_{printer_model}.gcode",
    "from": "system",
    "gap_infill_speed": "220",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "25%",
    "initial_layer_acceleration": "5000",
    "initial_layer_infill_speed": "100",
    "initial_layer_line_width": "110%",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "80",
    "inner_wall_acceleration": "5000",
    "inner_wall_line_width": "110%",
    "inner_wall_speed": "220",
    "instantiation": "false",
    "interface_shells": "0",
    "internal_solid_infill_acceleration": "5000",
    "internal_solid_infill_line_width": "110%",
    "internal_solid_infill_pattern": "monotonicline",
    "internal_solid_infill_speed": "220",
    "ironing_flow": "10%",
    "ironing_spacing": "0.25",
    "ironing_speed": "100",
    "ironing_type": "no ironing",
    "layer_height": "0.2",
    "line_width": "110%",
    "max_travel_detour_distance": "0",
    "min_skirt_length": "30",
    "minimum_sparse_infill_area": "15",
    "name": "fdm_process_common",
    "only_one_wall_first_layer": "1",
    "only_one_wall_top": "1",
    "outer_wall_acceleration": "5000",
    "outer_wall_line_width": "100%",
    "outer_wall_speed": "220",
    "overhang_1_4_speed": "70",
    "overhang_2_4_speed": "40",
    "overhang_3_4_speed": "25",
    "overhang_4_4_speed": "10",
    "prime_tower_width": "60",
    "print_sequence": "by layer",
    "print_settings_id": "",
    "raft_layers": "0",
    "reduce_crossing_wall": "1",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "seam_position": "aligned",
    "skirt_distance": "2",
    "skirt_height": "1",
    "skirt_loops": "5",
    "slowdown_for_curled_perimeters": "1",
    "small_perimeter_speed": "220",
    "sparse_infill_acceleration": "8000",
    "sparse_infill_density": "20%",
    "sparse_infill_line_width": "115%",
    "sparse_infill_pattern": "cubic",
    "sparse_infill_speed": "300",
    "spiral_mode": "0",
    "standby_temperature_delta": "-5",
    "support_base_pattern": "default",
    "support_base_pattern_spacing": "2.0",
    "support_bottom_z_distance": "0.2",
    "support_filament": "0",
    "support_interface_bottom_layers": "0",
    "support_interface_filament": "0",
    "support_interface_loop_pattern": "0",
    "support_interface_spacing": "0.2",
    "support_interface_speed": "80",
    "support_interface_top_layers": "3",
    "support_line_width": "100%",
    "support_object_xy_distance": "0.4",
    "support_on_build_plate_only": "0",
    "support_speed": "180",
    "support_threshold_angle": "40",
    "support_top_z_distance": "0.2",
    "support_type": "normal(auto)",
    "top_shell_layers": "4",
    "top_shell_thickness": "0.8",
    "top_surface_acceleration": "5000",
    "top_surface_line_width": "85%",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "180",
    "travel_acceleration": "5000",
    "travel_speed": "400",
    "tree_support_branch_angle": "30",
    "tree_support_wall_count": "0",
    "tree_support_with_infill": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "3",
    "wipe_before_external_loop": "1",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/process_common_E3NG v1.2S.json": {
    "from": "system",
    "inherits": "fdm_process_common",
    "instantiation": "false",
    "name": "process_common_E3NG v1.2S",
    "type": "process"
  }
}

FILAMENT = {
  "filament/Generic ABS @E3NG v1.2S.json": {
    "compatible_printers": [
      "E3NG v1.2S - 0.2 nozzle",
      "E3NG v1.2S - 0.3 nozzle",
      "E3NG v1.2S - 0.4 nozzle",
      "E3NG v1.2S - 0.5 nozzle",
      "E3NG v1.2S - 0.6 nozzle"
    ],
    "filament_id": "Generic ABS @E3NG v1.2S",
    "from": "system",
    "inherits": "fdm_filament_abs",
    "instantiation": "true",
    "name": "Generic ABS @E3NG v1.2S",
    "setting_id": "",
    "type": "filament"
  },
  "filament/Generic ASA @E3NG v1.2S.json": {
    "compatible_printers": [
      "E3NG v1.2S - 0.2 nozzle",
      "E3NG v1.2S - 0.3 nozzle",
      "E3NG v1.2S - 0.4 nozzle",
      "E3NG v1.2S - 0.5 nozzle",
      "E3NG v1.2S - 0.6 nozzle"
    ],
    "filament_id": "Generic ASA @E3NG v1.2S",
    "from": "system",
    "inherits": "fdm_filament_asa",
    "instantiation": "true",
    "name": "Generic ASA @E3NG v1.2S",
    "setting_id": "",
    "type": "filament"
  },
  "filament/Generic PCCF @E3NG v1.2S.json": {
    "compatible_printers": [
      "E3NG v1.2S - 0.5 nozzle",
      "E3NG v1.2S - 0.6 nozzle"
    ],
    "filament_id": "Generic PCCF @E3NG v1.2S",
    "from": "system",
    "inherits": "fdm_filament_pccf",
    "instantiation": "true",
    "name": "Generic PCCF @E3NG v1.2S",
    "setting_id": "",
    "type": "filament"
  },
  "filament/Generic PETG @E3NG v1.2S.json": {
    "compatible_printers": [
      "E3NG v1.2S - 0.2 nozzle",
      "E3NG v1.2S - 0.3 nozzle",
      "E3NG v1.2S - 0.4 nozzle",
      "E3NG v1.2S - 0.5 nozzle",
      "E3NG v1.2S - 0.6 nozzle"
    ],
    "filament_id": "Generic PETG @E3NG v1.2S",
    "from": "system",
    "inherits": "fdm_filament_petg",
    "instantiation": "true",
    "name": "Generic PETG @E3NG v1.2S",
    "setting_id": "",
    "type": "filament"
  },
  "filament/Generic PLA @E3NG v1.2S.json": {
    "compatible_printers": [
      "E3NG v1.2S - 0.2 nozzle",
      "E3NG v1.2S - 0.3 nozzle",
      "E3NG v1.2S - 0.4 nozzle",
      "E3NG v1.2S - 0.5 nozzle",
      "E3NG v1.2S - 0.6 nozzle"
    ],
    "filament_id": "Generic PLA @E3NG v1.2S",
    "from": "system",
    "inherits": "fdm_filament_pla",
    "instantiation": "true",
    "name": "Generic PLA @E3NG v1.2S",
    "setting_id": "",
    "type": "filament"
  },
  "filament/Generic TPU @E3NG v1.2S.json": {
    "compatible_printers": [
      "E3NG v1.2S - 0.4 nozzle",
      "E3NG v1.2S - 0.5 nozzle",
      "E3NG v1.2S - 0.6 nozzle"
    ],
    "filament_id": "Generic TPU @E3NG v1.2S",
    "from": "system",
    "inherits": "fdm_filament_tpu",
    "instantiation": "true",
    "name": "Generic TPU @E3NG v1.2S",
    "setting_id": "",
    "type": "filament"
  },
  "filament/fdm_filament_abs.json": {
    "chamber_temperature": [
      "55"
    ],
    "cool_plate_temp": [
      "100"
    ],
    "cool_plate_temp_initial_layer": [
      "100"
    ],
    "eng_plate_temp": [
      "115"
    ],
    "eng_plate_temp_initial_layer": [
      "115"
    ],
    "fan_cooling_layer_time": [
      "10"
    ],
    "fan_max_speed": [
      "60"
    ],
    "fan_min_speed": [
      "20"
    ],
    "filament_cost": [
      "20"
    ],
    "filament_density": [
      "1.04"
    ],
    "filament_flow_ratio": [
      "0.94"
    ],
    "filament_id": "GFRH01",
    "filament_max_volumetric_speed": [
      "32"
    ],
    "filament_shrink": [
      "99.487"
    ],
    "filament_type": [
      "ABS"
    ],
    "from": "system",
    "hot_plate_temp": [
      "115"
    ],
    "hot_plate_temp_initial_layer": [
      "115"
    ],
    "idle_temperature": "200",
    "inherits": "fdm_filament_common",
    "instantiation": "false",
    "name": "fdm_filament_abs",
    "nozzle_temperature": [
      "265"
    ],
    "nozzle_temperature_initial_layer": [
      "265"
    ],
    "nozzle_temperature_range_high": [
      "275"
    ],
    "nozzle_temperature_range_low": [
      "250"
    ],
    "overhang_fan_speed": [
      "80"
    ],
    "overhang_fan_threshold": [
      "25%"
    ],
    "slow_down_layer_time": [
      "2"
    ],
    "slow_down_min_speed": [
      "10"
    ],
    "temperature_vitrification": [
      "110"
    ],
    "type": "filament"
  },
  "filament/fdm_filament_asa.json": {
    "chamber_temperature": [
      "55"
    ],
    "cool_plate_temp": [
      "100"
    ],
    "cool_plate_temp_initial_layer": [
      "100"
    ],
    "eng_plate_temp": [
      "115"
    ],
    "eng_plate_temp_initial_layer": [
      "115"
    ],
    "fan_cooling_layer_time": [
      "10"
    ],
    "fan_max_speed": [
      "50"
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
    "filament_flow_ratio": [
      "0.94"
    ],
    "filament_id": "GFRH02",
    "filament_max_volumetric_speed": [
      "32"
    ],
    "filament_shrink": [
      "99.487"
    ],
    "filament_type": [
      "ASA"
    ],
    "from": "system",
    "hot_plate_temp": [
      "115"
    ],
    "hot_plate_temp_initial_layer": [
      "115"
    ],
    "idle_temperature": "200",
    "inherits": "fdm_filament_common",
    "instantiation": "false",
    "name": "fdm_filament_asa",
    "nozzle_temperature": [
      "265"
    ],
    "nozzle_temperature_initial_layer": [
      "265"
    ],
    "nozzle_temperature_range_high": [
      "275"
    ],
    "nozzle_temperature_range_low": [
      "250"
    ],
    "overhang_fan_speed": [
      "80"
    ],
    "overhang_fan_threshold": [
      "25%"
    ],
    "slow_down_layer_time": [
      "2"
    ],
    "slow_down_min_speed": [
      "10"
    ],
    "temperature_vitrification": [
      "110"
    ],
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
      "15"
    ],
    "fan_max_speed": [
      "100"
    ],
    "fan_min_speed": [
      "10"
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
      "10"
    ],
    "filament_minimal_purge_on_wipe_tower": [
      "40"
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
      "3"
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
      "3"
    ],
    "slow_down_min_speed": [
      "10"
    ],
    "temperature_vitrification": [
      "100"
    ],
    "type": "filament"
  },
  "filament/fdm_filament_pccf.json": {
    "chamber_temperature": [
      "55"
    ],
    "cool_plate_temp": [
      "0"
    ],
    "cool_plate_temp_initial_layer": [
      "0"
    ],
    "eng_plate_temp": [
      "90"
    ],
    "eng_plate_temp_initial_layer": [
      "90"
    ],
    "fan_cooling_layer_time": [
      "10"
    ],
    "fan_max_speed": [
      "40"
    ],
    "fan_min_speed": [
      "25"
    ],
    "filament_cost": [
      "40"
    ],
    "filament_density": [
      "1.04"
    ],
    "filament_flow_ratio": [
      "0.9"
    ],
    "filament_id": "GFRH06",
    "filament_max_volumetric_speed": [
      "8"
    ],
    "filament_shrink": [
      "99.85"
    ],
    "filament_type": [
      "PC-CF"
    ],
    "from": "system",
    "hot_plate_temp": [
      "90"
    ],
    "hot_plate_temp_initial_layer": [
      "90"
    ],
    "idle_temperature": "240",
    "inherits": "fdm_filament_common",
    "instantiation": "false",
    "name": "fdm_filament_pccf",
    "nozzle_temperature": [
      "320"
    ],
    "nozzle_temperature_initial_layer": [
      "300"
    ],
    "nozzle_temperature_range_high": [
      "330"
    ],
    "nozzle_temperature_range_low": [
      "290"
    ],
    "overhang_fan_speed": [
      "60"
    ],
    "overhang_fan_threshold": [
      "25%"
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
    "type": "filament"
  },
  "filament/fdm_filament_petg.json": {
    "cool_plate_temp": [
      "70"
    ],
    "cool_plate_temp_initial_layer": [
      "70"
    ],
    "eng_plate_temp": [
      "0"
    ],
    "eng_plate_temp_initial_layer": [
      "0"
    ],
    "fan_cooling_layer_time": [
      "10"
    ],
    "fan_max_speed": [
      "60"
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
    "filament_flow_ratio": [
      "0.96"
    ],
    "filament_id": "GFRH03",
    "filament_max_volumetric_speed": [
      "26"
    ],
    "filament_shrink": [
      "99.85"
    ],
    "filament_type": [
      "PETG"
    ],
    "from": "system",
    "hot_plate_temp": [
      "90"
    ],
    "hot_plate_temp_initial_layer": [
      "90"
    ],
    "idle_temperature": "190",
    "inherits": "fdm_filament_common",
    "instantiation": "false",
    "name": "fdm_filament_petg",
    "nozzle_temperature": [
      "250"
    ],
    "nozzle_temperature_initial_layer": [
      "250"
    ],
    "nozzle_temperature_range_high": [
      "260"
    ],
    "nozzle_temperature_range_low": [
      "230"
    ],
    "overhang_fan_speed": [
      "100"
    ],
    "overhang_fan_threshold": [
      "25%"
    ],
    "slow_down_layer_time": [
      "3"
    ],
    "slow_down_min_speed": [
      "12"
    ],
    "temperature_vitrification": [
      "80"
    ],
    "type": "filament"
  },
  "filament/fdm_filament_pla.json": {
    "cool_plate_temp": [
      "40"
    ],
    "cool_plate_temp_initial_layer": [
      "45"
    ],
    "eng_plate_temp": [
      "67"
    ],
    "eng_plate_temp_initial_layer": [
      "70"
    ],
    "fan_cooling_layer_time": [
      "15"
    ],
    "fan_max_speed": [
      "100"
    ],
    "fan_min_speed": [
      "80"
    ],
    "filament_cost": [
      "20"
    ],
    "filament_density": [
      "1.24"
    ],
    "filament_flow_ratio": [
      "0.92"
    ],
    "filament_id": "GFRH04",
    "filament_max_volumetric_speed": [
      "24"
    ],
    "filament_shrink": [
      "99.95"
    ],
    "filament_type": [
      "PLA"
    ],
    "from": "system",
    "hot_plate_temp": [
      "67"
    ],
    "hot_plate_temp_initial_layer": [
      "70"
    ],
    "idle_temperature": "180",
    "inherits": "fdm_filament_common",
    "instantiation": "false",
    "name": "fdm_filament_pla",
    "nozzle_temperature": [
      "230"
    ],
    "nozzle_temperature_initial_layer": [
      "230"
    ],
    "nozzle_temperature_range_high": [
      "250"
    ],
    "nozzle_temperature_range_low": [
      "210"
    ],
    "overhang_fan_speed": [
      "100"
    ],
    "overhang_fan_threshold": [
      "25%"
    ],
    "slow_down_layer_time": [
      "6"
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
    "cool_plate_temp": [
      "30"
    ],
    "cool_plate_temp_initial_layer": [
      "30"
    ],
    "eng_plate_temp": [
      "50"
    ],
    "eng_plate_temp_initial_layer": [
      "50"
    ],
    "fan_cooling_layer_time": [
      "50"
    ],
    "fan_max_speed": [
      "1000"
    ],
    "fan_min_speed": [
      "80"
    ],
    "filament_cost": [
      "20"
    ],
    "filament_density": [
      "1.24"
    ],
    "filament_flow_ratio": [
      "0.96"
    ],
    "filament_id": "GFRH05",
    "filament_max_volumetric_speed": [
      "10"
    ],
    "filament_shrink": [
      "99.95"
    ],
    "filament_type": [
      "TPU"
    ],
    "from": "system",
    "hot_plate_temp": [
      "50"
    ],
    "hot_plate_temp_initial_layer": [
      "50"
    ],
    "idle_temperature": "170",
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
      "230"
    ],
    "overhang_fan_speed": [
      "100"
    ],
    "overhang_fan_threshold": [
      "25%"
    ],
    "slow_down_layer_time": [
      "5"
    ],
    "slow_down_min_speed": [
      "15"
    ],
    "temperature_vitrification": [
      "60"
    ],
    "type": "filament"
  }
}

MISC = {}

ASSETS = [
  "E3NG v1.2S_cover.png",
  "E3NG-bed-texture.svg",
  "E3NG-bed.stl"
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
