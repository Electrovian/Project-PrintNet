from __future__ import annotations

VENDOR = "Comgrow"
INDEX = {
  "description": "Comgrow configurations",
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
      "name": "fdm_filament_pet",
      "sub_path": "filament/fdm_filament_pet.json"
    },
    {
      "name": "fdm_filament_pla",
      "sub_path": "filament/fdm_filament_pla.json"
    },
    {
      "name": "Comgrow Generic ABS",
      "sub_path": "filament/Comgrow Generic ABS.json"
    },
    {
      "name": "Comgrow Generic PETG",
      "sub_path": "filament/Comgrow Generic PETG.json"
    },
    {
      "name": "Comgrow Generic PLA",
      "sub_path": "filament/Comgrow Generic PLA.json"
    },
    {
      "name": "Comgrow T300 PLA",
      "sub_path": "filament/Comgrow T300 PLA.json"
    }
  ],
  "force_update": "0",
  "machine_list": [
    {
      "name": "fdm_machine_common",
      "sub_path": "machine/fdm_machine_common.json"
    },
    {
      "name": "fdm_comgrow_common",
      "sub_path": "machine/fdm_comgrow_common.json"
    },
    {
      "name": "Comgrow T300 0.4 nozzle",
      "sub_path": "machine/Comgrow T300 0.4 nozzle.json"
    },
    {
      "name": "Comgrow T500 0.4 nozzle",
      "sub_path": "machine/Comgrow T500 0.4 nozzle.json"
    },
    {
      "name": "Comgrow T500 0.6 nozzle",
      "sub_path": "machine/Comgrow T500 0.6 nozzle.json"
    },
    {
      "name": "Comgrow T500 0.8 nozzle",
      "sub_path": "machine/Comgrow T500 0.8 nozzle.json"
    }
  ],
  "machine_model_list": [
    {
      "name": "Comgrow T300",
      "sub_path": "machine/Comgrow T300.json"
    },
    {
      "name": "Comgrow T500",
      "sub_path": "machine/Comgrow T500.json"
    }
  ],
  "name": "Comgrow",
  "process_list": [
    {
      "name": "fdm_process_common",
      "sub_path": "process/fdm_process_common.json"
    },
    {
      "name": "0.18mm Optimal @Comgrow T500",
      "sub_path": "process/0.18mm Optimal @Comgrow T500.json"
    },
    {
      "name": "0.20mm Standard @Comgrow T500",
      "sub_path": "process/0.20mm Standard @Comgrow T500.json"
    },
    {
      "name": "fdm_process_comgrow_common",
      "sub_path": "process/fdm_process_comgrow_common.json"
    },
    {
      "name": "0.16mm Opitmal @Comgrow T500 0.6",
      "sub_path": "process/0.16mm Opitmal @Comgrow T500 0.6.json"
    },
    {
      "name": "0.16mm Optimal @Comgrow T500 0.4",
      "sub_path": "process/0.16mm Optimal @Comgrow T500 0.4.json"
    },
    {
      "name": "0.20mm Optimal @Comgrow T300 0.4 - official",
      "sub_path": "process/0.20mm Optimal @Comgrow T300 0.4 - official.json"
    },
    {
      "name": "0.20mm Standard @Comgrow T500 0.4",
      "sub_path": "process/0.20mm Standard @Comgrow T500 0.4.json"
    },
    {
      "name": "0.20mm Standard @Comgrow T500 0.6",
      "sub_path": "process/0.20mm Standard @Comgrow T500 0.6.json"
    },
    {
      "name": "0.20mm Standard @Comgrow T500 1.0",
      "sub_path": "process/0.20mm Standard @Comgrow T500 1.0.json"
    },
    {
      "name": "0.24mm Draft @Comgrow T500 0.4",
      "sub_path": "process/0.24mm Draft @Comgrow T500 0.4.json"
    },
    {
      "name": "0.24mm Draft @Comgrow T500 0.6",
      "sub_path": "process/0.24mm Draft @Comgrow T500 0.6.json"
    },
    {
      "name": "0.24mm Optimal @Comgrow T500 0.8",
      "sub_path": "process/0.24mm Optimal @Comgrow T500 0.8.json"
    },
    {
      "name": "0.28mm SuperDraft @Comgrow T500 0.4",
      "sub_path": "process/0.28mm SuperDraft @Comgrow T500 0.4.json"
    },
    {
      "name": "0.28mm SuperDraft @Comgrow T500 0.6",
      "sub_path": "process/0.28mm SuperDraft @Comgrow T500 0.6.json"
    },
    {
      "name": "0.32mm Standard @Comgrow T500 0.8",
      "sub_path": "process/0.32mm Standard @Comgrow T500 0.8.json"
    },
    {
      "name": "0.40mm Draft @Comgrow T500 0.8",
      "sub_path": "process/0.40mm Draft @Comgrow T500 0.8.json"
    },
    {
      "name": "0.48mm Draft @Comgrow T500 0.8",
      "sub_path": "process/0.48mm Draft @Comgrow T500 0.8.json"
    },
    {
      "name": "0.56mm SuperChunky @Comgrow T500 0.8",
      "sub_path": "process/0.56mm SuperDraft @Comgrow T500 0.8.json"
    }
  ],
  "version": "02.03.01.10"
}

