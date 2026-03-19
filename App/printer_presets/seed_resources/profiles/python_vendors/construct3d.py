from __future__ import annotations

VENDOR = "CONSTRUCT3D"
INDEX = {
  "description": "Construct3D configurations",
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
      "name": "C1 Generic High Flow PETG",
      "sub_path": "filament/C1 Generic High Flow PETG.json"
    },
    {
      "name": "C1 Generic PETG",
      "sub_path": "filament/C1 Generic PETG.json"
    },
    {
      "name": "C1 Generic PLA",
      "sub_path": "filament/C1 Generic PLA.json"
    }
  ],
  "force_update": "0",
  "machine_list": [
    {
      "name": "fdm_machine_common",
      "sub_path": "machine/fdm_machine_common.json"
    },
    {
      "name": "Construct 1 0.4 nozzle",
      "sub_path": "machine/Construct 1 0.4 nozzle.json"
    },
    {
      "name": "Construct 1 XL 0.6 nozzle",
      "sub_path": "machine/Construct 1 XL 0.6 nozzle.json"
    }
  ],
  "machine_model_list": [
    {
      "name": "Construct 1",
      "sub_path": "machine/Construct 1.json"
    },
    {
      "name": "Construct 1 XL",
      "sub_path": "machine/Construct 1 XL.json"
    }
  ],
  "name": "CONSTRUCT3D",
  "process_list": [
    {
      "name": "fdm_process_common",
      "sub_path": "process/fdm_process_common.json"
    },
    {
      "name": "0.14mm Quality @Construct 1",
      "sub_path": "process/0.14mm Quality @Construct 1.json"
    },
    {
      "name": "0.20mm Quality @Construct 1 XL",
      "sub_path": "process/0.20mm Quality @Construct 1 XL.json"
    },
    {
      "name": "0.22mm Standard @Construct 1",
      "sub_path": "process/0.22mm Standard @Construct 1.json"
    },
    {
      "name": "0.25mm Industrial @Construct 1",
      "sub_path": "process/0.25mm Industrial @Construct 1.json"
    },
    {
      "name": "0.30mm Draft @Construct 1",
      "sub_path": "process/0.30mm Draft @Construct 1.json"
    },
    {
      "name": "0.30mm Industrial @Construct 1 XL",
      "sub_path": "process/0.30mm Industrial @Construct 1 XL.json"
    },
    {
      "name": "0.30mm Standard @Construct 1 XL",
      "sub_path": "process/0.30mm Standard @Construct 1 XL.json"
    },
    {
      "name": "0.38mm Draft @Construct 1 XL",
      "sub_path": "process/0.38mm Draft @Construct 1 XL.json"
    }
  ],
  "version": "02.03.01.10"
}

