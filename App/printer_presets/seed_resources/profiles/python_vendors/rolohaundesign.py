from __future__ import annotations

VENDOR = "RolohaunDesign"
INDEX = {
  "description": "RolohaunDesign Printer Profiles",
  "filament_list": [],
  "force_update": "0",
  "machine_list": [
    {
      "name": "fdm_machine_common",
      "sub_path": "machine/fdm_machine_common.json"
    },
    {
      "name": "fdm_common_Rook MK1 LDO",
      "sub_path": "machine/fdm_common_Rook MK1 LDO.json"
    },
    {
      "name": "Rolohaun Delta Flyer Refit 0.4 nozzle",
      "sub_path": "machine/Rolohaun Delta Flyer Refit 0.4 nozzle.json"
    },
    {
      "name": "Rook MK1 LDO 0.2 nozzle",
      "sub_path": "machine/Rook MK1 LDO 0.2 nozzle.json"
    },
    {
      "name": "Rook MK1 LDO 0.4 nozzle",
      "sub_path": "machine/Rook MK1 LDO 0.4 nozzle.json"
    },
    {
      "name": "Rook MK1 LDO 0.6 nozzle",
      "sub_path": "machine/Rook MK1 LDO 0.6 nozzle.json"
    },
    {
      "name": "Rook MK1 LDO 0.8 nozzle",
      "sub_path": "machine/Rook MK1 LDO 0.8 nozzle.json"
    }
  ],
  "machine_model_list": [
    {
      "name": "Rolohaun Delta Flyer Refit",
      "sub_path": "machine/Rolohaun Delta Flyer Refit.json"
    },
    {
      "name": "Rook MK1 LDO",
      "sub_path": "machine/Rook MK1 LDO.json"
    }
  ],
  "name": "RolohaunDesign",
  "process_list": [
    {
      "name": "fdm_process_common",
      "sub_path": "process/fdm_process_common.json"
    },
    {
      "name": "fdm_process_Rook MK1 LDO_common",
      "sub_path": "process/fdm_process_Rook MK1 LDO_common.json"
    },
    {
      "name": "0.08mm Extra Fine @Rook MK1 LDO",
      "sub_path": "process/0.08mm Extra Fine @Rook MK1 LDO.json"
    },
    {
      "name": "0.08mm Super Fine @Delta Flyer Refit",
      "sub_path": "process/0.08mm Super Fine @Rolohaun Delta Flyer Refit.json"
    },
    {
      "name": "0.10mm Fine @Delta Flyer Refit",
      "sub_path": "process/0.10mm Fine @Rolohaun Delta Flyer Refit.json"
    },
    {
      "name": "0.12mm Fine @Rook MK1 LDO",
      "sub_path": "process/0.12mm Fine @Rook MK1 LDO.json"
    },
    {
      "name": "0.16mm Optimal @Delta Flyer Refit",
      "sub_path": "process/0.16mm Optimal @Rolohaun Delta Flyer Refit.json"
    },
    {
      "name": "0.16mm Optimal @Rook MK1 LDO",
      "sub_path": "process/0.16mm Optimal @Rook MK1 LDO.json"
    },
    {
      "name": "0.20mm Standard @Delta Flyer Refit",
      "sub_path": "process/0.20mm Standard @Rolohaun Delta Flyer Refit.json"
    },
    {
      "name": "0.20mm Standard @Rook MK1 LDO",
      "sub_path": "process/0.20mm Standard @Rook MK1 LDO.json"
    },
    {
      "name": "0.24mm Draft @Delta Flyer Refit",
      "sub_path": "process/0.24mm Draft @Rolohaun Delta Flyer Refit.json"
    },
    {
      "name": "0.24mm Draft @Rook MK1 LDO",
      "sub_path": "process/0.24mm Draft @Rook MK1 LDO.json"
    },
    {
      "name": "0.28mm Extra Draft @Rook MK1 LDO",
      "sub_path": "process/0.28mm Extra Draft @Rook MK1 LDO.json"
    },
    {
      "name": "0.28mm Rough Draft @Delta Flyer Refit",
      "sub_path": "process/0.28mm Rough Draft @Rolohaun Delta Flyer Refit.json"
    },
    {
      "name": "0.2mm Vase Mode @Delta Flyer Refit",
      "sub_path": "process/0.2mm Vase Mode @Rolohaun Delta Flyer Refit.json"
    },
    {
      "name": "0.32mm Standard @Rook MK1 LDO",
      "sub_path": "process/0.32mm Extra Draft @Rook MK1 LDO.json"
    },
    {
      "name": "0.40mm Standard @Rook MK1 LDO",
      "sub_path": "process/0.40mm Extra Draft @Rook MK1 LDO.json"
    },
    {
      "name": "0.56mm Standard @Rook MK1 LDO",
      "sub_path": "process/0.56mm Extra Draft @Rook MK1 LDO.json"
    }
  ],
  "version": "02.03.02.10"
}

