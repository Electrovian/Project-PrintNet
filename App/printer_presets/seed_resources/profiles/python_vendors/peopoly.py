from __future__ import annotations

VENDOR = "Peopoly"
INDEX = {
  "description": "Peopoly configurations",
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
      "name": "fdm_filament_petg",
      "sub_path": "filament/fdm_filament_petg.json"
    },
    {
      "name": "fdm_filament_pla",
      "sub_path": "filament/fdm_filament_pla.json"
    },
    {
      "name": "Peopoly Generic ABS",
      "sub_path": "filament/Peopoly Generic ABS.json"
    },
    {
      "name": "Peopoly Lancer ABS-GF",
      "sub_path": "filament/Peopoly Lancer ABS-GF.json"
    },
    {
      "name": "Peopoly Lancer PET-CF",
      "sub_path": "filament/Peopoly Lancer PET-CF.json"
    },
    {
      "name": "Peopoly Generic PETG",
      "sub_path": "filament/Peopoly Generic PETG.json"
    },
    {
      "name": "Peopoly Lancer PETG-C",
      "sub_path": "filament/Peopoly Lancer PETG-C.json"
    },
    {
      "name": "Peopoly Generic PLA",
      "sub_path": "filament/Peopoly Generic PLA.json"
    },
    {
      "name": "Peopoly Lancer PLA-C",
      "sub_path": "filament/Peopoly Lancer PLA-C.json"
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
      "name": "Peopoly Magneto X 0.4 nozzle",
      "sub_path": "machine/Peopoly Magneto X 0.4 nozzle.json"
    },
    {
      "name": "Peopoly Magneto X 0.6 nozzle",
      "sub_path": "machine/Peopoly Magneto X 0.6 nozzle.json"
    },
    {
      "name": "Peopoly Magneto X 0.8 nozzle",
      "sub_path": "machine/Peopoly Magneto X 0.8 nozzle.json"
    }
  ],
  "machine_model_list": [
    {
      "name": "Peopoly Magneto X",
      "sub_path": "machine/Peopoly Magneto X.json"
    }
  ],
  "name": "Peopoly",
  "process_list": [
    {
      "name": "fdm_process_common",
      "sub_path": "process/fdm_process_common.json"
    },
    {
      "name": "fdm_process_peopoly_common",
      "sub_path": "process/fdm_process_peopoly_common.json"
    },
    {
      "name": "fdm_process_pply_common",
      "sub_path": "process/fdm_process_pply_common.json"
    },
    {
      "name": "fdm_process_peopoly_common_0_2",
      "sub_path": "process/fdm_process_peopoly_common_0_2.json"
    },
    {
      "name": "fdm_process_pply_0.16",
      "sub_path": "process/fdm_process_pply_0.16.json"
    },
    {
      "name": "fdm_process_pply_0.20",
      "sub_path": "process/fdm_process_pply_0.20.json"
    },
    {
      "name": "fdm_process_pply_0.24",
      "sub_path": "process/fdm_process_pply_0.24.json"
    },
    {
      "name": "fdm_process_pply_0.28",
      "sub_path": "process/fdm_process_pply_0.28.json"
    },
    {
      "name": "fdm_process_pply_0.30_nozzle_0.6",
      "sub_path": "process/fdm_process_pply_0.30_nozzle_0.6.json"
    },
    {
      "name": "fdm_process_pply_0.40_nozzle_0.8",
      "sub_path": "process/fdm_process_pply_0.40_nozzle_0.8.json"
    },
    {
      "name": "0.16mm Optimal @Magneto X",
      "sub_path": "process/0.16mm Optimal @MagnetoX.json"
    },
    {
      "name": "0.20mm ABS-GF 0.4 Nozzle Standard @MagnetoX",
      "sub_path": "process/0.20mm ABS-GF 0.4 Nozzle Standard @MagnetoX.json"
    },
    {
      "name": "0.20mm PET-CF 0.4 Nozzle Standard @MagnetoX",
      "sub_path": "process/0.20mm PET-CF 0.4 Nozzle Standard @MagnetoX.json"
    },
    {
      "name": "0.20mm Standard @Magneto X",
      "sub_path": "process/0.20mm Standard @MagnetoX.json"
    },
    {
      "name": "0.20mm Strength @Magneto X",
      "sub_path": "process/0.20mm Strength @MagnetoX.json"
    },
    {
      "name": "0.24mm Draft @Magneto X",
      "sub_path": "process/0.24mm Draft @MagnetoX.json"
    },
    {
      "name": "0.28mm Extra Draft @Magneto X",
      "sub_path": "process/0.28mm Extra Draft @MagnetoX.json"
    },
    {
      "name": "0.30mm Standard @Magneto X 0.6 nozzle",
      "sub_path": "process/0.30mm Standard @Magneto X 0.6 nozzle.json"
    },
    {
      "name": "0.40mm Standard @Magneto X 0.8 nozzle",
      "sub_path": "process/0.40mm Standard @Magneto X 0.8 nozzle.json"
    }
  ],
  "version": "02.03.01.10"
}

