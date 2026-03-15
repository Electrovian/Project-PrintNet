from __future__ import annotations

VENDOR = "TwoTrees"
INDEX = {
  "description": "TwoTrees configurations",
  "filament_list": [
    {
      "name": "TwoTrees Generic 95A TPU @SK1",
      "sub_path": "filament/TwoTrees Generic 95A TPU @SK1.json"
    },
    {
      "name": "TwoTrees Generic HS PLA @SK1",
      "sub_path": "filament/TwoTrees Generic HS PLA @SK1.json"
    }
  ],
  "force_update": "1",
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
      "name": "TwoTrees SK1 0.4 nozzle",
      "sub_path": "machine/TwoTrees SK1 0.4 nozzle.json"
    },
    {
      "name": "TwoTrees SP-5 Klipper 0.4 nozzle",
      "sub_path": "machine/TwoTrees SP-5 Klipper 0.4 nozzle.json"
    }
  ],
  "machine_model_list": [
    {
      "name": "TwoTrees SK1",
      "sub_path": "machine/TwoTrees SK1.json"
    },
    {
      "name": "TwoTrees SP-5 Klipper",
      "sub_path": "machine/TwoTrees SP-5 Klipper.json"
    }
  ],
  "name": "TwoTrees",
  "process_list": [
    {
      "name": "fdm_process_common",
      "sub_path": "process/fdm_process_common.json"
    },
    {
      "name": "0.08mm Extra Fine @SK1",
      "sub_path": "process/0.08mm Extra Fine @SK1.json"
    },
    {
      "name": "0.08mm Extra Fine @TwoTrees",
      "sub_path": "process/0.08mm Extra Fine @TwoTrees.json"
    },
    {
      "name": "0.12mm Fine @SK1",
      "sub_path": "process/0.12mm Fine @SK1.json"
    },
    {
      "name": "0.12mm Fine @TwoTrees",
      "sub_path": "process/0.12mm Fine @TwoTrees.json"
    },
    {
      "name": "0.15mm Optimal @TwoTrees",
      "sub_path": "process/0.15mm Optimal @TwoTrees.json"
    },
    {
      "name": "0.16mm Optimal @SK1",
      "sub_path": "process/0.16mm Optimal @SK1.json"
    },
    {
      "name": "0.20mm Quality @SK1",
      "sub_path": "process/0.20mm Quality @SK1.json"
    },
    {
      "name": "0.20mm Standard @SK1",
      "sub_path": "process/0.20mm Standard @SK1.json"
    },
    {
      "name": "0.20mm Standard @TwoTrees",
      "sub_path": "process/0.20mm Standard @TwoTrees.json"
    },
    {
      "name": "0.24mm Draft @SK1",
      "sub_path": "process/0.24mm Draft @SK1.json"
    },
    {
      "name": "0.24mm Draft @TwoTrees",
      "sub_path": "process/0.24mm Draft @TwoTrees.json"
    },
    {
      "name": "0.24mm HSpeed @SK1",
      "sub_path": "process/0.24mm HSpeed @SK1.json"
    },
    {
      "name": "0.28mm Extra Draft @SK1",
      "sub_path": "process/0.28mm Extra Draft @SK1.json"
    },
    {
      "name": "0.28mm Extra Draft @TwoTrees",
      "sub_path": "process/0.28mm Extra Draft @TwoTrees.json"
    },
    {
      "name": "fdm_process_TwoTrees_common",
      "sub_path": "process/fdm_process_TwoTrees_common.json"
    }
  ],
  "version": "02.03.01.10"
}