MACHINE = {
  "machine/Construct 1 0.4 nozzle.json": {
    "bed_mesh_max": "200,235",
    "bed_mesh_min": "10,20",
    "default_print_profile": "0.22mm Quality @Construct 1",
    "fan_kickstart": "0.5",
    "fan_speedup_time": "1",
    "from": "system",
    "inherits": "fdm_machine_common",
    "instantiation": "true",
    "machine_end_gcode": ";Retract the filament\nG92 E1\nG1 E-5 F900\n;Move nozzle fast\nG1 X5 Y258 F15000\n;Move Bed Down\nG1 Z180 F6000\n\n;Set machine to idle\nM104 S0\nM104 S0 ; turn off temperature\nM140 S0 ; turn off heatbed\nM107 ; turn off fan\nM84 ; disable motors",
    "machine_max_acceleration_e": [
      "9000"
    ],
    "machine_max_acceleration_extruding": [
      "9000"
    ],
    "machine_max_acceleration_retracting": [
      "9000"
    ],
    "machine_max_acceleration_travel": [
      "9000",
      "1250"
    ],
    "machine_max_acceleration_x": [
      "18000"
    ],
    "machine_max_acceleration_y": [
      "18000"
    ],
    "machine_max_jerk_e": [
      "6"
    ],
    "machine_max_jerk_x": [
      "25"
    ],
    "machine_max_jerk_y": [
      "25"
    ],
    "machine_max_speed_e": [
      "100"
    ],
    "machine_max_speed_x": [
      "320"
    ],
    "machine_max_speed_y": [
      "320"
    ],
    "machine_max_speed_z": [
      "40"
    ],
    "machine_start_gcode": "G90 ; use absolute coordinates\nM83 ; extruder relative mode\nM106 S0 ; Turn Fan off\nM204 S[machine_max_acceleration_extruding] T[machine_max_acceleration_retracting]\nM190 S[first_layer_bed_temperature] ; set bed temp\nM109 S160 ; set extruder temp\nM557 P5 X{adaptive_bed_mesh_min[0]}:{adaptive_bed_mesh_max[0]} Y{adaptive_bed_mesh_min[1]}:{adaptive_bed_mesh_max[1]} ; dynamic meshing\nG28 ; home all\nG1 Z15 F6000 ; move the printer down 15mm\nG1 Y1.0 Z0.3 F4000 ; move print head up\nM109 S[first_layer_temperature] ; set extruder temp\n\nM190 S[first_layer_bed_temperature] ; wait for bed temp\nM109 S[first_layer_temperature] ; wait for extruder temp\n;prime the extruder\nG1 X5 Y2 Z0.3 F6000; go to edge of build volume\nG1 X60 E10 F1000 ;gentle purge start\nG1 X110 E25 F1000; heavy purge\nG1 X60;",
    "max_layer_height": [
      "0.38"
    ],
    "min_layer_height": [
      "0.08"
    ],
    "name": "Construct 1 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "nozzle_type": "hardened_steel",
    "printable_area": [
      "0x0",
      "225x0",
      "225x260",
      "0x260"
    ],
    "printable_height": "180",
    "printer_model": "Construct 1",
    "printer_settings_id": "CONSTRUCT3D",
    "printer_variant": "0.4",
    "retraction_length": [
      "0.7"
    ],
    "retraction_speed": [
      "50"
    ],
    "setting_id": "GM001",
    "thumbnails_format": "QOI",
    "type": "machine",
    "z_hop": [
      "0.2"
    ],
    "z_hop_types": [
      "Auto Lift"
    ]
  },
  "machine/Construct 1 XL 0.6 nozzle.json": {
    "bed_mesh_max": "320,330",
    "bed_mesh_min": "10,20",
    "default_print_profile": "0.20mm Quality @Construct 1 XL",
    "fan_kickstart": "0.5",
    "fan_speedup_time": "1",
    "from": "system",
    "inherits": "fdm_machine_common",
    "instantiation": "true",
    "machine_end_gcode": ";Retract the filament\nG92 E1\nG1 E-5 F900\n;Move nozzle fast\nG1 X5 Y369 F15000\n;Move Bed Down\nG1 Z400 F6000\n\n;Set machine to idle\nT-1\nM104 S0\nM104 S0 ; turn off temperature\nM140 S0 ; turn off heatbed\nM107 ; turn off fan\nM84 ; disable motors\n",
    "machine_max_acceleration_e": [
      "9000"
    ],
    "machine_max_acceleration_extruding": [
      "9000"
    ],
    "machine_max_acceleration_retracting": [
      "9000"
    ],
    "machine_max_acceleration_travel": [
      "9000",
      "1250"
    ],
    "machine_max_acceleration_x": [
      "18000"
    ],
    "machine_max_acceleration_y": [
      "18000"
    ],
    "machine_max_jerk_e": [
      "6"
    ],
    "machine_max_jerk_x": [
      "25"
    ],
    "machine_max_jerk_y": [
      "25"
    ],
    "machine_max_speed_e": [
      "100"
    ],
    "machine_max_speed_x": [
      "320"
    ],
    "machine_max_speed_y": [
      "320"
    ],
    "machine_max_speed_z": [
      "40"
    ],
    "machine_start_gcode": "G90 ; use absolute coordinates\nM83 ; extruder relative mode\nM106 S0 ; Turn Fan off\nM204 S[machine_max_acceleration_extruding] T[machine_max_acceleration_retracting]\nM190 S[first_layer_bed_temperature] ; set bed temp\nM109 S160 ; set extruder temp\nM557 P5 X{adaptive_bed_mesh_min[0]}:{adaptive_bed_mesh_max[0]} Y{adaptive_bed_mesh_min[1]}:{adaptive_bed_mesh_max[1]} ; dynamic meshing\nG28 ; home all\nG1 Z15 F6000 ; move the printer down 15mm\nG1 Y1.0 Z0.3 F4000 ; move print head up\nM109 S[first_layer_temperature] ; set extruder temp\n\nM190 S[first_layer_bed_temperature] ; wait for bed temp\nM109 S[first_layer_temperature] T0 ; wait for extruder temp\n;prime the extruder\nG1 X5 Y2 Z0.3 F6000; go to edge of build volume\nG1 X60 E10 F1000 ;gentle purge start\nG1 X110 E25 F1000; heavy purge\nG1 X60;",
    "max_layer_height": [
      "0.6"
    ],
    "name": "Construct 1 XL 0.6 nozzle",
    "nozzle_diameter": [
      "0.6"
    ],
    "nozzle_type": "hardened_steel",
    "printable_area": [
      "0x0",
      "325x0",
      "325x370",
      "0x370"
    ],
    "printable_height": "400",
    "printer_model": "Construct 1 XL",
    "printer_settings_id": "CONSTRUCT3D",
    "printer_variant": "0.6",
    "retraction_length": [
      "0.7"
    ],
    "retraction_speed": [
      "50"
    ],
    "setting_id": "GM001",
    "thumbnails_format": "QOI",
    "type": "machine",
    "z_hop": [
      "0.2"
    ],
    "z_hop_types": [
      "Auto Lift"
    ]
  },
  "machine/Construct 1 XL.json": {
    "bed_model": "construct_1_xl_buildplate_model.stl",
    "default_materials": "C1 Generic PLA;C1 Generic PETG;C1 Generic High Flow PETG",
    "family": "CONSTRUCT3D",
    "machine_tech": "FFF",
    "model_id": "Construct-1-XL",
    "name": "Construct 1 XL",
    "nozzle_diameter": "0.6",
    "type": "machine_model"
  },
  "machine/Construct 1.json": {
    "bed_model": "construct_1_buildplate_model.stl",
    "default_materials": "C1 Generic PLA;C1 Generic PETG;C1 Generic High Flow PETG",
    "family": "CONSTRUCT3D",
    "machine_tech": "FFF",
    "model_id": "Construct-1",
    "name": "Construct 1",
    "nozzle_diameter": "0.4",
    "type": "machine_model"
  },
  "machine/fdm_machine_common.json": {
    "auxiliary_fan": "0",
    "before_layer_change_gcode": ";BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n",
    "change_filament_gcode": "",
    "default_print_profile": "",
    "deretraction_speed": [
      "50"
    ],
    "extruder_clearance_height_to_lid": "140",
    "extruder_clearance_height_to_rod": "36",
    "extruder_clearance_radius": "65",
    "extruder_colour": [
      "#003f87"
    ],
    "extruder_offset": [
      "0x0"
    ],
    "from": "system",
    "gcode_flavor": "reprapfirmware",
    "host_type": "duet",
    "instantiation": "false",
    "layer_change_gcode": ";AFTER_LAYER_CHANGE\n;[layer_z]",
    "machine_end_gcode": ";Retract the filament\nG92 E1\nG1 E-5 F900\n;Move nozzle fast\nG1 X5 Y258 F15000\n;Move Bed Down\nG1 Z180 F6000\n\n;Set machine to idle\nM104 S0\nM104 S0 ; turn off temperature\nM140 S0 ; turn off heatbed\nM107 ; turn off fan\nM84 ; disable motors",
    "machine_max_acceleration_e": [
      "8000"
    ],
    "machine_max_acceleration_extruding": [
      "9000"
    ],
    "machine_max_acceleration_retracting": [
      "9000"
    ],
    "machine_max_acceleration_x": [
      "9000"
    ],
    "machine_max_acceleration_y": [
      "9000"
    ],
    "machine_max_acceleration_z": [
      "400"
    ],
    "machine_max_jerk_e": [
      "10"
    ],
    "machine_max_jerk_x": [
      "20"
    ],
    "machine_max_jerk_y": [
      "20"
    ],
    "machine_max_jerk_z": [
      "0.2"
    ],
    "machine_max_speed_e": [
      "100"
    ],
    "machine_max_speed_x": [
      "320"
    ],
    "machine_max_speed_y": [
      "320"
    ],
    "machine_max_speed_z": [
      "30"
    ],
    "machine_min_extruding_rate": [
      "0"
    ],
    "machine_min_travel_rate": [
      "0"
    ],
    "machine_start_gcode": "G90 ; use absolute coordinates\nM83 ; extruder relative mode\nM106 S0 ; Turn Fan off\nM204 S[machine_max_acceleration_extruding] T[machine_max_acceleration_retracting]\nM190 S[first_layer_bed_temperature] ; set bed temp\nM109 S160 ; set extruder temp\nG28 ; home all\nG1 Z15 F6000 ; move the printer down 15mm\nG1 Y1.0 Z0.3 F4000 ; move print head up\nM109 S[first_layer_temperature] ; set extruder temp\n\nM190 S[first_layer_bed_temperature] ; wait for bed temp\nM109 S[first_layer_temperature] ; wait for extruder temp\n;prime the extruder\nG1 X5 Y2 Z0.3 F6000; go to edge of build volume\nG1 X60 E10 F1000 ;gentle purge start\nG1 X110 E25 F1000; heavy purge\nG1 X60;",
    "max_layer_height": [
      "0.80"
    ],
    "min_layer_height": [
      "0.08"
    ],
    "name": "fdm_machine_common",
    "nozzle_diameter": [
      "0.6"
    ],
    "printable_height": "180",
    "printer_settings_id": "",
    "printer_technology": "FFF",
    "printhost_apikey": "",
    "printhost_authorization_type": "key",
    "printhost_cafile": "",
    "printhost_password": "",
    "printhost_port": "",
    "printhost_ssl_ignore_revoke": "0",
    "printhost_user": "",
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
      "2.6"
    ],
    "retraction_speed": [
      "50"
    ],
    "silent_mode": "0",
    "single_extruder_multi_material": "1",
    "thumbnails": [
      "160x160"
    ],
    "thumbnails_format": "QOI",
    "type": "machine",
    "wipe": [
      "1"
    ],
    "z_hop": [
      "0.2"
    ],
    "z_lift_type": "Auto Lift"
  }
}