MACHINE = {
  "machine/Peopoly Magneto X 0.4 nozzle.json": {
    "from": "system",
    "inherits": "fdm_klipper_common",
    "instantiation": "true",
    "name": "Peopoly Magneto X 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "printable_area": [
      "0x0",
      "300x0",
      "300x400",
      "0x400"
    ],
    "printable_height": "300",
    "printer_model": "Peopoly Magneto X",
    "printer_variant": "0.4",
    "setting_id": "GM001",
    "type": "machine"
  },
  "machine/Peopoly Magneto X 0.6 nozzle.json": {
    "from": "system",
    "inherits": "fdm_klipper_common",
    "instantiation": "true",
    "max_layer_height": [
      "0.42"
    ],
    "min_layer_height": [
      "0.12"
    ],
    "name": "Peopoly Magneto X 0.6 nozzle",
    "nozzle_diameter": [
      "0.6"
    ],
    "printable_area": [
      "0x0",
      "300x0",
      "300x400",
      "0x400"
    ],
    "printable_height": "300",
    "printer_model": "Peopoly Magneto X",
    "printer_variant": "0.6",
    "retract_length_toolchange": [
      "3"
    ],
    "retraction_length": [
      "1"
    ],
    "setting_id": "GM002",
    "type": "machine"
  },
  "machine/Peopoly Magneto X 0.8 nozzle.json": {
    "from": "system",
    "inherits": "fdm_klipper_common",
    "instantiation": "true",
    "max_layer_height": [
      "0.56"
    ],
    "min_layer_height": [
      "0.16"
    ],
    "name": "Peopoly Magneto X 0.8 nozzle",
    "nozzle_diameter": [
      "0.8"
    ],
    "printable_area": [
      "0x0",
      "300x0",
      "300x400",
      "0x400"
    ],
    "printable_height": "300",
    "printer_model": "Peopoly Magneto X",
    "printer_variant": "0.8",
    "retract_length_toolchange": [
      "3"
    ],
    "retraction_length": [
      "3"
    ],
    "setting_id": "GM003",
    "type": "machine"
  },
  "machine/Peopoly Magneto X.json": {
    "bed_model": "magnetox_model.stl",
    "bed_texture": "magnetox_model_texture.png",
    "default_materials": "Peopoly Generic PLA",
    "family": "Peopoly",
    "hotend_model": "",
    "machine_tech": "FFF",
    "model_id": "Peopoly-Magneto-X",
    "name": "Peopoly Magneto X",
    "nozzle_diameter": "0.4;0.6;0.8",
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
      "Peopoly Generic PLA"
    ],
    "default_print_profile": "fdm_process_peopoly_common_0_2",
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
      "12",
      "12"
    ],
    "machine_max_jerk_y": [
      "12",
      "12"
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
    "machine_start_gcode": "M190 S[bed_temperature_initial_layer_single]\nM109 S[nozzle_temperature_initial_layer]\nPRINT_START EXTRUDER=[nozzle_temperature_initial_layer] BED=[bed_temperature_initial_layer_single]\n; You can use following code instead if your PRINT_START macro support Chamber and print area bedmesh\n; PRINT_START EXTRUDER=[nozzle_temperature_initial_layer] BED=[bed_temperature_initial_layer_single] Chamber=[chamber_temperature] PRINT_MIN={first_layer_print_min[0]},{first_layer_print_min[1]} PRINT_MAX={first_layer_print_max[0]},{first_layer_print_max[1]}\n",
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
      "0"
    ],
    "z_hop_types": [
      "Auto Lift"
    ]
  },
  "machine/fdm_machine_common.json": {
    "before_layer_change_gcode": ";BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n",
    "change_filament_gcode": "",
    "default_print_profile": "0.20mm Standard @MagnetoX",
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
      "30"
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
    "z_hop_types": [
      "Auto Lift"
    ]
  }
}

