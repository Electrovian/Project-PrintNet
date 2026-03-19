from __future__ import annotations

VENDOR = "Voxelab"
INDEX = {
  "description": "Voxelab configurations",
  "filament_list": [],
  "force_update": "0",
  "machine_list": [
    {
      "name": "fdm_machine_common",
      "sub_path": "machine/fdm_machine_common.json"
    },
    {
      "name": "Voxelab Aquila X2 0.4 nozzle",
      "sub_path": "machine/Voxelab Aquila X2 0.4 nozzle.json"
    }
  ],
  "machine_model_list": [
    {
      "name": "Voxelab Aquila X2",
      "sub_path": "machine/Voxelab Aquila X2.json"
    }
  ],
  "name": "Voxelab",
  "process_list": [
    {
      "name": "fdm_process_common",
      "sub_path": "process/fdm_process_common.json"
    },
    {
      "name": "0.16mm Optimal @Voxelab AquilaX2",
      "sub_path": "process/0.16mm Optimal @Voxelab AquilaX2.json"
    },
    {
      "name": "0.20mm Standard @Voxelab AquilaX2",
      "sub_path": "process/0.20mm Standard @Voxelab AquilaX2.json"
    }
  ],
  "url": "",
  "version": "02.03.01.10"
}

MACHINE = {
  "machine/Voxelab Aquila X2 0.4 nozzle.json": {
    "auxiliary_fan": "0",
    "change_filament_gcode": "M600",
    "default_filament_profile": [
      "Generic PLA @System"
    ],
    "default_print_profile": "0.20mm Standard @Voxelab AquilaX2",
    "deretraction_speed": [
      "40"
    ],
    "from": "system",
    "inherits": "fdm_machine_common",
    "instantiation": "true",
    "machine_end_gcode": "{if max_layer_z < printable_height}G1 Z{z_offset+min(max_layer_z+2, printable_height)} F600 ; Move print head up{endif}\nG1 X5 Y{print_bed_max[1]*0.8} F{travel_speed*60} ; present print\n{if max_layer_z < printable_height-10}G1 Z{z_offset+min(max_layer_z+70, printable_height-10)} F600 ; Move print head further up{endif}\n{if max_layer_z < max_print_height*0.6}G1 Z{printable_height*0.6} F600 ; Move print head further up{endif}\nM140 S0 ; turn off heatbed\nM104 S0 ; turn off temperature\nM107 ; turn off fan\nM84 X Y E ; disable motors",
    "machine_max_acceleration_extruding": [
      "500",
      "500"
    ],
    "machine_max_acceleration_retracting": [
      "1000",
      "1000"
    ],
    "machine_max_acceleration_travel": [
      "1500",
      "1250"
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
      "100",
      "100"
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
    "machine_pause_gcode": "M0",
    "machine_start_gcode": "G90 ; use absolute coordinates\nM83 ; extruder relative mode\nM140 S[bed_temperature_initial_layer_single] ; set final bed temp\nM104 S150 ; set temporary nozzle temp to prevent oozing during homing\nG4 S10 ; allow partial nozzle warmup\nG28 ; home all axis\nG1 Z50 F240\nG1 X2 Y10 F3000\nM104 S[nozzle_temperature_initial_layer] ; set final nozzle temp\nM190 S[bed_temperature_initial_layer_single] ; wait for bed temp to stabilize\nM109 S[nozzle_temperature_initial_layer] ; wait for nozzle temp to stabilize\nG1 Z0.28 F240\nG92 E0\nG1 Y140 E10 F1500 ; prime the nozzle\nG1 X2.3 F5000\nG92 E0\nG1 Y10 E10 F1200 ; prime the nozzle\nG92 E0",
    "max_layer_height": [
      "0.32"
    ],
    "min_layer_height": [
      "0.08"
    ],
    "name": "Voxelab Aquila X2 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "nozzle_type": "undefine",
    "printable_area": [
      "0x0",
      "220x0",
      "220x220",
      "0x220"
    ],
    "printable_height": "250",
    "printer_model": "Voxelab Aquila X2",
    "printer_settings_id": "Voxelab",
    "retract_before_wipe": [
      "70%"
    ],
    "retract_length_toolchange": [
      "1"
    ],
    "retraction_length": [
      "5"
    ],
    "retraction_minimum_travel": [
      "2"
    ],
    "scan_first_layer": "0",
    "setting_id": "GM001",
    "single_extruder_multi_material": "1",
    "type": "machine"
  },
  "machine/Voxelab Aquila X2.json": {
    "bed_model": "voxelab_aquilax2_buildplate_model.stl",
    "bed_texture": "voxelab_aquilax2_buildplate_texture.png",
    "default_materials": "Generic ABS @System;Generic PETG @System;Generic PLA @System",
    "family": "Voxelab",
    "hotend_model": "",
    "machine_tech": "FFF",
    "model_id": "Voxelab-Aquila-X2",
    "name": "Voxelab Aquila X2",
    "nozzle_diameter": "0.4",
    "type": "machine_model"
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
    "machine_end_gcode": "",
    "machine_max_acceleration_e": [
      "5000"
    ],
    "machine_max_acceleration_extruding": [
      "500"
    ],
    "machine_max_acceleration_retracting": [
      "1000"
    ],
    "machine_max_acceleration_x": [
      "500"
    ],
    "machine_max_acceleration_y": [
      "500"
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
    "machine_start_gcode": "",
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
    ],
    "z_lift_type": "NormalLift"
  }
}

PROCESS = {
  "process/0.16mm Optimal @Voxelab AquilaX2.json": {
    "adaptive_layer_height": "1",
    "bottom_shell_layers": "5",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.85",
    "bridge_no_support": "0",
    "bridge_speed": "25",
    "brim_object_gap": "0",
    "brim_width": "0",
    "compatible_printers": [
      "Voxelab Aquila X2 0.4 nozzle"
    ],
    "compatible_printers_condition": "",
    "default_acceleration": "0",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "30",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "25%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "0",
    "initial_layer_infill_speed": "35%",
    "initial_layer_line_width": "0.45",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "35%",
    "inner_wall_acceleration": "0",
    "inner_wall_line_width": "0.45",
    "inner_wall_speed": "40",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0",
    "internal_solid_infill_speed": "40",
    "ironing_flow": "15%",
    "ironing_spacing": "0.1",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.16",
    "line_width": "0.45",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.16mm Optimal @Voxelab AquilaX2",
    "outer_wall_acceleration": "0",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "40",
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
    "setting_id": "GP004",
    "skirt_distance": "3",
    "skirt_height": "1",
    "skirt_loops": "2",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.45",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "60",
    "spiral_mode": "0",
    "standby_temperature_delta": "-5",
    "support_base_pattern": "rectilinear",
    "support_base_pattern_spacing": "0.2",
    "support_filament": "0",
    "support_interface_bottom_layers": "-1",
    "support_interface_filament": "0",
    "support_interface_loop_pattern": "0",
    "support_interface_spacing": "0.2",
    "support_interface_speed": "100%",
    "support_interface_top_layers": "3",
    "support_line_width": "0.38",
    "support_object_xy_distance": "60%",
    "support_on_build_plate_only": "0",
    "support_speed": "40",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.15",
    "support_type": "normal(auto)",
    "top_shell_layers": "5",
    "top_shell_thickness": "0.8",
    "top_surface_acceleration": "0",
    "top_surface_line_width": "0.38",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "30",
    "travel_acceleration": "0",
    "travel_speed": "150",
    "tree_support_branch_angle": "40",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "2",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/0.20mm Standard @Voxelab AquilaX2.json": {
    "adaptive_layer_height": "1",
    "bottom_shell_layers": "5",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.85",
    "bridge_no_support": "0",
    "bridge_speed": "25",
    "brim_object_gap": "0",
    "brim_width": "0",
    "compatible_printers": [
      "Voxelab Aquila X2 0.4 nozzle"
    ],
    "compatible_printers_condition": "",
    "default_acceleration": "0",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "30",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "25%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "0",
    "initial_layer_infill_speed": "35%",
    "initial_layer_line_width": "0.45",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "35%",
    "inner_wall_acceleration": "0",
    "inner_wall_line_width": "0.45",
    "inner_wall_speed": "40",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0",
    "internal_solid_infill_speed": "40",
    "ironing_flow": "15%",
    "ironing_spacing": "0.1",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.2",
    "line_width": "0.45",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.20mm Standard @Voxelab AquilaX2",
    "outer_wall_acceleration": "0",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "40",
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
    "setting_id": "GP004",
    "skirt_distance": "3",
    "skirt_height": "1",
    "skirt_loops": "2",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.45",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "60",
    "spiral_mode": "0",
    "standby_temperature_delta": "-5",
    "support_base_pattern": "rectilinear",
    "support_base_pattern_spacing": "0.2",
    "support_filament": "0",
    "support_interface_bottom_layers": "-1",
    "support_interface_filament": "0",
    "support_interface_loop_pattern": "0",
    "support_interface_spacing": "0.2",
    "support_interface_speed": "100%",
    "support_interface_top_layers": "3",
    "support_line_width": "0.38",
    "support_object_xy_distance": "60%",
    "support_on_build_plate_only": "0",
    "support_speed": "40",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.19",
    "support_type": "normal(auto)",
    "top_shell_layers": "5",
    "top_shell_thickness": "0.8",
    "top_surface_acceleration": "0",
    "top_surface_line_width": "0.38",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "30",
    "travel_acceleration": "0",
    "travel_speed": "150",
    "tree_support_branch_angle": "40",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "2",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/fdm_process_common.json": {
    "adaptive_layer_height": "0",
    "bridge_flow": "0.95",
    "bridge_no_support": "0",
    "bridge_speed": "25",
    "brim_width": "5",
    "compatible_printers": [],
    "default_acceleration": "0",
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
  }
}

FILAMENT = {}

MISC = {}

ASSETS = [
  "Voxelab Aquila X2_cover.png",
  "voxelab_aquilax2_buildplate_model.stl",
  "voxelab_aquilax2_buildplate_texture.png"
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
