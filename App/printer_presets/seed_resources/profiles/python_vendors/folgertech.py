from __future__ import annotations

VENDOR = "Folgertech"
INDEX = {
  "description": "Folgertech configurations",
  "filament_list": [],
  "force_update": "0",
  "machine_list": [
    {
      "name": "fdm_machine_common",
      "sub_path": "machine/fdm_machine_common.json"
    },
    {
      "name": "fdm_folgertech_common",
      "sub_path": "machine/fdm_folgertech_common.json"
    },
    {
      "name": "Folgertech FT-5 0.4 nozzle",
      "sub_path": "machine/Folgertech FT-5 0.4 nozzle.json"
    },
    {
      "name": "Folgertech FT-5 0.6 nozzle",
      "sub_path": "machine/Folgertech FT-5 0.6 nozzle.json"
    },
    {
      "name": "Folgertech FT-6 0.4 nozzle",
      "sub_path": "machine/Folgertech FT-6 0.4 nozzle.json"
    },
    {
      "name": "Folgertech FT-6 0.6 nozzle",
      "sub_path": "machine/Folgertech FT-6 0.6 nozzle.json"
    },
    {
      "name": "Folgertech i3 0.4 nozzle",
      "sub_path": "machine/Folgertech i3 0.4 nozzle.json"
    },
    {
      "name": "Folgertech i3 0.6 nozzle",
      "sub_path": "machine/Folgertech i3 0.6 nozzle.json"
    }
  ],
  "machine_model_list": [
    {
      "name": "Folgertech FT-5",
      "sub_path": "machine/Folgertech FT-5.json"
    },
    {
      "name": "Folgertech FT-6",
      "sub_path": "machine/Folgertech FT-6.json"
    },
    {
      "name": "Folgertech i3",
      "sub_path": "machine/Folgertech i3.json"
    }
  ],
  "name": "Folgertech",
  "process_list": [
    {
      "name": "fdm_process_common",
      "sub_path": "process/fdm_process_common.json"
    },
    {
      "name": "fdm_process_folgertech_common",
      "sub_path": "process/fdm_process_folgertech_common.json"
    },
    {
      "name": "0.08mm Extra Fine @FT 0.4 nozzle",
      "sub_path": "process/0.08mm Extra Fine @FT.json"
    },
    {
      "name": "0.12mm Fine @FT 0.4 nozzle",
      "sub_path": "process/0.12mm Fine @FT.json"
    },
    {
      "name": "0.16mm Optimal @FT 0.4 nozzle",
      "sub_path": "process/0.16mm Optimal @FT.json"
    },
    {
      "name": "0.18mm Fine @FT 0.6 nozzle",
      "sub_path": "process/0.18mm Fine @FT 0.6 nozzle.json"
    },
    {
      "name": "0.20mm Standard @FT 0.4 nozzle",
      "sub_path": "process/0.20mm Standard @FT.json"
    },
    {
      "name": "0.20mm Strength @FT 0.4 nozzle",
      "sub_path": "process/0.20mm Strength @FT.json"
    },
    {
      "name": "0.24mm Draft @FT 0.4 nozzle",
      "sub_path": "process/0.24mm Draft @FT.json"
    },
    {
      "name": "0.24mm Optimal @FT 0.6 nozzle",
      "sub_path": "process/0.24mm Optimal @FT 0.6 nozzle.json"
    },
    {
      "name": "0.28mm Extra Draft @FT 0.4 nozzle",
      "sub_path": "process/0.28mm Extra Draft @FT.json"
    },
    {
      "name": "0.30mm Standard @FT 0.6 nozzle",
      "sub_path": "process/0.30mm Standard @FT 0.6 nozzle.json"
    },
    {
      "name": "0.30mm Strength @FT 0.6 nozzle",
      "sub_path": "process/0.30mm Strength @FT 0.6 nozzle.json"
    },
    {
      "name": "0.36mm Draft @FT 0.6 nozzle",
      "sub_path": "process/0.36mm Draft @FT 0.6 nozzle.json"
    },
    {
      "name": "0.42mm Extra Draft @FT 0.6 nozzle",
      "sub_path": "process/0.42mm Extra Draft @FT 0.6 nozzle.json"
    }
  ],
  "version": "02.03.01.10"
}

