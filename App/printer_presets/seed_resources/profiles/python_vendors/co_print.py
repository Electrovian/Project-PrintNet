from __future__ import annotations

VENDOR = "Co Print"
INDEX = {
  "description": "CoPrint configurations",
  "filament_list": [
    {
      "name": "fdm_filament_common",
      "sub_path": "filament/fdm_filament_common.json"
    },
    {
      "name": "fdm_filament_pla",
      "sub_path": "filament/fdm_filament_pla.json"
    },
    {
      "name": "CoPrint Generic PLA",
      "sub_path": "filament/CoPrint Generic PLA.json"
    },
    {
      "name": "CoPrint Generic ABS",
      "sub_path": "filament/CoPrint Generic ABS.json"
    },
    {
      "name": "CoPrint Generic PETG",
      "sub_path": "filament/CoPrint Generic PETG.json"
    },
    {
      "name": "CoPrint Generic TPU",
      "sub_path": "filament/CoPrint Generic TPU.json"
    }
  ],
  "force_update": "0",
  "machine_list": [
    {
      "name": "fdm_machine_common",
      "sub_path": "machine/fdm_machine_common.json"
    },
    {
      "name": "Co Print ChromaSet 0.4 nozzle",
      "sub_path": "machine/Co Print ChromaSet 0.4 nozzle.json"
    },
    {
      "name": "Co Print ChromaSet 0.4 nozzle - Ender-3 V3",
      "sub_path": "machine/Co Print ChromaSet 0.4 nozzle - Ender-3 V3.json"
    },
    {
      "name": "Co Print ChromaSet 0.4 nozzle - Ender-3 V3 Plus",
      "sub_path": "machine/Co Print ChromaSet 0.4 nozzle - Ender-3 V3 Plus.json"
    },
    {
      "name": "Co Print ChromaSet 0.4 nozzle fast",
      "sub_path": "machine/Co Print ChromaSet 0.4 nozzle fast.json"
    },
    {
      "name": "fdm_coprint_common",
      "sub_path": "machine/fdm_coprint_common.json"
    }
  ],
  "machine_model_list": [
    {
      "name": "Co Print ChromaSet",
      "sub_path": "machine/Co Print ChromaSet.json"
    }
  ],
  "name": "Co Print",
  "process_list": [
    {
      "name": "fdm_process_common",
      "sub_path": "process/fdm_process_common.json"
    },
    {
      "name": "fdm_process_coprint_common",
      "sub_path": "process/fdm_process_coprint_common.json"
    },
    {
      "name": "0.2mm Fast @Co Print ChromaSet 0.4",
      "sub_path": "process/0.2mm Fast @Co Print ChromaSet 0.4.json"
    },
    {
      "name": "0.2mm Standard @Co Print ChromaSet 0.4",
      "sub_path": "process/0.2mm Standard @Co Print ChromaSet 0.4.json"
    }
  ],
  "version": "02.03.01.10"
}

