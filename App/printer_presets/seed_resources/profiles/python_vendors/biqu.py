from __future__ import annotations

VENDOR = "BIQU"
INDEX = {
  "description": "BIQU configurations",
  "filament_list": [],
  "force_update": "0",
  "machine_list": [
    {
      "name": "fdm_machine_common",
      "sub_path": "machine/fdm_machine_common.json"
    },
    {
      "name": "fdm_biqu_common",
      "sub_path": "machine/fdm_biqu_common.json"
    },
    {
      "name": "fdm_klipper_common",
      "sub_path": "machine/fdm_klipper_common.json"
    },
    {
      "name": "BIQU B1 (0.4 nozzle)",
      "sub_path": "machine/BIQU B1 (0.4 nozzle).json"
    },
    {
      "name": "BIQU BX (0.4 nozzle)",
      "sub_path": "machine/BIQU BX (0.4 nozzle).json"
    },
    {
      "name": "BIQU Hurakan (0.4 nozzle)",
      "sub_path": "machine/BIQU Hurakan (0.4 nozzle).json"
    }
  ],
  "machine_model_list": [
    {
      "name": "BIQU B1",
      "sub_path": "machine/BIQU B1.json"
    },
    {
      "name": "BIQU BX",
      "sub_path": "machine/BIQU BX.json"
    },
    {
      "name": "BIQU Hurakan",
      "sub_path": "machine/BIQU Hurakan.json"
    }
  ],
  "name": "BIQU",
  "process_list": [
    {
      "name": "fdm_process_common",
      "sub_path": "process/fdm_process_common.json"
    },
    {
      "name": "fdm_process_biqu_common",
      "sub_path": "process/fdm_process_biqu_common.json"
    },
    {
      "name": "0.12mm Fine @BIQU B1 (0.4 nozzle)",
      "sub_path": "process/0.12mm Fine @BIQU B1 (0.4 nozzle).json"
    },
    {
      "name": "0.12mm Fine @BIQU BX (0.4 nozzle)",
      "sub_path": "process/0.12mm Fine @BIQU BX (0.4 nozzle).json"
    },
    {
      "name": "0.12mm Fine @BIQU Hurakan (0.4 nozzle)",
      "sub_path": "process/0.12mm Fine @BIQU Hurakan (0.4 nozzle).json"
    },
    {
      "name": "0.15mm Optimal @BIQU B1 (0.4 nozzle)",
      "sub_path": "process/0.15mm Optimal @BIQU B1 (0.4 nozzle).json"
    },
    {
      "name": "0.15mm Optimal @BIQU BX (0.4 nozzle)",
      "sub_path": "process/0.15mm Optimal @BIQU BX (0.4 nozzle).json"
    },
    {
      "name": "0.20mm Standard @BIQU B1 (0.4 nozzle)",
      "sub_path": "process/0.20mm Standard @BIQU B1 (0.4 nozzle).json"
    },
    {
      "name": "0.20mm Standard @BIQU BX (0.4 nozzle)",
      "sub_path": "process/0.20mm Standard @BIQU BX (0.4 nozzle).json"
    },
    {
      "name": "0.24mm Draft @BIQU B1 (0.4 nozzle)",
      "sub_path": "process/0.24mm Draft @BIQU B1 (0.4 nozzle).json"
    },
    {
      "name": "0.24mm Draft @BIQU BX (0.4 nozzle)",
      "sub_path": "process/0.24mm Draft @BIQU BX (0.4 nozzle).json"
    },
    {
      "name": "fdm_process_hurakan_common",
      "sub_path": "process/fdm_process_hurakan_common.json"
    },
    {
      "name": "0.15mm Optimal @BIQU Hurakan (0.4 nozzle)",
      "sub_path": "process/0.15mm Optimal @BIQU Hurakan (0.4 nozzle).json"
    },
    {
      "name": "0.20mm Standard @BIQU Hurakan (0.4 nozzle)",
      "sub_path": "process/0.20mm Standard @BIQU Hurakan (0.4 nozzle).json"
    },
    {
      "name": "0.24mm Draft @BIQU Hurakan (0.4 nozzle)",
      "sub_path": "process/0.24mm Draft @BIQU Hurakan (0.4 nozzle).json"
    }
  ],
  "version": "02.03.01.10"
}