MACHINE = {
  "machine/Comgrow T300 0.4 nozzle.json": {
    "before_layer_change_gcode": "",
    "deretraction_speed": [
      "50"
    ],
    "from": "system",
    "inherits": "fdm_comgrow_common",
    "instantiation": "true",
    "machine_end_gcode": "END_PRINT\n",
    "machine_max_acceleration_e": [
      "5000"
    ],
    "machine_max_acceleration_extruding": [
      "20000"
    ],
    "machine_max_acceleration_retracting": [
      "5000"
    ],
    "machine_max_acceleration_x": [
      "12000"
    ],
    "machine_max_acceleration_y": [
      "12000"
    ],
    "machine_max_acceleration_z": [
      "500"
    ],
    "machine_max_jerk_e": [
      "3"
    ],
    "machine_max_jerk_x": [
      "9"
    ],
    "machine_max_jerk_y": [
      "9"
    ],
    "machine_max_jerk_z": [
      "0.25"
    ],
    "machine_max_speed_e": [
      "50"
    ],
    "machine_max_speed_x": [
      "500"
    ],
    "machine_max_speed_y": [
      "500"
    ],
    "machine_max_speed_z": [
      "20"
    ],
    "machine_start_gcode": "G28\nG90\nG1 X0 F3000\nG1 Z0.300 F600\nG1 Y0 F3000\nG91 \nG1 X-2 Y-6 F3000\nSTART_PRINT\nM400\nG90\nM83\nG90\nG1 X0 F3000\nG1 Z0.300 F600\nG1 Y0 F3000\nG91 \nG1 X-2 Y-6 F3000\nM140 S[bed_temperature_initial_layer_single] ;set bed temp\nM104 S[nozzle_temperature_initial_layer] ;set extruder temp\nM190 S[bed_temperature_initial_layer_single] ;wait for bed temp\nM109 S[nozzle_temperature_initial_layer];wait for extruder temp\nG1 E25 F480\nG4 P1000\nG1 E-0.200 Z5 F600\nG1 X90.000 F6000\nG1 Z-5.200 F600\nG1 X60.000 E14.4 F3000\nG1 X60.000 E9.6 F3000\nG1 Y1 E0.16 F3000\nG1 X-60.000 E9.6 F3000\nG1 X-60.000 E14.4 F3000\nG1 Y1 E0.16 F3000\nG1 X60.000 E14.4 F3000\nG1 X60.000 E9.6 F3000\nG1 E-0.100 Z0.5 F600\nM400\n\n",
    "max_layer_height": [
      "0.32"
    ],
    "name": "Comgrow T300 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "printable_area": [
      "0x0",
      "300x0",
      "300x300",
      "0x300"
    ],
    "printable_height": "350",
    "printer_model": "Comgrow T300",
    "retract_lift_below": [
      "348"
    ],
    "retraction_length": [
      "0.8"
    ],
    "retraction_speed": [
      "50"
    ],
    "setting_id": "GM001",
    "thumbnails": [
      "64x64",
      "160x160",
      "176x176"
    ],
    "thumbnails_format": "JPG",
    "type": "machine",
    "z_hop": [
      "0.4"
    ]
  },
  "machine/Comgrow T300.json": {
    "bed_model": "comgrow_t300_buildplate_model.stl",
    "bed_texture": "comgrow_t300_buildplate_texture.png",
    "default_materials": "Comgrow T300 PLA",
    "family": "Comgrow",
    "hotend_model": "",
    "machine_tech": "FFF",
    "model_id": "Comgrow_T300",
    "name": "Comgrow T300",
    "nozzle_diameter": "0.4",
    "type": "machine_model"
  },
  "machine/Comgrow T500 0.4 nozzle.json": {
    "from": "system",
    "inherits": "fdm_comgrow_common",
    "instantiation": "true",
    "name": "Comgrow T500 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "printable_area": [
      "0x0",
      "500x0",
      "500x500",
      "0x500"
    ],
    "printable_height": "500",
    "printer_model": "Comgrow T500",
    "setting_id": "GM001",
    "type": "machine"
  },
  "machine/Comgrow T500 0.6 nozzle.json": {
    "from": "system",
    "inherits": "fdm_comgrow_common",
    "instantiation": "true",
    "name": "Comgrow T500 0.6 nozzle",
    "nozzle_diameter": [
      "0.6"
    ],
    "printable_area": [
      "0x0",
      "500x0",
      "500x500",
      "0x500"
    ],
    "printable_height": "500",
    "printer_model": "Comgrow T500",
    "printer_variant": "0.6",
    "retraction_length": [
      "1.0"
    ],
    "setting_id": "GM002",
    "type": "machine"
  },
  "machine/Comgrow T500 0.8 nozzle.json": {
    "from": "system",
    "inherits": "fdm_comgrow_common",
    "instantiation": "true",
    "name": "Comgrow T500 0.8 nozzle",
    "nozzle_diameter": [
      "0.8"
    ],
    "printable_area": [
      "0x0",
      "500x0",
      "500x500",
      "0x500"
    ],
    "printable_height": "500",
    "printer_model": "Comgrow T500",
    "printer_variant": "0.8",
    "retraction_length": [
      "1.0"
    ],
    "setting_id": "GM003",
    "type": "machine"
  },
  "machine/Comgrow T500.json": {
    "bed_model": "comgrow_t500_buildplate_model.stl",
    "bed_texture": "comgrow_t500_buildplate_texture.png",
    "default_materials": "Comgrow Generic PLA;Comgrow Generic PETG;Comgrow Generic ABS",
    "family": "Comgrow",
    "hotend_model": "",
    "machine_tech": "FFF",
    "model_id": "Comgrow_T500",
    "name": "Comgrow T500",
    "nozzle_diameter": "0.4;0.6;0.8",
    "type": "machine_model"
  },
  "machine/fdm_comgrow_common.json": {
    "auxiliary_fan": "0",
    "bed_exclude_area": [
      "0x0"
    ],
    "before_layer_change_gcode": ";BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n",
    "change_filament_gcode": "PAUSE",
    "default_filament_profile": [
      "Comgrow Generic PETG"
    ],
    "default_print_profile": "0.20mm Standard @Comgrow T500",
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
    "machine_end_gcode": "{if max_layer_z < printable_height}G1 Z{z_offset+min(max_layer_z+2, printable_height)} F600 ; Move print head up{endif}\nG1 X5 Y{print_bed_max[1]*0.8} F{travel_speed*60} ; present print\n{if max_layer_z < printable_height-10}G1 Z{z_offset+min(max_layer_z+70, printable_height-10)} F600 ; Move print head further up{endif}\n{if max_layer_z < max_print_height*0.6}G1 Z{printable_height*0.6} F600 ; Move print head further up{endif}\nM140 S0 ; turn off heatbed\nM104 S0 ; turn off temperature\nM107 ; turn off fan\nM84 X Y E ; disable motors",
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
    "machine_pause_gcode": "PAUSE",
    "machine_start_gcode": "G90 ; use absolute coordinates\nM83 ; extruder relative mode\nG28 ; home all\nM104 S[nozzle_temperature_initial_layer] ; set extruder temp\nM140 S[bed_temperature_initial_layer_single] ; set bed temp\nM190 S[bed_temperature_initial_layer_single] ; wait for bed temp\nM109 S[nozzle_temperature_initial_layer] ; wait for extruder temp\nG1 Z2 F240\nG1 X2 Y10 F3000\nG1 Z0.28 F240\nG92 E0\nG1 Y190 E15 F1500 ; intro line\nG1 X2.3 F5000\nG92 E0\nG1 Y10 E15 F1200 ; intro line\nG92 E0",
    "max_layer_height": [
      "0.56"
    ],
    "min_layer_height": [
      "0.08"
    ],
    "name": "fdm_comgrow_common",
    "nozzle_type": "hardened_steel",
    "printable_height": "500",
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
      "0.5"
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
    "thumbnails": [
      "32x32",
      "300x300"
    ],
    "thumbnails_format": "PNG",
    "type": "machine",
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
      "500"
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
  "process/0.16mm Opitmal @Comgrow T500 0.6.json": {
    "adaptive_layer_height": "1",
    "bottom_shell_layers": "2",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.85",
    "bridge_no_support": "0",
    "bridge_speed": "25",
    "brim_object_gap": "0",
    "brim_width": "0",
    "compatible_printers": [
      "Comgrow T500 0.6 nozzle"
    ],
    "compatible_printers_condition": "",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "from": "system",
    "gap_infill_speed": "60",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "23%",
    "inherits": "fdm_process_comgrow_common",
    "initial_layer_infill_speed": "60",
    "initial_layer_line_width": "0.6",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "45",
    "inner_wall_line_width": "0.6",
    "inner_wall_speed": "140",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0",
    "internal_solid_infill_speed": "120",
    "ironing_flow": "15%",
    "ironing_spacing": "0.25",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.16",
    "line_width": "0.6",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.16mm Opitmal @Comgrow T500 0.6",
    "outer_wall_line_width": "0.6",
    "outer_wall_speed": "120",
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
    "seam_gap": "5%",
    "seam_position": "aligned",
    "setting_id": "GP004",
    "skirt_distance": "3",
    "skirt_height": "2",
    "skirt_loops": "2",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.6",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "150",
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
    "support_line_width": "0.6",
    "support_object_xy_distance": "60%",
    "support_on_build_plate_only": "0",
    "support_speed": "120",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.15",
    "support_type": "normal(auto)",
    "top_shell_layers": "2",
    "top_shell_thickness": "0.8",
    "top_surface_line_width": "0.6",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "30",
    "travel_speed": "170",
    "tree_support_branch_angle": "40",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "2",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/0.16mm Optimal @Comgrow T500 0.4.json": {
    "adaptive_layer_height": "1",
    "bottom_shell_layers": "2",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.85",
    "bridge_no_support": "0",
    "bridge_speed": "25",
    "brim_object_gap": "0",
    "brim_width": "0",
    "compatible_printers": [
      "Comgrow T500 0.4 nozzle"
    ],
    "compatible_printers_condition": "",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "from": "system",
    "gap_infill_speed": "70",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "23%",
    "inherits": "fdm_process_comgrow_common",
    "initial_layer_infill_speed": "60",
    "initial_layer_line_width": "0.4",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "40",
    "inner_wall_line_width": "0.4",
    "inner_wall_speed": "160",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0",
    "internal_solid_infill_speed": "200",
    "ironing_flow": "15%",
    "ironing_spacing": "0.25",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.16",
    "line_width": "0.4",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.16mm Optimal @Comgrow T500 0.4",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "140",
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
    "seam_gap": "5%",
    "seam_position": "aligned",
    "setting_id": "GP004",
    "skirt_distance": "3",
    "skirt_height": "2",
    "skirt_loops": "2",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.4",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "200",
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
    "support_object_xy_distance": "60%",
    "support_on_build_plate_only": "0",
    "support_speed": "140",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.15",
    "support_type": "normal(auto)",
    "top_shell_layers": "2",
    "top_shell_thickness": "0.8",
    "top_surface_line_width": "0.4",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "40",
    "travel_speed": "200",
    "tree_support_branch_angle": "40",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "2",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/0.18mm Optimal @Comgrow T500.json": {
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
      "Comgrow T500 0.4 nozzle"
    ],
    "compatible_printers_condition": "",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "from": "system",
    "gap_infill_speed": "30",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "23%",
    "inherits": "fdm_process_common",
    "initial_layer_infill_speed": "35%",
    "initial_layer_line_width": "0.42",
    "initial_layer_print_height": "0.24",
    "initial_layer_speed": "35%",
    "inner_wall_line_width": "0.45",
    "inner_wall_speed": "40",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0",
    "internal_solid_infill_speed": "40",
    "ironing_flow": "15%",
    "ironing_spacing": "0.25",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.18",
    "line_width": "0.44",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.18mm Optimal @Comgrow T500",
    "outer_wall_line_width": "0.42",
    "outer_wall_speed": "25",
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
    "skirt_height": "2",
    "skirt_loops": "2",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.44",
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
    "top_surface_line_width": "0.38",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "30",
    "travel_speed": "150",
    "tree_support_branch_angle": "40",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "3",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/0.20mm Optimal @Comgrow T300 0.4 - official.json": {
    "accel_to_decel_enable": "0",
    "accel_to_decel_factor": "30%",
    "adaptive_layer_height": "1",
    "bottom_shell_layers": "3",
    "bottom_shell_thickness": "0",
    "bottom_solid_infill_flow_ratio": "1.25",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.95",
    "bridge_no_support": "0",
    "bridge_speed": "50",
    "brim_object_gap": "0",
    "brim_type": "outer_only",
    "brim_width": "5",
    "compatible_printers": [
      "Comgrow T300 0.4 nozzle"
    ],
    "compatible_printers_condition": "",
    "default_acceleration": "8000",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "exclude_object": "1",
    "from": "system",
    "gap_infill_speed": "150",
    "gcode_label_objects": "1",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "25%",
    "inherits": "fdm_process_comgrow_common",
    "initial_layer_acceleration": "5000",
    "initial_layer_infill_speed": "60",
    "initial_layer_line_width": "0.5",
    "initial_layer_print_height": "0.3",
    "initial_layer_speed": "30",
    "initial_layer_travel_speed": "60%",
    "inner_wall_acceleration": "6000",
    "inner_wall_line_width": "0.45",
    "inner_wall_speed": "300",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_bridge_speed": "50",
    "internal_solid_infill_line_width": "0.45",
    "internal_solid_infill_speed": "180",
    "ironing_flow": "15%",
    "ironing_spacing": "0.25",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.2",
    "line_width": "0.42",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.20mm Optimal @Comgrow T300 0.4 - official",
    "outer_wall_acceleration": "5000",
    "outer_wall_line_width": "0.42",
    "outer_wall_speed": "150",
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
    "seam_gap": "5%",
    "seam_position": "aligned",
    "setting_id": "GP004",
    "skirt_distance": "3",
    "skirt_height": "1",
    "skirt_loops": "1",
    "skirt_speed": "0",
    "slow_down_layers": "3",
    "sparse_infill_density": "10%",
    "sparse_infill_line_width": "0.5",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "300",
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
    "support_object_xy_distance": "60%",
    "support_on_build_plate_only": "0",
    "support_speed": "80",
    "support_style": "snug",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.15",
    "support_type": "tree(auto)",
    "top_shell_layers": "4",
    "top_shell_thickness": "0.8",
    "top_surface_acceleration": "6000",
    "top_surface_line_width": "0.45",
    "top_surface_pattern": "monotonic",
    "top_surface_speed": "180",
    "travel_acceleration": "8000",
    "travel_speed": "350",
    "tree_support_branch_angle": "40",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_generator": "classic",
    "wall_infill_order": "outer wall/inner wall/infill",
    "wall_loops": "2",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/0.20mm Standard @Comgrow T500 0.4.json": {
    "adaptive_layer_height": "1",
    "bottom_shell_layers": "2",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.85",
    "bridge_no_support": "0",
    "bridge_speed": "25",
    "brim_object_gap": "0",
    "brim_width": "0",
    "compatible_printers": [
      "Comgrow T500 0.4 nozzle"
    ],
    "compatible_printers_condition": "",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "from": "system",
    "gap_infill_speed": "70",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "23%",
    "inherits": "fdm_process_comgrow_common",
    "initial_layer_infill_speed": "60",
    "initial_layer_line_width": "0.4",
    "initial_layer_print_height": "0.24",
    "initial_layer_speed": "40",
    "inner_wall_line_width": "0.4",
    "inner_wall_speed": "160",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0",
    "internal_solid_infill_speed": "200",
    "ironing_flow": "15%",
    "ironing_spacing": "0.25",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.2",
    "line_width": "0.4",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.20mm Standard @Comgrow T500 0.4",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "140",
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
    "seam_gap": "5%",
    "seam_position": "aligned",
    "setting_id": "GP004",
    "skirt_distance": "3",
    "skirt_height": "2",
    "skirt_loops": "2",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.4",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "200",
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
    "support_object_xy_distance": "60%",
    "support_on_build_plate_only": "0",
    "support_speed": "140",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.15",
    "support_type": "normal(auto)",
    "top_shell_layers": "2",
    "top_shell_thickness": "0.8",
    "top_surface_line_width": "0.4",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "40",
    "travel_speed": "200",
    "tree_support_branch_angle": "40",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "2",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/0.20mm Standard @Comgrow T500 0.6.json": {
    "adaptive_layer_height": "1",
    "bottom_shell_layers": "2",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.85",
    "bridge_no_support": "0",
    "bridge_speed": "25",
    "brim_object_gap": "0",
    "brim_width": "0",
    "compatible_printers": [
      "Comgrow T500 0.6 nozzle"
    ],
    "compatible_printers_condition": "",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "from": "system",
    "gap_infill_speed": "60",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "23%",
    "inherits": "fdm_process_comgrow_common",
    "initial_layer_infill_speed": "60",
    "initial_layer_line_width": "0.6",
    "initial_layer_print_height": "0.24",
    "initial_layer_speed": "45",
    "inner_wall_line_width": "0.6",
    "inner_wall_speed": "140",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0",
    "internal_solid_infill_speed": "120",
    "ironing_flow": "15%",
    "ironing_spacing": "0.25",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.20",
    "line_width": "0.6",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.20mm Standard @Comgrow T500 0.6",
    "outer_wall_line_width": "0.6",
    "outer_wall_speed": "120",
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
    "seam_gap": "5%",
    "seam_position": "aligned",
    "setting_id": "GP004",
    "skirt_distance": "3",
    "skirt_height": "2",
    "skirt_loops": "2",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.6",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "150",
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
    "support_line_width": "0.6",
    "support_object_xy_distance": "60%",
    "support_on_build_plate_only": "0",
    "support_speed": "120",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.15",
    "support_type": "normal(auto)",
    "top_shell_layers": "2",
    "top_shell_thickness": "0.8",
    "top_surface_line_width": "0.6",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "30",
    "travel_speed": "170",
    "tree_support_branch_angle": "40",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "2",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/0.20mm Standard @Comgrow T500 1.0.json": {
    "adaptive_layer_height": "1",
    "bottom_shell_layers": "2",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.85",
    "bridge_no_support": "0",
    "bridge_speed": "25",
    "brim_object_gap": "0",
    "brim_width": "0",
    "compatible_printers": [
      "Comgrow T500 1.0 nozzle"
    ],
    "compatible_printers_condition": "",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "from": "system",
    "gap_infill_speed": "60",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "23%",
    "inherits": "fdm_process_comgrow_common",
    "initial_layer_infill_speed": "80",
    "initial_layer_line_width": "1.0",
    "initial_layer_print_height": "0.28",
    "initial_layer_speed": "25",
    "inner_wall_line_width": "1.0",
    "inner_wall_speed": "60",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0",
    "internal_solid_infill_speed": "60",
    "ironing_flow": "15%",
    "ironing_spacing": "0.25",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.24",
    "line_width": "1.0",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.20mm Standard @Comgrow T500 1.0",
    "outer_wall_line_width": "1.0",
    "outer_wall_speed": "50",
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
    "seam_gap": "5%",
    "seam_position": "aligned",
    "setting_id": "GP004",
    "skirt_distance": "3",
    "skirt_height": "2",
    "skirt_loops": "2",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "1.0",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "50",
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
    "support_line_width": "1.0",
    "support_object_xy_distance": "60%",
    "support_on_build_plate_only": "0",
    "support_speed": "60",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.15",
    "support_type": "normal(auto)",
    "top_shell_layers": "2",
    "top_shell_thickness": "0.8",
    "top_surface_line_width": "1.0",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "40",
    "travel_speed": "80",
    "tree_support_branch_angle": "40",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "2",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/0.20mm Standard @Comgrow T500.json": {
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
      "Comgrow T500 0.4 nozzle"
    ],
    "compatible_printers_condition": "",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "from": "system",
    "gap_infill_speed": "30",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "23%",
    "inherits": "fdm_process_common",
    "initial_layer_infill_speed": "35%",
    "initial_layer_line_width": "0.42",
    "initial_layer_print_height": "0.24",
    "initial_layer_speed": "35%",
    "inner_wall_line_width": "0.45",
    "inner_wall_speed": "40",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0",
    "internal_solid_infill_speed": "40",
    "ironing_flow": "15%",
    "ironing_spacing": "0.25",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.20",
    "line_width": "0.44",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.20mm Standard @Comgrow T500",
    "outer_wall_line_width": "0.42",
    "outer_wall_speed": "25",
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
    "skirt_height": "2",
    "skirt_loops": "2",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.44",
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
    "support_top_z_distance": "0.18",
    "support_type": "normal(auto)",
    "top_shell_layers": "5",
    "top_shell_thickness": "0.8",
    "top_surface_line_width": "0.38",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "30",
    "travel_speed": "150",
    "tree_support_branch_angle": "40",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "3",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/0.24mm Draft @Comgrow T500 0.4.json": {
    "adaptive_layer_height": "1",
    "bottom_shell_layers": "2",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.85",
    "bridge_no_support": "0",
    "bridge_speed": "25",
    "brim_object_gap": "0",
    "brim_width": "0",
    "compatible_printers": [
      "Comgrow T500 0.4 nozzle"
    ],
    "compatible_printers_condition": "",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "from": "system",
    "gap_infill_speed": "70",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "23%",
    "inherits": "fdm_process_comgrow_common",
    "initial_layer_infill_speed": "60",
    "initial_layer_line_width": "0.4",
    "initial_layer_print_height": "0.28",
    "initial_layer_speed": "40",
    "inner_wall_line_width": "0.4",
    "inner_wall_speed": "160",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0",
    "internal_solid_infill_speed": "200",
    "ironing_flow": "15%",
    "ironing_spacing": "0.25",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.24",
    "line_width": "0.4",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.24mm Draft @Comgrow T500 0.4",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "140",
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
    "seam_gap": "5%",
    "seam_position": "aligned",
    "setting_id": "GP004",
    "skirt_distance": "3",
    "skirt_height": "2",
    "skirt_loops": "2",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.4",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "200",
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
    "support_object_xy_distance": "60%",
    "support_on_build_plate_only": "0",
    "support_speed": "140",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.15",
    "support_type": "normal(auto)",
    "top_shell_layers": "2",
    "top_shell_thickness": "0.8",
    "top_surface_line_width": "0.4",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "40",
    "travel_speed": "200",
    "tree_support_branch_angle": "40",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "2",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/0.24mm Draft @Comgrow T500 0.6.json": {
    "adaptive_layer_height": "1",
    "bottom_shell_layers": "2",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.85",
    "bridge_no_support": "0",
    "bridge_speed": "25",
    "brim_object_gap": "0",
    "brim_width": "0",
    "compatible_printers": [
      "Comgrow T500 0.6 nozzle"
    ],
    "compatible_printers_condition": "",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "from": "system",
    "gap_infill_speed": "60",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "23%",
    "inherits": "fdm_process_comgrow_common",
    "initial_layer_infill_speed": "60",
    "initial_layer_line_width": "0.6",
    "initial_layer_print_height": "0.28",
    "initial_layer_speed": "45",
    "inner_wall_line_width": "0.6",
    "inner_wall_speed": "140",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0",
    "internal_solid_infill_speed": "120",
    "ironing_flow": "15%",
    "ironing_spacing": "0.25",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.24",
    "line_width": "0.6",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.24mm Draft @Comgrow T500 0.6",
    "outer_wall_line_width": "0.6",
    "outer_wall_speed": "120",
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
    "seam_gap": "5%",
    "seam_position": "aligned",
    "setting_id": "GP004",
    "skirt_distance": "3",
    "skirt_height": "2",
    "skirt_loops": "2",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.6",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "150",
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
    "support_line_width": "0.6",
    "support_object_xy_distance": "60%",
    "support_on_build_plate_only": "0",
    "support_speed": "120",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.15",
    "support_type": "normal(auto)",
    "top_shell_layers": "2",
    "top_shell_thickness": "0.8",
    "top_surface_line_width": "0.6",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "30",
    "travel_speed": "170",
    "tree_support_branch_angle": "40",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "2",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/0.24mm Optimal @Comgrow T500 0.8.json": {
    "adaptive_layer_height": "1",
    "bottom_shell_layers": "2",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.85",
    "bridge_no_support": "0",
    "bridge_speed": "25",
    "brim_object_gap": "0",
    "brim_width": "0",
    "compatible_printers": [
      "Comgrow T500 0.8 nozzle"
    ],
    "compatible_printers_condition": "",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "from": "system",
    "gap_infill_speed": "60",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "23%",
    "inherits": "fdm_process_comgrow_common",
    "initial_layer_infill_speed": "50",
    "initial_layer_line_width": "0.8",
    "initial_layer_print_height": "0.28",
    "initial_layer_speed": "40",
    "inner_wall_line_width": "0.8",
    "inner_wall_speed": "90",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0",
    "internal_solid_infill_speed": "80",
    "ironing_flow": "15%",
    "ironing_spacing": "0.25",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.24",
    "line_width": "0.8",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.24mm Optimal @Comgrow T500 0.8",
    "outer_wall_line_width": "0.8",
    "outer_wall_speed": "70",
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
    "seam_gap": "5%",
    "seam_position": "aligned",
    "setting_id": "GP004",
    "skirt_distance": "3",
    "skirt_height": "2",
    "skirt_loops": "2",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.8",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "100",
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
    "support_line_width": "0.8",
    "support_object_xy_distance": "60%",
    "support_on_build_plate_only": "0",
    "support_speed": "70",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.15",
    "support_type": "normal(auto)",
    "top_shell_layers": "2",
    "top_shell_thickness": "0.8",
    "top_surface_line_width": "0.8",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "40",
    "travel_speed": "110",
    "tree_support_branch_angle": "40",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "2",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/0.28mm SuperDraft @Comgrow T500 0.4.json": {
    "adaptive_layer_height": "1",
    "bottom_shell_layers": "2",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.85",
    "bridge_no_support": "0",
    "bridge_speed": "25",
    "brim_object_gap": "0",
    "brim_width": "0",
    "compatible_printers": [
      "Comgrow T500 0.4 nozzle"
    ],
    "compatible_printers_condition": "",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "from": "system",
    "gap_infill_speed": "70",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "23%",
    "inherits": "fdm_process_comgrow_common",
    "initial_layer_infill_speed": "60",
    "initial_layer_line_width": "0.4",
    "initial_layer_print_height": "0.32",
    "initial_layer_speed": "40",
    "inner_wall_line_width": "0.4",
    "inner_wall_speed": "160",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0",
    "internal_solid_infill_speed": "200",
    "ironing_flow": "15%",
    "ironing_spacing": "0.25",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.28",
    "line_width": "0.4",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.28mm SuperDraft @Comgrow T500 0.4",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "140",
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
    "seam_gap": "5%",
    "seam_position": "aligned",
    "setting_id": "GP004",
    "skirt_distance": "3",
    "skirt_height": "2",
    "skirt_loops": "2",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.4",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "200",
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
    "support_object_xy_distance": "60%",
    "support_on_build_plate_only": "0",
    "support_speed": "140",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.15",
    "support_type": "normal(auto)",
    "top_shell_layers": "2",
    "top_shell_thickness": "0.8",
    "top_surface_line_width": "0.4",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "40",
    "travel_speed": "200",
    "tree_support_branch_angle": "40",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "2",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/0.28mm SuperDraft @Comgrow T500 0.6.json": {
    "adaptive_layer_height": "1",
    "bottom_shell_layers": "2",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.85",
    "bridge_no_support": "0",
    "bridge_speed": "25",
    "brim_object_gap": "0",
    "brim_width": "0",
    "compatible_printers": [
      "Comgrow T500 0.6 nozzle"
    ],
    "compatible_printers_condition": "",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "from": "system",
    "gap_infill_speed": "60",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "23%",
    "inherits": "fdm_process_comgrow_common",
    "initial_layer_infill_speed": "60",
    "initial_layer_line_width": "0.6",
    "initial_layer_print_height": "0.32",
    "initial_layer_speed": "45",
    "inner_wall_line_width": "0.6",
    "inner_wall_speed": "140",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0",
    "internal_solid_infill_speed": "120",
    "ironing_flow": "15%",
    "ironing_spacing": "0.25",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.28",
    "line_width": "0.6",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.28mm SuperDraft @Comgrow T500 0.6",
    "outer_wall_line_width": "0.6",
    "outer_wall_speed": "120",
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
    "seam_gap": "5%",
    "seam_position": "aligned",
    "setting_id": "GP004",
    "skirt_distance": "3",
    "skirt_height": "2",
    "skirt_loops": "2",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.6",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "150",
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
    "support_line_width": "0.6",
    "support_object_xy_distance": "60%",
    "support_on_build_plate_only": "0",
    "support_speed": "120",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.15",
    "support_type": "normal(auto)",
    "top_shell_layers": "2",
    "top_shell_thickness": "0.8",
    "top_surface_line_width": "0.6",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "30",
    "travel_speed": "170",
    "tree_support_branch_angle": "40",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "2",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/0.32mm Standard @Comgrow T500 0.8.json": {
    "adaptive_layer_height": "1",
    "bottom_shell_layers": "2",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.85",
    "bridge_no_support": "0",
    "bridge_speed": "25",
    "brim_object_gap": "0",
    "brim_width": "0",
    "compatible_printers": [
      "Comgrow T500 0.8 nozzle"
    ],
    "compatible_printers_condition": "",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "from": "system",
    "gap_infill_speed": "60",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "23%",
    "inherits": "fdm_process_comgrow_common",
    "initial_layer_infill_speed": "50",
    "initial_layer_line_width": "0.8",
    "initial_layer_print_height": "0.36",
    "initial_layer_speed": "40",
    "inner_wall_line_width": "0.8",
    "inner_wall_speed": "90",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0",
    "internal_solid_infill_speed": "80",
    "ironing_flow": "15%",
    "ironing_spacing": "0.25",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.32",
    "line_width": "0.8",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.32mm Standard @Comgrow T500 0.8",
    "outer_wall_line_width": "0.8",
    "outer_wall_speed": "70",
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
    "seam_gap": "5%",
    "seam_position": "aligned",
    "setting_id": "GP004",
    "skirt_distance": "3",
    "skirt_height": "2",
    "skirt_loops": "2",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.8",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "100",
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
    "support_line_width": "0.8",
    "support_object_xy_distance": "60%",
    "support_on_build_plate_only": "0",
    "support_speed": "70",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.15",
    "support_type": "normal(auto)",
    "top_shell_layers": "2",
    "top_shell_thickness": "0.8",
    "top_surface_line_width": "0.8",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "40",
    "travel_speed": "110",
    "tree_support_branch_angle": "40",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "2",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/0.40mm Draft @Comgrow T500 0.8.json": {
    "adaptive_layer_height": "1",
    "bottom_shell_layers": "2",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.85",
    "bridge_no_support": "0",
    "bridge_speed": "25",
    "brim_object_gap": "0",
    "brim_width": "0",
    "compatible_printers": [
      "Comgrow T500 0.8 nozzle"
    ],
    "compatible_printers_condition": "",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "from": "system",
    "gap_infill_speed": "60",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "23%",
    "inherits": "fdm_process_comgrow_common",
    "initial_layer_infill_speed": "50",
    "initial_layer_line_width": "0.8",
    "initial_layer_print_height": "0.44",
    "initial_layer_speed": "40",
    "inner_wall_line_width": "0.8",
    "inner_wall_speed": "90",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0",
    "internal_solid_infill_speed": "80",
    "ironing_flow": "15%",
    "ironing_spacing": "0.25",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.40",
    "line_width": "0.8",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.40mm Draft @Comgrow T500 0.8",
    "outer_wall_line_width": "0.8",
    "outer_wall_speed": "70",
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
    "seam_gap": "5%",
    "seam_position": "aligned",
    "setting_id": "GP004",
    "skirt_distance": "3",
    "skirt_height": "2",
    "skirt_loops": "2",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.8",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "100",
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
    "support_line_width": "0.8",
    "support_object_xy_distance": "60%",
    "support_on_build_plate_only": "0",
    "support_speed": "70",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.15",
    "support_type": "normal(auto)",
    "top_shell_layers": "2",
    "top_shell_thickness": "0.8",
    "top_surface_line_width": "0.8",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "40",
    "travel_speed": "110",
    "tree_support_branch_angle": "40",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "2",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/0.48mm Draft @Comgrow T500 0.8.json": {
    "adaptive_layer_height": "1",
    "bottom_shell_layers": "2",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.85",
    "bridge_no_support": "0",
    "bridge_speed": "25",
    "brim_object_gap": "0",
    "brim_width": "0",
    "compatible_printers": [
      "Comgrow T500 0.8 nozzle"
    ],
    "compatible_printers_condition": "",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "from": "system",
    "gap_infill_speed": "60",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "23%",
    "inherits": "fdm_process_comgrow_common",
    "initial_layer_infill_speed": "50",
    "initial_layer_line_width": "0.8",
    "initial_layer_print_height": "0.52",
    "initial_layer_speed": "40",
    "inner_wall_line_width": "0.8",
    "inner_wall_speed": "90",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0",
    "internal_solid_infill_speed": "80",
    "ironing_flow": "15%",
    "ironing_spacing": "0.25",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.48",
    "line_width": "0.8",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.48mm Draft @Comgrow T500 0.8",
    "outer_wall_line_width": "0.8",
    "outer_wall_speed": "70",
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
    "seam_gap": "5%",
    "seam_position": "aligned",
    "setting_id": "GP004",
    "skirt_distance": "3",
    "skirt_height": "2",
    "skirt_loops": "2",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.8",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "100",
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
    "support_line_width": "0.8",
    "support_object_xy_distance": "60%",
    "support_on_build_plate_only": "0",
    "support_speed": "70",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.15",
    "support_type": "normal(auto)",
    "top_shell_layers": "2",
    "top_shell_thickness": "0.8",
    "top_surface_line_width": "0.8",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "40",
    "travel_speed": "110",
    "tree_support_branch_angle": "40",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "2",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/0.56mm SuperDraft @Comgrow T500 0.8.json": {
    "adaptive_layer_height": "1",
    "bottom_shell_layers": "2",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.85",
    "bridge_no_support": "0",
    "bridge_speed": "25",
    "brim_object_gap": "0",
    "brim_width": "0",
    "compatible_printers": [
      "Comgrow T500 0.8 nozzle"
    ],
    "compatible_printers_condition": "",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "from": "system",
    "gap_infill_speed": "60",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "23%",
    "inherits": "fdm_process_comgrow_common",
    "initial_layer_infill_speed": "50",
    "initial_layer_line_width": "0.8",
    "initial_layer_print_height": "0.60",
    "initial_layer_speed": "40",
    "inner_wall_line_width": "0.8",
    "inner_wall_speed": "90",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0",
    "internal_solid_infill_speed": "80",
    "ironing_flow": "15%",
    "ironing_spacing": "0.25",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.56",
    "line_width": "0.8",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.56mm SuperChunky @Comgrow T500 0.8",
    "outer_wall_line_width": "0.8",
    "outer_wall_speed": "70",
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
    "seam_gap": "5%",
    "seam_position": "aligned",
    "setting_id": "GP004",
    "skirt_distance": "3",
    "skirt_height": "2",
    "skirt_loops": "2",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.8",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "100",
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
    "support_line_width": "0.8",
    "support_object_xy_distance": "60%",
    "support_on_build_plate_only": "0",
    "support_speed": "70",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.15",
    "support_type": "normal(auto)",
    "top_shell_layers": "2",
    "top_shell_thickness": "0.8",
    "top_surface_line_width": "0.8",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "40",
    "travel_speed": "110",
    "tree_support_branch_angle": "40",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "2",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/fdm_process_comgrow_common.json": {
    "accel_to_decel_enable": "1",
    "accel_to_decel_factor": "50%",
    "bottom_shell_layers": "2",
    "bottom_shell_thickness": "0",
    "bottom_solid_infill_flow_ratio": "1",
    "bottom_surface_pattern": "monotonic",
    "bridge_acceleration": "50%",
    "bridge_angle": "0",
    "bridge_density": "100%",
    "bridge_flow": "0.85",
    "bridge_no_support": "0",
    "bridge_speed": "25",
    "brim_ears_detection_length": "1",
    "brim_ears_max_angle": "125",
    "brim_object_gap": "0",
    "brim_type": "auto_brim",
    "brim_width": "0",
    "compatible_printers_condition": "",
    "default_acceleration": "3000",
    "default_jerk": "0",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "elefant_foot_compensation_layers": "1",
    "enable_arc_fitting": "0",
    "enable_overhang_speed": "1",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "enforce_support_layers": "0",
    "exclude_object": "0",
    "extra_perimeters_on_overhangs": "0",
    "filename_format": "{printer_model}_{input_filename_base}_{filament_type[0]}_{layer_height}_{print_time}.gcode",
    "filter_out_gap_fill": "0",
    "flush_into_infill": "0",
    "flush_into_objects": "0",
    "flush_into_support": "1",
    "from": "",
    "fuzzy_skin": "none",
    "fuzzy_skin_point_distance": "0.8",
    "fuzzy_skin_thickness": "0.3",
    "gap_infill_speed": "70",
    "gcode_add_line_number": "0",
    "gcode_comments": "0",
    "gcode_label_objects": "0",
    "hole_to_polyhole": "0",
    "hole_to_polyhole_threshold": "0.01",
    "hole_to_polyhole_twisted": "1",
    "independent_support_layer_height": "1",
    "infill_anchor": "400%",
    "infill_anchor_max": "20",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_jerk": "9",
    "infill_wall_overlap": "23%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "1000",
    "initial_layer_infill_speed": "60",
    "initial_layer_jerk": "9",
    "initial_layer_line_width": "0.4",
    "initial_layer_min_bead_width": "85%",
    "initial_layer_print_height": "0.24",
    "initial_layer_speed": "40",
    "initial_layer_travel_speed": "100%",
    "inner_wall_acceleration": "3000",
    "inner_wall_jerk": "9",
    "inner_wall_line_width": "0.4",
    "inner_wall_speed": "160",
    "instantiation": "false",
    "interface_shells": "0",
    "internal_bridge_speed": "150%",
    "internal_solid_infill_acceleration": "100%",
    "internal_solid_infill_line_width": "0",
    "internal_solid_infill_pattern": "monotonic",
    "internal_solid_infill_speed": "200",
    "ironing_angle": "0",
    "ironing_flow": "15%",
    "ironing_pattern": "zig-zag",
    "ironing_spacing": "0.25",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.2",
    "line_width": "0.4",
    "make_overhang_printable": "0",
    "make_overhang_printable_angle": "55",
    "make_overhang_printable_hole_size": "0",
    "max_bridge_length": "10",
    "max_travel_detour_distance": "0",
    "max_volumetric_extrusion_rate_slope": "0",
    "max_volumetric_extrusion_rate_slope_segment_length": "3",
    "min_bead_width": "85%",
    "min_feature_size": "25%",
    "min_width_top_surface": "300%",
    "minimum_sparse_infill_area": "10",
    "name": "fdm_process_comgrow_common",
    "only_one_wall_first_layer": "0",
    "only_one_wall_top": "0",
    "ooze_prevention": "0",
    "outer_wall_acceleration": "1000",
    "outer_wall_jerk": "9",
    "outer_wall_speed": "140",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "20",
    "overhang_3_4_speed": "15",
    "overhang_4_4_speed": "10",
    "overhang_reverse": "0",
    "overhang_reverse_threshold": "50%",
    "overhang_speed_classic": "0",
    "post_process": [],
    "precise_outer_wall": "0",
    "prime_tower_brim_width": "3",
    "prime_tower_width": "60",
    "prime_volume": "45",
    "print_flow_ratio": "1",
    "print_sequence": "by layer",
    "raft_contact_distance": "0.1",
    "raft_expansion": "1.5",
    "raft_first_layer_density": "90%",
    "raft_first_layer_expansion": "2",
    "raft_layers": "0",
    "reduce_crossing_wall": "0",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "role_based_wipe_speed": "1",
    "seam_gap": "5%",
    "seam_position": "aligned",
    "single_extruder_multi_material_priming": "0",
    "skirt_distance": "3",
    "skirt_height": "2",
    "skirt_loops": "0",
    "skirt_speed": "50",
    "slice_closing_radius": "0.049",
    "slicing_mode": "regular",
    "slow_down_layers": "0",
    "slowdown_for_curled_perimeters": "0",
    "small_perimeter_speed": "50%",
    "small_perimeter_threshold": "0",
    "solid_infill_filament": "1",
    "sparse_infill_acceleration": "100%",
    "sparse_infill_density": "10%",
    "sparse_infill_filament": "1",
    "sparse_infill_line_width": "0.4",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "200",
    "spiral_mode": "0",
    "staggered_inner_seams": "0",
    "standby_temperature_delta": "-5",
    "support_angle": "0",
    "support_base_pattern": "rectilinear",
    "support_base_pattern_spacing": "0.2",
    "support_bottom_interface_spacing": "0.5",
    "support_bottom_z_distance": "0.2",
    "support_critical_regions_only": "0",
    "support_expansion": "0",
    "support_filament": "0",
    "support_interface_bottom_layers": "-1",
    "support_interface_filament": "0",
    "support_interface_loop_pattern": "0",
    "support_interface_pattern": "rectilinear",
    "support_interface_spacing": "0.2",
    "support_interface_speed": "80",
    "support_interface_top_layers": "3",
    "support_object_xy_distance": "0.35",
    "support_on_build_plate_only": "0",
    "support_remove_small_overhang": "1",
    "support_speed": "140",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.15",
    "support_type": "normal(auto)",
    "thick_bridges": "0",
    "timelapse_type": "0",
    "top_shell_layers": "2",
    "top_solid_infill_flow_ratio": "1",
    "top_surface_acceleration": "2000",
    "top_surface_jerk": "9",
    "top_surface_line_width": "0.4",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "40",
    "travel_acceleration": "3000",
    "travel_jerk": "12",
    "travel_speed": "200",
    "travel_speed_z": "0",
    "tree_support_adaptive_layer_height": "1",
    "tree_support_angle_slow": "25",
    "tree_support_auto_brim": "1",
    "tree_support_branch_angle": "40",
    "tree_support_branch_angle_organic": "40",
    "tree_support_branch_diameter": "5",
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
    "wall_distribution_count": "1",
    "wall_filament": "1",
    "wall_generator": "arachne",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "3",
    "wall_transition_angle": "10",
    "wall_transition_filter_deviation": "25%",
    "wall_transition_length": "100%",
    "wipe_on_loops": "0",
    "wipe_speed": "80%",
    "wipe_tower_bridging": "10",
    "wipe_tower_cone_angle": "0",
    "wipe_tower_extra_spacing": "100%",
    "wipe_tower_extruder": "0",
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
  }
}