MACHINE = {
  "machine/Rolohaun Delta Flyer Refit 0.4 nozzle.json": {
    "bed_custom_model": "",
    "deretraction_speed": [
      "60"
    ],
    "from": "system",
    "inherits": "fdm_common_Rook MK1 LDO",
    "instantiation": "true",
    "machine_max_acceleration_extruding": [
      "10000",
      "20000"
    ],
    "machine_max_acceleration_x": [
      "10000",
      "20000"
    ],
    "machine_max_acceleration_y": [
      "10000",
      "20000"
    ],
    "machine_start_gcode": "PRINT_START EXTRUDER=[nozzle_temperature_initial_layer] BED=[bed_temperature_initial_layer_single]\n",
    "min_layer_height": [
      "0.04"
    ],
    "name": "Rolohaun Delta Flyer Refit 0.4 nozzle",
    "nozzle_type": "brass",
    "printable_area": [
      "54.7907x4.79357",
      "54.1644x9.55065",
      "53.1259x14.235",
      "51.6831x18.8111",
      "49.8469x23.244",
      "47.6314x27.5",
      "45.0534x31.5467",
      "42.1324x35.3533",
      "38.8909x38.8909",
      "35.3533x42.1324",
      "31.5467x45.0534",
      "27.5x47.6314",
      "23.244x49.8469",
      "18.8111x51.6831",
      "14.235x53.1259",
      "9.55065x54.1644",
      "4.79357x54.7907",
      "3.36778e-15x55",
      "-4.79357x54.7907",
      "-9.55065x54.1644",
      "-14.235x53.1259",
      "-18.8111x51.6831",
      "-23.244x49.8469",
      "-27.5x47.6314",
      "-31.5467x45.0534",
      "-35.3533x42.1324",
      "-38.8909x38.8909",
      "-42.1324x35.3533",
      "-45.0534x31.5467",
      "-47.6314x27.5",
      "-49.8469x23.244",
      "-51.6831x18.8111",
      "-53.1259x14.235",
      "-54.1644x9.55065",
      "-54.7907x4.79357",
      "-55x6.73556e-15",
      "-54.7907x-4.79357",
      "-54.1644x-9.55065",
      "-53.1259x-14.235",
      "-51.6831x-18.8111",
      "-49.8469x-23.244",
      "-47.6314x-27.5",
      "-45.0534x-31.5467",
      "-42.1324x-35.3533",
      "-38.8909x-38.8909",
      "-35.3533x-42.1324",
      "-31.5467x-45.0534",
      "-27.5x-47.6314",
      "-23.244x-49.8469",
      "-18.8111x-51.6831",
      "-14.235x-53.1259",
      "-9.55065x-54.1644",
      "-4.79357x-54.7907",
      "-1.01033e-14x-55",
      "4.79357x-54.7907",
      "9.55065x-54.1644",
      "14.235x-53.1259",
      "18.8111x-51.6831",
      "23.244x-49.8469",
      "27.5x-47.6314",
      "31.5467x-45.0534",
      "35.3533x-42.1324",
      "38.8909x-38.8909",
      "42.1324x-35.3533",
      "45.0534x-31.5467",
      "47.6314x-27.5",
      "49.8469x-23.244",
      "51.6831x-18.8111",
      "53.1259x-14.235",
      "54.1644x-9.55065",
      "54.7907x-4.79357",
      "55x-1.34711e-14"
    ],
    "printable_height": "115",
    "printer_model": "Rolohaun Delta Flyer Refit",
    "printer_structure": "delta",
    "retraction_length": [
      "1.8"
    ],
    "retraction_speed": [
      "60"
    ],
    "setting_id": "RDFR_01",
    "support_multi_bed_types": "1",
    "thumbnails": "48x48/PNG, 300x300/PNG",
    "type": "machine",
    "z_hop": [
      "0.8"
    ]
  },
  "machine/Rolohaun Delta Flyer Refit.json": {
    "bed_model": "",
    "bed_texture": "bedtexture-rook-green-120.png",
    "default_materials": "Generic PLA @System;Generic PETG @System",
    "family": "RolohaunDesign",
    "hotend_model": "",
    "machine_tech": "FFF",
    "model_id": "RDFR1_1",
    "name": "Rolohaun Delta Flyer Refit",
    "nozzle_diameter": "0.4",
    "type": "machine_model"
  },
  "machine/Rook MK1 LDO 0.2 nozzle.json": {
    "from": "system",
    "inherits": "fdm_common_Rook MK1 LDO",
    "instantiation": "true",
    "max_layer_height": [
      "0.16"
    ],
    "min_layer_height": [
      "0.04"
    ],
    "name": "Rook MK1 LDO 0.2 nozzle",
    "nozzle_diameter": [
      "0.2"
    ],
    "printable_area": [
      "0x0",
      "110x0",
      "110x110",
      "0x110"
    ],
    "printable_height": "111",
    "printer_model": "Rook MK1 LDO",
    "printer_variant": "0.2",
    "setting_id": "RKMK1_m002",
    "type": "machine"
  },
  "machine/Rook MK1 LDO 0.4 nozzle.json": {
    "from": "system",
    "inherits": "fdm_common_Rook MK1 LDO",
    "instantiation": "true",
    "name": "Rook MK1 LDO 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "printable_area": [
      "0x0",
      "110x0",
      "110x110",
      "0x110"
    ],
    "printable_height": "111",
    "printer_model": "Rook MK1 LDO",
    "printer_variant": "0.4",
    "setting_id": "RKMK1_m001",
    "type": "machine"
  },
  "machine/Rook MK1 LDO 0.6 nozzle.json": {
    "from": "system",
    "inherits": "fdm_common_Rook MK1 LDO",
    "instantiation": "true",
    "max_layer_height": [
      "0.4"
    ],
    "min_layer_height": [
      "0.12"
    ],
    "name": "Rook MK1 LDO 0.6 nozzle",
    "nozzle_diameter": [
      "0.6"
    ],
    "printable_area": [
      "0x0",
      "110x0",
      "110x110",
      "0x110"
    ],
    "printable_height": "111",
    "printer_model": "Rook MK1 LDO",
    "printer_variant": "0.6",
    "setting_id": "RKMK1_m003",
    "type": "machine"
  },
  "machine/Rook MK1 LDO 0.8 nozzle.json": {
    "from": "system",
    "inherits": "fdm_common_Rook MK1 LDO",
    "instantiation": "true",
    "max_layer_height": [
      "0.6"
    ],
    "min_layer_height": [
      "0.2"
    ],
    "name": "Rook MK1 LDO 0.8 nozzle",
    "nozzle_diameter": [
      "0.8"
    ],
    "printable_area": [
      "0x0",
      "110x0",
      "110x110",
      "0x110"
    ],
    "printable_height": "111",
    "printer_model": "Rook MK1 LDO",
    "printer_variant": "0.8",
    "setting_id": "RKMK1_m004",
    "type": "machine"
  },
  "machine/Rook MK1 LDO.json": {
    "bed_model": "",
    "bed_texture": "bedtexture-rook-green-120.png",
    "default_materials": "Generic ABS @System;Generic PLA @System;Generic PLA-CF @System;Generic PETG @System;Generic TPU @System;Generic ASA @System;Generic PC @System;Generic PVA @System;Generic PA @System;Generic PA-CF @System",
    "family": "RolohaunDesign",
    "hotend_model": "",
    "machine_tech": "FFF",
    "model_id": "RKMK1_1",
    "name": "Rook MK1 LDO",
    "nozzle_diameter": "0.4;0.2;0.6;0.8",
    "type": "machine_model"
  },
  "machine/fdm_common_Rook MK1 LDO.json": {
    "auxiliary_fan": "0",
    "bed_exclude_area": [
      "0x0"
    ],
    "before_layer_change_gcode": ";BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n",
    "change_filament_gcode": "",
    "default_filament_profile": [
      "Generic PLA @System"
    ],
    "default_print_profile": "0.20mm Standard @Rook MK1 LDO",
    "deretraction_speed": [
      "40"
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
      "8000",
      "8000"
    ],
    "machine_max_acceleration_retracting": [
      "5000",
      "5000"
    ],
    "machine_max_acceleration_travel": [
      "8000",
      "8000"
    ],
    "machine_max_acceleration_x": [
      "8000",
      "8000"
    ],
    "machine_max_acceleration_y": [
      "8000",
      "8000"
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
      "420",
      "420"
    ],
    "machine_max_speed_y": [
      "420",
      "420"
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
    "machine_start_gcode": "M190 S[bed_temperature_initial_layer_single]\nM109 S[nozzle_temperature_initial_layer]\nPRINT_START EXTRUDER=[nozzle_temperature_initial_layer] BED=[bed_temperature_initial_layer_single]\n",
    "max_layer_height": [
      "0.32"
    ],
    "min_layer_height": [
      "0.08"
    ],
    "name": "fdm_common_Rook MK1 LDO",
    "nozzle_type": "undefine",
    "printable_height": "165",
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
      "50"
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
    ],
    "z_hop_types": "Normal Lift"
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
    "layer_change_gcode": ";AFTER_LAYER_CHANGE\n;[layer_z]",
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
    "machine_pause_gcode": "M601",
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
    "printable_height": "165",
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
  "process/0.08mm Extra Fine @Rook MK1 LDO.json": {
    "bottom_shell_layers": "7",
    "compatible_printers": [
      "Rook MK1 LDO 0.4 nozzle",
      "Rook MK1 LDO 0.2 nozzle",
      "Rook MK1 LDO 0.6 nozzle"
    ],
    "from": "system",
    "inherits": "fdm_process_Rook MK1 LDO_common",
    "initial_layer_print_height": "0.2",
    "instantiation": "true",
    "layer_height": "0.08",
    "name": "0.08mm Extra Fine @Rook MK1 LDO",
    "setting_id": "RKMK1_p001",
    "support_bottom_z_distance": "0.08",
    "support_top_z_distance": "0.08",
    "top_shell_layers": "9",
    "type": "process"
  },
  "process/0.08mm Super Fine @Rolohaun Delta Flyer Refit.json": {
    "bottom_shell_layers": "4",
    "compatible_printers": [
      "Rolohaun Delta Flyer Refit 0.4 nozzle"
    ],
    "from": "system",
    "inherits": "fdm_process_Rook MK1 LDO_common",
    "initial_layer_infill_speed": "100",
    "initial_layer_speed": "80",
    "instantiation": "true",
    "layer_height": "0.08",
    "min_skirt_length": "8",
    "name": "0.08mm Super Fine @Delta Flyer Refit",
    "skirt_height": "1",
    "skirt_loops": "2",
    "sparse_infill_density": "5%",
    "top_shell_layers": "6",
    "top_solid_infill_flow_ratio": "0.95",
    "travel_speed": "300",
    "type": "process",
    "wall_loops": "4"
  },
  "process/0.10mm Fine @Rolohaun Delta Flyer Refit.json": {
    "bottom_shell_layers": "4",
    "compatible_printers": [
      "Rolohaun Delta Flyer Refit 0.4 nozzle"
    ],
    "from": "system",
    "inherits": "fdm_process_Rook MK1 LDO_common",
    "initial_layer_infill_speed": "100",
    "initial_layer_speed": "80",
    "instantiation": "true",
    "layer_height": "0.1",
    "min_skirt_length": "8",
    "name": "0.10mm Fine @Delta Flyer Refit",
    "skirt_height": "1",
    "skirt_loops": "2",
    "sparse_infill_density": "5%",
    "top_shell_layers": "6",
    "top_solid_infill_flow_ratio": "0.95",
    "travel_speed": "300",
    "type": "process",
    "wall_loops": "4"
  },
  "process/0.12mm Fine @Rook MK1 LDO.json": {
    "bottom_shell_layers": "5",
    "compatible_printers": [
      "Rook MK1 LDO 0.4 nozzle",
      "Rook MK1 LDO 0.2 nozzle",
      "Rook MK1 LDO 0.6 nozzle"
    ],
    "from": "system",
    "inherits": "fdm_process_Rook MK1 LDO_common",
    "initial_layer_print_height": "0.2",
    "instantiation": "true",
    "layer_height": "0.12",
    "name": "0.12mm Fine @Rook MK1 LDO",
    "setting_id": "RKMK1_p002",
    "support_bottom_z_distance": "0.08",
    "support_top_z_distance": "0.08",
    "top_shell_layers": "6",
    "type": "process"
  },
  "process/0.16mm Optimal @Rolohaun Delta Flyer Refit.json": {
    "compatible_printers": [
      "Rolohaun Delta Flyer Refit 0.4 nozzle"
    ],
    "from": "system",
    "inherits": "fdm_process_Rook MK1 LDO_common",
    "initial_layer_infill_speed": "100",
    "initial_layer_speed": "80",
    "instantiation": "true",
    "layer_height": "0.16",
    "min_skirt_length": "8",
    "name": "0.16mm Optimal @Delta Flyer Refit",
    "skirt_height": "1",
    "skirt_loops": "2",
    "sparse_infill_density": "10%",
    "top_shell_layers": "5",
    "top_solid_infill_flow_ratio": "0.95",
    "travel_speed": "300",
    "type": "process"
  },
  "process/0.16mm Optimal @Rook MK1 LDO.json": {
    "bottom_shell_layers": "4",
    "compatible_printers": [
      "Rook MK1 LDO 0.4 nozzle",
      "Rook MK1 LDO 0.2 nozzle",
      "Rook MK1 LDO 0.6 nozzle",
      "Rook MK1 LDO 0.8 nozzle"
    ],
    "from": "system",
    "inherits": "fdm_process_Rook MK1 LDO_common",
    "initial_layer_print_height": "0.2",
    "instantiation": "true",
    "layer_height": "0.16",
    "name": "0.16mm Optimal @Rook MK1 LDO",
    "setting_id": "RKMK1_p003",
    "support_bottom_z_distance": "0.16",
    "support_top_z_distance": "0.16",
    "top_shell_layers": "5",
    "type": "process"
  },
  "process/0.20mm Standard @Rolohaun Delta Flyer Refit.json": {
    "compatible_printers": [
      "Rolohaun Delta Flyer Refit 0.4 nozzle"
    ],
    "from": "system",
    "inherits": "fdm_process_Rook MK1 LDO_common",
    "initial_layer_infill_speed": "100",
    "initial_layer_speed": "80",
    "instantiation": "true",
    "min_skirt_length": "8",
    "name": "0.20mm Standard @Delta Flyer Refit",
    "skirt_height": "1",
    "skirt_loops": "2",
    "top_solid_infill_flow_ratio": "0.95",
    "travel_speed": "300",
    "type": "process"
  },
  "process/0.20mm Standard @Rook MK1 LDO.json": {
    "compatible_printers": [
      "Rook MK1 LDO 0.4 nozzle",
      "Rook MK1 LDO 0.6 nozzle",
      "Rook MK1 LDO 0.8 nozzle"
    ],
    "from": "system",
    "inherits": "fdm_process_Rook MK1 LDO_common",
    "instantiation": "true",
    "layer_height": "0.2",
    "name": "0.20mm Standard @Rook MK1 LDO",
    "setting_id": "RKMK1_p004",
    "type": "process"
  },
  "process/0.24mm Draft @Rolohaun Delta Flyer Refit.json": {
    "bottom_shell_layers": "2",
    "compatible_printers": [
      "Rolohaun Delta Flyer Refit 0.4 nozzle"
    ],
    "from": "system",
    "inherits": "fdm_process_Rook MK1 LDO_common",
    "initial_layer_infill_speed": "100",
    "initial_layer_speed": "80",
    "instantiation": "true",
    "layer_height": "0.24",
    "min_skirt_length": "8",
    "name": "0.24mm Draft @Delta Flyer Refit",
    "skirt_height": "1",
    "skirt_loops": "2",
    "sparse_infill_density": "10%",
    "top_shell_layers": "3",
    "top_solid_infill_flow_ratio": "0.95",
    "travel_speed": "300",
    "type": "process",
    "wall_loops": "2"
  },
  "process/0.24mm Draft @Rook MK1 LDO.json": {
    "compatible_printers": [
      "Rook MK1 LDO 0.4 nozzle",
      "Rook MK1 LDO 0.6 nozzle",
      "Rook MK1 LDO 0.8 nozzle"
    ],
    "from": "system",
    "inherits": "fdm_process_Rook MK1 LDO_common",
    "initial_layer_print_height": "0.2",
    "instantiation": "true",
    "layer_height": "0.24",
    "name": "0.24mm Draft @Rook MK1 LDO",
    "setting_id": "RKMK1_p005",
    "support_bottom_z_distance": "0.2",
    "support_top_z_distance": "0.2",
    "type": "process"
  },
  "process/0.28mm Extra Draft @Rook MK1 LDO.json": {
    "compatible_printers": [
      "Rook MK1 LDO 0.4 nozzle",
      "Rook MK1 LDO 0.6 nozzle",
      "Rook MK1 LDO 0.8 nozzle"
    ],
    "from": "system",
    "inherits": "fdm_process_Rook MK1 LDO_common",
    "initial_layer_print_height": "0.2",
    "instantiation": "true",
    "layer_height": "0.28",
    "name": "0.28mm Extra Draft @Rook MK1 LDO",
    "setting_id": "RKMK1_p006",
    "type": "process"
  },
  "process/0.28mm Rough Draft @Rolohaun Delta Flyer Refit.json": {
    "bottom_shell_layers": "2",
    "compatible_printers": [
      "Rolohaun Delta Flyer Refit 0.4 nozzle"
    ],
    "from": "system",
    "inherits": "fdm_process_Rook MK1 LDO_common",
    "initial_layer_infill_speed": "100",
    "initial_layer_speed": "80",
    "instantiation": "true",
    "layer_height": "0.28",
    "min_skirt_length": "8",
    "name": "0.28mm Rough Draft @Delta Flyer Refit",
    "skirt_height": "1",
    "skirt_loops": "2",
    "sparse_infill_density": "10%",
    "top_shell_layers": "3",
    "top_solid_infill_flow_ratio": "0.95",
    "travel_speed": "300",
    "type": "process",
    "wall_loops": "2"
  },
  "process/0.2mm Vase Mode @Rolohaun Delta Flyer Refit.json": {
    "bottom_shell_layers": "4",
    "compatible_printers": [
      "Rolohaun Delta Flyer Refit 0.4 nozzle"
    ],
    "from": "system",
    "inherits": "fdm_process_Rook MK1 LDO_common",
    "initial_layer_infill_speed": "100",
    "initial_layer_speed": "80",
    "instantiation": "true",
    "min_skirt_length": "8",
    "name": "0.2mm Vase Mode @Delta Flyer Refit",
    "outer_wall_line_width": "1",
    "skirt_height": "1",
    "skirt_loops": "2",
    "sparse_infill_density": "0%",
    "spiral_mode": "1",
    "top_shell_layers": "0",
    "top_solid_infill_flow_ratio": "0.95",
    "travel_speed": "300",
    "type": "process",
    "wall_loops": "1"
  },
  "process/0.32mm Extra Draft @Rook MK1 LDO.json": {
    "compatible_printers": [
      "Rook MK1 LDO 0.4 nozzle",
      "Rook MK1 LDO 0.6 nozzle",
      "Rook MK1 LDO 0.8 nozzle"
    ],
    "from": "system",
    "inherits": "fdm_process_Rook MK1 LDO_common",
    "initial_layer_print_height": "0.2",
    "instantiation": "true",
    "layer_height": "0.32",
    "name": "0.32mm Standard @Rook MK1 LDO",
    "setting_id": "RKMK1_p007",
    "support_bottom_z_distance": "0.24",
    "support_top_z_distance": "0.24",
    "type": "process"
  },
  "process/0.40mm Extra Draft @Rook MK1 LDO.json": {
    "compatible_printers": [
      "Rook MK1 LDO 0.6 nozzle",
      "Rook MK1 LDO 0.8 nozzle"
    ],
    "from": "system",
    "inherits": "fdm_process_Rook MK1 LDO_common",
    "initial_layer_print_height": "0.2",
    "instantiation": "true",
    "layer_height": "0.40",
    "name": "0.40mm Standard @Rook MK1 LDO",
    "setting_id": "RKMK1_p008",
    "support_bottom_z_distance": "0.24",
    "support_top_z_distance": "0.24",
    "type": "process"
  },
  "process/0.56mm Extra Draft @Rook MK1 LDO.json": {
    "compatible_printers": [
      "Rook MK1 LDO 0.8 nozzle"
    ],
    "from": "system",
    "inherits": "fdm_process_Rook MK1 LDO_common",
    "initial_layer_print_height": "0.2",
    "instantiation": "true",
    "layer_height": "0.56",
    "name": "0.56mm Standard @Rook MK1 LDO",
    "setting_id": "RKMK1_p009",
    "support_bottom_z_distance": "0.24",
    "support_top_z_distance": "0.24",
    "type": "process"
  },
  "process/fdm_process_Rook MK1 LDO_common.json": {
    "default_acceleration": "10000",
    "default_jerk": "9",
    "exclude_object": "1",
    "from": "system",
    "gap_infill_speed": "200",
    "infill_jerk": "12",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "2000",
    "initial_layer_infill_speed": "105",
    "initial_layer_jerk": "7",
    "initial_layer_speed": "50",
    "inner_wall_acceleration": "8000",
    "inner_wall_jerk": "7",
    "inner_wall_speed": "200",
    "instantiation": "false",
    "internal_solid_infill_speed": "300",
    "name": "fdm_process_Rook MK1 LDO_common",
    "outer_wall_acceleration": "5000",
    "outer_wall_jerk": "7",
    "outer_wall_speed": "150",
    "sparse_infill_speed": "300",
    "top_surface_acceleration": "5000",
    "top_surface_jerk": "7",
    "top_surface_speed": "120",
    "travel_acceleration": "10000",
    "travel_jerk": "12",
    "travel_speed": "500",
    "type": "process"
  },
  "process/fdm_process_common.json": {
    "adaptive_layer_height": "0",
    "bottom_shell_layers": "3",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "1",
    "bridge_no_support": "0",
    "bridge_speed": "25",
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
    "filename_format": "{input_filename_base}_{layer_height}mm_{filament_type[initial_tool]}_{printer_model}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "30",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "25%",
    "initial_layer_acceleration": "500",
    "initial_layer_infill_speed": "45",
    "initial_layer_line_width": "120%",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "45",
    "inner_wall_acceleration": "1000",
    "inner_wall_line_width": "110%",
    "inner_wall_speed": "80",
    "instantiation": "false",
    "interface_shells": "0",
    "internal_bridge_speed": "70",
    "internal_solid_infill_line_width": "120%",
    "internal_solid_infill_speed": "150",
    "ironing_flow": "10%",
    "ironing_spacing": "0.15",
    "ironing_speed": "30",
    "ironing_type": "no ironing",
    "layer_height": "0.2",
    "line_width": "110%",
    "max_travel_detour_distance": "0",
    "min_skirt_length": "4",
    "minimum_sparse_infill_area": "15",
    "name": "fdm_process_common",
    "outer_wall_acceleration": "700",
    "outer_wall_line_width": "100%",
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
    "skirt_height": "3",
    "skirt_loops": "0",
    "slowdown_for_curled_perimeters": "1",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "110%",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "150",
    "spiral_mode": "0",
    "standby_temperature_delta": "-5",
    "support_base_pattern": "default",
    "support_base_pattern_spacing": "2.5",
    "support_bottom_z_distance": "0.2",
    "support_filament": "0",
    "support_interface_bottom_layers": "2",
    "support_interface_filament": "0",
    "support_interface_loop_pattern": "0",
    "support_interface_spacing": "0.5",
    "support_interface_speed": "80",
    "support_interface_top_layers": "2",
    "support_line_width": "96%",
    "support_object_xy_distance": "0.35",
    "support_on_build_plate_only": "0",
    "support_speed": "150",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.2",
    "support_type": "normal(auto)",
    "top_shell_layers": "4",
    "top_shell_thickness": "0.8",
    "top_surface_acceleration": "1000",
    "top_surface_line_width": "93.75%",
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

FILAMENT = {}

MISC = {}

ASSETS = [
  "bedtexture-rook-green-120.png",
  "Rolohaun Delta Flyer Refit_cover.png",
  "Rook MK1 LDO_cover.png"
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