MACHINE = {
  "machine/BIQU B1 (0.4 nozzle).json": {
    "auxiliary_fan": "0",
    "default_print_profile": "0.20mm Standard @BIQU B1 (0.4 nozzle)",
    "deretraction_speed": [
      "70"
    ],
    "from": "system",
    "gcode_flavor": "marlin",
    "inherits": "fdm_biqu_common",
    "instantiation": "true",
    "machine_end_gcode": ";BIQU B1 Default End Gcode\nG91;Relative positioning\nG1 E-2 F2700;Retract a bit\nG1 E-2 Z0.2 F2400;Retract a bit more and raise Z\nG1 X5 Y5 F3000;Wipe out\nG1 Z10;Raise Z by 10mm\nG90;Return to absolute positioning\nG1 X0 Y{print_bed_max[1]};\nM106 S0;Turn-off fan\nM104 S0;Turn-off hotend\nM140 S0;Turn-off bed\nM84 X Y E;Disable all steppers but Z",
    "machine_max_acceleration_e": [
      "10000"
    ],
    "machine_max_acceleration_extruding": [
      "1000"
    ],
    "machine_max_acceleration_retracting": [
      "1000"
    ],
    "machine_max_acceleration_x": [
      "1000"
    ],
    "machine_max_acceleration_y": [
      "1000"
    ],
    "machine_max_acceleration_z": [
      "100"
    ],
    "machine_max_jerk_e": [
      "5"
    ],
    "machine_max_jerk_x": [
      "10"
    ],
    "machine_max_jerk_y": [
      "10"
    ],
    "machine_max_jerk_z": [
      "0.3"
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
    "machine_start_gcode": "; BIQU B1 Start G-code\nM117 Getting the bed up to temp!\nM140 S[first_layer_bed_temperature]; Set Heat Bed temperature\nM190 S[first_layer_bed_temperature]; Wait for Heat Bed temperature\nM117 Getting the extruder up to temp!\nM104 S[first_layer_temperature]; Set Extruder temperature\nG92 E0; Reset Extruder\nM117 Homing axes\nG28; Home all axes\nM109 S[first_layer_temperature]; Wait for Extruder temperature\nG1 Z2.0 F3000; Move Z Axis up little to prevent scratching of Heat Bed\nG1 X4.1 Y20 Z0.3 F5000.0; Move to start position\nM117 Purging\nG1 X4.1 Y200.0 Z0.3 F1500.0 E15; Draw the first line\nG1 X4.4 Y200.0 Z0.3 F5000.0; Move to side a little\nG1 X4.4 Y20 Z0.3 F1500.0 E30; Draw the second line\nG92 E0; Reset Extruder\nM117 Lets make\nG1 Z2.0 F3000; Move Z Axis up little to prevent scratching of Heat Bed\nG1 X5 Y20 Z0.3 F5000.0; Move over to prevent blob squish",
    "max_layer_height": [
      "0.32"
    ],
    "min_layer_height": [
      "0.10"
    ],
    "name": "BIQU B1 (0.4 nozzle)",
    "nozzle_diameter": [
      "0.4"
    ],
    "nozzle_type": "undefine",
    "printable_area": [
      "0x0",
      "235x0",
      "235x235",
      "0x235"
    ],
    "printable_height": "270",
    "printer_model": "BIQU B1",
    "printer_variant": "0.4",
    "retraction_length": [
      "7"
    ],
    "retraction_minimum_travel": [
      "1.5"
    ],
    "retraction_speed": [
      "70"
    ],
    "setting_id": "GM001",
    "type": "machine"
  },
  "machine/BIQU B1.json": {
    "bed_model": "BIQU_B1_buildplate_model.stl",
    "bed_texture": "BIQU_B1_buildplate_texture.png",
    "default_materials": "Generic PLA @System;Generic PETG @System;Generic ABS @System",
    "family": "BIQU",
    "hotend_model": "biqu_b1_hotend.stl",
    "machine_tech": "FFF",
    "model_id": "B1",
    "name": "BIQU B1",
    "nozzle_diameter": "0.4",
    "type": "machine_model"
  },
  "machine/BIQU BX (0.4 nozzle).json": {
    "auxiliary_fan": "0",
    "default_print_profile": "0.20mm Standard @BIQU BX (0.4 nozzle)",
    "deretraction_speed": [
      "70"
    ],
    "from": "system",
    "gcode_flavor": "marlin",
    "inherits": "fdm_biqu_common",
    "instantiation": "true",
    "machine_end_gcode": "; BIQU BX Default End Gcode\nG91;Relative positioning\nG1 E-2 F2700;Retract a bit\nG1 E-2 Z0.2 F2400;Retract a bit more and raise Z\nG1 X5 Y5 F3000;Wipe out\nG1 Z10;Raise Z by 10mm\nG90;Return to absolute positioning\nG1 X0 Y{print_bed_max[1]};TaDaaaa\nM106 S0;Turn-off fan\nM104 S0;Turn-off hotend\nM140 S0;Turn-off bed\nM84 X Y E;Disable all steppers but Z",
    "machine_max_acceleration_e": [
      "10000"
    ],
    "machine_max_acceleration_extruding": [
      "1000"
    ],
    "machine_max_acceleration_retracting": [
      "1000"
    ],
    "machine_max_acceleration_x": [
      "1000"
    ],
    "machine_max_acceleration_y": [
      "1000"
    ],
    "machine_max_acceleration_z": [
      "100"
    ],
    "machine_max_jerk_e": [
      "5"
    ],
    "machine_max_jerk_x": [
      "10"
    ],
    "machine_max_jerk_y": [
      "10"
    ],
    "machine_max_jerk_z": [
      "0.3"
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
    "machine_start_gcode": "; BIQU BX Start G-code\n;M117 Initial homing sequence; Home so that the probe is positioned to heat\nG28\nM117 Probe heating position\nG0 X65 Y5 Z1; Move the probe to the heating position.\nM117 Getting the heaters up to temp!\nM104 S140; Set Extruder temperature, no wait\nM140 S60; Set Heat Bed temperature\nM190 S60; Wait for Heat Bed temperature\nM117 Waiting for probe to warm; Wait another 90s for the probe to absorb heat.\nG4 S90\nM117 Post warming re-home\nG28; Home all axes again after warming\nM117 Z-Dance of my people\nG34\nM117 ABL Probing\nG29\nM900 K0 L0 T0;Edit the K and L values if you have calibrated a k factor for your filament\nM900 T0 S0\nG1 Z2.0 F3000; Move Z Axis up little to prevent scratching of Heat Bed\nG1 X4.1 Y10 Z0.3 F5000.0; Move to start position\nM117 Getting the extruder up to temp\nM140 S[first_layer_bed_temperature]; Set Heat Bed temperature\nM104 S[first_layer_temperature]; Set Extruder temperature\nM109 S[first_layer_temperature]; Wait for Extruder temperature\nM190 S[first_layer_bed_temperature]; Wait for Heat Bed temperature\nG92 E0; Reset Extruder\nM117 Purging\nG1 X4.1 Y200.0 Z0.3 F1500.0 E15; Draw the first line\nG1 X4.4 Y200.0 Z0.3 F5000.0; Move to side a little\nG1 X4.4 Y20 Z0.3 F1500.0 E30; Draw the second line\nG92 E0; Reset Extruder\nM117 Lets make\nG1 X8 Y20 Z0.3 F5000.0; Move over to prevent blob squish",
    "max_layer_height": [
      "0.32"
    ],
    "min_layer_height": [
      "0.10"
    ],
    "name": "BIQU BX (0.4 nozzle)",
    "nozzle_diameter": [
      "0.4"
    ],
    "nozzle_type": "undefine",
    "printable_area": [
      "0x0",
      "250x0",
      "250x250",
      "0x250"
    ],
    "printable_height": "250",
    "printer_model": "BIQU BX",
    "printer_variant": "0.4",
    "retraction_length": [
      "1"
    ],
    "retraction_minimum_travel": [
      "1.5"
    ],
    "retraction_speed": [
      "40"
    ],
    "setting_id": "GM001",
    "type": "machine"
  },
  "machine/BIQU BX.json": {
    "bed_model": "BIQU_BX_buildplate_model.stl",
    "bed_texture": "BIQU_BX_buildplate_texture.png",
    "default_materials": "Generic PLA @System;Generic PETG @System;Generic ABS @System",
    "family": "BIQU",
    "hotend_model": "biqu_bx_hotend.stl",
    "machine_tech": "FFF",
    "model_id": "BX",
    "name": "BIQU BX",
    "nozzle_diameter": "0.4",
    "type": "machine_model"
  },
  "machine/BIQU Hurakan (0.4 nozzle).json": {
    "auxiliary_fan": "0",
    "bed_exclude_area": [
      "0x0"
    ],
    "before_layer_change_gcode": ";BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n",
    "change_filament_gcode": "",
    "default_filament_profile": [
      "Generic PLA @System"
    ],
    "default_print_profile": "0.20mm Standard @BIQU Hurakan (0.4 nozzle)",
    "deretraction_speed": [
      "40"
    ],
    "extruder_clearance_height_to_lid": "350",
    "extruder_clearance_height_to_rod": "60",
    "extruder_clearance_radius": "50",
    "from": "system",
    "inherits": "fdm_klipper_common",
    "instantiation": "true",
    "layer_change_gcode": ";AFTER_LAYER_CHANGE\n;[layer_z]",
    "machine_end_gcode": "END_PRINT",
    "machine_max_acceleration_e": [
      "10000",
      "10000"
    ],
    "machine_max_acceleration_extruding": [
      "3000",
      "3000"
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
      "500"
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
      "180",
      "180"
    ],
    "machine_max_speed_y": [
      "180",
      "180"
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
    "machine_pause_gcode": "PAUSE\n",
    "machine_start_gcode": "START_PRINT EXTRUDER_TEMP=[nozzle_temperature_initial_layer] BED_TEMP=[bed_temperature_initial_layer_single]\n",
    "max_layer_height": [
      "0.32"
    ],
    "min_layer_height": [
      "0.08"
    ],
    "name": "BIQU Hurakan (0.4 nozzle)",
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
    "printable_height": "270",
    "printer_model": "BIQU Hurakan",
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
      "4.5"
    ],
    "retraction_minimum_travel": [
      "1"
    ],
    "retraction_speed": [
      "40"
    ],
    "scan_first_layer": "0",
    "setting_id": "GM001",
    "silent_mode": "0",
    "single_extruder_multi_material": "1",
    "type": "machine",
    "wipe": [
      "1"
    ],
    "z_hop": [
      "0"
    ],
    "z_hop_types": "Normal Lift"
  },
  "machine/BIQU Hurakan.json": {
    "bed_model": "BIQU_Hurakan_buildplate_model.stl",
    "bed_texture": "BIQU_Hurakan_buildplate_model.png",
    "default_materials": "Generic PLA @System;Generic PETG @System;Generic ABS @System",
    "family": "BIQU",
    "hotend_model": "biqu_hurakan_hotend.stl",
    "machine_tech": "FFF",
    "model_id": "Hurakan",
    "name": "BIQU Hurakan",
    "nozzle_diameter": "0.4",
    "type": "machine_model"
  },
  "machine/fdm_biqu_common.json": {
    "auxiliary_fan": "0",
    "bed_exclude_area": [
      "0x0"
    ],
    "change_filament_gcode": "",
    "default_filament_profile": [
      "Generic PLA @System"
    ],
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
    "machine_end_gcode": "{if max_layer_z < printable_height}G1 Z{min(max_layer_z+2, printable_height)} F600 ; Move print head up{endif}\nG1 X5 Y{print_bed_max[1]*0.8} F{travel_speed*60} ; present print\n{if max_layer_z < printable_height-10}G1 Z{min(max_layer_z+70, printable_height-10)} F600 ; Move print head further up{endif}\n{if max_layer_z < printable_height*0.6}G1 Z{printable_height*0.6} F600 ; Move print head further up{endif}\nM140 S0 ; turn off heatbed\nM104 S0 ; turn off temperature\nM107 ; turn off fan\nM84 X Y E ; disable motors",
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
      "500",
      "500"
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
    "machine_start_gcode": "G90 ; use absolute coordinates\nM83 ; extruder relative mode\nM140 S[bed_temperature_initial_layer] ; set final bed temp\nM104 S150 ; set temporary nozzle temp to prevent oozing during homing\nG4 S10 ; allow partial nozzle warmup\nG28 ; home all axis\nG1 Z50 F240\nG1 X2 Y10 F3000\nM104 S[nozzle_temperature_initial_layer] ; set final nozzle temp\nM190 S[bed_temperature_initial_layer] ; wait for bed temp to stabilize\nM109 S[nozzle_temperature_initial_layer] ; wait for nozzle temp to stabilize\nG1 Z0.28 F240\nG92 E0\nG1 Y140 E10 F1500 ; prime the nozzle\nG1 X2.3 F5000\nG92 E0\nG1 Y10 E10 F1200 ; prime the nozzle\nG92 E0",
    "max_layer_height": [
      "0.32"
    ],
    "min_layer_height": [
      "0.08"
    ],
    "name": "fdm_biqu_common",
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
  "machine/fdm_klipper_common.json": {
    "auxiliary_fan": "0",
    "bed_exclude_area": [
      "0x0"
    ],
    "before_layer_change_gcode": ";BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n",
    "change_filament_gcode": "",
    "default_filament_profile": [
      "Generic PLA @System"
    ],
    "deretraction_speed": [
      "40"
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
      "500",
      "500"
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
      "5"
    ],
    "retraction_minimum_travel": [
      "1"
    ],
    "retraction_speed": [
      "60"
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
    ],
    "z_lift_type": "NormalLift"
  }
}

PROCESS = {
  "process/0.12mm Fine @BIQU B1 (0.4 nozzle).json": {
    "bottom_shell_layers": "5",
    "compatible_printers": [
      "BIQU B1 (0.4 nozzle)"
    ],
    "from": "system",
    "inherits": "fdm_process_biqu_common",
    "instantiation": "true",
    "layer_height": "0.12",
    "name": "0.12mm Fine @BIQU B1 (0.4 nozzle)",
    "setting_id": "GP004",
    "top_shell_layers": "6",
    "type": "process"
  },
  "process/0.12mm Fine @BIQU BX (0.4 nozzle).json": {
    "bottom_shell_layers": "5",
    "compatible_printers": [
      "BIQU BX (0.4 nozzle)"
    ],
    "from": "system",
    "inherits": "fdm_process_biqu_common",
    "instantiation": "true",
    "layer_height": "0.12",
    "name": "0.12mm Fine @BIQU BX (0.4 nozzle)",
    "setting_id": "GP004",
    "top_shell_layers": "6",
    "type": "process"
  },
  "process/0.12mm Fine @BIQU Hurakan (0.4 nozzle).json": {
    "bottom_shell_layers": "5",
    "compatible_printers": [
      "BIQU Hurakan (0.4 nozzle)"
    ],
    "from": "system",
    "inherits": "fdm_process_biqu_common",
    "instantiation": "true",
    "layer_height": "0.12",
    "name": "0.12mm Fine @BIQU Hurakan (0.4 nozzle)",
    "setting_id": "GP004",
    "top_shell_layers": "6",
    "type": "process"
  },
  "process/0.15mm Optimal @BIQU B1 (0.4 nozzle).json": {
    "bottom_shell_layers": "4",
    "compatible_printers": [
      "BIQU B1 (0.4 nozzle)"
    ],
    "from": "system",
    "inherits": "fdm_process_biqu_common",
    "instantiation": "true",
    "layer_height": "0.15",
    "name": "0.15mm Optimal @BIQU B1 (0.4 nozzle)",
    "setting_id": "GP004",
    "top_shell_layers": "5",
    "type": "process"
  },
  "process/0.15mm Optimal @BIQU BX (0.4 nozzle).json": {
    "bottom_shell_layers": "4",
    "compatible_printers": [
      "BIQU BX (0.4 nozzle)"
    ],
    "from": "system",
    "inherits": "fdm_process_biqu_common",
    "instantiation": "true",
    "layer_height": "0.15",
    "name": "0.15mm Optimal @BIQU BX (0.4 nozzle)",
    "setting_id": "GP004",
    "top_shell_layers": "5",
    "type": "process"
  },
  "process/0.15mm Optimal @BIQU Hurakan (0.4 nozzle).json": {
    "bottom_shell_layers": "4",
    "compatible_printers": [
      "BIQU Hurakan (0.4 nozzle)"
    ],
    "from": "system",
    "inherits": "fdm_process_hurakan_common",
    "instantiation": "true",
    "layer_height": "0.15",
    "name": "0.15mm Optimal @BIQU Hurakan (0.4 nozzle)",
    "setting_id": "GP004",
    "top_shell_layers": "5",
    "type": "process"
  },
  "process/0.20mm Standard @BIQU B1 (0.4 nozzle).json": {
    "bottom_shell_layers": "3",
    "compatible_printers": [
      "BIQU B1 (0.4 nozzle)"
    ],
    "from": "system",
    "inherits": "fdm_process_biqu_common",
    "instantiation": "true",
    "layer_height": "0.2",
    "name": "0.20mm Standard @BIQU B1 (0.4 nozzle)",
    "setting_id": "GP004",
    "top_shell_layers": "4",
    "type": "process"
  },
  "process/0.20mm Standard @BIQU BX (0.4 nozzle).json": {
    "bottom_shell_layers": "3",
    "compatible_printers": [
      "BIQU BX (0.4 nozzle)"
    ],
    "from": "system",
    "inherits": "fdm_process_biqu_common",
    "instantiation": "true",
    "layer_height": "0.2",
    "name": "0.20mm Standard @BIQU BX (0.4 nozzle)",
    "setting_id": "GP004",
    "top_shell_layers": "4",
    "type": "process"
  },
  "process/0.20mm Standard @BIQU Hurakan (0.4 nozzle).json": {
    "bottom_shell_layers": "3",
    "compatible_printers": [
      "BIQU Hurakan (0.4 nozzle)"
    ],
    "from": "system",
    "inherits": "fdm_process_hurakan_common",
    "instantiation": "true",
    "layer_height": "0.2",
    "name": "0.20mm Standard @BIQU Hurakan (0.4 nozzle)",
    "setting_id": "GP004",
    "top_shell_layers": "4",
    "type": "process"
  },
  "process/0.24mm Draft @BIQU B1 (0.4 nozzle).json": {
    "bottom_shell_layers": "3",
    "compatible_printers": [
      "BIQU B1 (0.4 nozzle)"
    ],
    "from": "system",
    "inherits": "fdm_process_biqu_common",
    "instantiation": "true",
    "layer_height": "0.24",
    "name": "0.24mm Draft @BIQU B1 (0.4 nozzle)",
    "setting_id": "GP004",
    "top_shell_layers": "4",
    "top_surface_line_width": "0.45",
    "type": "process"
  },
  "process/0.24mm Draft @BIQU BX (0.4 nozzle).json": {
    "bottom_shell_layers": "3",
    "compatible_printers": [
      "BIQU BX (0.4 nozzle)"
    ],
    "from": "system",
    "inherits": "fdm_process_biqu_common",
    "instantiation": "true",
    "layer_height": "0.24",
    "name": "0.24mm Draft @BIQU BX (0.4 nozzle)",
    "setting_id": "GP004",
    "top_shell_layers": "4",
    "top_surface_line_width": "0.45",
    "type": "process"
  },
  "process/0.24mm Draft @BIQU Hurakan (0.4 nozzle).json": {
    "bottom_shell_layers": "3",
    "compatible_printers": [
      "BIQU Hurakan (0.4 nozzle)"
    ],
    "from": "system",
    "inherits": "fdm_process_hurakan_common",
    "instantiation": "true",
    "layer_height": "0.24",
    "name": "0.24mm Draft @BIQU Hurakan (0.4 nozzle)",
    "setting_id": "GP004",
    "top_shell_layers": "4",
    "top_surface_line_width": "0.45",
    "type": "process"
  },
  "process/fdm_process_biqu_common.json": {
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
    "name": "fdm_process_biqu_common",
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
    "wall_loops": "3",
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
  "process/fdm_process_hurakan_common.json": {
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
    "inherits": "fdm_process_biqu_common",
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
    "name": "fdm_process_hurakan_common",
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
    "wall_loops": "3",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  }
}

FILAMENT = {}

MISC = {}

ASSETS = [
  "BIQU B1_cover.png",
  "BIQU BX_cover.png",
  "BIQU Hurakan_cover.png",
  "BIQU_B1_buildplate_model.stl",
  "BIQU_B1_buildplate_texture.png",
  "BIQU_BX_buildplate_model.stl",
  "BIQU_BX_buildplate_texture.png",
  "BIQU_Hurakan_buildplate_model.stl",
  "BIQU_Hurakan_buildplate_texture.png"
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