MACHINE = {
  "machine/TwoTrees SK1 0.4 nozzle.json": {
    "change_filament_gcode": "PAUSE",
    "default_print_profile": "0.20mm Standard @SK1",
    "deretraction_speed": [
      "0"
    ],
    "from": "system",
    "inherits": "fdm_klipper_common",
    "instantiation": "true",
    "machine_end_gcode": [
      "M104 S0 ; turn off temperature\nM140 S0 ; turn off heatbed\n\nG92 E0.0     ; reset extruder distance position\nG1 E-1 F2100 ; retract\n\nG0 X50 Y250 F12000;\nM84    ; disable motors\n\nM107   ; turn off fan\n\nSET_VELOCITY_LIMIT ACCEL_TO_DECEL=4000"
    ],
    "machine_max_acceleration_e": [
      "20000",
      "5000"
    ],
    "machine_max_acceleration_extruding": [
      "20000",
      "1250"
    ],
    "machine_max_acceleration_retracting": [
      "15000",
      "1250"
    ],
    "machine_max_acceleration_travel": [
      "1500",
      "1250"
    ],
    "machine_max_acceleration_x": [
      "20000",
      "1000"
    ],
    "machine_max_acceleration_y": [
      "20000",
      "1000"
    ],
    "machine_max_acceleration_z": [
      "100",
      "200"
    ],
    "machine_max_jerk_e": [
      "1",
      "2.5"
    ],
    "machine_max_jerk_x": [
      "5",
      "10"
    ],
    "machine_max_jerk_y": [
      "5",
      "10"
    ],
    "machine_max_jerk_z": [
      "0.2",
      "0.4"
    ],
    "machine_max_speed_e": [
      "50",
      "120"
    ],
    "machine_max_speed_x": [
      "730",
      "200"
    ],
    "machine_max_speed_y": [
      "730",
      "200"
    ],
    "machine_max_speed_z": [
      "15",
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
    "machine_start_gcode": [
      "M107 ; Turn off the fan\nG21  ; set units to millimeters\nG90  ; use absolute coordinates\nM83  ; use relative distances for extrusion\n\nM104 S220     ; set extruder temp\nM140 S60  ; set bed temp\nM109 S220      ; wait for extruder temp\nM190 S60  ; wait for bed temp\nG1 E-1.5 F2100 ; retract\n\n;G32  ;Load bed mesh\nG28   ;home\nG29   ;bed leveling\n\nM104 S[first_layer_temperature]      ; set extruder temp\nM140 S[first_layer_bed_temperature]  ; set bed temp\nM109 S[first_layer_temperature]      ; wait for extruder temp\nM190 S[first_layer_bed_temperature]  ; wait for bed temp\n\nG0 Z2.0 F600;\nG0 X50 Y10 F12000;\n\nG92 E0.0 ; reset extruder distance position\nG0 Z0.4 F600;\nG1 X100.0 E10 F3000.0 ; intro line\nG92 E0.0 ; reset extruder distance position\nG1 X200.0 E15 F3000.0 ; intro line\nG92 E0.0 ; reset extruder distance position\nG0 Z0.8 F600;\nG1 X100.0 E15 F3000.0 ; intro line\n\nG1 Z0.4 F600     ;Wipe\nG0 Y12 F6000    ;Wipe\nG1 X100 F6000    ;Wipe\nG0 Y8 F12000   ;Wipe\nG1 X200 F6000    ;Wipe\nG1 X190 Y12 F6000 ;Wipe\nG1 X180 Y8 F6000 ;Wipe\nG1 X170 Y12 F6000 ;Wipe\nG1 X160 Y8 F6000 ;Wipe\nG1 X150 Y12 F6000 ;Wipe\n\n\n;G0 Z2.0 F600;\nG92 E0.0 ; reset extruder distance position\n\nSET_VELOCITY_LIMIT ACCEL_TO_DECEL=10000"
    ],
    "max_layer_height": "0.32",
    "min_layer_height": "0.08",
    "name": "TwoTrees SK1 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "nozzle_type": "hardened_steel",
    "printable_area": [
      "0x0",
      "256x0",
      "256x256",
      "0x256"
    ],
    "printable_height": "256",
    "printer_model": "TwoTrees SK1",
    "retract_before_wipe": "100%",
    "retract_length_toolchange": "10",
    "retraction_length": "0.4",
    "retraction_minimum_travel": [
      "2"
    ],
    "retraction_speed": [
      "50"
    ],
    "setting_id": "GM001",
    "support_multi_bed_types": "1",
    "thumbnails": [
      "300x300"
    ],
    "thumbnails_format": "PNG",
    "type": "machine"
  },
  "machine/TwoTrees SK1.json": {
    "bed_model": "TwoTrees SK1_buildplate_model.stl",
    "bed_texture": "TwoTrees SK1_buildplate_texture.svg",
    "default_materials": "TwoTrees Generic 95A TPU @SK1;TwoTrees Generic PETG @SK1;TwoTrees Generic HS PLA @SK1;TwoTrees Generic PLA @SK1;TwoTrees Generic PLA-CF @SK1;TwoTrees Generic PLA Matte @SK1;TwoTrees Generic PLA Silk @SK1",
    "family": "TwoTreesDesign",
    "hotend_model": "",
    "machine_tech": "FFF",
    "model_id": "TwoTrees_SK1",
    "name": "TwoTrees SK1",
    "nozzle_diameter": "0.4",
    "type": "machine_model"
  },
  "machine/TwoTrees SP-5 Klipper 0.4 nozzle.json": {
    "from": "system",
    "inherits": "fdm_klipper_common",
    "instantiation": "true",
    "name": "TwoTrees SP-5 Klipper 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "printable_area": [
      "0x0",
      "310x0",
      "310x310",
      "0x310"
    ],
    "printable_height": "350",
    "printer_model": "TwoTrees SP-5 Klipper",
    "setting_id": "GM003",
    "type": "machine"
  },
  "machine/TwoTrees SP-5 Klipper.json": {
    "bed_model": "SP-5_bed.stl",
    "bed_texture": "SP-5_texture.svg",
    "default_materials": "TwoTrees Generic ABS;TwoTrees Generic PLA;TwoTrees Generic PLA-CF;TwoTrees Generic PETG;TwoTrees Generic TPU;TwoTrees Generic ASA;TwoTrees Generic PC;TwoTrees Generic PVA;TwoTrees Generic PA;TwoTrees Generic PA-CF",
    "family": "TwoTreesDesign",
    "hotend_model": "",
    "machine_tech": "FFF",
    "model_id": "TwoTrees_SP-5_Klipper",
    "name": "TwoTrees SP-5 Klipper",
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
      "TwoTrees Generic PLA"
    ],
    "deretraction_speed": [
      "30"
    ],
    "extruder_clearance_height_to_lid": "350",
    "extruder_clearance_height_to_rod": "60",
    "extruder_clearance_radius": "50",
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
      "9000",
      "9000"
    ],
    "machine_max_acceleration_y": [
      "9000",
      "9000"
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
    "machine_start_gcode": "START_PRINT EXTRUDER_TEMP=[nozzle_temperature_initial_layer] BED_TEMP=[bed_temperature_initial_layer_single]\n",
    "max_layer_height": [
      "0.32"
    ],
    "min_layer_height": [
      "0.08"
    ],
    "name": "fdm_klipper_common",
    "nozzle_type": "undefine",
    "printable_height": "350",
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
    "use_firmware_retraction": "0",
    "wipe": [
      "1"
    ],
    "z_hop": [
      "0"
    ],
    "z_hop_types": "Normal Lift"
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
  "process/0.08mm Extra Fine @SK1.json": {
    "bottom_shell_layers": "7",
    "bottom_shell_thickness": "0",
    "bridge_acceleration": "4000",
    "bridge_angle": "0",
    "bridge_no_support": "1",
    "bridge_speed": "60",
    "compatible_printers": [
      "TwoTrees SK1 0.4 nozzle"
    ],
    "default_acceleration": "20000",
    "detect_thin_wall": "1",
    "enable_arc_fitting": "0",
    "enable_overhang_speed": "1",
    "enforce_support_layers": "0",
    "extra_perimeters_on_overhangs": "0",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "250",
    "infill_anchor": "600%",
    "infill_anchor_max": "50",
    "infill_combination": "1",
    "infill_wall_overlap": "15%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "1000",
    "initial_layer_infill_speed": "105",
    "initial_layer_line_width": "0.45",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "60",
    "inner_wall_acceleration": "6000",
    "inner_wall_line_width": "0.42",
    "inner_wall_speed": "350",
    "instantiation": "true",
    "internal_solid_infill_acceleration": "6000",
    "internal_solid_infill_line_width": "0.42",
    "internal_solid_infill_speed": "350",
    "ironing_flow": "15%",
    "ironing_spacing": "0.1",
    "ironing_speed": "15",
    "layer_height": "0.08",
    "line_width": "0.42",
    "min_bead_width": "85%",
    "min_feature_size": "25%",
    "minimum_sparse_infill_area": "70",
    "name": "0.08mm Extra Fine @SK1",
    "only_one_wall_top": "1",
    "ooze_prevention": "0",
    "outer_wall_acceleration": "5000",
    "outer_wall_line_width": "0.42",
    "outer_wall_speed": "200",
    "overhang_1_4_speed": "60",
    "overhang_2_4_speed": "30",
    "overhang_3_4_speed": "10",
    "prime_tower_brim_width": "2",
    "raft_contact_distance": "0.1",
    "raft_expansion": "1.5",
    "raft_first_layer_density": "90%",
    "raft_first_layer_expansion": "3",
    "skirt_distance": "6",
    "slice_closing_radius": "0.049",
    "small_perimeter_speed": "200",
    "sparse_infill_acceleration": "6000",
    "sparse_infill_line_width": "0.42",
    "sparse_infill_speed": "450",
    "staggered_inner_seams": "0",
    "support_angle": "0",
    "support_bottom_z_distance": "0.2",
    "support_interface_bottom_layers": "-1",
    "support_interface_pattern": "rectilinear",
    "support_interface_spacing": "0",
    "support_interface_speed": "100",
    "support_interface_top_layers": "3",
    "support_line_width": "0.35",
    "support_object_xy_distance": "0.21",
    "support_speed": "100",
    "support_threshold_angle": "30",
    "thick_bridges": "1",
    "top_shell_layers": "9",
    "top_shell_thickness": "0",
    "top_surface_acceleration": "5000",
    "top_surface_line_width": "0.42",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "200",
    "travel_acceleration": "20000",
    "travel_speed": "500",
    "travel_speed_z": "15",
    "tree_support_angle_slow": "25",
    "tree_support_branch_angle": "40",
    "tree_support_branch_diameter": "2",
    "tree_support_branch_diameter_angle": "5",
    "tree_support_branch_diameter_double_wall": "3",
    "tree_support_tip_diameter": "0.8",
    "tree_support_top_rate": "15%",
    "type": "process",
    "wall_distribution_count": "1",
    "wall_generator": "classic",
    "wall_loops": "2",
    "wall_transition_angle": "10",
    "wall_transition_filter_deviation": "25%",
    "wall_transition_length": "100%"
  },
  "process/0.08mm Extra Fine @TwoTrees.json": {
    "bottom_shell_layers": "7",
    "from": "system",
    "inherits": "fdm_process_common",
    "instantiation": "true",
    "layer_height": "0.08",
    "name": "0.08mm Extra Fine @TwoTrees",
    "setting_id": "GP001",
    "top_shell_layers": "9",
    "type": "process"
  },
  "process/0.12mm Fine @SK1.json": {
    "bottom_shell_layers": "5",
    "bridge_acceleration": "4000",
    "bridge_angle": "0",
    "bridge_flow": "1",
    "bridge_no_support": "1",
    "bridge_speed": "60",
    "compatible_printers": [
      "TwoTrees SK1 0.4 nozzle"
    ],
    "default_acceleration": "20000",
    "detect_thin_wall": "1",
    "enable_overhang_speed": "1",
    "enforce_support_layers": "0",
    "extra_perimeters_on_overhangs": "0",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "250",
    "infill_anchor": "600%",
    "infill_anchor_max": "50",
    "infill_combination": "1",
    "infill_wall_overlap": "15%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "1000",
    "initial_layer_infill_speed": "105",
    "initial_layer_line_width": "0.45",
    "initial_layer_speed": "60",
    "inner_wall_acceleration": "6000",
    "inner_wall_line_width": "0.42",
    "inner_wall_speed": "350",
    "instantiation": "true",
    "internal_solid_infill_acceleration": "6000",
    "internal_solid_infill_line_width": "0.42",
    "internal_solid_infill_speed": "350",
    "ironing_flow": "15%",
    "ironing_spacing": "0.1",
    "ironing_speed": "15",
    "layer_height": "0.12",
    "line_width": "0.42",
    "min_bead_width": "85%",
    "min_feature_size": "25%",
    "minimum_sparse_infill_area": "70",
    "name": "0.12mm Fine @SK1",
    "only_one_wall_top": "1",
    "ooze_prevention": "0",
    "outer_wall_acceleration": "5000",
    "outer_wall_line_width": "0.42",
    "outer_wall_speed": "200",
    "overhang_1_4_speed": "60",
    "overhang_2_4_speed": "30",
    "overhang_3_4_speed": "10",
    "prime_tower_brim_width": "2",
    "raft_contact_distance": "0.1",
    "raft_expansion": "1.5",
    "raft_first_layer_density": "90%",
    "raft_first_layer_expansion": "3",
    "skirt_distance": "6",
    "slice_closing_radius": "0.049",
    "small_perimeter_speed": "200",
    "sparse_infill_acceleration": "6000",
    "sparse_infill_line_width": "0.42",
    "sparse_infill_speed": "400",
    "staggered_inner_seams": "0",
    "support_angle": "0",
    "support_bottom_z_distance": "0.2",
    "support_interface_bottom_layers": "-1",
    "support_interface_pattern": "rectilinear",
    "support_interface_spacing": "0",
    "support_interface_speed": "100",
    "support_interface_top_layers": "3",
    "support_line_width": "0.35",
    "support_object_xy_distance": "0.21",
    "support_speed": "100",
    "support_threshold_angle": "30",
    "thick_bridges": "1",
    "top_shell_layers": "5",
    "top_shell_thickness": "0",
    "top_surface_acceleration": "5000",
    "top_surface_line_width": "0.42",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "200",
    "travel_acceleration": "20000",
    "travel_speed": "500",
    "travel_speed_z": "15",
    "tree_support_angle_slow": "25",
    "tree_support_branch_angle": "40",
    "tree_support_branch_diameter": "2",
    "tree_support_branch_diameter_angle": "5",
    "tree_support_branch_diameter_double_wall": "3",
    "tree_support_tip_diameter": "0.8",
    "tree_support_top_rate": "15%",
    "type": "process",
    "wall_distribution_count": "1",
    "wall_generator": "classic",
    "wall_loops": "2",
    "wall_transition_angle": "10",
    "wall_transition_filter_deviation": "25%",
    "wall_transition_length": "100%"
  },
  "process/0.12mm Fine @TwoTrees.json": {
    "bottom_shell_layers": "5",
    "from": "system",
    "inherits": "fdm_process_common",
    "instantiation": "true",
    "layer_height": "0.12",
    "name": "0.12mm Fine @TwoTrees",
    "setting_id": "GP002",
    "top_shell_layers": "6",
    "type": "process"
  },
  "process/0.15mm Optimal @TwoTrees.json": {
    "bottom_shell_layers": "4",
    "from": "system",
    "inherits": "fdm_process_common",
    "instantiation": "true",
    "layer_height": "0.15",
    "name": "0.15mm Optimal @TwoTrees",
    "setting_id": "GP003",
    "top_shell_layers": "5",
    "type": "process"
  },
  "process/0.16mm Optimal @SK1.json": {
    "bottom_shell_layers": "4",
    "bridge_acceleration": "4000",
    "bridge_angle": "0",
    "bridge_flow": "1",
    "bridge_no_support": "1",
    "bridge_speed": "60",
    "compatible_printers": [
      "TwoTrees SK1 0.4 nozzle"
    ],
    "default_acceleration": "20000",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "enable_overhang_speed": "1",
    "enforce_support_layers": "0",
    "extra_perimeters_on_overhangs": "0",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "250",
    "infill_anchor": "600%",
    "infill_anchor_max": "50",
    "infill_combination": "1",
    "infill_direction": "45",
    "infill_wall_overlap": "15%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "1000",
    "initial_layer_infill_speed": "105",
    "initial_layer_line_width": "0.45",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "60",
    "inner_wall_acceleration": "6000",
    "inner_wall_line_width": "0.42",
    "inner_wall_speed": "300",
    "instantiation": "true",
    "internal_solid_infill_acceleration": "6000",
    "internal_solid_infill_line_width": "0.42",
    "internal_solid_infill_speed": "300",
    "ironing_flow": "15%",
    "ironing_spacing": "0.1",
    "ironing_speed": "15",
    "layer_height": "0.16",
    "line_width": "0.42",
    "min_bead_width": "85%",
    "min_feature_size": "25%",
    "minimum_sparse_infill_area": "70",
    "name": "0.16mm Optimal @SK1",
    "only_one_wall_top": "1",
    "ooze_prevention": "0",
    "outer_wall_acceleration": "5000",
    "outer_wall_line_width": "0.42",
    "outer_wall_speed": "200",
    "overhang_1_4_speed": "60",
    "overhang_2_4_speed": "30",
    "overhang_3_4_speed": "10",
    "prime_tower_brim_width": "2",
    "raft_contact_distance": "0.1",
    "raft_expansion": "1.5",
    "raft_first_layer_density": "90%",
    "raft_first_layer_expansion": "3",
    "skirt_distance": "6",
    "slice_closing_radius": "0.049",
    "small_perimeter_speed": "200",
    "sparse_infill_acceleration": "6000",
    "sparse_infill_line_width": "0.42",
    "sparse_infill_speed": "320",
    "staggered_inner_seams": "0",
    "support_angle": "0",
    "support_bottom_z_distance": "0.2",
    "support_interface_bottom_layers": "-1",
    "support_interface_pattern": "rectilinear",
    "support_interface_spacing": "0",
    "support_interface_speed": "100",
    "support_interface_top_layers": "3",
    "support_line_width": "0.35",
    "support_object_xy_distance": "0.21",
    "support_speed": "100",
    "support_threshold_angle": "30",
    "thick_bridges": "1",
    "top_shell_layers": "4",
    "top_shell_thickness": "0",
    "top_surface_acceleration": "5000",
    "top_surface_line_width": "0.42",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "200",
    "travel_acceleration": "20000",
    "travel_speed": "500",
    "travel_speed_z": "15",
    "tree_support_angle_slow": "25",
    "tree_support_branch_angle": "40",
    "tree_support_branch_diameter": "2",
    "tree_support_branch_diameter_angle": "5",
    "tree_support_branch_diameter_double_wall": "3",
    "tree_support_tip_diameter": "0.8",
    "tree_support_top_rate": "15%",
    "type": "process",
    "wall_distribution_count": "1",
    "wall_generator": "classic",
    "wall_loops": "2",
    "wall_transition_angle": "10",
    "wall_transition_filter_deviation": "25%",
    "wall_transition_length": "100%"
  },
  "process/0.20mm Quality @SK1.json": {
    "bottom_shell_layers": "3",
    "bridge_acceleration": "4000",
    "bridge_angle": "0",
    "bridge_flow": "1",
    "bridge_no_support": "1",
    "bridge_speed": "60",
    "compatible_printers": [
      "TwoTrees SK1 0.4 nozzle"
    ],
    "default_acceleration": "20000",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "enable_overhang_speed": "1",
    "enforce_support_layers": "0",
    "extra_perimeters_on_overhangs": "0",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "250",
    "infill_anchor": "600%",
    "infill_anchor_max": "50",
    "infill_combination": "1",
    "infill_direction": "45",
    "infill_wall_overlap": "15%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "1000",
    "initial_layer_infill_speed": "105",
    "initial_layer_line_width": "0.45",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "60",
    "inner_wall_acceleration": "6000",
    "inner_wall_line_width": "0.42",
    "inner_wall_speed": "300",
    "instantiation": "true",
    "internal_solid_infill_acceleration": "6000",
    "internal_solid_infill_line_width": "0.42",
    "internal_solid_infill_speed": "250",
    "ironing_flow": "15%",
    "ironing_spacing": "0.1",
    "ironing_speed": "15",
    "layer_height": "0.2",
    "line_width": "0.42",
    "min_bead_width": "85%",
    "min_feature_size": "25%",
    "minimum_sparse_infill_area": "70",
    "name": "0.20mm Quality @SK1",
    "only_one_wall_top": "1",
    "ooze_prevention": "0",
    "outer_wall_acceleration": "5000",
    "outer_wall_line_width": "0.42",
    "outer_wall_speed": "60",
    "prime_tower_brim_width": "2",
    "raft_contact_distance": "0.1",
    "raft_expansion": "1.5",
    "raft_first_layer_density": "90%",
    "raft_first_layer_expansion": "3",
    "skirt_distance": "6",
    "slice_closing_radius": "0.049",
    "small_perimeter_speed": "200",
    "sparse_infill_acceleration": "6000",
    "sparse_infill_line_width": "0.42",
    "sparse_infill_speed": "300",
    "staggered_inner_seams": "0",
    "support_angle": "0",
    "support_base_pattern": "rectilinear",
    "support_base_pattern_spacing": "2.5",
    "support_bottom_z_distance": "0.2",
    "support_interface_bottom_layers": "-1",
    "support_interface_loop_pattern": "0",
    "support_interface_pattern": "rectilinear",
    "support_interface_spacing": "0",
    "support_interface_speed": "100",
    "support_interface_top_layers": "3",
    "support_line_width": "0.35",
    "support_object_xy_distance": "0.21",
    "support_speed": "100",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.2",
    "thick_bridges": "1",
    "top_shell_layers": "3",
    "top_shell_thickness": "0",
    "top_surface_acceleration": "5000",
    "top_surface_line_width": "0.42",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "60",
    "travel_acceleration": "20000",
    "travel_speed": "500",
    "travel_speed_z": "15",
    "tree_support_angle_slow": "25",
    "tree_support_branch_angle": "40",
    "tree_support_branch_diameter": "2",
    "tree_support_branch_diameter_angle": "5",
    "tree_support_branch_diameter_double_wall": "3",
    "tree_support_tip_diameter": "0.8",
    "tree_support_top_rate": "15%",
    "type": "process",
    "wall_distribution_count": "1",
    "wall_generator": "classic",
    "wall_loops": "2",
    "wall_transition_angle": "10",
    "wall_transition_filter_deviation": "25%",
    "wall_transition_length": "100%"
  },
  "process/0.20mm Standard @SK1.json": {
    "bottom_shell_layers": "3",
    "bridge_acceleration": "4000",
    "bridge_angle": "0",
    "bridge_flow": "1",
    "bridge_no_support": "1",
    "bridge_speed": "60",
    "compatible_printers": [
      "TwoTrees SK1 0.4 nozzle"
    ],
    "default_acceleration": "20000",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "enable_overhang_speed": "1",
    "enforce_support_layers": "0",
    "extra_perimeters_on_overhangs": "0",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "250",
    "infill_anchor": "600%",
    "infill_anchor_max": "50",
    "infill_combination": "1",
    "infill_direction": "45",
    "infill_wall_overlap": "15%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "1000",
    "initial_layer_infill_speed": "105",
    "initial_layer_line_width": "0.45",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "60",
    "inner_wall_acceleration": "6000",
    "inner_wall_line_width": "0.42",
    "inner_wall_speed": "300",
    "instantiation": "true",
    "internal_solid_infill_acceleration": "6000",
    "internal_solid_infill_line_width": "0.42",
    "internal_solid_infill_speed": "250",
    "ironing_flow": "15%",
    "ironing_spacing": "0.1",
    "ironing_speed": "15",
    "layer_height": "0.2",
    "line_width": "0.42",
    "min_bead_width": "85%",
    "min_feature_size": "25%",
    "minimum_sparse_infill_area": "70",
    "name": "0.20mm Standard @SK1",
    "only_one_wall_top": "1",
    "ooze_prevention": "0",
    "outer_wall_acceleration": "5000",
    "outer_wall_line_width": "0.42",
    "outer_wall_speed": "200",
    "prime_tower_brim_width": "2",
    "raft_contact_distance": "0.1",
    "raft_expansion": "1.5",
    "raft_first_layer_density": "90%",
    "raft_first_layer_expansion": "3",
    "skirt_distance": "6",
    "slice_closing_radius": "0.049",
    "small_perimeter_speed": "200",
    "sparse_infill_acceleration": "6000",
    "sparse_infill_line_width": "0.42",
    "sparse_infill_speed": "300",
    "staggered_inner_seams": "0",
    "support_angle": "0",
    "support_base_pattern": "rectilinear",
    "support_base_pattern_spacing": "2.5",
    "support_bottom_z_distance": "0.2",
    "support_interface_bottom_layers": "-1",
    "support_interface_loop_pattern": "0",
    "support_interface_pattern": "rectilinear",
    "support_interface_spacing": "0",
    "support_interface_speed": "100",
    "support_interface_top_layers": "3",
    "support_line_width": "0.35",
    "support_object_xy_distance": "0.21",
    "support_speed": "100",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.2",
    "thick_bridges": "1",
    "top_shell_layers": "3",
    "top_shell_thickness": "0",
    "top_surface_acceleration": "5000",
    "top_surface_line_width": "0.42",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "200",
    "travel_acceleration": "20000",
    "travel_speed": "500",
    "travel_speed_z": "15",
    "tree_support_angle_slow": "25",
    "tree_support_branch_angle": "40",
    "tree_support_branch_diameter": "2",
    "tree_support_branch_diameter_angle": "5",
    "tree_support_branch_diameter_double_wall": "3",
    "tree_support_tip_diameter": "0.8",
    "tree_support_top_rate": "15%",
    "type": "process",
    "wall_distribution_count": "1",
    "wall_generator": "classic",
    "wall_loops": "2",
    "wall_transition_angle": "10",
    "wall_transition_filter_deviation": "25%",
    "wall_transition_length": "100%"
  },
  "process/0.20mm Standard @TwoTrees.json": {
    "bottom_shell_layers": "3",
    "from": "system",
    "inherits": "fdm_process_common",
    "instantiation": "true",
    "layer_height": "0.2",
    "name": "0.20mm Standard @TwoTrees",
    "setting_id": "GP004",
    "top_shell_layers": "4",
    "type": "process"
  },
  "process/0.24mm Draft @SK1.json": {
    "bottom_shell_layers": "3",
    "bridge_acceleration": "4000",
    "bridge_angle": "0",
    "bridge_flow": "1",
    "bridge_no_support": "1",
    "bridge_speed": "60",
    "compatible_printers": [
      "TwoTrees SK1 0.4 nozzle"
    ],
    "default_acceleration": "20000",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "enable_overhang_speed": "1",
    "enforce_support_layers": "0",
    "extra_perimeters_on_overhangs": "0",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "250",
    "infill_anchor": "600%",
    "infill_anchor_max": "50",
    "infill_combination": "1",
    "infill_direction": "45",
    "infill_wall_overlap": "15%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "1000",
    "initial_layer_infill_speed": "105",
    "initial_layer_line_width": "0.45",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "60",
    "inner_wall_acceleration": "6000",
    "inner_wall_line_width": "0.42",
    "inner_wall_speed": "220",
    "instantiation": "true",
    "internal_solid_infill_acceleration": "6000",
    "internal_solid_infill_line_width": "0.42",
    "internal_solid_infill_speed": "240",
    "ironing_flow": "15%",
    "ironing_spacing": "0.1",
    "ironing_speed": "15",
    "layer_height": "0.24",
    "line_width": "0.42",
    "min_bead_width": "85%",
    "min_feature_size": "25%",
    "minimum_sparse_infill_area": "70",
    "name": "0.24mm Draft @SK1",
    "only_one_wall_top": "1",
    "ooze_prevention": "0",
    "outer_wall_acceleration": "5000",
    "outer_wall_line_width": "0.42",
    "outer_wall_speed": "200",
    "prime_tower_brim_width": "2",
    "raft_contact_distance": "0.1",
    "raft_expansion": "1.5",
    "raft_first_layer_density": "90%",
    "raft_first_layer_expansion": "3",
    "skirt_distance": "6",
    "slice_closing_radius": "0.049",
    "small_perimeter_speed": "200",
    "sparse_infill_acceleration": "6000",
    "sparse_infill_line_width": "0.42",
    "sparse_infill_speed": "250",
    "staggered_inner_seams": "0",
    "support_angle": "0",
    "support_base_pattern": "rectilinear",
    "support_base_pattern_spacing": "2.5",
    "support_bottom_z_distance": "0.2",
    "support_interface_bottom_layers": "-1",
    "support_interface_loop_pattern": "0",
    "support_interface_pattern": "rectilinear",
    "support_interface_spacing": "0",
    "support_interface_speed": "100",
    "support_interface_top_layers": "3",
    "support_line_width": "0.35",
    "support_object_xy_distance": "0.21",
    "support_speed": "100",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.2",
    "thick_bridges": "1",
    "top_shell_layers": "3",
    "top_shell_thickness": "0",
    "top_surface_acceleration": "5000",
    "top_surface_line_width": "0.42",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "200",
    "travel_acceleration": "20000",
    "travel_speed": "500",
    "travel_speed_z": "15",
    "tree_support_angle_slow": "25",
    "tree_support_branch_angle": "40",
    "tree_support_branch_diameter": "2",
    "tree_support_branch_diameter_angle": "5",
    "tree_support_branch_diameter_double_wall": "3",
    "tree_support_tip_diameter": "0.8",
    "tree_support_top_rate": "15%",
    "type": "process",
    "wall_distribution_count": "1",
    "wall_generator": "classic",
    "wall_loops": "2",
    "wall_transition_angle": "10",
    "wall_transition_filter_deviation": "25%",
    "wall_transition_length": "100%"
  },
  "process/0.24mm Draft @TwoTrees.json": {
    "bottom_shell_layers": "3",
    "from": "system",
    "inherits": "fdm_process_common",
    "instantiation": "true",
    "layer_height": "0.24",
    "name": "0.24mm Draft @TwoTrees",
    "setting_id": "GP005",
    "top_shell_layers": "4",
    "top_surface_line_width": "0.45",
    "type": "process"
  },
  "process/0.24mm HSpeed @SK1.json": {
    "bottom_shell_layers": "3",
    "bridge_acceleration": "0",
    "bridge_angle": "0",
    "bridge_flow": "1",
    "bridge_no_support": "1",
    "bridge_speed": "60",
    "compatible_printers": [
      "TwoTrees SK1 0.4 nozzle"
    ],
    "default_acceleration": "20000",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "enable_overhang_speed": "1",
    "enforce_support_layers": "0",
    "extra_perimeters_on_overhangs": "0",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "320",
    "infill_anchor": "600%",
    "infill_anchor_max": "5",
    "infill_combination": "1",
    "infill_direction": "45",
    "infill_wall_overlap": "15%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "2000",
    "initial_layer_infill_speed": "105",
    "initial_layer_line_width": "0.45",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "60",
    "inner_wall_acceleration": "0",
    "inner_wall_line_width": "0.42",
    "inner_wall_speed": "300",
    "instantiation": "true",
    "internal_solid_infill_acceleration": "0",
    "internal_solid_infill_line_width": "0.42",
    "internal_solid_infill_pattern": "alignedrectilinear",
    "internal_solid_infill_speed": "300",
    "ironing_flow": "15%",
    "ironing_spacing": "0.1",
    "ironing_speed": "15",
    "layer_height": "0.24",
    "line_width": "0.42",
    "min_bead_width": "85%",
    "min_feature_size": "25%",
    "minimum_sparse_infill_area": "70",
    "name": "0.24mm HSpeed @SK1",
    "only_one_wall_top": "1",
    "ooze_prevention": "0",
    "outer_wall_acceleration": "0",
    "outer_wall_line_width": "0.42",
    "outer_wall_speed": "230",
    "prime_tower_brim_width": "2",
    "raft_contact_distance": "0.1",
    "raft_expansion": "1.5",
    "raft_first_layer_density": "90%",
    "raft_first_layer_expansion": "3",
    "reduce_crossing_wall": "0",
    "seam_position": "nearest",
    "skirt_distance": "6",
    "slice_closing_radius": "0.049",
    "small_perimeter_speed": "200",
    "sparse_infill_acceleration": "0",
    "sparse_infill_density": "10%",
    "sparse_infill_line_width": "0.42",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "400",
    "staggered_inner_seams": "0",
    "support_angle": "0",
    "support_base_pattern": "rectilinear",
    "support_base_pattern_spacing": "2.5",
    "support_bottom_z_distance": "0.2",
    "support_interface_bottom_layers": "-1",
    "support_interface_loop_pattern": "0",
    "support_interface_pattern": "rectilinear",
    "support_interface_spacing": "0",
    "support_interface_speed": "100",
    "support_interface_top_layers": "3",
    "support_line_width": "0.35",
    "support_object_xy_distance": "0.21",
    "support_speed": "100",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.2",
    "support_type": "normal(auto)",
    "thick_bridges": "1",
    "top_shell_layers": "3",
    "top_shell_thickness": "0",
    "top_surface_acceleration": "0",
    "top_surface_line_width": "0.42",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "200",
    "travel_acceleration": "20000",
    "travel_speed": "700",
    "travel_speed_z": "15",
    "tree_support_angle_slow": "25",
    "tree_support_branch_angle": "40",
    "tree_support_branch_diameter": "2",
    "tree_support_branch_diameter_angle": "5",
    "tree_support_branch_diameter_double_wall": "3",
    "tree_support_tip_diameter": "0.8",
    "tree_support_top_rate": "15%",
    "type": "process",
    "wall_distribution_count": "1",
    "wall_generator": "classic",
    "wall_loops": "2",
    "wall_transition_angle": "10",
    "wall_transition_filter_deviation": "25%",
    "wall_transition_length": "100%"
  },
  "process/0.28mm Extra Draft @SK1.json": {
    "bottom_shell_layers": "3",
    "bridge_acceleration": "4000",
    "bridge_angle": "0",
    "bridge_flow": "1",
    "bridge_no_support": "1",
    "bridge_speed": "60",
    "compatible_printers": [
      "TwoTrees SK1 0.4 nozzle"
    ],
    "default_acceleration": "20000",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "enable_overhang_speed": "1",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "enforce_support_layers": "0",
    "extra_perimeters_on_overhangs": "0",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "250",
    "infill_anchor": "600%",
    "infill_anchor_max": "50",
    "infill_combination": "1",
    "infill_direction": "45",
    "infill_wall_overlap": "15%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "1000",
    "initial_layer_infill_speed": "105",
    "initial_layer_line_width": "0.45",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "60",
    "inner_wall_acceleration": "6000",
    "inner_wall_line_width": "0.42",
    "inner_wall_speed": "200",
    "instantiation": "true",
    "internal_solid_infill_acceleration": "6000",
    "internal_solid_infill_line_width": "0.42",
    "internal_solid_infill_speed": "200",
    "ironing_flow": "15%",
    "ironing_spacing": "0.1",
    "ironing_speed": "15",
    "layer_height": "0.28",
    "line_width": "0.42",
    "min_bead_width": "85%",
    "min_feature_size": "25%",
    "minimum_sparse_infill_area": "70",
    "name": "0.28mm Extra Draft @SK1",
    "only_one_wall_top": "1",
    "ooze_prevention": "0",
    "outer_wall_acceleration": "5000",
    "outer_wall_line_width": "0.42",
    "outer_wall_speed": "200",
    "prime_tower_brim_width": "2",
    "raft_contact_distance": "0.1",
    "raft_expansion": "1.5",
    "raft_first_layer_density": "90%",
    "raft_first_layer_expansion": "3",
    "skirt_distance": "6",
    "slice_closing_radius": "0.049",
    "small_perimeter_speed": "200",
    "sparse_infill_acceleration": "6000",
    "sparse_infill_line_width": "0.42",
    "sparse_infill_speed": "200",
    "staggered_inner_seams": "0",
    "support_angle": "0",
    "support_base_pattern": "rectilinear",
    "support_base_pattern_spacing": "2.5",
    "support_bottom_z_distance": "0.2",
    "support_interface_bottom_layers": "-1",
    "support_interface_loop_pattern": "0",
    "support_interface_pattern": "rectilinear",
    "support_interface_spacing": "0",
    "support_interface_speed": "100",
    "support_interface_top_layers": "3",
    "support_line_width": "0.35",
    "support_object_xy_distance": "0.21",
    "support_speed": "100",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.2",
    "thick_bridges": "1",
    "top_shell_layers": "3",
    "top_shell_thickness": "0",
    "top_surface_acceleration": "5000",
    "top_surface_line_width": "0.42",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "200",
    "travel_acceleration": "20000",
    "travel_speed": "500",
    "travel_speed_z": "15",
    "tree_support_angle_slow": "25",
    "tree_support_branch_angle": "40",
    "tree_support_branch_diameter": "2",
    "tree_support_branch_diameter_angle": "5",
    "tree_support_branch_diameter_double_wall": "3",
    "tree_support_tip_diameter": "0.8",
    "tree_support_top_rate": "15%",
    "type": "process",
    "wall_distribution_count": "1",
    "wall_generator": "classic",
    "wall_loops": "2",
    "wall_transition_angle": "10",
    "wall_transition_filter_deviation": "25%",
    "wall_transition_length": "100%"
  },
  "process/0.28mm Extra Draft @TwoTrees.json": {
    "bottom_shell_layers": "3",
    "from": "system",
    "inherits": "fdm_process_common",
    "instantiation": "true",
    "layer_height": "0.28",
    "name": "0.28mm Extra Draft @TwoTrees",
    "setting_id": "GP006",
    "top_shell_layers": "4",
    "top_surface_line_width": "0.45",
    "type": "process"
  },
  "process/fdm_process_TwoTrees_common.json": {
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
      "TwoTrees SP-5 0.4 nozzle"
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
    "name": "fdm_process_TwoTrees_common",
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
      "TwoTrees SP-5 Klipper 0.4 nozzle"
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
    "filename_format": "{input_filename_base}_{filament_type[0]}.gcode",
    "from": "system",
    "gap_infill_speed": "100",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "25%",
    "initial_layer_acceleration": "500",
    "initial_layer_infill_speed": "60",
    "initial_layer_line_width": "0.5",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "40",
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
    "reduce_crossing_wall": "1",
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
    "wall_loops": "3",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  }
}