PROCESS = {
  "process/0.16mm Optimal @MagnetoX.json": {
    "compatible_printers": [
      "Peopoly Magneto X 0.4 nozzle"
    ],
    "from": "system",
    "inherits": "fdm_process_pply_0.16",
    "instantiation": "true",
    "name": "0.16mm Optimal @Magneto X",
    "setting_id": "GP003",
    "type": "process"
  },
  "process/0.20mm ABS-GF 0.4 Nozzle Standard @MagnetoX.json": {
    "bottom_shell_layers": "5",
    "bridge_flow": "1",
    "brim_type": "no_brim",
    "compatible_printers": [
      "Peopoly Magneto X 0.4 nozzle"
    ],
    "from": "system",
    "gap_infill_speed": "200",
    "inherits": "fdm_process_pply_0.20",
    "initial_layer_infill_speed": "140",
    "initial_layer_speed": "100",
    "inner_wall_speed": "200",
    "instantiation": "true",
    "internal_solid_infill_speed": "200",
    "name": "0.20mm ABS-GF 0.4 Nozzle Standard @MagnetoX",
    "outer_wall_speed": "160",
    "setting_id": "GP015",
    "skirt_distance": "2",
    "skirt_loops": "2",
    "sparse_infill_density": "20",
    "sparse_infill_speed": "200",
    "top_shell_layers": "5",
    "top_shell_thickness": "0.6",
    "top_surface_speed": "140",
    "type": "process",
    "wall_loops": "3"
  },
  "process/0.20mm PET-CF 0.4 Nozzle Standard @MagnetoX.json": {
    "bottom_shell_layers": "5",
    "bridge_flow": "1",
    "brim_type": "no_brim",
    "compatible_printers": [
      "Peopoly Magneto X 0.4 nozzle"
    ],
    "from": "system",
    "gap_infill_speed": "200",
    "inherits": "fdm_process_pply_0.20",
    "initial_layer_infill_speed": "140",
    "initial_layer_speed": "100",
    "inner_wall_speed": "200",
    "instantiation": "true",
    "internal_solid_infill_speed": "200",
    "name": "0.20mm PET-CF 0.4 Nozzle Standard @MagnetoX",
    "outer_wall_speed": "160",
    "setting_id": "GP016",
    "skirt_distance": "2",
    "skirt_loops": "2",
    "sparse_infill_density": "20",
    "sparse_infill_speed": "200",
    "top_shell_layers": "5",
    "top_shell_thickness": "0.6",
    "top_surface_speed": "140",
    "type": "process",
    "wall_loops": "3"
  },
  "process/0.20mm Standard @MagnetoX.json": {
    "compatible_printers": [
      "Peopoly Magneto X 0.4 nozzle"
    ],
    "from": "system",
    "inherits": "fdm_process_pply_0.20",
    "instantiation": "true",
    "name": "0.20mm Standard @Magneto X",
    "setting_id": "GP004",
    "type": "process"
  },
  "process/0.20mm Strength @MagnetoX.json": {
    "compatible_printers": [
      "Peopoly Magneto X 0.4 nozzle"
    ],
    "from": "system",
    "inherits": "fdm_process_pply_0.20",
    "instantiation": "true",
    "name": "0.20mm Strength @Magneto X",
    "outer_wall_speed": "120",
    "setting_id": "GP013",
    "sparse_infill_density": "25%",
    "type": "process",
    "wall_loops": "6"
  },
  "process/0.24mm Draft @MagnetoX.json": {
    "compatible_printers": [
      "Peopoly Magneto X 0.4 nozzle"
    ],
    "from": "system",
    "inherits": "fdm_process_pply_0.24",
    "instantiation": "true",
    "name": "0.24mm Draft @Magneto X",
    "setting_id": "GP005",
    "type": "process"
  },
  "process/0.28mm Extra Draft @MagnetoX.json": {
    "compatible_printers": [
      "Peopoly Magneto X 0.4 nozzle"
    ],
    "from": "system",
    "inherits": "fdm_process_pply_0.28",
    "instantiation": "true",
    "name": "0.28mm Extra Draft @Magneto X",
    "setting_id": "GP006",
    "type": "process"
  },
  "process/0.30mm Standard @Magneto X 0.6 nozzle.json": {
    "compatible_printers": [
      "Peopoly Magneto X 0.6 nozzle"
    ],
    "from": "system",
    "inherits": "fdm_process_pply_0.30_nozzle_0.6",
    "instantiation": "true",
    "name": "0.30mm Standard @Magneto X 0.6 nozzle",
    "outer_wall_speed": "120",
    "setting_id": "GP008",
    "type": "process"
  },
  "process/0.40mm Standard @Magneto X 0.8 nozzle.json": {
    "compatible_printers": [
      "Peopoly Magneto X 0.8 nozzle"
    ],
    "from": "system",
    "inherits": "fdm_process_pply_0.40_nozzle_0.8",
    "instantiation": "true",
    "name": "0.40mm Standard @Magneto X 0.8 nozzle",
    "setting_id": "GP009",
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
    "infill_wall_overlap": "5%",
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
    "only_one_wall_top": "0",
    "outer_wall_line_width": "0.42",
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
    "support_base_pattern": "default",
    "support_base_pattern_spacing": "2",
    "support_filament": "0",
    "support_interface_filament": "0",
    "support_interface_loop_pattern": "0",
    "support_interface_pattern": "auto",
    "support_interface_spacing": "0",
    "support_interface_speed": "80",
    "support_interface_top_layers": "2",
    "support_line_width": "0.42",
    "support_object_xy_distance": "0.5",
    "support_on_build_plate_only": "0",
    "support_speed": "40",
    "support_threshold_angle": "40",
    "support_top_z_distance": "0.15",
    "top_surface_line_width": "0.42",
    "top_surface_speed": "30",
    "travel_speed": "400",
    "type": "process",
    "wall_loops": "2",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/fdm_process_peopoly_common.json": {
    "accel_to_decel_enable": "1",
    "accel_to_decel_factor": "50%",
    "adaptive_layer_height": "0",
    "bottom_shell_layers": "3",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.95",
    "bridge_no_support": "0",
    "bridge_speed": "25",
    "brim_object_gap": "0.1",
    "brim_width": "5",
    "compatible_printers": [
      "Peopoly Magneto X 0.4 nozzle",
      "Peopoly Magneto X 0.6 nozzle",
      "Peopoly Magneto X 0.8 nozzle"
    ],
    "compatible_printers_condition": "",
    "default_acceleration": "5000",
    "default_jerk": "9",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "0",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "filename_format": "{input_filename_base}_{filament_type[0]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "100",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_jerk": "12",
    "infill_wall_overlap": "25%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "500",
    "initial_layer_infill_speed": "105",
    "initial_layer_jerk": "9",
    "initial_layer_line_width": "0.5",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "50",
    "inner_wall_acceleration": "5000",
    "inner_wall_jerk": "7",
    "inner_wall_line_width": "0.4",
    "inner_wall_speed": "200",
    "instantiation": "false",
    "interface_shells": "0",
    "internal_bridge_speed": "70",
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
    "name": "fdm_process_peopoly_common",
    "outer_wall_acceleration": "3000",
    "outer_wall_jerk": "7",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "120",
    "overhang_1_4_speed": "80%",
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
    "support_style": "default",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.2",
    "support_type": "normal(auto)",
    "top_shell_layers": "3",
    "top_shell_thickness": "0.8",
    "top_surface_acceleration": "3000",
    "top_surface_jerk": "9",
    "top_surface_line_width": "0.4",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "100",
    "travel_acceleration": "7000",
    "travel_jerk": "12",
    "travel_speed": "350",
    "tree_support_branch_angle": "45",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "3",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/fdm_process_peopoly_common_0_2.json": {
    "compatible_printers": [
      "Peopoly Magneto X 0.4 nozzle",
      "Peopoly Magneto X 0.6 nozzle",
      "Peopoly Magneto X 0.8 nozzle"
    ],
    "from": "system",
    "inherits": "fdm_process_peopoly_common",
    "initial_layer_line_width": "0.25",
    "initial_layer_print_height": "0.1",
    "inner_wall_line_width": "0.22",
    "instantiation": "false",
    "internal_solid_infill_line_width": "0.22",
    "line_width": "0.22",
    "name": "fdm_process_peopoly_common_0_2",
    "outer_wall_line_width": "0.22",
    "sparse_infill_line_width": "0.22",
    "support_line_width": "0.22",
    "top_surface_line_width": "0.22",
    "type": "process"
  },
  "process/fdm_process_pply_0.16.json": {
    "bottom_shell_layers": "4",
    "bridge_flow": "1",
    "elefant_foot_compensation": "0.15",
    "from": "system",
    "gap_infill_speed": "320",
    "inherits": "fdm_process_pply_common",
    "initial_layer_infill_speed": "105",
    "initial_layer_speed": "50",
    "inner_wall_speed": "300",
    "instantiation": "false",
    "internal_solid_infill_speed": "350",
    "layer_height": "0.16",
    "name": "fdm_process_pply_0.16",
    "outer_wall_speed": "200",
    "overhang_1_4_speed": "60",
    "overhang_2_4_speed": "30",
    "overhang_3_4_speed": "10",
    "sparse_infill_speed": "330",
    "support_threshold_angle": "25",
    "top_shell_layers": "4",
    "top_shell_thickness": "0.6",
    "type": "process"
  },
  "process/fdm_process_pply_0.20.json": {
    "bridge_flow": "1",
    "elefant_foot_compensation": "0.15",
    "from": "system",
    "gap_infill_speed": "300",
    "inherits": "fdm_process_pply_common",
    "initial_layer_infill_speed": "105",
    "initial_layer_speed": "100",
    "inner_wall_speed": "300",
    "instantiation": "false",
    "internal_solid_infill_speed": "300",
    "name": "fdm_process_pply_0.20",
    "outer_wall_speed": "200",
    "sparse_infill_speed": "300",
    "top_shell_thickness": "0.6",
    "type": "process"
  },
  "process/fdm_process_pply_0.24.json": {
    "bridge_flow": "1",
    "elefant_foot_compensation": "0.15",
    "from": "system",
    "gap_infill_speed": "230",
    "inherits": "fdm_process_pply_common",
    "initial_layer_infill_speed": "105",
    "initial_layer_speed": "50",
    "inner_wall_speed": "200",
    "instantiation": "false",
    "internal_solid_infill_speed": "230",
    "layer_height": "0.24",
    "name": "fdm_process_pply_0.24",
    "outer_wall_speed": "180",
    "sparse_infill_speed": "230",
    "support_threshold_angle": "35",
    "top_shell_thickness": "0.6",
    "top_surface_line_width": "0.45",
    "type": "process"
  },
  "process/fdm_process_pply_0.28.json": {
    "bridge_flow": "1",
    "elefant_foot_compensation": "0.15",
    "from": "system",
    "gap_infill_speed": "200",
    "inherits": "fdm_process_pply_common",
    "initial_layer_infill_speed": "105",
    "initial_layer_speed": "50",
    "inner_wall_speed": "180",
    "instantiation": "false",
    "internal_solid_infill_speed": "200",
    "layer_height": "0.28",
    "name": "fdm_process_pply_0.28",
    "outer_wall_speed": "150",
    "sparse_infill_speed": "200",
    "support_threshold_angle": "40",
    "top_shell_thickness": "0.6",
    "top_surface_line_width": "0.45",
    "type": "process"
  },
  "process/fdm_process_pply_0.30_nozzle_0.6.json": {
    "bridge_flow": "1",
    "elefant_foot_compensation": "0.15",
    "from": "system",
    "gap_infill_speed": "200",
    "inherits": "fdm_process_pply_common",
    "initial_layer_infill_speed": "105",
    "initial_layer_line_width": "0.6",
    "initial_layer_speed": "100",
    "inner_wall_line_width": "0.6",
    "inner_wall_speed": "180",
    "instantiation": "false",
    "internal_solid_infill_line_width": "0.6",
    "internal_solid_infill_speed": "200",
    "layer_height": "0.30",
    "line_width": "0.6",
    "name": "fdm_process_pply_0.30_nozzle_0.6",
    "outer_wall_line_width": "0.6",
    "outer_wall_speed": "120",
    "sparse_infill_line_width": "0.6",
    "sparse_infill_speed": "180",
    "support_line_width": "0.6",
    "top_shell_thickness": "0.6",
    "top_surface_line_width": "0.45",
    "type": "process"
  },
  "process/fdm_process_pply_0.40_nozzle_0.8.json": {
    "bridge_flow": "1",
    "bridge_speed": "30",
    "from": "system",
    "inherits": "fdm_process_pply_common",
    "initial_layer_infill_speed": "80",
    "initial_layer_line_width": "0.82",
    "initial_layer_print_height": "0.4",
    "initial_layer_speed": "45",
    "inner_wall_line_width": "0.82",
    "instantiation": "false",
    "internal_solid_infill_line_width": "0.82",
    "layer_height": "0.4",
    "line_width": "0.82",
    "name": "fdm_process_pply_0.40_nozzle_0.8",
    "outer_wall_line_width": "0.82",
    "overhang_3_4_speed": "25",
    "overhang_4_4_speed": "5",
    "sparse_infill_line_width": "0.82",
    "sparse_infill_speed": "150",
    "support_line_width": "0.82",
    "top_surface_line_width": "0.82",
    "top_surface_pattern": "monotonic",
    "top_surface_speed": "180",
    "type": "process"
  },
  "process/fdm_process_pply_common.json": {
    "bottom_shell_layers": "3",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_speed": "50",
    "brim_object_gap": "0.1",
    "compatible_printers": [
      "Peopoly Magneto X 0.4 nozzle",
      "Peopoly Magneto X 0.6 nozzle",
      "Peopoly Magneto X 0.8 nozzle"
    ],
    "compatible_printers_condition": "",
    "detect_overhang_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "1",
    "filename_format": "{input_filename_base}_{filament_type[0]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "150",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "500",
    "initial_layer_infill_speed": "60",
    "initial_layer_line_width": "0.5",
    "initial_layer_speed": "80",
    "inner_wall_speed": "150",
    "instantiation": "false",
    "internal_bridge_support_thickness": "0.8",
    "internal_solid_infill_line_width": "0.42",
    "internal_solid_infill_speed": "150",
    "ironing_flow": "10%",
    "ironing_spacing": "0.15",
    "ironing_speed": "30",
    "ironing_type": "no ironing",
    "layer_height": "0.2",
    "line_width": "0.42",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "15",
    "name": "fdm_process_pply_common",
    "only_one_wall_top": "0",
    "outer_wall_acceleration": "5000",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "50",
    "overhang_3_4_speed": "30",
    "overhang_4_4_speed": "10",
    "prime_tower_width": "35",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "seam_position": "aligned",
    "skirt_height": "1",
    "skirt_loops": "0",
    "sparse_infill_speed": "250",
    "support_base_pattern_spacing": "2.5",
    "support_bottom_z_distance": "0.2",
    "support_expansion": "0",
    "support_interface_bottom_layers": "2",
    "support_interface_spacing": "0.5",
    "support_object_xy_distance": "0.35",
    "support_speed": "150",
    "support_style": "default",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.2",
    "support_type": "normal(auto)",
    "top_shell_layers": "3",
    "top_shell_thickness": "0.8",
    "top_surface_acceleration": "2000",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "200",
    "travel_speed": "500",
    "tree_support_branch_angle": "45",
    "tree_support_branch_diameter": "2",
    "tree_support_wall_count": "1",
    "type": "process",
    "wall_generator": "classic",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wipe_tower_no_sparse_layers": "0"
  }
}

