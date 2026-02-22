from __future__ import annotations

VENDOR = "UltiMaker"
INDEX = {
  "description": "UltiMaker configurations",
  "filament_list": [],
  "force_update": "0",
  "machine_list": [
    {
      "name": "fdm_machine_common",
      "sub_path": "machine/fdm_machine_common.json"
    },
    {
      "name": "UltiMaker 2 0.4 nozzle",
      "sub_path": "machine/UltiMaker 2 0.4 nozzle.json"
    }
  ],
  "machine_model_list": [
    {
      "name": "UltiMaker 2",
      "sub_path": "machine/UltiMaker 2.json"
    }
  ],
  "name": "UltiMaker",
  "process_list": [
    {
      "name": "fdm_process_common",
      "sub_path": "process/fdm_process_common.json"
    },
    {
      "name": "0.12mm Fine @UltiMaker 2",
      "sub_path": "process/0.12mm Fine @UltiMaker 2.json"
    },
    {
      "name": "0.18mm Standard @UltiMaker 2",
      "sub_path": "process/0.18mm Standard @UltiMaker 2.json"
    },
    {
      "name": "0.25mm Draft @UltiMaker 2",
      "sub_path": "process/0.25mm Darft @UltiMaker 2.json"
    }
  ],
  "url": "",
  "version": "02.03.01.10"
}