PROCESS = {
  "process/0.14mm Quality @Construct 1.json": {
    "bottom_shell_layers": "4",
    "bridge_speed": "60",
    "compatible_printers": [
      "Construct 1 0.4 nozzle"
    ],
    "default_acceleration": "4000",
    "default_jerk": "12",
    "enable_arc_fitting": "1",
    "extra_perimeters_on_overhangs": "1",
    "from": "system",
    "gap_infill_speed": "125",
    "infill_jerk": "12",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "2000",
    "initial_layer_infill_speed": "100",
    "initial_layer_jerk": "8",
    "initial_layer_print_height": "0.32",
    "initial_layer_speed": "50",
    "inner_wall_acceleration": "3000",
    "inner_wall_jerk": "8",
    "inner_wall_line_width": "0.44",
    "inner_wall_speed": "220",
    "instantiation": "true",
    "internal_solid_infill_line_width": "0.44",
    "internal_solid_infill_speed": "300",
    "layer_height": "0.14",
    "name": "0.14mm Quality @Construct 1",
    "only_one_wall_top": "1",
    "outer_wall_acceleration": "2200",
    "outer_wall_jerk": "8",
    "outer_wall_speed": "140",
    "overhang_2_4_speed": "60",
    "overhang_3_4_speed": "40",
    "overhang_4_4_speed": "15",
    "precise_outer_wall": "1",
    "setting_id": "GP004",
    "skirt_loops": "1",
    "slow_down_layers": "1",
    "sparse_infill_density": "12%",
    "sparse_infill_line_width": "0.4",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "300",
    "support_speed": "300",
    "top_shell_layers": "5",
    "top_surface_acceleration": "2000",
    "top_surface_jerk": "8",
    "top_surface_line_width": "0.44",
    "top_surface_speed": "160",
    "travel_acceleration": "6400",
    "travel_speed": "320",
    "type": "process",
    "wall_loops": "2",
    "wall_sequence": "inner-outer-inner wall"
  },
  "process/0.20mm Quality @Construct 1 XL.json": {
    "bottom_shell_layers": "4",
    "compatible_printers": [
      "Construct 1 XL 0.6 nozzle"
    ],
    "default_acceleration": "4000",
    "default_jerk": "12",
    "enable_arc_fitting": "1",
    "extra_perimeters_on_overhangs": "1",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "100",
    "infill_jerk": "12",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "1400",
    "initial_layer_infill_speed": "100",
    "initial_layer_jerk": "8",
    "initial_layer_line_width": "0.72",
    "initial_layer_print_height": "0.32",
    "initial_layer_speed": "50",
    "inner_wall_acceleration": "3000",
    "inner_wall_jerk": "8",
    "inner_wall_line_width": "0.66",
    "inner_wall_speed": "220",
    "instantiation": "true",
    "internal_solid_infill_line_width": "0.6",
    "internal_solid_infill_speed": "240",
    "layer_height": "0.2",
    "line_width": "0.6",
    "name": "0.20mm Quality @Construct 1 XL",
    "only_one_wall_top": "1",
    "outer_wall_acceleration": "2200",
    "outer_wall_jerk": "8",
    "outer_wall_line_width": "0.6",
    "outer_wall_speed": "140",
    "precise_outer_wall": "1",
    "setting_id": "GP004",
    "skirt_loops": "1",
    "slow_down_layers": "1",
    "sparse_infill_density": "18%",
    "sparse_infill_line_width": "0.6",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "240",
    "support_line_width": "0.6",
    "top_shell_layers": "5",
    "top_surface_acceleration": "2000",
    "top_surface_jerk": "8",
    "top_surface_line_width": "0.66",
    "top_surface_speed": "100",
    "travel_acceleration": "6000",
    "travel_speed": "320",
    "type": "process",
    "wall_loops": "2",
    "wall_sequence": "inner-outer-inner wall"
  },
  "process/0.22mm Standard @Construct 1.json": {
    "bridge_speed": "60",
    "compatible_printers": [
      "Construct 1 0.4 nozzle"
    ],
    "default_acceleration": "4000",
    "default_jerk": "12",
    "enable_arc_fitting": "1",
    "extra_perimeters_on_overhangs": "1",
    "from": "system",
    "gap_infill_speed": "125",
    "infill_jerk": "12",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "2000",
    "initial_layer_infill_speed": "100",
    "initial_layer_jerk": "8",
    "initial_layer_print_height": "0.32",
    "initial_layer_speed": "50",
    "inner_wall_acceleration": "3600",
    "inner_wall_jerk": "10",
    "inner_wall_line_width": "0.44",
    "inner_wall_speed": "300",
    "instantiation": "true",
    "internal_solid_infill_line_width": "0.44",
    "internal_solid_infill_speed": "300",
    "layer_height": "0.22",
    "name": "0.22mm Standard @Construct 1",
    "only_one_wall_top": "1",
    "outer_wall_acceleration": "2800",
    "outer_wall_jerk": "8",
    "outer_wall_line_width": "0.42",
    "outer_wall_speed": "140",
    "overhang_2_4_speed": "60",
    "overhang_3_4_speed": "40",
    "overhang_4_4_speed": "15",
    "precise_outer_wall": "1",
    "setting_id": "GP004",
    "skirt_loops": "1",
    "slow_down_layers": "1",
    "sparse_infill_density": "12%",
    "sparse_infill_line_width": "0.4",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "300",
    "support_speed": "300",
    "top_shell_layers": "3",
    "top_surface_acceleration": "2400",
    "top_surface_jerk": "8",
    "top_surface_line_width": "0.44",
    "top_surface_speed": "160",
    "travel_acceleration": "6400",
    "travel_speed": "320",
    "type": "process",
    "wall_loops": "2",
    "wall_sequence": "inner-outer-inner wall"
  },
  "process/0.25mm Industrial @Construct 1.json": {
    "bottom_shell_layers": "4",
    "bridge_speed": "60",
    "compatible_printers": [
      "Construct 1 0.4 nozzle"
    ],
    "default_acceleration": "4000",
    "default_jerk": "12",
    "enable_arc_fitting": "1",
    "extra_perimeters_on_overhangs": "1",
    "from": "system",
    "gap_infill_speed": "125",
    "infill_jerk": "12",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "2000",
    "initial_layer_infill_speed": "100",
    "initial_layer_jerk": "8",
    "initial_layer_print_height": "0.32",
    "initial_layer_speed": "50",
    "inner_wall_acceleration": "3200",
    "inner_wall_jerk": "8",
    "inner_wall_line_width": "0.44",
    "inner_wall_speed": "240",
    "instantiation": "true",
    "internal_solid_infill_line_width": "0.44",
    "internal_solid_infill_speed": "300",
    "layer_height": "0.22",
    "line_width": "0.44",
    "name": "0.25mm Industrial @Construct 1",
    "only_one_wall_top": "1",
    "outer_wall_acceleration": "2400",
    "outer_wall_jerk": "8",
    "outer_wall_line_width": "0.44",
    "outer_wall_speed": "140",
    "overhang_2_4_speed": "60",
    "overhang_3_4_speed": "40",
    "overhang_4_4_speed": "15",
    "precise_outer_wall": "1",
    "setting_id": "GP004",
    "skirt_loops": "1",
    "slow_down_layers": "1",
    "sparse_infill_density": "30%",
    "sparse_infill_line_width": "0.62",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "300",
    "support_speed": "300",
    "top_surface_acceleration": "2000",
    "top_surface_jerk": "8",
    "top_surface_line_width": "0.44",
    "top_surface_speed": "160",
    "travel_acceleration": "6400",
    "travel_speed": "320",
    "type": "process",
    "wall_loops": "3",
    "wall_sequence": "inner-outer-inner wall"
  },
  "process/0.30mm Draft @Construct 1.json": {
    "bottom_shell_layers": "2",
    "bridge_speed": "60",
    "compatible_printers": [
      "Construct 1 0.4 nozzle"
    ],
    "default_acceleration": "4000",
    "default_jerk": "13",
    "enable_arc_fitting": "1",
    "extra_perimeters_on_overhangs": "1",
    "from": "system",
    "gap_infill_speed": "200",
    "infill_jerk": "12",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "2000",
    "initial_layer_infill_speed": "100",
    "initial_layer_jerk": "8",
    "initial_layer_print_height": "0.32",
    "initial_layer_speed": "50",
    "inner_wall_acceleration": "4000",
    "inner_wall_jerk": "10",
    "inner_wall_line_width": "0.44",
    "inner_wall_speed": "300",
    "instantiation": "true",
    "internal_solid_infill_line_width": "0.44",
    "internal_solid_infill_speed": "300",
    "layer_height": "0.3",
    "line_width": "0.44",
    "name": "0.30mm Draft @Construct 1",
    "only_one_wall_top": "1",
    "outer_wall_acceleration": "4000",
    "outer_wall_jerk": "8",
    "outer_wall_line_width": "0.44",
    "outer_wall_speed": "200",
    "overhang_2_4_speed": "60",
    "overhang_3_4_speed": "40",
    "overhang_4_4_speed": "15",
    "precise_outer_wall": "1",
    "setting_id": "GP004",
    "skirt_loops": "1",
    "slow_down_layers": "1",
    "sparse_infill_density": "12%",
    "sparse_infill_line_width": "0.4",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "300",
    "support_speed": "300",
    "top_shell_layers": "2",
    "top_surface_acceleration": "3000",
    "top_surface_jerk": "12",
    "top_surface_line_width": "0.44",
    "top_surface_speed": "200",
    "travel_acceleration": "6400",
    "travel_speed": "320",
    "type": "process",
    "wall_loops": "2",
    "wall_sequence": "inner-outer-inner wall"
  },
  "process/0.30mm Industrial @Construct 1 XL.json": {
    "bottom_shell_layers": "4",
    "compatible_printers": [
      "Construct 1 XL 0.6 nozzle"
    ],
    "default_acceleration": "4000",
    "default_jerk": "12",
    "enable_arc_fitting": "1",
    "extra_perimeters_on_overhangs": "1",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "140",
    "infill_jerk": "12",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "1400",
    "initial_layer_infill_speed": "100",
    "initial_layer_jerk": "8",
    "initial_layer_line_width": "0.72",
    "initial_layer_print_height": "0.32",
    "initial_layer_speed": "50",
    "inner_wall_acceleration": "3200",
    "inner_wall_jerk": "8",
    "inner_wall_line_width": "0.66",
    "inner_wall_speed": "240",
    "instantiation": "true",
    "internal_solid_infill_line_width": "0.62",
    "internal_solid_infill_speed": "240",
    "layer_height": "0.3",
    "line_width": "0.62",
    "name": "0.30mm Industrial @Construct 1 XL",
    "only_one_wall_top": "1",
    "outer_wall_acceleration": "2400",
    "outer_wall_jerk": "8",
    "outer_wall_line_width": "0.62",
    "outer_wall_speed": "140",
    "precise_outer_wall": "1",
    "print_settings_id": "",
    "setting_id": "GP004",
    "skirt_loops": "1",
    "slow_down_layers": "1",
    "sparse_infill_density": "30%",
    "sparse_infill_line_width": "0.82",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "240",
    "support_line_width": "0.6",
    "top_shell_layers": "5",
    "top_surface_acceleration": "2000",
    "top_surface_jerk": "8",
    "top_surface_line_width": "0.66",
    "top_surface_speed": "140",
    "travel_acceleration": "6000",
    "travel_speed": "320",
    "type": "process",
    "wall_loops": "3",
    "wall_sequence": "inner-outer-inner wall"
  },
  "process/0.30mm Standard @Construct 1 XL.json": {
    "bridge_speed": "60",
    "compatible_printers": [
      "Construct 1 XL 0.6 nozzle"
    ],
    "default_acceleration": "4000",
    "default_jerk": "13",
    "enable_arc_fitting": "1",
    "extra_perimeters_on_overhangs": "1",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "140",
    "infill_jerk": "12",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "1400",
    "initial_layer_infill_speed": "100",
    "initial_layer_jerk": "8",
    "initial_layer_line_width": "0.72",
    "initial_layer_print_height": "0.32",
    "initial_layer_speed": "80",
    "inner_wall_acceleration": "3600",
    "inner_wall_jerk": "10",
    "inner_wall_line_width": "0.66",
    "inner_wall_speed": "300",
    "instantiation": "true",
    "internal_solid_infill_line_width": "0.62",
    "internal_solid_infill_speed": "300",
    "layer_height": "0.3",
    "line_width": "0.64",
    "name": "0.30mm Standard @Construct 1 XL",
    "only_one_wall_top": "1",
    "outer_wall_acceleration": "2800",
    "outer_wall_jerk": "8",
    "outer_wall_line_width": "0.64",
    "outer_wall_speed": "140",
    "overhang_2_4_speed": "60",
    "overhang_3_4_speed": "40",
    "overhang_4_4_speed": "15",
    "precise_outer_wall": "1",
    "print_settings_id": "",
    "setting_id": "GP004",
    "skirt_loops": "1",
    "slow_down_layers": "1",
    "sparse_infill_density": "12%",
    "sparse_infill_line_width": "0.64",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "300",
    "support_line_width": "0.6",
    "support_speed": "300",
    "top_surface_acceleration": "2400",
    "top_surface_jerk": "8",
    "top_surface_line_width": "0.66",
    "top_surface_speed": "140",
    "travel_acceleration": "6400",
    "travel_speed": "320",
    "type": "process",
    "wall_loops": "2",
    "wall_sequence": "inner-outer-inner wall"
  },
  "process/0.38mm Draft @Construct 1 XL.json": {
    "bottom_shell_layers": "2",
    "bridge_speed": "60",
    "compatible_printers": [
      "Construct 1 XL 0.6 nozzle"
    ],
    "default_acceleration": "4000",
    "default_jerk": "13",
    "enable_arc_fitting": "1",
    "extra_perimeters_on_overhangs": "1",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "200",
    "infill_jerk": "12",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "2000",
    "initial_layer_infill_speed": "100",
    "initial_layer_jerk": "8",
    "initial_layer_line_width": "0.72",
    "initial_layer_print_height": "0.32",
    "initial_layer_speed": "100",
    "inner_wall_acceleration": "4000",
    "inner_wall_jerk": "10",
    "inner_wall_line_width": "0.66",
    "inner_wall_speed": "300",
    "instantiation": "true",
    "internal_solid_infill_line_width": "0.64",
    "internal_solid_infill_speed": "300",
    "layer_height": "0.38",
    "line_width": "0.64",
    "name": "0.38mm Draft @Construct 1 XL",
    "only_one_wall_top": "1",
    "outer_wall_acceleration": "4000",
    "outer_wall_jerk": "8",
    "outer_wall_line_width": "0.64",
    "outer_wall_speed": "200",
    "overhang_2_4_speed": "60",
    "overhang_3_4_speed": "40",
    "overhang_4_4_speed": "15",
    "precise_outer_wall": "1",
    "print_settings_id": "",
    "setting_id": "GP004",
    "skirt_loops": "1",
    "slow_down_layers": "1",
    "sparse_infill_density": "12%",
    "sparse_infill_line_width": "0.64",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "300",
    "support_line_width": "0.6",
    "support_speed": "300",
    "top_shell_layers": "3",
    "top_surface_acceleration": "3000",
    "top_surface_jerk": "12",
    "top_surface_line_width": "0.66",
    "top_surface_speed": "200",
    "travel_acceleration": "6400",
    "travel_speed": "320",
    "type": "process",
    "wall_loops": "2",
    "wall_sequence": "inner-outer-inner wall"
  },
  "process/fdm_process_common.json": {
    "adaptive_layer_height": "0",
    "bottom_shell_layers": "3",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "1",
    "bridge_no_support": "0",
    "bridge_speed": "40",
    "brim_object_gap": "0.1",
    "brim_width": "5",
    "compatible_printers": [],
    "compatible_printers_condition": "",
    "default_acceleration": "3000",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "0",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0",
    "enable_arc_fitting": "1",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "100",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "10%",
    "initial_layer_acceleration": "1500",
    "initial_layer_infill_speed": "65",
    "initial_layer_line_width": "120%",
    "initial_layer_print_height": "0.24",
    "initial_layer_speed": "45",
    "inner_wall_acceleration": "2800",
    "inner_wall_line_width": "110%",
    "inner_wall_speed": "140",
    "instantiation": "false",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "120%",
    "internal_solid_infill_speed": "200",
    "ironing_flow": "10%",
    "ironing_spacing": "0.20",
    "ironing_speed": "40",
    "ironing_type": "no ironing",
    "layer_height": "0.2",
    "line_width": "110%",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "15",
    "name": "fdm_process_common",
    "outer_wall_acceleration": "2000",
    "outer_wall_line_width": "100%",
    "outer_wall_speed": "120",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "60",
    "overhang_3_4_speed": "40",
    "overhang_4_4_speed": "15",
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
    "sparse_infill_density": "12%",
    "sparse_infill_line_width": "110%",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "200",
    "spiral_mode": "0",
    "standby_temperature_delta": "-10",
    "support_base_pattern": "rectilinear",
    "support_base_pattern_spacing": "2.5",
    "support_bottom_z_distance": "0.24",
    "support_filament": "0",
    "support_interface_bottom_layers": "2",
    "support_interface_filament": "0",
    "support_interface_loop_pattern": "0",
    "support_interface_spacing": "0.5",
    "support_interface_speed": "120",
    "support_interface_top_layers": "2",
    "support_line_width": "98%",
    "support_object_xy_distance": "0.35",
    "support_on_build_plate_only": "1",
    "support_speed": "250",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.24",
    "support_type": "tree(auto)",
    "top_shell_layers": "4",
    "top_shell_thickness": "0.8",
    "top_surface_acceleration": "2000",
    "top_surface_line_width": "94%",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "100",
    "travel_acceleration": "6000",
    "travel_speed": "320",
    "tree_support_branch_angle": "30",
    "tree_support_wall_count": "0",
    "tree_support_with_infill": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "2",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  }
}