FILAMENT = {
  "filament/Peopoly Generic ABS.json": {
    "compatible_printers": [
      "Peopoly Magneto X 0.4 nozzle",
      "Peopoly Magneto X 0.6 nozzle",
      "Peopoly Magneto X 0.8 nozzle"
    ],
    "enable_pressure_advance": [
      "1"
    ],
    "filament_flow_ratio": [
      "0.93"
    ],
    "filament_id": "GFSL99",
    "filament_type": [
      "ABS"
    ],
    "from": "system",
    "inherits": "fdm_filament_abs",
    "instantiation": "true",
    "name": "Peopoly Generic ABS",
    "pressure_advance": [
      "0.02"
    ],
    "type": "filament"
  },
  "filament/Peopoly Generic PETG.json": {
    "compatible_printers": [
      "Peopoly Magneto X 0.4 nozzle",
      "Peopoly Magneto X 0.6 nozzle",
      "Peopoly Magneto X 0.8 nozzle"
    ],
    "fan_max_speed": [
      "40"
    ],
    "filament_flow_ratio": [
      "0.92"
    ],
    "filament_id": "GFPETG-1",
    "filament_max_volumetric_speed": [
      "20"
    ],
    "filament_type": [
      "PETG"
    ],
    "from": "system",
    "hot_plate_temp": [
      "70"
    ],
    "hot_plate_temp_initial_layer": [
      "70"
    ],
    "inherits": "fdm_filament_petg",
    "instantiation": "true",
    "name": "Peopoly Generic PETG",
    "nozzle_temperature": [
      "235"
    ],
    "nozzle_temperature_initial_layer": [
      "245"
    ],
    "setting_id": "GSPETG-1",
    "slow_down_layer_time": [
      "8"
    ],
    "type": "filament"
  },
  "filament/Peopoly Generic PLA.json": {
    "compatible_printers": [
      "Peopoly Magneto X 0.4 nozzle",
      "Peopoly Magneto X 0.6 nozzle",
      "Peopoly Magneto X 0.8 nozzle"
    ],
    "enable_pressure_advance": [
      "1"
    ],
    "fan_max_speed": [
      "60"
    ],
    "filament_flow_ratio": [
      "0.92"
    ],
    "filament_id": "GFL99",
    "filament_max_volumetric_speed": [
      "18"
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
    "inherits": "fdm_filament_pla",
    "instantiation": "true",
    "name": "Peopoly Generic PLA",
    "nozzle_temperature": [
      "220"
    ],
    "nozzle_temperature_initial_layer": [
      "225"
    ],
    "pressure_advance": [
      "0.02"
    ],
    "setting_id": "GFSL99",
    "slow_down_layer_time": [
      "8"
    ],
    "type": "filament"
  },
  "filament/Peopoly Lancer ABS-GF.json": {
    "compatible_printers": [
      "Peopoly Magneto X 0.4 nozzle",
      "Peopoly Magneto X 0.6 nozzle",
      "Peopoly Magneto X 0.8 nozzle"
    ],
    "enable_pressure_advance": [
      "1"
    ],
    "fan_max_speed": [
      "40"
    ],
    "filament_deretraction_speed": [
      "60"
    ],
    "filament_flow_ratio": [
      "0.91"
    ],
    "filament_id": "GFL99",
    "filament_max_volumetric_speed": [
      "35"
    ],
    "filament_retraction_length": [
      "0.8"
    ],
    "filament_retraction_speed": [
      "60"
    ],
    "filament_type": [
      "ABS"
    ],
    "filament_vendor": [
      "Peopoly"
    ],
    "filament_wipe": [
      "1"
    ],
    "filament_wipe_distance": [
      "1"
    ],
    "from": "system",
    "hot_plate_temp": [
      "100"
    ],
    "hot_plate_temp_initial_layer": [
      "90"
    ],
    "inherits": "fdm_filament_abs",
    "instantiation": "true",
    "name": "Peopoly Lancer ABS-GF",
    "nozzle_temperature": [
      "270"
    ],
    "nozzle_temperature_initial_layer": [
      "260"
    ],
    "overhang_fan_speed": [
      "30"
    ],
    "pressure_advance": [
      "0.016"
    ],
    "reduce_fan_stop_start_freq": [
      "0"
    ],
    "setting_id": "GFSL99",
    "slow_down_layer_time": [
      "6"
    ],
    "type": "filament"
  },
  "filament/Peopoly Lancer PET-CF.json": {
    "compatible_printers": [
      "Peopoly Magneto X 0.4 nozzle",
      "Peopoly Magneto X 0.6 nozzle",
      "Peopoly Magneto X 0.8 nozzle"
    ],
    "enable_pressure_advance": [
      "1"
    ],
    "fan_max_speed": [
      "40"
    ],
    "filament_density": [
      "1.3"
    ],
    "filament_deretraction_speed": [
      "60"
    ],
    "filament_flow_ratio": [
      "0.90"
    ],
    "filament_id": "GFL99",
    "filament_max_volumetric_speed": [
      "35"
    ],
    "filament_retraction_length": [
      "0.8"
    ],
    "filament_retraction_speed": [
      "60"
    ],
    "filament_type": [
      "PET-CF"
    ],
    "filament_vendor": [
      "Peopoly"
    ],
    "filament_wipe": [
      "1"
    ],
    "filament_wipe_distance": [
      "1"
    ],
    "from": "system",
    "hot_plate_temp": [
      "80"
    ],
    "hot_plate_temp_initial_layer": [
      "70"
    ],
    "inherits": "fdm_filament_abs",
    "instantiation": "true",
    "name": "Peopoly Lancer PET-CF",
    "nozzle_temperature": [
      "300"
    ],
    "nozzle_temperature_initial_layer": [
      "280"
    ],
    "overhang_fan_speed": [
      "30"
    ],
    "pressure_advance": [
      "0.005"
    ],
    "reduce_fan_stop_start_freq": [
      "0"
    ],
    "setting_id": "GFSL99",
    "slow_down_layer_time": [
      "8"
    ],
    "type": "filament"
  },
  "filament/Peopoly Lancer PETG-C.json": {
    "compatible_printers": [
      "Peopoly Magneto X 0.4 nozzle",
      "Peopoly Magneto X 0.6 nozzle",
      "Peopoly Magneto X 0.8 nozzle"
    ],
    "enable_pressure_advance": [
      "1"
    ],
    "fan_cooling_layer_time": [
      "20"
    ],
    "fan_max_speed": [
      "40"
    ],
    "fan_min_speed": [
      "5"
    ],
    "filament_flow_ratio": [
      "0.90"
    ],
    "filament_id": "GFL99",
    "filament_max_volumetric_speed": [
      "32"
    ],
    "filament_vendor": [
      "Peopoly"
    ],
    "from": "system",
    "inherits": "fdm_filament_petg",
    "instantiation": "true",
    "name": "Peopoly Lancer PETG-C",
    "nozzle_temperature": [
      "225"
    ],
    "nozzle_temperature_initial_layer": [
      "235"
    ],
    "overhang_fan_speed": [
      "100"
    ],
    "pressure_advance": [
      "0.04"
    ],
    "setting_id": "GFSL99",
    "type": "filament"
  },
  "filament/Peopoly Lancer PLA-C.json": {
    "compatible_printers": [
      "Peopoly Magneto X 0.4 nozzle",
      "Peopoly Magneto X 0.6 nozzle",
      "Peopoly Magneto X 0.8 nozzle"
    ],
    "enable_pressure_advance": [
      "1"
    ],
    "fan_max_speed": [
      "50"
    ],
    "filament_flow_ratio": [
      "0.92"
    ],
    "filament_id": "GFL99",
    "filament_max_volumetric_speed": [
      "35"
    ],
    "filament_type": [
      "PLA"
    ],
    "filament_vendor": [
      "Peopoly"
    ],
    "from": "system",
    "hot_plate_temp": [
      "70"
    ],
    "hot_plate_temp_initial_layer": [
      "70"
    ],
    "inherits": "fdm_filament_pla",
    "instantiation": "true",
    "name": "Peopoly Lancer PLA-C",
    "nozzle_temperature": [
      "210"
    ],
    "nozzle_temperature_initial_layer": [
      "215"
    ],
    "pressure_advance": [
      "0.03"
    ],
    "setting_id": "GFSL99",
    "slow_down_layer_time": [
      "6"
    ],
    "type": "filament"
  },
  "filament/fdm_filament_abs.json": {
    "activate_air_filtration": [
      "1"
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
      "22"
    ],
    "filament_type": [
      "ABS"
    ],
    "from": "system",
    "hot_plate_temp": [
      "90"
    ],
    "hot_plate_temp_initial_layer": [
      "90"
    ],
    "inherits": "fdm_filament_common",
    "instantiation": "false",
    "name": "fdm_filament_abs",
    "nozzle_temperature": [
      "270"
    ],
    "nozzle_temperature_initial_layer": [
      "275"
    ],
    "nozzle_temperature_range_high": [
      "280"
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
    "slow_down_layer_time": [
      "3"
    ],
    "slow_down_min_speed": [
      "20"
    ],
    "textured_plate_temp": [
      "90"
    ],
    "textured_plate_temp_initial_layer": [
      "90"
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
  "filament/fdm_filament_petg.json": {
    "eng_plate_temp": [
      "0"
    ],
    "eng_plate_temp_initial_layer": [
      "0"
    ],
    "fan_cooling_layer_time": [
      "20"
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
      "18"
    ],
    "filament_start_gcode": [
      "; filament start gcode\n{if (bed_temperature[current_extruder] >45)||(bed_temperature_initial_layer[current_extruder] >45)}M106 P3 S180\n{elsif (bed_temperature[current_extruder] >50)||(bed_temperature_initial_layer[current_extruder] >50)}M106 P3 S255\n{endif};Prevent PLA from jamming\n\n{if activate_air_filtration[current_extruder] && support_air_filtration}\nM106 P3 S{during_print_exhaust_fan_speed_num[current_extruder]} \n{endif}"
    ],
    "filament_type": [
      "PETG"
    ],
    "from": "system",
    "hot_plate_temp": [
      "70"
    ],
    "hot_plate_temp_initial_layer": [
      "70"
    ],
    "inherits": "fdm_filament_common",
    "instantiation": "false",
    "name": "fdm_filament_petg",
    "nozzle_temperature": [
      "260"
    ],
    "nozzle_temperature_initial_layer": [
      "270"
    ],
    "nozzle_temperature_range_high": [
      "280"
    ],
    "nozzle_temperature_range_low": [
      "220"
    ],
    "reduce_fan_stop_start_freq": [
      "1"
    ],
    "temperature_vitrification": [
      "70"
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
      "15"
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
      "225"
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
  "magnetox_model-400x300.stl",
  "magnetox_model-back.stl",
  "magnetox_model.stl",
  "magnetox_model_texture-400x300.png",
  "magnetox_model_texture.png",
  "Peopoly Magneto X_cover.png"
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
