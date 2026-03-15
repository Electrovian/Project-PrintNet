from __future__ import annotations

VENDOR = "Phrozen"
INDEX = {
  "description": "Phrozen configurations",
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
      "name": "Phrozen PLA @Phrozen Arco 0.4 nozzle",
      "sub_path": "filament/Phrozen PLA @Phrozen Arco 0.4 nozzle.json"
    }
  ],
  "force_update": "0",
  "machine_list": [
    {
      "name": "fdm_machine_common",
      "sub_path": "machine/fdm_machine_common.json"
    },
    {
      "name": "Phrozen Arco 0.4 nozzle",
      "sub_path": "machine/Phrozen Arco 0.4 nozzle.json"
    }
  ],
  "machine_model_list": [
    {
      "name": "Phrozen Arco",
      "sub_path": "machine/Phrozen Arco.json"
    }
  ],
  "name": "Phrozen",
  "process_list": [
    {
      "name": "fdm_process_common",
      "sub_path": "process/fdm_process_common.json"
    },
    {
      "name": "0.20mm Standard @Phrozen Arco 0.4 nozzle",
      "sub_path": "process/0.20mm Standard @Phrozen Arco 0.4 nozzle.json"
    }
  ],
  "version": "02.03.01.11"
}

MACHINE = {
  "machine/Phrozen Arco 0.4 nozzle.json": {
    "adaptive_bed_mesh_margin": "0",
    "auxiliary_fan": "1",
    "bbl_use_printhost": "0",
    "bed_custom_model": "",
    "bed_custom_texture": "",
    "bed_exclude_area": [],
    "bed_mesh_max": "0,0",
    "bed_mesh_min": "0,0",
    "bed_mesh_probe_distance": "0,0",
    "before_layer_change_gcode": "; BEFORE_LAYER_CHANGE [layer_num] @ [layer_z]mm",
    "best_object_pos": "0.5,0.5",
    "change_extrusion_role_gcode": "",
    "change_filament_gcode": "G1 E-1 F3600",
    "cooling_tube_length": "0",
    "cooling_tube_retraction": "0",
    "default_filament_profile": [
      "Phrozen PLA @Phrozen Arco 0.4 nozzle"
    ],
    "default_print_profile": "0.20mm Standard @Phrozen Arco 0.4 nozzle",
    "deretraction_speed": [
      "0"
    ],
    "disable_m73": "1",
    "emit_machine_limits_to_gcode": "1",
    "enable_filament_ramming": "0",
    "enable_long_retraction_when_cut": "0",
    "extra_loading_move": "0",
    "extruder_clearance_height_to_lid": "240",
    "extruder_clearance_height_to_rod": "48",
    "extruder_clearance_radius": "60",
    "extruder_colour": [
      "#FF4D4F"
    ],
    "extruder_offset": [
      "0x0"
    ],
    "fan_kickstart": "0",
    "fan_speedup_overhangs": "1",
    "fan_speedup_time": "0",
    "from": "User",
    "gcode_flavor": "klipper",
    "head_wrap_detect_zone": [],
    "high_current_on_filament_swap": "0",
    "host_type": "octoprint",
    "inherits": "fdm_machine_common",
    "instantiation": "true",
    "layer_change_gcode": "; AFTER_LAYER_CHANGE [layer_num] @ [layer_z]mm",
    "long_retractions_when_cut": [
      "0"
    ],
    "machine_end_gcode": "PRINT_END",
    "machine_load_filament_time": "126.423",
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
      "10000",
      "10000"
    ],
    "machine_max_acceleration_y": [
      "10000",
      "10000"
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
      "9",
      "9"
    ],
    "machine_max_jerk_y": [
      "9",
      "9"
    ],
    "machine_max_jerk_z": [
      "3",
      "3"
    ],
    "machine_max_speed_e": [
      "80",
      "80"
    ],
    "machine_max_speed_x": [
      "600",
      "600"
    ],
    "machine_max_speed_y": [
      "600",
      "600"
    ],
    "machine_max_speed_z": [
      "15",
      "15"
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
    "machine_start_gcode": "M107\nG90\nM140 S65 ; set bed temperature\nM104 S140 ; set temperature\nM190 S65 ; set bed temperature\nM109 S140 ; set temperature\nPG28\nM106 S255 \nG30\n;AUTO_LEVELING_2\nM106 S0\nG21\nM83\nM140 S[bed_temperature_initial_layer_single]\nM104 S[nozzle_temperature_initial_layer]\nM109 S[nozzle_temperature_initial_layer]\nM190 S[bed_temperature_initial_layer_single]\nP0 M1\nP28\nP2 A1",
    "machine_tool_change_time": "0",
    "machine_unload_filament_time": "0",
    "manual_filament_change": "0",
    "max_layer_height": [
      "0.28"
    ],
    "min_layer_height": [
      "0.08"
    ],
    "name": "Phrozen Arco 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "nozzle_height": "4",
    "nozzle_hrc": "0",
    "nozzle_type": "brass",
    "nozzle_volume": "71.6",
    "parking_pos_retraction": "0",
    "pellet_modded_printer": "0",
    "preferred_orientation": "0",
    "printable_area": [
      "0x0",
      "300x0",
      "300x300",
      "0x300"
    ],
    "printable_height": "300",
    "printer_model": "Phrozen Arco",
    "printer_notes": "",
    "printer_settings_id": "Phrozen Arco 0.4 nozzle",
    "printer_structure": "corexy",
    "printer_technology": "FFF",
    "printer_variant": "0.4",
    "printhost_authorization_type": "key",
    "printhost_ssl_ignore_revoke": "0",
    "printing_by_object_gcode": "",
    "purge_in_prime_tower": "0",
    "retract_before_wipe": [
      "0%"
    ],
    "retract_length_toolchange": [
      "0"
    ],
    "retract_lift_above": [
      "0.3"
    ],
    "retract_lift_below": [
      "249"
    ],
    "retract_lift_enforce": [
      "All Surfaces"
    ],
    "retract_on_top_layer": [
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
    "retraction_distances_when_cut": [
      "18"
    ],
    "retraction_length": [
      "2"
    ],
    "retraction_minimum_travel": [
      "1"
    ],
    "retraction_speed": [
      "45"
    ],
    "scan_first_layer": "0",
    "silent_mode": "0",
    "single_extruder_multi_material": "1",
    "support_air_filtration": "1",
    "support_chamber_temp_control": "0",
    "support_multi_bed_types": "0",
    "template_custom_gcode": "",
    "thumbnails": "240x224/PNG",
    "thumbnails_format": "PNG",
    "time_cost": "0",
    "time_lapse_gcode": "",
    "travel_slope": [
      "3"
    ],
    "type": "machine",
    "upward_compatible_machine": [],
    "use_firmware_retraction": "0",
    "use_relative_e_distances": "1",
    "wipe": [
      "1"
    ],
    "wipe_distance": [
      "2"
    ],
    "z_hop": [
      "0.4"
    ],
    "z_hop_types": [
      "Spiral Lift"
    ],
    "z_offset": "0"
  },
  "machine/Phrozen Arco.json": {
    "bed_model": "Phrozen Arco_buildplate_model.stl",
    "bed_texture": "Phrozen Arco_buildplate_texture.svg",
    "default_materials": "Phrozen PLA @Phrozen Arco 0.4 nozzle",
    "family": "Phrozen",
    "hotend_model": "",
    "machine_tech": "FFF",
    "model_id": "Phrozen Arco",
    "name": "Phrozen Arco",
    "nozzle_diameter": "0.4",
    "type": "machine_model"
  },
  "machine/_fdm_machine_common.json": {
    "before_layer_change_gcode": ";BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n",
    "change_filament_gcode": "",
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
    "from": "system",
    "gcode_flavor": "marlin",
    "instantiation": "false",
    "layer_change_gcode": ";AFTER_LAYER_CHANGE\n;[layer_z]",
    "machine_end_gcode": "",
    "machine_max_acceleration_e": [
      "5000",
      "5000"
    ],
    "machine_max_acceleration_extruding": [
      "2000",
      "2000"
    ],
    "machine_max_acceleration_retracting": [
      "5000",
      "5000"
    ],
    "machine_max_acceleration_travel": [
      "3000",
      "3000"
    ],
    "machine_max_acceleration_x": [
      "2000",
      "2000"
    ],
    "machine_max_acceleration_y": [
      "2000",
      "2000"
    ],
    "machine_max_acceleration_z": [
      "300",
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
      "300",
      "200"
    ],
    "machine_max_speed_y": [
      "300",
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
    "machine_pause_gcode": "M400 U1\n",
    "machine_start_gcode": "",
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
    "printable_height": "300",
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
    "from": "system",
    "gcode_flavor": "marlin",
    "instantiation": "false",
    "name": "fdm_machine_common",
    "type": "machine"
  }
}

PROCESS = {
  "process/0.20mm Standard @Phrozen Arco 0.4 nozzle.json": {
    "accel_to_decel_enable": "1",
    "accel_to_decel_factor": "50%",
    "alternate_extra_wall": "0",
    "bottom_shell_layers": "3",
    "bottom_shell_thickness": "0",
    "bottom_solid_infill_flow_ratio": "1",
    "bottom_surface_pattern": "monotonic",
    "bridge_acceleration": "50%",
    "bridge_angle": "0",
    "bridge_density": "100%",
    "bridge_flow": "0.9",
    "bridge_no_support": "0",
    "bridge_speed": "30",
    "brim_ears_detection_length": "1",
    "brim_ears_max_angle": "125",
    "brim_object_gap": "0.1",
    "brim_type": "auto_brim",
    "brim_width": "5",
    "compatible_printers": [
      "Phrozen Arco 0.4 nozzle"
    ],
    "compatible_printers_condition": "",
    "counterbore_hole_bridging": "none",
    "default_acceleration": "10000",
    "default_jerk": "9",
    "detect_narrow_internal_solid_infill": "1",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "dont_filter_internal_bridges": "disabled",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.075",
    "elefant_foot_compensation_layers": "1",
    "enable_arc_fitting": "0",
    "enable_overhang_speed": "1",
    "enable_prime_tower": "1",
    "enable_support": "0",
    "enforce_support_layers": "0",
    "ensure_vertical_shell_thickness": "ensure_all",
    "exclude_object": "1",
    "extra_perimeters_on_overhangs": "1",
    "filename_format": "{input_filename_base}_{filament_type[0]}_{layer_height}_{print_time}.gcode",
    "filter_out_gap_fill": "0",
    "flush_into_infill": "0",
    "flush_into_objects": "0",
    "flush_into_support": "1",
    "from": "system",
    "fuzzy_skin": "none",
    "fuzzy_skin_first_layer": "0",
    "fuzzy_skin_point_distance": "0.8",
    "fuzzy_skin_thickness": "0.3",
    "gap_fill_target": "topbottom",
    "gap_infill_speed": "250",
    "gcode_add_line_number": "0",
    "gcode_comments": "0",
    "gcode_label_objects": "1",
    "hole_to_polyhole": "0",
    "hole_to_polyhole_threshold": "0.01",
    "hole_to_polyhole_twisted": "1",
    "independent_support_layer_height": "1",
    "infill_anchor": "400%",
    "infill_anchor_max": "20",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_jerk": "9",
    "infill_wall_overlap": "15%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "500",
    "initial_layer_infill_speed": "80",
    "initial_layer_jerk": "9",
    "initial_layer_line_width": "0.5",
    "initial_layer_min_bead_width": "85%",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "50",
    "initial_layer_travel_speed": "100%",
    "inner_wall_acceleration": "5000",
    "inner_wall_jerk": "9",
    "inner_wall_line_width": "0.45",
    "inner_wall_speed": "300",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_bridge_flow": "1",
    "internal_bridge_speed": "150%",
    "internal_solid_infill_acceleration": "5000",
    "internal_solid_infill_line_width": "0.42",
    "internal_solid_infill_pattern": "monotonic",
    "internal_solid_infill_speed": "250",
    "ironing_angle": "0",
    "ironing_flow": "10%",
    "ironing_pattern": "zig-zag",
    "ironing_spacing": "0.15",
    "ironing_speed": "30",
    "ironing_type": "no ironing",
    "is_infill_first": "0",
    "layer_height": "0.2",
    "line_width": "0.42",
    "make_overhang_printable": "0",
    "make_overhang_printable_angle": "55",
    "make_overhang_printable_hole_size": "0",
    "max_bridge_length": "10",
    "max_travel_detour_distance": "0",
    "max_volumetric_extrusion_rate_slope": "0",
    "max_volumetric_extrusion_rate_slope_segment_length": "3",
    "min_bead_width": "85%",
    "min_feature_size": "25%",
    "min_length_factor": "0.5",
    "min_width_top_surface": "300%",
    "minimum_sparse_infill_area": "15",
    "mmu_segmented_region_interlocking_depth": "0",
    "mmu_segmented_region_max_width": "0",
    "name": "0.20mm Standard @Phrozen Arco 0.4 nozzle",
    "notes": "",
    "only_one_wall_first_layer": "0",
    "only_one_wall_top": "1",
    "ooze_prevention": "0",
    "outer_wall_acceleration": "5000",
    "outer_wall_jerk": "9",
    "outer_wall_line_width": "0.42",
    "outer_wall_speed": "200",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "50",
    "overhang_3_4_speed": "30",
    "overhang_4_4_speed": "10",
    "overhang_reverse": "0",
    "overhang_reverse_internal_only": "0",
    "overhang_reverse_threshold": "50%",
    "overhang_speed_classic": "1",
    "overhang_totally_speed": "10",
    "post_process": [],
    "precise_outer_wall": "1",
    "precise_z_height": "0",
    "prime_tower_brim_width": "5",
    "prime_tower_width": "35",
    "prime_volume": "20",
    "print_flow_ratio": "1",
    "print_order": "default",
    "print_sequence": "by layer",
    "print_settings_id": "0.20mm Standard @Phrozen Arco 0.4 nozzle",
    "raft_contact_distance": "0.1",
    "raft_expansion": "1.5",
    "raft_first_layer_density": "90%",
    "raft_first_layer_expansion": "5",
    "raft_layers": "0",
    "reduce_crossing_wall": "0",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "role_based_wipe_speed": "1",
    "rotate_solid_infill_direction": "1",
    "scarf_angle_threshold": "155",
    "scarf_joint_flow_ratio": "1",
    "scarf_joint_speed": "35",
    "scarf_overhang_threshold": "40%",
    "seam_gap": "10%",
    "seam_position": "aligned",
    "seam_slope_conditional": "1",
    "seam_slope_entire_loop": "0",
    "seam_slope_inner_walls": "0",
    "seam_slope_min_length": "10",
    "seam_slope_start_height": "0",
    "seam_slope_steps": "10",
    "seam_slope_type": "none",
    "setting_id": "GP004",
    "single_extruder_multi_material_priming": "0",
    "skirt_distance": "2",
    "skirt_height": "1",
    "skirt_loops": "0",
    "skirt_speed": "50",
    "slice_closing_radius": "0.049",
    "slicing_mode": "regular",
    "slow_down_layers": "0",
    "slowdown_for_curled_perimeters": "0",
    "small_area_infill_flow_compensation": "0",
    "small_area_infill_flow_compensation_model": [
      "0,0",
      "\n0.2,0.4444",
      "\n0.4,0.6145",
      "\n0.6,0.7059",
      "\n0.8,0.7619",
      "\n1.5,0.8571",
      "\n2,0.8889",
      "\n3,0.9231",
      "\n5,0.9520",
      "\n10,1"
    ],
    "small_perimeter_speed": "50%",
    "small_perimeter_threshold": "0",
    "solid_infill_direction": "45",
    "solid_infill_filament": "1",
    "sparse_infill_acceleration": "100%",
    "sparse_infill_density": "15%",
    "sparse_infill_filament": "1",
    "sparse_infill_line_width": "0.45",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "270",
    "spiral_mode": "0",
    "spiral_mode_max_xy_smoothing": "200%",
    "spiral_mode_smooth": "0",
    "staggered_inner_seams": "0",
    "standby_temperature_delta": "-5",
    "support_angle": "0",
    "support_base_pattern": "default",
    "support_base_pattern_spacing": "2.5",
    "support_bottom_interface_spacing": "0.5",
    "support_bottom_z_distance": "0.2",
    "support_critical_regions_only": "0",
    "support_expansion": "0",
    "support_filament": "0",
    "support_interface_bottom_layers": "2",
    "support_interface_filament": "0",
    "support_interface_loop_pattern": "0",
    "support_interface_not_for_body": "1",
    "support_interface_pattern": "auto",
    "support_interface_spacing": "0.5",
    "support_interface_speed": "80",
    "support_interface_top_layers": "2",
    "support_line_width": "0.42",
    "support_object_xy_distance": "0.35",
    "support_on_build_plate_only": "1",
    "support_remove_small_overhang": "1",
    "support_speed": "150",
    "support_style": "default",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.18",
    "support_type": "tree(auto)",
    "thick_bridges": "0",
    "thick_internal_bridges": "1",
    "timelapse_type": "0",
    "top_bottom_infill_wall_overlap": "25%",
    "top_shell_layers": "5",
    "top_shell_thickness": "1",
    "top_solid_infill_flow_ratio": "0.97",
    "top_surface_acceleration": "2000",
    "top_surface_jerk": "9",
    "top_surface_line_width": "0.42",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "200",
    "travel_acceleration": "10000",
    "travel_jerk": "9",
    "travel_speed": "300",
    "travel_speed_z": "0",
    "tree_support_adaptive_layer_height": "1",
    "tree_support_angle_slow": "25",
    "tree_support_auto_brim": "1",
    "tree_support_branch_angle": "45",
    "tree_support_branch_angle_organic": "40",
    "tree_support_branch_diameter": "2",
    "tree_support_branch_diameter_angle": "5",
    "tree_support_branch_diameter_double_wall": "3",
    "tree_support_branch_diameter_organic": "2",
    "tree_support_branch_distance": "5",
    "tree_support_branch_distance_organic": "1",
    "tree_support_brim_width": "3",
    "tree_support_tip_diameter": "0.8",
    "tree_support_top_rate": "30%",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_direction": "auto",
    "wall_distribution_count": "1",
    "wall_filament": "1",
    "wall_generator": "classic",
    "wall_loops": "2",
    "wall_sequence": "outer wall/inner wall",
    "wall_transition_angle": "10",
    "wall_transition_filter_deviation": "25%",
    "wall_transition_length": "100%",
    "wipe_before_external_loop": "0",
    "wipe_on_loops": "0",
    "wipe_speed": "80%",
    "wipe_tower_bridging": "10",
    "wipe_tower_cone_angle": "15",
    "wipe_tower_extra_spacing": "120%",
    "wipe_tower_extruder": "0",
    "wipe_tower_max_purge_speed": "90",
    "wipe_tower_no_sparse_layers": "0",
    "wipe_tower_rotation_angle": "0",
    "wiping_volumes_extruders": [
      "70",
      "70",
      "70",
      "70",
      "70",
      "70",
      "70",
      "70",
      "70",
      "70"
    ],
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/fdm_process_common.json": {
    "adaptive_layer_height": "0",
    "bottom_shell_layers": "3",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "1",
    "bridge_no_support": "0",
    "bridge_speed": "50",
    "brim_object_gap": "0.1",
    "brim_width": "5",
    "compatible_printers": [],
    "compatible_printers_condition": "",
    "default_acceleration": "1000",
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
    "infill_wall_overlap": "25%",
    "initial_layer_acceleration": "500",
    "initial_layer_infill_speed": "45",
    "initial_layer_line_width": "0.5",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "45",
    "inner_wall_acceleration": "900",
    "inner_wall_line_width": "0.45",
    "inner_wall_speed": "80",
    "instantiation": "false",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0.4",
    "internal_solid_infill_speed": "150",
    "ironing_flow": "10%",
    "ironing_spacing": "0.15",
    "ironing_speed": "30",
    "ironing_type": "no ironing",
    "layer_height": "0.2",
    "line_width": "0.4",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "15",
    "name": "fdm_process_common",
    "outer_wall_acceleration": "700",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "45",
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
    "sparse_infill_speed": "150",
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
    "top_shell_layers": "4",
    "top_shell_thickness": "0.8",
    "top_surface_acceleration": "800",
    "top_surface_line_width": "0.4",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "50",
    "travel_acceleration": "1000",
    "travel_speed": "200",
    "tree_support_branch_angle": "30",
    "tree_support_wall_count": "0",
    "tree_support_with_infill": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "3",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  }
}

FILAMENT = {
  "filament/Phrozen PLA @Phrozen Arco 0.4 nozzle.json": {
    "activate_air_filtration": [
      "1"
    ],
    "activate_chamber_temp_control": [
      "0"
    ],
    "adaptive_pressure_advance_model": [
      "0.042,0.72,5000\n0.044,1.44,5000\n0.045,2.16,5000\n0.045,2.88,5000\n0.045,3.58,5000\n0.044,4.3,5000\n0.045,5.02,5000\n0.043,5.73,5000\n0.045,6.45,5000\n0.041,7.17,5000\n0.039,7.89,5000\n0.038,8.61,5000\n0.036,9.33,5000\n0.033,10.05,5000\n0.032,10.77,5000\n0.034,11.49,5000\n0.033,12.21,5000"
    ],
    "additional_cooling_fan_speed": [
      "60"
    ],
    "bed_type": [
      "Cool Plate"
    ],
    "chamber_temperature": [
      "0"
    ],
    "close_fan_the_first_x_layers": [
      "1"
    ],
    "compatible_printers": [
      "Phrozen Arco 0.4 nozzle"
    ],
    "compatible_printers_condition": "",
    "compatible_prints": [],
    "compatible_prints_condition": "",
    "complete_print_exhaust_fan_speed": [
      "80"
    ],
    "cool_plate_temp": [
      "35"
    ],
    "cool_plate_temp_initial_layer": [
      "35"
    ],
    "default_filament_colour": [
      ""
    ],
    "during_print_exhaust_fan_speed": [
      "60"
    ],
    "enable_overhang_bridge_fan": [
      "1"
    ],
    "enable_pressure_advance": [
      "1"
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
    "filament_cooling_final_speed": [
      "0"
    ],
    "filament_cooling_initial_speed": [
      "0"
    ],
    "filament_cooling_moves": [
      "0"
    ],
    "filament_cost": [
      "20"
    ],
    "filament_density": [
      "1.24"
    ],
    "filament_deretraction_speed": [
      "nil"
    ],
    "filament_diameter": [
      "1.75"
    ],
    "filament_end_gcode": [
      "; filament end gcode\n"
    ],
    "filament_flow_ratio": [
      "0.98"
    ],
    "filament_id": "GFL99",
    "filament_is_support": [
      "0"
    ],
    "filament_load_time": [
      "31.925"
    ],
    "filament_loading_speed": [
      "0"
    ],
    "filament_loading_speed_start": [
      "0"
    ],
    "filament_long_retractions_when_cut": [
      "nil"
    ],
    "filament_max_volumetric_speed": [
      "12"
    ],
    "filament_minimal_purge_on_wipe_tower": [
      "15"
    ],
    "filament_multitool_ramming": [
      "0"
    ],
    "filament_multitool_ramming_flow": [
      "0"
    ],
    "filament_multitool_ramming_volume": [
      "0"
    ],
    "filament_notes": [
      ""
    ],
    "filament_ramming_parameters": [
      "120 100 6.6 6.8 7.2 7.6 7.9 8.2 8.7 9.4 9.9 10.0| 0.05 6.6 0.45 6.8 0.95 7.8 1.45 8.3 1.95 9.7 2.45 10 2.95 7.6 3.45 7.6 3.95 7.6 4.45 7.6 4.95 7.6"
    ],
    "filament_retract_before_wipe": [
      "nil"
    ],
    "filament_retract_lift_above": [
      "nil"
    ],
    "filament_retract_lift_below": [
      "nil"
    ],
    "filament_retract_lift_enforce": [
      "nil"
    ],
    "filament_retract_restart_extra": [
      "nil"
    ],
    "filament_retract_when_changing_layer": [
      "nil"
    ],
    "filament_retraction_distances_when_cut": [
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
      "Phrozen PLA @Phrozen Arco 0.4 nozzle"
    ],
    "filament_shrink": [
      "100%"
    ],
    "filament_soluble": [
      "0"
    ],
    "filament_start_gcode": [
      "; filament start gcode"
    ],
    "filament_toolchange_delay": [
      "0"
    ],
    "filament_unload_time": [
      "24.75"
    ],
    "filament_unloading_speed": [
      "0"
    ],
    "filament_unloading_speed_start": [
      "0"
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
    "hot_plate_temp": [
      "55"
    ],
    "hot_plate_temp_initial_layer": [
      "55"
    ],
    "inherits": "fdm_filament_pla",
    "instantiation": "true",
    "name": "Phrozen PLA @Phrozen Arco 0.4 nozzle",
    "nozzle_temperature": [
      "205"
    ],
    "nozzle_temperature_initial_layer": [
      "215"
    ],
    "nozzle_temperature_range_high": [
      "240"
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
    "pressure_advance": [
      "0.035"
    ],
    "reduce_fan_stop_start_freq": [
      "1"
    ],
    "required_nozzle_HRC": [
      "3"
    ],
    "setting_id": "GFSA04",
    "slow_down_for_layer_cooling": [
      "1"
    ],
    "slow_down_layer_time": [
      "8"
    ],
    "slow_down_min_speed": [
      "20"
    ],
    "support_material_interface_fan_speed": [
      "-1"
    ],
    "temperature_vitrification": [
      "55"
    ],
    "textured_plate_temp": [
      "55"
    ],
    "textured_plate_temp_initial_layer": [
      "55"
    ],
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
    "filament_z_hop_types": [
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
      "45"
    ],
    "hot_plate_temp_initial_layer": [
      "45"
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
    "type": "filament"
  }
}

MISC = {}

ASSETS = [
  "Phrozen Arco_buildplate_model.stl",
  "Phrozen Arco_buildplate_texture.svg",
  "Phrozen Arco_cover.png"
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