MACHINE = {
  "machine/UltiMaker 2 0.4 nozzle.json": {
    "auxiliary_fan": "0",
    "change_filament_gcode": "",
    "default_filament_profile": [
      "Generic PLA @System"
    ],
    "default_print_profile": "0.18mm Standard @UltiMaker 2",
    "deretraction_speed": [
      "0"
    ],
    "from": "system",
    "inherits": "fdm_machine_common",
    "instantiation": "true",
    "machine_end_gcode": "; # # # # # # START Footer\nG91; relative coordinates\n;G1 E-1 F1200; retract the filament\nG1 Z+15  X-10 Y-10 E-7  F6000; move Z a bit\n; G1 X-10 Y-10 F6000; move XY a bit\nG1 E-5.5 F300; retract the filament\nG28 X0 Y0; move X/Y to min endstops, so the head is out of the way\nM104 S0; extruder heater off\nM140 S0; heated bed heater off (if you have it)\nM84; disable motors\n; # # # # # # END Footer\n",
    "machine_max_acceleration_extruding": [
      "1500",
      "1500"
    ],
    "machine_max_acceleration_retracting": [
      "1500",
      "1500"
    ],
    "machine_max_acceleration_travel": [
      "3000",
      "3000"
    ],
    "machine_max_acceleration_x": [
      "3000",
      "3000"
    ],
    "machine_max_acceleration_y": [
      "3000",
      "3000"
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
      "20",
      "20"
    ],
    "machine_max_jerk_y": [
      "20",
      "20"
    ],
    "machine_max_jerk_z": [
      "0.4",
      "0.4"
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
    "machine_pause_gcode": "M0",
    "machine_start_gcode": "; # # # # # # START Header\nG21; metric values\nG90; absolute positioning\nM82 ; set extruder to absolute mode\nM107; start with the fan off\n\nM140 S[bed_temperature_initial_layer_single]; start bed heating\n\nG28 X0 Y0 Z0; move X/Y/Z to endstops\nG1 X1 Y6 F15000; move X/Y to start position\nG1 Z35 F9000; move Z to start position\n\n; Wait for bed and nozzle temperatures\nM190 S{hot_plate_temp_initial_layer[0] - 5}; wait for bed temperature - 5\nM140 S[bed_temperature_initial_layer_single]; continue bed heating\nM109 S[nozzle_temperature_initial_layer]; wait for nozzle temperature\n\n; Purge and prime\nM83; set extruder to relative mode\nG92 E0; reset extrusion distance\nG0 X0 Y1 F10000\nG1 F150 E20 ; compress the bowden tube\nG1 E-8 F1200\nG0 X30 Y1 F5000\nG0 F1200 Z{initial_layer_print_height/2}; Cut the connection to priming blob\nG0 X100 F10000; disconnect with the prime blob\nG0 X50; Avoid the metal clip holding the Ultimaker glass plate\nG0 Z0.2 F720\nG1 E8 F1200\nG1 X80 E3 F1000; intro line 1\nG1 X110 E4 F1000 ; intro line 2\nG1 X140 F600; drag filament to decompress bowden tube\nG1 X100 F3200; wipe backwards a bit\nG1 X150 F3200; back to where there is no plastic: avoid dragging\nG92 E0; reset extruder reference\nM82; set extruder to absolute mode\n\n; # # # # # # END Header",
    "max_layer_height": [
      "0.3"
    ],
    "min_layer_height": [
      "0.08"
    ],
    "name": "UltiMaker 2 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "nozzle_type": "undefine",
    "printable_area": [
      "0x0",
      "224x0",
      "224x225",
      "0x225"
    ],
    "printable_height": "212",
    "printer_model": "UltiMaker 2",
    "printer_settings_id": "Qidi",
    "retract_before_wipe": [
      "70%"
    ],
    "retract_length_toolchange": [
      "10"
    ],
    "retraction_length": [
      "4.5"
    ],
    "retraction_minimum_travel": [
      "5"
    ],
    "retraction_speed": [
      "35"
    ],
    "scan_first_layer": "0",
    "setting_id": "GM001",
    "single_extruder_multi_material": "1",
    "type": "machine",
    "wipe_distance": [
      "0.2"
    ]
  },
  "machine/UltiMaker 2.json": {
    "bed_model": "ultimaker_2_buildplate_model.stl",
    "bed_texture": "ultimaker_2_buildplate_texture.png",
    "default_materials": "Generic ABS @System;Generic PETG @System;Generic PLA @System",
    "family": "UltiMaker",
    "hotend_model": "ultimaker_hotend.stl",
    "machine_tech": "FFF",
    "model_id": "UltiMaker-2",
    "name": "UltiMaker 2",
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
      "10000"
    ],
    "machine_max_acceleration_extruding": [
      "1500"
    ],
    "machine_max_acceleration_retracting": [
      "1500"
    ],
    "machine_max_acceleration_x": [
      "3000"
    ],
    "machine_max_acceleration_y": [
      "3000"
    ],
    "machine_max_acceleration_z": [
      "500"
    ],
    "machine_max_jerk_e": [
      "2.5"
    ],
    "machine_max_jerk_x": [
      "20"
    ],
    "machine_max_jerk_y": [
      "20"
    ],
    "machine_max_jerk_z": [
      "0.4"
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
      "12"
    ],
    "machine_min_extruding_rate": [
      "0"
    ],
    "machine_min_travel_rate": [
      "0"
    ],
    "machine_start_gcode": "",
    "max_layer_height": [
      "0.3"
    ],
    "min_layer_height": [
      "0.07"
    ],
    "name": "fdm_machine_common",
    "nozzle_diameter": [
      "0.4"
    ],
    "printable_height": "212",
    "printer_settings_id": "",
    "printer_technology": "FFF",
    "printer_variant": "0.4",
    "retract_before_wipe": [
      "0%"
    ],
    "retract_length_toolchange": [
      "10"
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
      "6"
    ],
    "retraction_minimum_travel": [
      "2"
    ],
    "retraction_speed": [
      "50"
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
  "process/0.12mm Fine @UltiMaker 2.json": {
    "adaptive_layer_height": "1",
    "bottom_shell_layers": "6",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "1",
    "bridge_no_support": "0",
    "bridge_speed": "60",
    "brim_object_gap": "0",
    "brim_width": "0",
    "compatible_printers": [
      "UltiMaker 2 0.4 nozzle"
    ],
    "compatible_printers_condition": "",
    "default_acceleration": "0",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "250",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "35%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "500",
    "initial_layer_infill_speed": "35%",
    "initial_layer_line_width": "0.42",
    "initial_layer_print_height": "0.3",
    "initial_layer_speed": "35%",
    "inner_wall_acceleration": "0",
    "inner_wall_line_width": "0.45",
    "inner_wall_speed": "300",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0",
    "internal_solid_infill_speed": "250",
    "ironing_flow": "15%",
    "ironing_spacing": "0.1",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.12",
    "line_width": "0.45",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.12mm Fine @UltiMaker 2",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "200",
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
    "sparse_infill_speed": "270",
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
    "support_line_width": "0.4",
    "support_object_xy_distance": "50%",
    "support_on_build_plate_only": "0",
    "support_speed": "60",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.2",
    "support_type": "normal(auto)",
    "top_shell_layers": "7",
    "top_shell_thickness": "0.8",
    "top_surface_acceleration": "0",
    "top_surface_line_width": "0.4",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "200",
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
  "process/0.18mm Standard @UltiMaker 2.json": {
    "adaptive_layer_height": "1",
    "bottom_shell_layers": "4",
    "bottom_shell_thickness": "0.8",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "1",
    "bridge_no_support": "0",
    "bridge_speed": "60",
    "brim_object_gap": "0",
    "brim_width": "0",
    "compatible_printers": [
      "UltiMaker 2 0.4 nozzle"
    ],
    "compatible_printers_condition": "",
    "default_acceleration": "0",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "20",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "35%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "500",
    "initial_layer_infill_speed": "30",
    "initial_layer_line_width": "0.45",
    "initial_layer_print_height": "0.25",
    "initial_layer_speed": "15",
    "initial_layer_travel_speed": "60",
    "inner_wall_acceleration": "0",
    "inner_wall_line_width": "0.45",
    "inner_wall_speed": "40",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0.45",
    "internal_solid_infill_speed": "40",
    "ironing_flow": "15%",
    "ironing_spacing": "0.1",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.18",
    "line_width": "0.45",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.18mm Standard @UltiMaker 2",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "30",
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
    "sparse_infill_density": "20%",
    "sparse_infill_line_width": "0.5",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "40",
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
    "support_line_width": "0.45",
    "support_object_xy_distance": "50%",
    "support_on_build_plate_only": "0",
    "support_speed": "45",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.2",
    "support_type": "normal(auto)",
    "top_shell_layers": "5",
    "top_shell_thickness": "0.8",
    "top_surface_acceleration": "0",
    "top_surface_line_width": "0.4",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "15",
    "travel_acceleration": "0",
    "travel_speed": "120",
    "tree_support_branch_angle": "40",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "3",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/0.25mm Darft @UltiMaker 2.json": {
    "adaptive_layer_height": "1",
    "bottom_shell_layers": "3",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "1",
    "bridge_no_support": "0",
    "bridge_speed": "60",
    "brim_object_gap": "0",
    "brim_width": "0",
    "compatible_printers": [
      "UltiMaker 2 0.4 nozzle"
    ],
    "compatible_printers_condition": "",
    "default_acceleration": "0",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "250",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "35%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "500",
    "initial_layer_infill_speed": "35%",
    "initial_layer_line_width": "0.42",
    "initial_layer_print_height": "0.3",
    "initial_layer_speed": "35%",
    "inner_wall_acceleration": "0",
    "inner_wall_line_width": "0.45",
    "inner_wall_speed": "300",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0",
    "internal_solid_infill_speed": "250",
    "ironing_flow": "15%",
    "ironing_spacing": "0.1",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.25",
    "line_width": "0.45",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.25mm Draft @UltiMaker 2",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "200",
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
    "sparse_infill_speed": "270",
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
    "support_line_width": "0.4",
    "support_object_xy_distance": "50%",
    "support_on_build_plate_only": "0",
    "support_speed": "60",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.2",
    "support_type": "normal(auto)",
    "top_shell_layers": "4",
    "top_shell_thickness": "0.8",
    "top_surface_acceleration": "0",
    "top_surface_line_width": "0.4",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "200",
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
  "UltiMaker 2_cover.png",
  "ultimaker_2_buildplate_model.stl",
  "ultimaker_2_buildplate_texture.png",
  "ultimaker_hotend.stl"
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