FILAMENT = {
  "filament/Comgrow Generic ABS.json": {
    "compatible_printers": [
      "Comgrow T500 0.4 nozzle",
      "Comgrow T500 0.6 nozzle",
      "Comgrow T500 0.8 nozzle"
    ],
    "filament_flow_ratio": [
      "0.926"
    ],
    "filament_id": "GFB99",
    "filament_max_volumetric_speed": [
      "30"
    ],
    "filament_retraction_length": [
      "0.5"
    ],
    "from": "system",
    "inherits": "fdm_filament_abs",
    "instantiation": "true",
    "name": "Comgrow Generic ABS",
    "setting_id": "GFSA04",
    "type": "filament"
  },
  "filament/Comgrow Generic PETG.json": {
    "compatible_printers": [
      "Comgrow T500 0.4 nozzle",
      "Comgrow T500 0.6 nozzle",
      "Comgrow T500 0.8 nozzle"
    ],
    "fan_cooling_layer_time": [
      "30"
    ],
    "fan_max_speed": [
      "25"
    ],
    "fan_min_speed": [
      "10"
    ],
    "filament_flow_ratio": [
      "0.98"
    ],
    "filament_id": "GFG99",
    "filament_max_volumetric_speed": [
      "8"
    ],
    "filament_retraction_length": [
      "0.5"
    ],
    "filament_start_gcode": [
      "; filament start gcode\n"
    ],
    "from": "system",
    "inherits": "fdm_filament_pet",
    "instantiation": "true",
    "name": "Comgrow Generic PETG",
    "nozzle_temperature_initial_layer": [
      "260"
    ],
    "overhang_fan_speed": [
      "90"
    ],
    "overhang_fan_threshold": [
      "25%"
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
  "filament/Comgrow Generic PLA.json": {
    "compatible_printers": [
      "Comgrow T500 0.4 nozzle",
      "Comgrow T500 0.6 nozzle",
      "Comgrow T500 0.8 nozzle"
    ],
    "filament_flow_ratio": [
      "0.98"
    ],
    "filament_id": "GFL99",
    "filament_max_volumetric_speed": [
      "30"
    ],
    "filament_retraction_length": [
      "0.5"
    ],
    "from": "system",
    "inherits": "fdm_filament_pla",
    "instantiation": "true",
    "name": "Comgrow Generic PLA",
    "setting_id": "GFSA04",
    "slow_down_layer_time": [
      "8"
    ],
    "type": "filament"
  },
  "filament/Comgrow T300 PLA.json": {
    "compatible_printers": [
      "Comgrow T300 0.4 nozzle"
    ],
    "fan_cooling_layer_time": [
      "50"
    ],
    "fan_max_speed": [
      "100"
    ],
    "fan_min_speed": [
      "60"
    ],
    "filament_flow_ratio": [
      "0.98"
    ],
    "filament_id": "GFL99",
    "filament_max_volumetric_speed": [
      "24"
    ],
    "filament_retraction_length": [
      "0.5"
    ],
    "from": "system",
    "full_fan_speed_layer": [
      "3"
    ],
    "hot_plate_temp": [
      "65"
    ],
    "hot_plate_temp_initial_layer": [
      "65"
    ],
    "inherits": "Comgrow Generic PLA",
    "instantiation": "true",
    "name": "Comgrow T300 PLA",
    "nozzle_temperature": [
      "200"
    ],
    "nozzle_temperature_initial_layer": [
      "235"
    ],
    "nozzle_temperature_range_high": [
      "260"
    ],
    "nozzle_temperature_range_low": [
      "190"
    ],
    "setting_id": "GFSA04",
    "slow_down_layer_time": [
      "6"
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
    "textured_plate_temp": [
      "60"
    ],
    "textured_plate_temp_initial_layer": [
      "60"
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
  }
}

MISC = {}

ASSETS = [
  "Comgrow T300_cover.png",
  "Comgrow T500_cover.png",
  "comgrow_t300_buildplate_model.stl",
  "comgrow_t300_buildplate_texture.png",
  "comgrow_t500_buildplate_model.stl",
  "comgrow_t500_buildplate_texture.png"
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