MACHINE = {
  "machine/Co Print ChromaSet 0.4 nozzle - Ender-3 V3 Plus.json": {
    "change_filament_gcode": "FILAMENT_CHANGE LAYER_NUM=[layer_num] NEXT_EXTRUDER=[next_extruder]",
    "cooling_tube_length": [
      "0"
    ],
    "cooling_tube_retraction": [
      "0"
    ],
    "default_filament_profile": [
      "CoPrint Generic PLA"
    ],
    "default_print_profile": "0.2mm Standard @Co Print ChromaSet 0.4",
    "deretraction_speed": [
      "30"
    ],
    "enable_filament_ramming": [
      "0"
    ],
    "extra_loading_move": [
      "0"
    ],
    "extruder_clearance_height_to_lid": [
      "140"
    ],
    "extruder_clearance_height_to_rod": [
      "36"
    ],
    "extruder_clearance_radius": [
      "65"
    ],
    "from": "system",
    "gcode_flavor": "klipper",
    "high_current_on_filament_swap": [
      "0"
    ],
    "inherits": "fdm_machine_common",
    "instantiation": "true",
    "machine_end_gcode": "end_print",
    "machine_max_acceleration_e": [
      "2500"
    ],
    "machine_max_acceleration_extruding": [
      "5000"
    ],
    "machine_max_acceleration_retracting": [
      "2500"
    ],
    "machine_max_acceleration_travel": [
      "40000"
    ],
    "machine_max_acceleration_x": [
      "5000"
    ],
    "machine_max_acceleration_y": [
      "5000"
    ],
    "machine_max_acceleration_z": [
      "100"
    ],
    "machine_max_jerk_e": [
      "2.5"
    ],
    "machine_max_jerk_x": [
      "8"
    ],
    "machine_max_jerk_y": [
      "8"
    ],
    "machine_max_jerk_z": [
      "0.2"
    ],
    "machine_max_speed_e": [
      "100"
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
    "machine_start_gcode": "start_print  EXTRUDER=[initial_extruder] EXTRUDER_TEMP=[nozzle_temperature_initial_layer] BED_TEMP=[bed_temperature_initial_layer_single]",
    "max_layer_height": [
      "0.32"
    ],
    "min_layer_height": [
      "0.08"
    ],
    "name": "Co Print ChromaSet 0.4 nozzle - Ender-3 V3 Plus",
    "nozzle_diameter": [
      "0.4"
    ],
    "nozzle_volume": [
      "156"
    ],
    "parking_pos_retraction": [
      "0"
    ],
    "printable_area": [
      "0x0",
      "290x0",
      "290x283",
      "0x283"
    ],
    "printable_height": "330",
    "printer_model": "Co Print ChromaSet",
    "printer_variant": "0.4",
    "retract_before_wipe": [
      "0%"
    ],
    "retract_length_toolchange": [
      "2"
    ],
    "retract_lift_below": [
      "343"
    ],
    "retract_restart_extra": [
      "0"
    ],
    "retract_when_changing_layer": [
      "0"
    ],
    "retraction_length": [
      "0.5"
    ],
    "retraction_minimum_travel": [
      "1"
    ],
    "retraction_speed": [
      "60"
    ],
    "setting_id": "GM001",
    "thumbnails": [
      "300x300",
      "400x300",
      "96x96",
      "32x32"
    ],
    "thumbnails_format": "PNG",
    "type": "machine",
    "wipe": [
      "1"
    ],
    "wipe_distance": [
      "2"
    ],
    "z_hop": [
      "0.2"
    ],
    "z_hop_types": "Spiral Lift"
  },
  "machine/Co Print ChromaSet 0.4 nozzle - Ender-3 V3.json": {
    "change_filament_gcode": "FILAMENT_CHANGE LAYER_NUM=[layer_num] NEXT_EXTRUDER=[next_extruder]",
    "cooling_tube_length": [
      "0"
    ],
    "cooling_tube_retraction": [
      "0"
    ],
    "default_filament_profile": [
      "CoPrint Generic PLA"
    ],
    "default_print_profile": "0.2mm Standard @Co Print ChromaSet 0.4",
    "deretraction_speed": [
      "30"
    ],
    "enable_filament_ramming": [
      "0"
    ],
    "extra_loading_move": [
      "0"
    ],
    "extruder_clearance_height_to_lid": [
      "140"
    ],
    "extruder_clearance_height_to_rod": [
      "36"
    ],
    "extruder_clearance_radius": [
      "65"
    ],
    "from": "system",
    "gcode_flavor": "klipper",
    "high_current_on_filament_swap": [
      "0"
    ],
    "inherits": "fdm_machine_common",
    "instantiation": "true",
    "machine_end_gcode": "end_print",
    "machine_max_acceleration_e": [
      "2500"
    ],
    "machine_max_acceleration_extruding": [
      "5000"
    ],
    "machine_max_acceleration_retracting": [
      "2500"
    ],
    "machine_max_acceleration_travel": [
      "40000"
    ],
    "machine_max_acceleration_x": [
      "5000"
    ],
    "machine_max_acceleration_y": [
      "5000"
    ],
    "machine_max_acceleration_z": [
      "100"
    ],
    "machine_max_jerk_e": [
      "2.5"
    ],
    "machine_max_jerk_x": [
      "8"
    ],
    "machine_max_jerk_y": [
      "8"
    ],
    "machine_max_jerk_z": [
      "0.2"
    ],
    "machine_max_speed_e": [
      "100"
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
    "machine_start_gcode": "start_print  EXTRUDER=[initial_extruder] EXTRUDER_TEMP=[nozzle_temperature_initial_layer] BED_TEMP=[bed_temperature_initial_layer_single]",
    "max_layer_height": [
      "0.32"
    ],
    "min_layer_height": [
      "0.08"
    ],
    "name": "Co Print ChromaSet 0.4 nozzle - Ender-3 V3",
    "nozzle_diameter": [
      "0.4"
    ],
    "nozzle_volume": [
      "156"
    ],
    "parking_pos_retraction": [
      "0"
    ],
    "printable_area": [
      "0x0",
      "180x0",
      "180x173",
      "0x173"
    ],
    "printable_height": "250",
    "printer_model": "Co Print ChromaSet",
    "printer_variant": "0.4",
    "retract_before_wipe": [
      "0%"
    ],
    "retract_length_toolchange": [
      "2"
    ],
    "retract_lift_below": [
      "343"
    ],
    "retract_restart_extra": [
      "0"
    ],
    "retract_when_changing_layer": [
      "0"
    ],
    "retraction_length": [
      "0.5"
    ],
    "retraction_minimum_travel": [
      "1"
    ],
    "retraction_speed": [
      "60"
    ],
    "setting_id": "GM001",
    "thumbnails": [
      "300x300",
      "400x300",
      "96x96",
      "32x32"
    ],
    "thumbnails_format": "PNG",
    "type": "machine",
    "wipe": [
      "1"
    ],
    "wipe_distance": [
      "2"
    ],
    "z_hop": [
      "0.2"
    ],
    "z_hop_types": "Spiral Lift"
  },
  "machine/Co Print ChromaSet 0.4 nozzle fast.json": {
    "change_filament_gcode": "FILAMENT_CHANGE LAYER_NUM=[layer_num] NEXT_EXTRUDER=[next_extruder]",
    "cooling_tube_length": [
      "0"
    ],
    "cooling_tube_retraction": [
      "0"
    ],
    "default_filament_profile": [
      "CoPrint Generic PLA"
    ],
    "default_print_profile": "0.2mm Fast @Co Print ChromaSet 0.4",
    "deretraction_speed": [
      "30"
    ],
    "enable_filament_ramming": [
      "0"
    ],
    "extra_loading_move": [
      "0"
    ],
    "extruder_clearance_height_to_lid": [
      "140"
    ],
    "extruder_clearance_height_to_rod": [
      "36"
    ],
    "extruder_clearance_radius": [
      "65"
    ],
    "from": "system",
    "gcode_flavor": "klipper",
    "high_current_on_filament_swap": [
      "0"
    ],
    "inherits": "fdm_machine_common",
    "instantiation": "true",
    "machine_end_gcode": "end_print",
    "machine_max_acceleration_e": [
      "5000"
    ],
    "machine_max_acceleration_extruding": [
      "20000"
    ],
    "machine_max_acceleration_retracting": [
      "5000"
    ],
    "machine_max_acceleration_travel": [
      "40000"
    ],
    "machine_max_acceleration_x": [
      "20000"
    ],
    "machine_max_acceleration_y": [
      "20000"
    ],
    "machine_max_acceleration_z": [
      "500"
    ],
    "machine_max_jerk_e": [
      "5"
    ],
    "machine_max_jerk_x": [
      "20"
    ],
    "machine_max_jerk_y": [
      "20"
    ],
    "machine_max_jerk_z": [
      "0.5"
    ],
    "machine_max_speed_e": [
      "100"
    ],
    "machine_max_speed_x": [
      "700"
    ],
    "machine_max_speed_y": [
      "700"
    ],
    "machine_max_speed_z": [
      "20"
    ],
    "machine_start_gcode": "start_print  EXTRUDER=[initial_extruder] EXTRUDER_TEMP=[nozzle_temperature_initial_layer] BED_TEMP=[bed_temperature_initial_layer_single]",
    "max_layer_height": [
      "0.32"
    ],
    "min_layer_height": [
      "0.08"
    ],
    "name": "Co Print ChromaSet 0.4 nozzle fast",
    "nozzle_diameter": [
      "0.4"
    ],
    "nozzle_volume": [
      "156"
    ],
    "parking_pos_retraction": [
      "0"
    ],
    "printable_area": [
      "0x0",
      "225x0",
      "225x225",
      "0x225"
    ],
    "printable_height": "250",
    "printer_model": "Co Print ChromaSet",
    "printer_variant": "0.4",
    "retract_before_wipe": [
      "0%"
    ],
    "retract_length_toolchange": [
      "2"
    ],
    "retract_lift_below": [
      "343"
    ],
    "retract_restart_extra": [
      "0"
    ],
    "retract_when_changing_layer": [
      "0"
    ],
    "retraction_length": [
      "0.5"
    ],
    "retraction_minimum_travel": [
      "1"
    ],
    "retraction_speed": [
      "60"
    ],
    "setting_id": "GM001",
    "thumbnails": [
      "300x300",
      "400x300",
      "96x96",
      "32x32"
    ],
    "thumbnails_format": "PNG",
    "type": "machine",
    "wipe": [
      "1"
    ],
    "wipe_distance": [
      "2"
    ],
    "z_hop": [
      "0.2"
    ],
    "z_hop_types": "Spiral Lift"
  },
  "machine/Co Print ChromaSet 0.4 nozzle.json": {
    "change_filament_gcode": "FILAMENT_CHANGE LAYER_NUM=[layer_num] NEXT_EXTRUDER=[next_extruder]",
    "cooling_tube_length": [
      "0"
    ],
    "cooling_tube_retraction": [
      "0"
    ],
    "default_filament_profile": [
      "CoPrint Generic PLA"
    ],
    "default_print_profile": "0.2mm Standard @Co Print ChromaSet 0.4",
    "deretraction_speed": [
      "30"
    ],
    "enable_filament_ramming": [
      "0"
    ],
    "extra_loading_move": [
      "0"
    ],
    "extruder_clearance_height_to_lid": [
      "140"
    ],
    "extruder_clearance_height_to_rod": [
      "36"
    ],
    "extruder_clearance_radius": [
      "65"
    ],
    "from": "system",
    "gcode_flavor": "klipper",
    "high_current_on_filament_swap": [
      "0"
    ],
    "inherits": "fdm_machine_common",
    "instantiation": "true",
    "machine_end_gcode": "end_print",
    "machine_max_acceleration_e": [
      "2500"
    ],
    "machine_max_acceleration_extruding": [
      "5000"
    ],
    "machine_max_acceleration_retracting": [
      "2500"
    ],
    "machine_max_acceleration_travel": [
      "40000"
    ],
    "machine_max_acceleration_x": [
      "5000"
    ],
    "machine_max_acceleration_y": [
      "5000"
    ],
    "machine_max_acceleration_z": [
      "100"
    ],
    "machine_max_jerk_e": [
      "2.5"
    ],
    "machine_max_jerk_x": [
      "8"
    ],
    "machine_max_jerk_y": [
      "8"
    ],
    "machine_max_jerk_z": [
      "0.2"
    ],
    "machine_max_speed_e": [
      "100"
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
    "machine_start_gcode": "start_print  EXTRUDER=[initial_extruder] EXTRUDER_TEMP=[nozzle_temperature_initial_layer] BED_TEMP=[bed_temperature_initial_layer_single]",
    "max_layer_height": [
      "0.32"
    ],
    "min_layer_height": [
      "0.08"
    ],
    "name": "Co Print ChromaSet 0.4 nozzle",
    "nozzle_diameter": [
      "0.4"
    ],
    "nozzle_volume": [
      "156"
    ],
    "parking_pos_retraction": [
      "0"
    ],
    "printable_area": [
      "0x0",
      "225x0",
      "225x225",
      "0x225"
    ],
    "printable_height": "250",
    "printer_model": "Co Print ChromaSet",
    "printer_variant": "0.4",
    "retract_before_wipe": [
      "0%"
    ],
    "retract_length_toolchange": [
      "2"
    ],
    "retract_lift_below": [
      "343"
    ],
    "retract_restart_extra": [
      "0"
    ],
    "retract_when_changing_layer": [
      "0"
    ],
    "retraction_length": [
      "0.5"
    ],
    "retraction_minimum_travel": [
      "1"
    ],
    "retraction_speed": [
      "60"
    ],
    "setting_id": "GM001",
    "thumbnails": [
      "300x300",
      "400x300",
      "96x96",
      "32x32"
    ],
    "thumbnails_format": "PNG",
    "type": "machine",
    "wipe": [
      "1"
    ],
    "wipe_distance": [
      "2"
    ],
    "z_hop": [
      "0.2"
    ],
    "z_hop_types": "Spiral Lift"
  },
  "machine/Co Print ChromaSet.json": {
    "bed_model": "",
    "bed_texture": "Co_Print_ChromaSet_buildplate_texture.png",
    "default_materials": "CoPrint Generic PLA",
    "family": "Co Print",
    "hotend_model": "",
    "machine_tech": "FFF",
    "model_id": "Co_Print_ChromaSet",
    "name": "Co Print ChromaSet",
    "nozzle_diameter": "0.4",
    "type": "machine_model"
  },
  "machine/fdm_coprint_common.json": {
    "before_layer_change_gcode": "TIMELAPSE_TAKE_FRAME\nG92 E0",
    "cooling_tube_length": [
      "0"
    ],
    "cooling_tube_retraction": [
      "0"
    ],
    "default_filament_profile": [
      "CoPrint Generic PLA"
    ],
    "default_print_profile": "0.20mm Standard @Co Print ChromaSet 0.4",
    "deretraction_speed": [
      "30"
    ],
    "extra_loading_move": [
      "0"
    ],
    "extruder_clearance_height_to_lid": [
      "36"
    ],
    "extruder_clearance_height_to_rod": [
      "36"
    ],
    "extruder_clearance_radius": [
      "65"
    ],
    "from": "system",
    "gcode_flavor": "klipper",
    "inherits": "fdm_machine_common",
    "instantiation": "false",
    "machine_end_gcode": "end_print",
    "machine_max_acceleration_e": [
      "2500"
    ],
    "machine_max_acceleration_extruding": [
      "5000"
    ],
    "machine_max_acceleration_retracting": [
      "2500"
    ],
    "machine_max_acceleration_travel": [
      "40000"
    ],
    "machine_max_acceleration_x": [
      "5000"
    ],
    "machine_max_acceleration_y": [
      "5000"
    ],
    "machine_max_acceleration_z": [
      "100"
    ],
    "machine_max_jerk_e": [
      "2.5"
    ],
    "machine_max_jerk_x": [
      "8"
    ],
    "machine_max_jerk_y": [
      "8"
    ],
    "machine_max_jerk_z": [
      "0.2"
    ],
    "machine_max_speed_e": [
      "100"
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
    "machine_start_gcode": "start_print  EXTRUDER=[initial_extruder] EXTRUDER_TEMP=[nozzle_temperature_initial_layer] BED_TEMP=[bed_temperature_initial_layer_single]",
    "max_layer_height": [
      "0.32"
    ],
    "min_layer_height": [
      "0.08"
    ],
    "name": "fdm_coprint_common",
    "nozzle_diameter": [
      "0.4"
    ],
    "parking_pos_retraction": [
      "10"
    ],
    "printable_area": [
      "0x0",
      "225x0",
      "225x225",
      "0x225"
    ],
    "printable_height": "250",
    "printer_variant": "0.4",
    "retract_before_wipe": [
      "0%"
    ],
    "retract_length_toolchange": [
      "2"
    ],
    "retract_lift_below": [
      "343"
    ],
    "retract_restart_extra": [
      "0"
    ],
    "retraction_length": [
      "0.5"
    ],
    "retraction_minimum_travel": [
      "1"
    ],
    "retraction_speed": [
      "60"
    ],
    "thumbnails": [
      "300x300",
      "400x300",
      "96x96",
      "32x32"
    ],
    "thumbnails_format": "PNG",
    "type": "machine",
    "wipe_distance": [
      "2"
    ],
    "z_hop": [
      "0.2"
    ]
  },
  "machine/fdm_machine_common.json": {
    "deretraction_speed": [
      "30"
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
    "gcode_flavor": "klipper",
    "instantiation": "false",
    "machine_load_filament_time": "9.75",
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
    "machine_unload_filament_time": "9.75",
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
      "0%"
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
      "0"
    ],
    "retraction_length": [
      "0.5"
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
  "process/0.2mm Fast @Co Print ChromaSet 0.4.json": {
    "bridge_acceleration": "80%",
    "compatible_printers": [
      "Co Print ChromaSet 0.4 nozzle fast",
      "Co Print ChromaSet 0.4 nozzle - Ender-3 V3",
      "Co Print ChromaSet 0.4 nozzle - Ender-3 V3 Plus"
    ],
    "default_acceleration": "10000",
    "default_jerk": "0",
    "elefant_foot_compensation": "0.1",
    "from": "system",
    "gap_infill_speed": "300",
    "inherits": "fdm_process_coprint_common",
    "initial_layer_acceleration": "1500",
    "initial_layer_infill_speed": "100",
    "initial_layer_speed": "60",
    "inner_wall_acceleration": "8000",
    "inner_wall_speed": "200",
    "instantiation": "true",
    "internal_solid_infill_acceleration": "80%",
    "internal_solid_infill_speed": "300",
    "name": "0.2mm Fast @Co Print ChromaSet 0.4",
    "outer_wall_acceleration": "3000",
    "outer_wall_speed": "120",
    "setting_id": "GP004",
    "small_perimeter_speed": "50%",
    "sparse_infill_acceleration": "80%",
    "top_surface_acceleration": "2000",
    "top_surface_speed": "150",
    "travel_acceleration": "10000",
    "travel_speed": "500",
    "type": "process",
    "wipe_tower_max_purge_speed": "200"
  },
  "process/0.2mm Standard @Co Print ChromaSet 0.4.json": {
    "compatible_printers": [
      "Co Print ChromaSet 0.4 nozzle",
      "Co Print ChromaSet 0.4 nozzle - Ender-3 V3",
      "Co Print ChromaSet 0.4 nozzle - Ender-3 V3 Plus"
    ],
    "default_acceleration": "5000",
    "from": "system",
    "inherits": "fdm_process_coprint_common",
    "instantiation": "true",
    "name": "0.2mm Standard @Co Print ChromaSet 0.4",
    "setting_id": "GP004",
    "type": "process"
  },
  "process/fdm_process_common.json": {
    "accel_to_decel": "50%",
    "accel_to_decel_enable": "1",
    "adaptive_layer_height": "0",
    "bottom_solid_infill_flow_ratio": "1",
    "bridge_acceleration": "800%",
    "bridge_flow": "0.9031",
    "bridge_no_support": "0",
    "bridge_speed": "25",
    "brim_type": "no_brim",
    "brim_width": "5",
    "compatible_printers": [],
    "default_acceleration": "5000",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_prime_tower": "1",
    "enable_support": "0",
    "exclude_object": "1",
    "extra_perimeters_on_overhangs": "0",
    "filename_format": "{input_filename_base}{filament_type[0]}{layer_height}_{print_time}.gcode",
    "from": "system",
    "gap_fill_target": "nowhere",
    "gap_infill_speed": "200",
    "infill_anchor": "400%",
    "infill_anchor_max": "20",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_layer_acceleration": "1500",
    "infill_wall_overlap": "30%",
    "initial_layer_acceleration": "1500",
    "initial_layer_infill_speed": "60",
    "initial_layer_line_width": "0.5",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "60",
    "inner_wall_acceleration": "3000",
    "inner_wall_line_width": "0.45",
    "inner_wall_speed": "100",
    "instantiation": "false",
    "interface_shells": "0",
    "internal_bridge_flow": "0.9031",
    "internal_bridge_speed": "100",
    "internal_solid_infill_acceleration": "80%",
    "internal_solid_infill_line_width": "0.42",
    "internal_solid_infill_speed": "200",
    "layer_height": "0.2",
    "line_width": "0.42",
    "minimum_sparse_infill_area": "0",
    "name": "fdm_process_common",
    "outer_wall_acceleration": "1500",
    "outer_wall_line_width": "0.42",
    "outer_wall_speed": "60",
    "overhang_1_4_speed": "80",
    "overhang_2_4_speed": "50",
    "overhang_3_4_speed": "30",
    "overhang_4_4_speed": "10",
    "prime_tower_width": "150",
    "print_flow_ratio": "1",
    "print_sequence": "by layer",
    "print_settings_id": "",
    "raft_layers": "0",
    "reduce_crossing_wall": "1",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "seam_gap": "5%",
    "seam_position": "aligned",
    "skirt_distance": "2",
    "skirt_height": "1",
    "skirt_loops": "3",
    "skirt_speed": "50",
    "slow_down_layers": "3",
    "sparse_infill_acceleration": "80%",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.45",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "300",
    "spiral_mode": "0",
    "standby_temperature_delta": "-5",
    "support_base_pattern": "rectilinear",
    "support_base_pattern_spacing": "2.5",
    "support_filament": "0",
    "support_interface_filament": "0",
    "support_interface_loop_pattern": "0",
    "support_interface_spacing": "0.5",
    "support_interface_speed": "200",
    "support_interface_top_layers": "2",
    "support_line_width": "0.42",
    "support_object_xy_distance": "0.35",
    "support_on_build_plate_only": "0",
    "support_speed": "200",
    "support_threshold_angle": "35",
    "support_top_z_distance": "0.2",
    "top_shell_layers": "4",
    "top_shell_thickness": "1",
    "top_solid_infill_flow_ratio": "1",
    "top_surface_acceleration": "1000",
    "top_surface_line_width": "0.4",
    "top_surface_speed": "80",
    "travel_acceleration": "5000",
    "travel_speed": "350",
    "type": "process",
    "wall_generator": "arachne",
    "wall_loops": "2",
    "wall_sequence": "inner wall/outer wall",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/fdm_process_coprint_common.json": {
    "accel_to_decel": "50%",
    "accel_to_decel_enable": "1",
    "adaptive_layer_height": "0",
    "bottom_solid_infill_flow_ratio": "1",
    "bridge_acceleration": "80%",
    "bridge_flow": "0.9031",
    "bridge_no_support": "0",
    "bridge_speed": "25",
    "brim_type": "no_brim",
    "brim_width": "5",
    "default_acceleration": "5000",
    "default_jerk": "0",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_prime_tower": "1",
    "enable_support": "0",
    "exclude_object": "1",
    "extra_perimeters_on_overhangs": "0",
    "filename_format": "{input_filename_base}{filament_type[0]}{layer_height}_{print_time}.gcode",
    "from": "system",
    "gap_fill_target": "nowhere",
    "gap_infill_speed": "200",
    "infill_anchor": "400%",
    "infill_anchor_max": "20",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_jerk": "12",
    "infill_layer_acceleration": "1500",
    "infill_wall_overlap": "30%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "1500",
    "initial_layer_infill_speed": "60",
    "initial_layer_line_width": "0.5",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "60",
    "inner_wall_acceleration": "3000",
    "inner_wall_jerk": "7",
    "inner_wall_line_width": "0.45",
    "inner_wall_speed": "100",
    "instantiation": "false",
    "interface_shells": "0",
    "internal_bridge_flow": "0.9031",
    "internal_bridge_speed": "100",
    "internal_solid_infill_acceleration": "80%",
    "internal_solid_infill_line_width": "0.42",
    "internal_solid_infill_speed": "200",
    "layer_height": "0.2",
    "line_width": "0.42",
    "minimum_sparse_infill_area": "0",
    "name": "fdm_process_coprint_common",
    "outer_wall_acceleration": "1500",
    "outer_wall_jerk": "7",
    "outer_wall_line_width": "0.42",
    "outer_wall_speed": "60",
    "prime_tower_width": "150",
    "print_flow_ratio": "1",
    "print_sequence": "by layer",
    "print_settings_id": "",
    "raft_layers": "0",
    "reduce_crossing_wall": "1",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "role_based_wipe_speed": "0",
    "seam_gap": "5%",
    "seam_position": "aligned",
    "skirt_distance": "2",
    "skirt_height": "1",
    "skirt_loops": "3",
    "skirt_speed": "50",
    "slow_down_layers": "3",
    "sparse_infill_acceleration": "80%",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.45",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "300",
    "spiral_mode": "0",
    "staggered_inner_seams": "1",
    "standby_temperature_delta": "-5",
    "support_base_pattern": "rectilinear",
    "support_base_pattern_spacing": "2.5",
    "support_filament": "0",
    "support_interface_bottom_layers": "-1",
    "support_interface_filament": "0",
    "support_interface_loop_pattern": "0",
    "support_interface_spacing": "0.5",
    "support_interface_speed": "200",
    "support_interface_top_layers": "2",
    "support_line_width": "0.42",
    "support_object_xy_distance": "0.35",
    "support_on_build_plate_only": "0",
    "support_speed": "200",
    "support_threshold_angle": "35",
    "support_top_z_distance": "0.2",
    "support_type": "tree(auto)",
    "top_shell_layers": "4",
    "top_shell_thickness": "1",
    "top_solid_infill_flow_ratio": "1",
    "top_surface_acceleration": "1000",
    "top_surface_line_width": "0.4",
    "top_surface_speed": "80",
    "travel_acceleration": "5000",
    "travel_speed": "350",
    "tree_support_wall_count": "2",
    "type": "process",
    "wall_generator": "arachne",
    "wall_loops": "2",
    "wall_sequence": "inner wall/outer wall",
    "wipe_speed": "60%",
    "wipe_tower_max_purge_speed": "150",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  }
}

FILAMENT = {
  "filament/CoPrint Generic ABS.json": {
    "close_fan_the_first_x_layers": [
      "3"
    ],
    "compatible_printers": [
      "Co Print ChromaSet 0.4 nozzle",
      "Co Print ChromaSet 0.4 nozzle - Ender-3 V3",
      "Co Print ChromaSet 0.4 nozzle - Ender-3 V3 Plus",
      "Co Print ChromaSet 0.4 nozzle fast"
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
    "filament_density": [
      "1.04"
    ],
    "filament_flow_ratio": [
      "0.94"
    ],
    "filament_id": "GFL99",
    "filament_max_volumetric_speed": [
      "16"
    ],
    "filament_type": [
      "ABS"
    ],
    "from": "system",
    "full_fan_speed_layer": [
      "5"
    ],
    "hot_plate_temp": [
      "100"
    ],
    "hot_plate_temp_initial_layer": [
      "100"
    ],
    "inherits": "CoPrint Generic PLA",
    "instantiation": "true",
    "name": "CoPrint Generic ABS",
    "nozzle_temperature": [
      "280"
    ],
    "nozzle_temperature_initial_layer": [
      "260"
    ],
    "nozzle_temperature_range_high": [
      "280"
    ],
    "nozzle_temperature_range_low": [
      "240"
    ],
    "overhang_fan_threshold": [
      "25%"
    ],
    "pressure_advance": [
      "0.02"
    ],
    "setting_id": "GFSA04",
    "slow_down_layer_time": [
      "12"
    ],
    "slow_down_min_speed": [
      "20"
    ],
    "temperature_vitrification": [
      "100"
    ],
    "type": "filament"
  },
  "filament/CoPrint Generic PETG.json": {
    "compatible_printers": [
      "Co Print ChromaSet 0.4 nozzle",
      "Co Print ChromaSet 0.4 nozzle - Ender-3 V3",
      "Co Print ChromaSet 0.4 nozzle - Ender-3 V3 Plus",
      "Co Print ChromaSet 0.4 nozzle fast"
    ],
    "fan_max_speed": [
      "90"
    ],
    "fan_min_speed": [
      "60"
    ],
    "filament_deretraction_speed": [
      "50"
    ],
    "filament_id": "GFL99",
    "filament_retraction_length": [
      "1.2"
    ],
    "filament_retraction_speed": [
      "50"
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
    "inherits": "CoPrint Generic PLA",
    "instantiation": "true",
    "name": "CoPrint Generic PETG",
    "nozzle_temperature": [
      "240"
    ],
    "nozzle_temperature_initial_layer": [
      "240"
    ],
    "setting_id": "GFSA04",
    "type": "filament"
  },
  "filament/CoPrint Generic PLA.json": {
    "compatible_printers": [
      "Co Print ChromaSet 0.4 nozzle",
      "Co Print ChromaSet 0.4 nozzle - Ender-3 V3",
      "Co Print ChromaSet 0.4 nozzle - Ender-3 V3 Plus",
      "Co Print ChromaSet 0.4 nozzle fast"
    ],
    "filament_id": "GFL99",
    "filament_load_time": [
      "9.75"
    ],
    "filament_unload_time": [
      "9.75"
    ],
    "from": "system",
    "inherits": "fdm_filament_pla",
    "instantiation": "true",
    "name": "CoPrint Generic PLA",
    "setting_id": "GFSA04",
    "type": "filament"
  },
  "filament/CoPrint Generic TPU.json": {
    "compatible_printers": [
      "Co Print ChromaSet 0.4 nozzle",
      "Co Print ChromaSet 0.4 nozzle - Ender-3 V3",
      "Co Print ChromaSet 0.4 nozzle - Ender-3 V3 Plus",
      "Co Print ChromaSet 0.4 nozzle fast"
    ],
    "fan_max_speed": [
      "80"
    ],
    "fan_min_speed": [
      "80"
    ],
    "filament_deretraction_speed": [
      "20"
    ],
    "filament_flow_ratio": [
      "0.97"
    ],
    "filament_id": "GFL99",
    "filament_retract_when_changing_layer": [
      "0"
    ],
    "filament_retraction_length": [
      "1.8"
    ],
    "filament_retraction_speed": [
      "20"
    ],
    "filament_type": [
      "TPU"
    ],
    "from": "system",
    "hot_plate_temp": [
      "50"
    ],
    "hot_plate_temp_initial_layer": [
      "50"
    ],
    "inherits": "CoPrint Generic PLA",
    "instantiation": "true",
    "name": "CoPrint Generic TPU",
    "nozzle_temperature": [
      "230"
    ],
    "nozzle_temperature_initial_layer": [
      "230"
    ],
    "setting_id": "GFSA04",
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
      "100"
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
    "filament_flow_ratio": [
      "0.95"
    ],
    "filament_max_volumetric_speed": [
      "14"
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
    "filament_type": [
      "PLA"
    ],
    "filament_vendor": [
      "Co Print"
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
  "filament/fdm_filament_pla.json": {
    "activate_air_filtration": [
      "0"
    ],
    "additional_cooling_fan_speed": [
      "70"
    ],
    "chamber_temperatures": [
      "0"
    ],
    "close_fan_the_first_x_layers": [
      "1"
    ],
    "compatible_printers": [],
    "complete_print_exhaust_fan_speed": [
      "100"
    ],
    "cool_plate_temp": [
      "35"
    ],
    "cool_plate_temp_initial_layer": [
      "35"
    ],
    "during_print_exhaust_fan_speed": [
      "100"
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
      "50"
    ],
    "fan_max_speed": [
      "100"
    ],
    "fan_min_speed": [
      "100"
    ],
    "filament_cooling_final_speed": [
      "3.4"
    ],
    "filament_cooling_initial_speed": [
      "2.2"
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
    "filament_flow_ratio": [
      "0.95"
    ],
    "filament_is_support": [
      "0"
    ],
    "filament_load_time": [
      "9.75"
    ],
    "filament_loading_speed": [
      "28"
    ],
    "filament_loading_speed_start": [
      "3"
    ],
    "filament_max_volumetric_speed": [
      "14"
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
    "filament_shrink": [
      "100"
    ],
    "filament_soluble": [
      "0"
    ],
    "filament_toolchange_delay": [
      "0"
    ],
    "filament_type": [
      "PLA"
    ],
    "filament_unload_time": [
      "9.75"
    ],
    "filament_unloading_speed": [
      "90"
    ],
    "filament_unloading_speed_start": [
      "100"
    ],
    "filament_vendor": [
      "Co Print"
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
    "from": "system",
    "full_fan_speed_layer": [
      "3"
    ],
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
      "210"
    ],
    "nozzle_temperature_initial_layer": [
      "210"
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
    "pressure_advance": [
      "0.05"
    ],
    "reduce_fan_stop_start_freq": [
      "1"
    ],
    "required_nozzle_HRC": [
      "3"
    ],
    "slow_down_for_layer_cooling": [
      "1"
    ],
    "slow_down_layer_time": [
      "5"
    ],
    "slow_down_min_speed": [
      "10"
    ],
    "temperature_vitrification": [
      "45"
    ],
    "textured_plate_temp": [
      "55"
    ],
    "textured_plate_temp_initial_layer": [
      "55"
    ],
    "type": "filament"
  }
}

MISC = {}

ASSETS = [
  "Co Print ChromaSet_cover.png",
  "Co_Print_ChromaSet_buildplate_model.stl",
  "Co_Print_ChromaSet_buildplate_texture.png"
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