MACHINE = {
  "machine/Folgertech FT-5 0.4 nozzle.json": {
    "auxiliary_fan": "0",
    "default_print_profile": "0.20mm Standard @FT",
    "from": "system",
    "inherits": "fdm_folgertech_common",
    "instantiation": "true",
    "name": "Folgertech FT-5 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "nozzle_type": "undefine",
    "printable_area": [
      "0x0",
      "300x0",
      "300x300",
      "0x300"
    ],
    "printable_height": "400",
    "printer_model": "Folgertech FT-5",
    "retraction_length": [
      "4.5"
    ],
    "retraction_speed": [
      "40"
    ],
    "setting_id": "GM001",
    "type": "machine"
  },
  "machine/Folgertech FT-5 0.6 nozzle.json": {
    "auxiliary_fan": "0",
    "default_print_profile": "0.30mm Standard @FT 0.6 Nozzle",
    "from": "system",
    "inherits": "fdm_folgertech_common",
    "instantiation": "true",
    "name": "Folgertech FT-5 0.6 nozzle",
    "nozzle_diameter": [
      "0.6"
    ],
    "nozzle_type": "undefine",
    "printable_area": [
      "0x0",
      "300x0",
      "300x300",
      "0x300"
    ],
    "printable_height": "400",
    "printer_model": "Folgertech FT-5",
    "printer_variant": "0.6",
    "retraction_length": [
      "4.5"
    ],
    "retraction_speed": [
      "40"
    ],
    "setting_id": "GM001",
    "type": "machine"
  },
  "machine/Folgertech FT-5.json": {
    "bed_model": "Folgertech_FT5_buildplate_model.stl",
    "bed_texture": "Folgertech_FT5_buildplate_texture.png",
    "default_materials": "Generic PLA @System;Generic PETG @System;Generic ABS @System;",
    "family": "Folgertech",
    "hotend_model": "hotend.stl",
    "machine_tech": "FFF",
    "model_id": "FT-5",
    "name": "Folgertech FT-5",
    "nozzle_diameter": "0.4;0.6",
    "type": "machine_model"
  },
  "machine/Folgertech FT-6 0.4 nozzle.json": {
    "auxiliary_fan": "0",
    "default_print_profile": "0.20mm Standard @FT",
    "from": "system",
    "inherits": "fdm_folgertech_common",
    "instantiation": "true",
    "name": "Folgertech FT-6 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "nozzle_type": "undefine",
    "printable_area": [
      "0x0",
      "700x0",
      "700x350",
      "0x350"
    ],
    "printable_height": "400",
    "printer_model": "Folgertech FT-6",
    "setting_id": "GM001",
    "type": "machine"
  },
  "machine/Folgertech FT-6 0.6 nozzle.json": {
    "auxiliary_fan": "0",
    "default_print_profile": "0.30mm Standard @FT 0.6 Nozzle",
    "from": "system",
    "inherits": "fdm_folgertech_common",
    "instantiation": "true",
    "name": "Folgertech FT-6 0.6 nozzle",
    "nozzle_diameter": [
      "0.6"
    ],
    "nozzle_type": "undefine",
    "printable_area": [
      "0x0",
      "700x0",
      "700x350",
      "0x350"
    ],
    "printable_height": "400",
    "printer_model": "Folgertech FT-6",
    "printer_variant": "0.6",
    "setting_id": "GM002",
    "type": "machine"
  },
  "machine/Folgertech FT-6.json": {
    "bed_model": "Folgertech_FT6_buildplate_model.stl",
    "bed_texture": "Folgertech_FT6_buildplate_texture.png",
    "default_materials": "Generic PLA @System;Generic PETG @System;Generic ABS @System;Generic TPU @System;",
    "extruders_count": "2",
    "family": "Folgertech",
    "hotend_model": "hotend.stl",
    "machine_tech": "FFF",
    "model_id": "FT-6",
    "name": "Folgertech FT-6",
    "nozzle_diameter": "0.4;0.6",
    "type": "machine_model"
  },
  "machine/Folgertech i3 0.4 nozzle.json": {
    "auxiliary_fan": "0",
    "default_print_profile": "0.20mm Standard @FT",
    "from": "system",
    "inherits": "fdm_folgertech_common",
    "instantiation": "true",
    "name": "Folgertech i3 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "nozzle_type": "undefine",
    "printable_area": [
      "0x0",
      "200x0",
      "200x200",
      "0x200"
    ],
    "printable_height": "175",
    "printer_model": "Folgertech i3",
    "setting_id": "GM001",
    "type": "machine"
  },
  "machine/Folgertech i3 0.6 nozzle.json": {
    "auxiliary_fan": "0",
    "default_print_profile": "0.30mm Standard @FT 0.6 Nozzle",
    "from": "system",
    "inherits": "fdm_folgertech_common",
    "instantiation": "true",
    "name": "Folgertech i3 0.6 nozzle",
    "nozzle_diameter": [
      "0.6"
    ],
    "nozzle_type": "undefine",
    "printable_area": [
      "0x0",
      "20x0",
      "200x200",
      "0x200"
    ],
    "printable_height": "175",
    "printer_model": "Folgertech i3",
    "printer_variant": "0.6",
    "setting_id": "GM001",
    "type": "machine"
  },
  "machine/Folgertech i3.json": {
    "bed_model": "Folgertech_i3_buildplate_model.stl",
    "bed_texture": "Folgertech_i3_buildplate_texture.png",
    "default_materials": "Generic PLA @System;Generic PETG @System;Generic ABS @System;",
    "family": "Folgertech",
    "hotend_model": "hotend.stl",
    "machine_tech": "FFF",
    "model_id": "i3",
    "name": "Folgertech i3",
    "nozzle_diameter": "0.4;0.6",
    "type": "machine_model"
  },
  "machine/fdm_folgertech_common.json": {
    "auxiliary_fan": "0",
    "bed_exclude_area": [
      "0x0"
    ],
    "change_filament_gcode": "",
    "default_filament_profile": [
      "Generic PLA @System"
    ],
    "default_print_profile": "0.20mm Standard @FT 0.4 Nozzle",
    "deretraction_speed": [
      "40"
    ],
    "extruder_clearance_height_to_lid": "34",
    "extruder_clearance_height_to_rod": "34",
    "extruder_clearance_radius": "47",
    "from": "system",
    "gcode_flavor": "marlin",
    "inherits": "fdm_machine_common",
    "instantiation": "false",
    "layer_change_gcode": "",
    "machine_end_gcode": "M140 S0 ; turn off heatbed\nM104 S0 ; turn off temperature\nM107 ; turn off fan\nG28 X Y ; Home X and Y axis\nM84 X Y E ; disable motors",
    "machine_max_acceleration_e": [
      "5000",
      "5000"
    ],
    "machine_max_acceleration_extruding": [
      "500",
      "500"
    ],
    "machine_max_acceleration_retracting": [
      "1000",
      "1000"
    ],
    "machine_max_acceleration_travel": [
      "500",
      "500"
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
    "machine_min_extruding_rate": [
      "0",
      "0"
    ],
    "machine_min_travel_rate": [
      "0",
      "0"
    ],
    "machine_pause_gcode": "M25 ;pause print",
    "machine_start_gcode": "G28 ; Home all axis\nG1 X0 Y5 Z0.2 F3000 ; Get ready to prime\nG92 E0 ; Reset extrusion distance\nG1 X250 E20 F600 ; Prime nozzle",
    "max_layer_height": [
      "0.32"
    ],
    "min_layer_height": [
      "0.08"
    ],
    "name": "fdm_folgertech_common",
    "nozzle_type": "undefine",
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
      "5"
    ],
    "retraction_minimum_travel": [
      "2"
    ],
    "retraction_speed": [
      "60"
    ],
    "scan_first_layer": "0",
    "silent_mode": "0",
    "single_extruder_multi_material": "1",
    "type": "machine",
    "wipe": [
      "1"
    ],
    "z_hop": [
      "0.4"
    ]
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
  "process/0.08mm Extra Fine @FT.json": {
    "bottom_shell_layers": "7",
    "bridge_flow": "1",
    "compatible_printers": [
      "Folgertech i3 0.4 nozzle",
      "Folgertech FT-5 0.4 nozzle",
      "Folgertech FT-6 0.4 nozzle"
    ],
    "elefant_foot_compensation": "0.15",
    "from": "system",
    "gap_infill_speed": "150",
    "inherits": "fdm_process_folgertech_common",
    "initial_layer_infill_speed": "60",
    "initial_layer_speed": "30",
    "inner_wall_speed": "100",
    "instantiation": "true",
    "internal_solid_infill_speed": "125",
    "ironing_flow": "8%",
    "layer_height": "0.08",
    "name": "0.08mm Extra Fine @FT 0.4 nozzle",
    "outer_wall_speed": "80",
    "overhang_1_4_speed": "60",
    "overhang_2_4_speed": "30",
    "overhang_3_4_speed": "10",
    "overhang_4_4_speed": "10",
    "setting_id": "GP001",
    "sparse_infill_speed": "125",
    "support_threshold_angle": "30",
    "top_shell_layers": "9",
    "top_surface_speed": "80",
    "type": "process"
  },
  "process/0.12mm Fine @FT.json": {
    "bottom_shell_layers": "5",
    "bridge_flow": "1",
    "compatible_printers": [
      "Folgertech i3 0.4 nozzle",
      "Folgertech FT-5 0.4 nozzle",
      "Folgertech FT-6 0.4 nozzle"
    ],
    "elefant_foot_compensation": "0.15",
    "from": "system",
    "gap_infill_speed": "110",
    "inherits": "fdm_process_folgertech_common",
    "initial_layer_infill_speed": "60",
    "initial_layer_speed": "30",
    "inner_wall_speed": "110",
    "instantiation": "true",
    "internal_solid_infill_speed": "110",
    "layer_height": "0.12",
    "name": "0.12mm Fine @FT 0.4 nozzle",
    "outer_wall_speed": "70",
    "overhang_1_4_speed": "60",
    "overhang_2_4_speed": "30",
    "overhang_3_4_speed": "10",
    "overhang_4_4_speed": "10",
    "setting_id": "GP002",
    "sparse_infill_speed": "125",
    "support_threshold_angle": "30",
    "top_shell_layers": "5",
    "top_shell_thickness": "0.6",
    "top_surface_speed": "70",
    "type": "process"
  },
  "process/0.16mm Optimal @FT.json": {
    "bottom_shell_layers": "4",
    "bridge_flow": "1",
    "compatible_printers": [
      "Folgertech i3 0.4 nozzle",
      "Folgertech FT-5 0.4 nozzle",
      "Folgertech FT-6 0.4 nozzle"
    ],
    "elefant_foot_compensation": "0.15",
    "from": "system",
    "gap_infill_speed": "100",
    "inherits": "fdm_process_folgertech_common",
    "initial_layer_infill_speed": "60",
    "initial_layer_speed": "30",
    "inner_wall_speed": "100",
    "instantiation": "true",
    "internal_solid_infill_speed": "100",
    "layer_height": "0.16",
    "name": "0.16mm Optimal @FT 0.4 nozzle",
    "outer_wall_speed": "70",
    "overhang_1_4_speed": "60",
    "overhang_2_4_speed": "30",
    "overhang_3_4_speed": "10",
    "overhang_4_4_speed": "10",
    "setting_id": "GP003",
    "sparse_infill_speed": "110",
    "support_threshold_angle": "30",
    "top_shell_layers": "4",
    "top_shell_thickness": "0.6",
    "top_surface_speed": "70",
    "type": "process"
  },
  "process/0.18mm Fine @FT 0.6 nozzle.json": {
    "bottom_shell_layers": "3",
    "bridge_flow": "1",
    "bridge_speed": "30",
    "compatible_printers": [
      "Folgertech i3 0.6 nozzle",
      "Folgertech FT-5 0.6 nozzle",
      "Folgertech FT-6 0.6 nozzle"
    ],
    "from": "system",
    "gap_infill_speed": "40",
    "inherits": "fdm_process_folgertech_common",
    "initial_layer_infill_speed": "55",
    "initial_layer_line_width": "0.62",
    "initial_layer_print_height": "0.3",
    "initial_layer_speed": "35",
    "inner_wall_line_width": "0.62",
    "inner_wall_speed": "75",
    "instantiation": "true",
    "internal_solid_infill_line_width": "0.62",
    "internal_solid_infill_speed": "80",
    "layer_height": "0.18",
    "line_width": "0.62",
    "name": "0.18mm Fine @FT 0.6 nozzle",
    "outer_wall_line_width": "0.62",
    "outer_wall_speed": "60",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "50",
    "overhang_3_4_speed": "15",
    "overhang_4_4_speed": "10",
    "setting_id": "GP028",
    "sparse_infill_line_width": "0.62",
    "sparse_infill_speed": "80",
    "support_line_width": "0.62",
    "top_shell_layers": "3",
    "top_surface_line_width": "0.62",
    "top_surface_speed": "50",
    "type": "process",
    "wall_loops": "2"
  },
  "process/0.20mm Standard @FT.json": {
    "bottom_shell_layers": "3",
    "bridge_flow": "1",
    "compatible_printers": [
      "Folgertech i3 0.4 nozzle",
      "Folgertech FT-5 0.4 nozzle",
      "Folgertech FT-6 0.4 nozzle"
    ],
    "elefant_foot_compensation": "0.15",
    "from": "system",
    "gap_infill_speed": "80",
    "inherits": "fdm_process_folgertech_common",
    "initial_layer_infill_speed": "60",
    "initial_layer_speed": "30",
    "inner_wall_speed": "100",
    "instantiation": "true",
    "internal_solid_infill_speed": "80",
    "layer_height": "0.2",
    "name": "0.20mm Standard @FT 0.4 nozzle",
    "outer_wall_speed": "70",
    "setting_id": "GP004",
    "sparse_infill_speed": "90",
    "top_shell_layers": "3",
    "top_shell_thickness": "0.6",
    "top_surface_speed": "70",
    "type": "process"
  },
  "process/0.20mm Strength @FT.json": {
    "compatible_printers": [
      "Folgertech i3 0.4 nozzle",
      "Folgertech FT-5 0.4 nozzle",
      "Folgertech FT-6 0.4 nozzle"
    ],
    "from": "system",
    "inherits": "fdm_process_folgertech_common",
    "instantiation": "true",
    "name": "0.20mm Strength @FT 0.4 nozzle",
    "outer_wall_speed": "30",
    "setting_id": "GP013",
    "sparse_infill_density": "25%",
    "type": "process",
    "wall_loops": "6"
  },
  "process/0.24mm Draft @FT.json": {
    "bottom_shell_layers": "3",
    "bridge_flow": "1",
    "compatible_printers": [
      "Folgertech i3 0.4 nozzle",
      "Folgertech FT-5 0.4 nozzle",
      "Folgertech FT-6 0.4 nozzle"
    ],
    "elefant_foot_compensation": "0.15",
    "from": "system",
    "gap_infill_speed": "80",
    "inherits": "fdm_process_folgertech_common",
    "initial_layer_infill_speed": "50",
    "initial_layer_speed": "40",
    "inner_wall_speed": "80",
    "instantiation": "true",
    "internal_solid_infill_speed": "80",
    "layer_height": "0.24",
    "name": "0.24mm Draft @FT 0.4 nozzle",
    "outer_wall_speed": "70",
    "setting_id": "GP005",
    "sparse_infill_speed": "80",
    "support_threshold_angle": "30",
    "top_shell_layers": "3",
    "top_shell_thickness": "0.6",
    "top_surface_line_width": "0.45",
    "top_surface_speed": "70",
    "type": "process"
  },
  "process/0.24mm Optimal @FT 0.6 nozzle.json": {
    "bottom_shell_layers": "3",
    "bridge_flow": "1",
    "bridge_speed": "30",
    "compatible_printers": [
      "Folgertech i3 0.6 nozzle",
      "Folgertech FT-5 0.6 nozzle",
      "Folgertech FT-6 0.6 nozzle"
    ],
    "from": "system",
    "gap_infill_speed": "40",
    "inherits": "fdm_process_folgertech_common",
    "initial_layer_infill_speed": "55",
    "initial_layer_line_width": "0.62",
    "initial_layer_print_height": "0.3",
    "initial_layer_speed": "35",
    "inner_wall_line_width": "0.62",
    "inner_wall_speed": "80",
    "instantiation": "true",
    "internal_solid_infill_line_width": "0.62",
    "internal_solid_infill_speed": "80",
    "layer_height": "0.24",
    "line_width": "0.62",
    "name": "0.24mm Optimal @FT 0.6 nozzle",
    "outer_wall_line_width": "0.62",
    "outer_wall_speed": "60",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "50",
    "overhang_3_4_speed": "15",
    "overhang_4_4_speed": "10",
    "setting_id": "GP029",
    "sparse_infill_line_width": "0.62",
    "sparse_infill_speed": "60",
    "support_line_width": "0.62",
    "top_shell_layers": "3",
    "top_surface_line_width": "0.62",
    "top_surface_speed": "60",
    "type": "process",
    "wall_loops": "2"
  },
  "process/0.28mm Extra Draft @FT.json": {
    "bottom_shell_layers": "3",
    "bridge_flow": "1",
    "compatible_printers": [
      "Folgertech i3 0.4 nozzle",
      "Folgertech FT-5 0.4 nozzle",
      "Folgertech FT-6 0.4 nozzle"
    ],
    "elefant_foot_compensation": "0.15",
    "from": "system",
    "gap_infill_speed": "70",
    "inherits": "fdm_process_folgertech_common",
    "initial_layer_infill_speed": "50",
    "initial_layer_speed": "30",
    "inner_wall_speed": "70",
    "instantiation": "true",
    "internal_solid_infill_speed": "70",
    "layer_height": "0.28",
    "name": "0.28mm Extra Draft @FT 0.4 nozzle",
    "outer_wall_speed": "70",
    "setting_id": "GP006",
    "sparse_infill_speed": "70",
    "support_threshold_angle": "30",
    "top_shell_layers": "3",
    "top_shell_thickness": "0.6",
    "top_surface_line_width": "0.45",
    "top_surface_speed": "70",
    "type": "process"
  },
  "process/0.30mm Standard @FT 0.6 nozzle.json": {
    "bottom_shell_layers": "3",
    "bridge_flow": "1",
    "bridge_speed": "30",
    "compatible_printers": [
      "Folgertech i3 0.6 nozzle",
      "Folgertech FT-5 0.6 nozzle",
      "Folgertech FT-6 0.6 nozzle"
    ],
    "from": "system",
    "gap_infill_speed": "40",
    "inherits": "fdm_process_folgertech_common",
    "initial_layer_infill_speed": "55",
    "initial_layer_line_width": "0.62",
    "initial_layer_print_height": "0.3",
    "initial_layer_speed": "35",
    "inner_wall_line_width": "0.62",
    "inner_wall_speed": "80",
    "instantiation": "true",
    "internal_solid_infill_line_width": "0.62",
    "internal_solid_infill_speed": "80",
    "layer_height": "0.3",
    "line_width": "0.62",
    "name": "0.30mm Standard @FT 0.6 nozzle",
    "outer_wall_line_width": "0.62",
    "outer_wall_speed": "60",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "50",
    "overhang_3_4_speed": "15",
    "overhang_4_4_speed": "10",
    "setting_id": "GP010",
    "sparse_infill_line_width": "0.62",
    "sparse_infill_speed": "80",
    "support_line_width": "0.62",
    "top_shell_layers": "3",
    "top_surface_line_width": "0.62",
    "top_surface_speed": "60",
    "type": "process",
    "wall_loops": "3"
  },
  "process/0.30mm Strength @FT 0.6 nozzle.json": {
    "bottom_shell_layers": "3",
    "bridge_flow": "1",
    "bridge_speed": "30",
    "compatible_printers": [
      "Folgertech i3 0.6 nozzle",
      "Folgertech FT-5 0.6 nozzle",
      "Folgertech FT-6 0.6 nozzle"
    ],
    "from": "system",
    "gap_infill_speed": "40",
    "inherits": "fdm_process_folgertech_common",
    "initial_layer_infill_speed": "55",
    "initial_layer_line_width": "0.62",
    "initial_layer_print_height": "0.3",
    "initial_layer_speed": "35",
    "inner_wall_line_width": "0.62",
    "inner_wall_speed": "80",
    "instantiation": "true",
    "internal_solid_infill_line_width": "0.62",
    "internal_solid_infill_speed": "80",
    "layer_height": "0.3",
    "line_width": "0.62",
    "name": "0.30mm Strength @FT 0.6 nozzle",
    "outer_wall_line_width": "0.62",
    "outer_wall_speed": "60",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "50",
    "overhang_3_4_speed": "15",
    "overhang_4_4_speed": "10",
    "setting_id": "GP036",
    "sparse_infill_density": "25%",
    "sparse_infill_line_width": "0.62",
    "sparse_infill_speed": "80",
    "support_line_width": "0.62",
    "top_shell_layers": "4",
    "top_surface_line_width": "0.62",
    "top_surface_speed": "60",
    "type": "process",
    "wall_loops": "4"
  },
  "process/0.36mm Draft @FT 0.6 nozzle.json": {
    "bottom_shell_layers": "3",
    "bridge_flow": "1",
    "bridge_speed": "30",
    "compatible_printers": [
      "Folgertech i3 0.6 nozzle",
      "Folgertech FT-5 0.6 nozzle",
      "Folgertech FT-6 0.6 nozzle"
    ],
    "from": "system",
    "gap_infill_speed": "40",
    "inherits": "fdm_process_folgertech_common",
    "initial_layer_infill_speed": "55",
    "initial_layer_line_width": "0.62",
    "initial_layer_print_height": "0.3",
    "initial_layer_speed": "35",
    "inner_wall_line_width": "0.62",
    "inner_wall_speed": "80",
    "instantiation": "true",
    "internal_solid_infill_line_width": "0.62",
    "internal_solid_infill_speed": "80",
    "layer_height": "0.36",
    "line_width": "0.62",
    "name": "0.36mm Draft @FT 0.6 nozzle",
    "outer_wall_line_width": "0.62",
    "outer_wall_speed": "60",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "50",
    "overhang_3_4_speed": "15",
    "overhang_4_4_speed": "10",
    "setting_id": "GP030",
    "sparse_infill_line_width": "0.62",
    "sparse_infill_speed": "60",
    "support_line_width": "0.62",
    "top_shell_layers": "3",
    "top_surface_line_width": "0.62",
    "top_surface_speed": "60",
    "type": "process",
    "wall_loops": "2"
  },
  "process/0.42mm Extra Draft @FT 0.6 nozzle.json": {
    "bottom_shell_layers": "3",
    "bridge_flow": "1",
    "bridge_speed": "30",
    "compatible_printers": [
      "Folgertech i3 0.6 nozzle",
      "Folgertech FT-5 0.6 nozzle",
      "Folgertech FT-6 0.6 nozzle"
    ],
    "from": "system",
    "gap_infill_speed": "40",
    "inherits": "fdm_process_folgertech_common",
    "initial_layer_infill_speed": "55",
    "initial_layer_line_width": "0.62",
    "initial_layer_print_height": "0.3",
    "initial_layer_speed": "35",
    "inner_wall_line_width": "0.62",
    "inner_wall_speed": "80",
    "instantiation": "true",
    "internal_solid_infill_line_width": "0.62",
    "internal_solid_infill_speed": "80",
    "layer_height": "0.42",
    "line_width": "0.62",
    "name": "0.42mm Extra Draft @FT 0.6 nozzle",
    "outer_wall_line_width": "0.62",
    "outer_wall_speed": "60",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "50",
    "overhang_3_4_speed": "15",
    "overhang_4_4_speed": "10",
    "setting_id": "GP031",
    "sparse_infill_line_width": "0.62",
    "sparse_infill_speed": "80",
    "support_line_width": "0.62",
    "top_shell_layers": "3",
    "top_surface_line_width": "0.62",
    "top_surface_speed": "60",
    "type": "process",
    "wall_loops": "2"
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
  },
  "process/fdm_process_folgertech_common.json": {
    "adaptive_layer_height": "0",
    "bottom_shell_layers": "3",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.95",
    "bridge_no_support": "0",
    "bridge_speed": "25",
    "brim_object_gap": "0.1",
    "brim_width": "5",
    "compatible_printers_condition": "",
    "default_acceleration": "500",
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
    "infill_wall_overlap": "23%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "500",
    "initial_layer_infill_speed": "20",
    "initial_layer_line_width": "0.5",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "15",
    "inner_wall_acceleration": "500",
    "inner_wall_line_width": "0.45",
    "inner_wall_speed": "40",
    "instantiation": "false",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0.4",
    "internal_solid_infill_speed": "40",
    "ironing_flow": "15%",
    "ironing_spacing": "0.1",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.2",
    "line_width": "0.4",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "15",
    "name": "fdm_process_folgertech_common",
    "outer_wall_line_width": "0.4",
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
    "skirt_distance": "2",
    "skirt_height": "1",
    "skirt_loops": "1",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.45",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "50",
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
    "top_surface_acceleration": "500",
    "top_surface_line_width": "0.4",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "30",
    "travel_acceleration": "700",
    "travel_speed": "150",
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
  "Folgertech FT-5_cover.png",
  "Folgertech FT-6_cover.png",
  "Folgertech i3_cover.png",
  "Folgertech_FT5_buildplate_model.stl",
  "Folgertech_FT5_buildplate_texture.png",
  "Folgertech_FT6_buildplate_model.stl",
  "Folgertech_FT6_buildplate_texture.png",
  "Folgertech_i3_buildplate_model.stl",
  "Folgertech_i3_buildplate_texture.png",
  "hotend.stl"
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