FILAMENT = {
  "filament/TwoTrees Generic 95A TPU @SK1.json": {
    "compatible_printers": [
      "TwoTrees SK1 0.4 nozzle"
    ],
    "fan_cooling_layer_time": "60",
    "fan_max_speed": "100",
    "fan_min_speed": "35",
    "filament_id": "GFU99",
    "filament_max_volumetric_speed": [
      "15"
    ],
    "filament_minimal_purge_on_wipe_tower": "15",
    "from": "system",
    "full_fan_speed_layer": "0",
    "inherits": "fdm_filament_tpu",
    "instantiation": "true",
    "name": "TwoTrees Generic 95A TPU @SK1",
    "nozzle_temperature": "235",
    "nozzle_temperature_initial_layer": "235",
    "reduce_fan_stop_start_freq": "0",
    "setting_id": "GFSU99",
    "slow_down_layer_time": "5",
    "slow_down_min_speed": "10",
    "type": "filament"
  },
  "filament/TwoTrees Generic HS PLA @SK1.json": {
    "compatible_printers": [
      "TwoTrees SK1 0.4 nozzle"
    ],
    "cool_plate_temp": "60",
    "cool_plate_temp_initial_layer": "60",
    "enable_pressure_advance": [
      "1"
    ],
    "eng_plate_temp": "60",
    "eng_plate_temp_initial_layer": "60",
    "fan_min_speed": "35",
    "filament_flow_ratio": [
      "0.98"
    ],
    "filament_id": "GFL100",
    "filament_max_volumetric_speed": [
      "25"
    ],
    "filament_minimal_purge_on_wipe_tower": "15",
    "from": "system",
    "full_fan_speed_layer": "0",
    "hot_plate_temp": "60",
    "hot_plate_temp_initial_layer": "60",
    "inherits": "fdm_filament_pla",
    "instantiation": "true",
    "name": "TwoTrees Generic HS PLA @SK1",
    "nozzle_temperature": [
      "220"
    ],
    "nozzle_temperature_initial_layer": [
      "220"
    ],
    "nozzle_temperature_range_low": [
      "210"
    ],
    "pressure_advance": [
      "0.04"
    ],
    "reduce_fan_stop_start_freq": "0",
    "setting_id": "GFSL100",
    "slow_down_layer_time": "5",
    "slow_down_min_speed": "50",
    "textured_plate_temp": "60",
    "textured_plate_temp_initial_layer": "60",
    "type": "filament"
  }
}

MISC = {}

ASSETS = [
  "SP-5_bed.stl",
  "SP-5_texture.svg",
  "TwoTrees SK1_buildplate_model.stl",
  "TwoTrees SK1_buildplate_texture.svg",
  "TwoTrees SK1_cover.png",
  "TwoTrees SP-5 Klipper_cover.png"
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