FILAMENT = {
  "filament/C1 Generic High Flow PETG.json": {
    "compatible_printers": [
      "Construct 1 0.4 nozzle",
      "Construct 1 XL 0.6 nozzle"
    ],
    "fan_cooling_layer_time": [
      "20"
    ],
    "fan_max_speed": [
      "100"
    ],
    "fan_min_speed": [
      "30"
    ],
    "filament_flow_ratio": [
      "0.98"
    ],
    "filament_id": "GFG99",
    "filament_max_volumetric_speed": [
      "43"
    ],
    "filament_start_gcode": [
      "; filament start gcode\n"
    ],
    "from": "system",
    "inherits": "fdm_filament_pet",
    "instantiation": "true",
    "name": "C1 Generic High Flow PETG",
    "nozzle_temperature": [
      "270"
    ],
    "nozzle_temperature_initial_layer": [
      "270"
    ],
    "nozzle_temperature_range_high": [
      "275"
    ],
    "nozzle_temperature_range_low": [
      "230"
    ],
    "overhang_fan_speed": [
      "100"
    ],
    "reduce_fan_stop_start_freq": [
      "1"
    ],
    "setting_id": "GFSG99",
    "slow_down_for_layer_cooling": [
      "1"
    ],
    "slow_down_layer_time": [
      "6"
    ],
    "slow_down_min_speed": [
      "15"
    ],
    "type": "filament"
  },
  "filament/C1 Generic PETG.json": {
    "compatible_printers": [
      "Construct 1 0.4 nozzle",
      "Construct 1 XL 0.6 nozzle"
    ],
    "fan_cooling_layer_time": [
      "20"
    ],
    "fan_max_speed": [
      "100"
    ],
    "fan_min_speed": [
      "30"
    ],
    "filament_flow_ratio": [
      "0.98"
    ],
    "filament_id": "GFG99",
    "filament_max_volumetric_speed": [
      "35"
    ],
    "filament_start_gcode": [
      "; filament start gcode\n"
    ],
    "from": "system",
    "inherits": "fdm_filament_pet",
    "instantiation": "true",
    "name": "C1 Generic PETG",
    "overhang_fan_speed": [
      "80"
    ],
    "reduce_fan_stop_start_freq": [
      "1"
    ],
    "setting_id": "GFSG99",
    "slow_down_for_layer_cooling": [
      "1"
    ],
    "slow_down_layer_time": [
      "6"
    ],
    "slow_down_min_speed": [
      "15"
    ],
    "type": "filament"
  },
  "filament/C1 Generic PLA.json": {
    "compatible_printers": [
      "Construct 1 0.4 nozzle",
      "Construct 1 XL 0.6 nozzle"
    ],
    "filament_flow_ratio": [
      "0.98"
    ],
    "filament_id": "GFL99",
    "filament_max_volumetric_speed": [
      "30"
    ],
    "from": "system",
    "hot_plate_temp": [
      "62"
    ],
    "hot_plate_temp_initial_layer": [
      "68"
    ],
    "inherits": "fdm_filament_pla",
    "instantiation": "true",
    "name": "C1 Generic PLA",
    "setting_id": "GFSL99",
    "slow_down_layer_time": [
      "4"
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
      "62"
    ],
    "cool_plate_temp_initial_layer": [
      "66"
    ],
    "eng_plate_temp": [
      "62"
    ],
    "eng_plate_temp_initial_layer": [
      "66"
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
      "62"
    ],
    "hot_plate_temp_initial_layer": [
      "66"
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
      "62"
    ],
    "textured_plate_temp_initial_layer": [
      "66"
    ],
    "type": "filament"
  },
  "filament/fdm_filament_pet.json": {
    "close_fan_the_first_x_layers": [
      "3"
    ],
    "eng_plate_temp": [
      "75"
    ],
    "eng_plate_temp_initial_layer": [
      "80"
    ],
    "fan_cooling_layer_time": [
      "20"
    ],
    "fan_max_speed": [
      "100"
    ],
    "fan_min_speed": [
      "30"
    ],
    "filament_cost": [
      "25"
    ],
    "filament_density": [
      "1.27"
    ],
    "filament_max_volumetric_speed": [
      "35"
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
      "230"
    ],
    "overhang_fan_speed": [
      "70"
    ],
    "reduce_fan_stop_start_freq": [
      "1"
    ],
    "slow_down_for_layer_cooling": [
      "1"
    ],
    "temperature_vitrification": [
      "75"
    ],
    "type": "filament"
  },
  "filament/fdm_filament_pla.json": {
    "close_fan_the_first_x_layers": [
      "1"
    ],
    "cool_plate_temp": [
      "40"
    ],
    "cool_plate_temp_initial_layer": [
      "40"
    ],
    "eng_plate_temp": [
      "62"
    ],
    "eng_plate_temp_initial_layer": [
      "68"
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
      "25"
    ],
    "filament_density": [
      "1.24"
    ],
    "filament_max_volumetric_speed": [
      "30"
    ],
    "filament_start_gcode": [
      "; filament start gcode\n"
    ],
    "filament_type": [
      "PLA"
    ],
    "from": "system",
    "hot_plate_temp": [
      "62"
    ],
    "hot_plate_temp_initial_layer": [
      "68"
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
      "20"
    ],
    "temperature_vitrification": [
      "60"
    ],
    "type": "filament"
  }
}

MISC = {}

ASSETS = [
  "Construct 1 XL_cover.png",
  "Construct 1_cover.png",
  "construct_1_buildplate_model.stl",
  "construct_1_xl_buildplate_model.stl"
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
