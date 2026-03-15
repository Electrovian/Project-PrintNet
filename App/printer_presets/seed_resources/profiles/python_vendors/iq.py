from __future__ import annotations

VENDOR = "iQ"
INDEX = {
  "description": "innovatiQ configuration",
  "filament_list": [
    {
      "name": "fdm_filament_common",
      "sub_path": "filament/fdm_filament_common.json"
    },
    {
      "name": "Fiberthree PACF Pro P1 @iQ TiQ2 0.4 Nozzle",
      "sub_path": "filament/Fiberthree PACF Pro P1 @iQ TiQ2 0.4 Nozzle.json"
    },
    {
      "name": "Material4Print ABS Natur P1 @iQ TiQ8 0.4 Nozzle",
      "sub_path": "filament/Material4Print ABS Natur P1 @iQ TiQ8 0.4 Nozzle.json"
    },
    {
      "name": "Polymaker PETG Polymax black P1 @iQ TiQ2 0.4 Nozzle",
      "sub_path": "filament/Polymaker PETG Polymax black P1 @iQ TiQ2 0.4 Nozzle.json"
    },
    {
      "name": "Fiberthree PACF Pro P2 @iQ TiQ2 0.4 Nozzle",
      "sub_path": "filament/Fiberthree PACF Pro P2 @iQ TiQ2 0.4 Nozzle.json"
    },
    {
      "name": "VXL90 TiQ2 P2 @iQ TiQ2 0.4 Nozzle",
      "sub_path": "filament/VXL90 TiQ2 P2 @iQ TiQ2 0.4 Nozzle.json"
    },
    {
      "name": "Grauts HPP4GF25 P1 @iQ TiQ2 0.4 Nozzle",
      "sub_path": "filament/Grauts HPP4GF25 P1 @iQ TiQ2 0.4 Nozzle.json"
    }
  ],
  "force_update": "1",
  "machine_list": [
    {
      "name": "fdm_tiq_common",
      "sub_path": "machine/fdm_tiq_common.json"
    },
    {
      "name": "iQ TiQ2 0.4 Nozzle",
      "sub_path": "machine/iQ TiQ2 0.4 nozzle.json"
    },
    {
      "name": "iQ TiQ2 0.25 Nozzle",
      "sub_path": "machine/iQ TiQ2 0.25 nozzle.json"
    },
    {
      "name": "iQ TiQ2 0.6 Nozzle",
      "sub_path": "machine/iQ TiQ2 0.6 nozzle.json"
    },
    {
      "name": "iQ TiQ2 0.8 Nozzle",
      "sub_path": "machine/iQ TiQ2 0.8 nozzle.json"
    },
    {
      "name": "iQ TiQ8 0.4 Nozzle",
      "sub_path": "machine/iQ TiQ8 0.4 nozzle.json"
    },
    {
      "name": "iQ TiQ8 0.25 Nozzle",
      "sub_path": "machine/iQ TiQ8 0.25 nozzle.json"
    },
    {
      "name": "iQ TiQ8 0.6 Nozzle",
      "sub_path": "machine/iQ TiQ8 0.6 nozzle.json"
    },
    {
      "name": "iQ TiQ8 0.8 Nozzle",
      "sub_path": "machine/iQ TiQ8 0.8 nozzle.json"
    }
  ],
  "machine_model_list": [
    {
      "name": "TiQ2",
      "sub_path": "machine/TiQ2.json"
    },
    {
      "name": "TiQ8",
      "sub_path": "machine/TiQ8.json"
    }
  ],
  "name": "innovatiQ",
  "process_list": [
    {
      "name": "fdm_process_tiq_common",
      "sub_path": "process/fdm_process_tiq_common.json"
    },
    {
      "name": "0.20mm Standard @iQ TiQ2 P1 - PACF Pro Fiberthree (0.4 Nozzle)",
      "sub_path": "process/0.20mm Standard @iQ TiQ2 P1 - PACF Pro Fiberthree (0.4 Nozzle).json"
    },
    {
      "name": "0.20mm Standard @iQ TiQ2 P1 - PETG Polymax Polymaker (0.4 Nozzle)",
      "sub_path": "process/0.20mm Standard @iQ TiQ2 P1 - PETG Polymax Polymaker (0.4 Nozzle).json"
    },
    {
      "name": "0.20mm Standard @iQ TiQ8 P1 - ABS Natur Material4Print (0.4 Nozzle)",
      "sub_path": "process/0.20mm Standard @iQ TiQ8 P1 - ABS Natur Material4Print (0.4 Nozzle).json"
    },
    {
      "name": "0.20mm Standard @iQ TiQ2 P2 - PACF Pro Fiberthree + VXL90 Xioneer (0.4 Nozzle)",
      "sub_path": "process/0.20mm Standard @iQ TiQ2 P2 - PACF Pro Fiberthree + VXL90 Xioneer (0.4 Nozzle).json"
    },
    {
      "name": "0.20mm Standard @iQ TiQ2 P1 - HPP4GF25 Grauts (0.4 Nozzle)",
      "sub_path": "process/0.20mm Standard @iQ TiQ2 P1 - HPP4GF25 Grauts (0.4 Nozzle).json"
    }
  ],
  "version": "02.03.01.10"
}

MACHINE = {
  "machine/TiQ2.json": {
    "bed_model": "TiQ2.stl",
    "bed_texture": "TiQ2_texture.png",
    "default_materials": "Fiberthree PACF Pro P1 @iQ TiQ2 0.4 Nozzle",
    "family": "TiQ",
    "machine_tech": "FFF",
    "model_id": "TiQ2",
    "name": "TiQ2",
    "nozzle_diameter": "0.25;0.4;0.6;0.8",
    "type": "machine_model"
  },
  "machine/TiQ8.json": {
    "bed_model": "TiQ8.stl",
    "bed_texture": "TiQ8_texture.png",
    "default_materials": "Material4Print ABS Natur P1 @iQ TiQ8 0.4 Nozzle",
    "family": "TiQ",
    "machine_tech": "FFF",
    "model_id": "TiQ8",
    "name": "TiQ8",
    "nozzle_diameter": "0.25;0.4;0.6;0.8",
    "type": "machine_model"
  },
  "machine/fdm_tiq_common.json": {
    "adaptive_bed_mesh_margin": "0",
    "auxiliary_fan": "0",
    "bed_custom_texture": "",
    "bed_exclude_area": [
      "0x0"
    ],
    "before_layer_change_gcode": ";BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0\n",
    "best_object_pos": "0.5,0.5",
    "change_extrusion_role_gcode": "",
    "change_filament_gcode": "",
    "cooling_tube_length": "5",
    "cooling_tube_retraction": "91.5",
    "default_filament_profile": [
      "Fiberthree PACF Pro P1 @iQ TiQ2 0.4 Nozzle"
    ],
    "default_print_profile": "0.20mm Standard @iQ TiQ2 P1 - PACF Pro Fiberthree (0.4 Nozzle)",
    "deretraction_speed": [
      "30"
    ],
    "disable_m73": "0",
    "emit_machine_limits_to_gcode": "1",
    "enable_filament_ramming": "1",
    "extra_loading_move": "-2",
    "extruder_clearance_height_to_lid": "140",
    "extruder_clearance_height_to_rod": "36",
    "extruder_clearance_radius": "65",
    "extruder_colour": [
      "#FCE94F"
    ],
    "extruder_offset": [
      "0x0"
    ],
    "fan_kickstart": "0",
    "fan_speedup_overhangs": "1",
    "fan_speedup_time": "0",
    "from": "system",
    "gcode_flavor": "marlin",
    "head_wrap_detect_zone": [],
    "high_current_on_filament_swap": "0",
    "instantiation": "false",
    "layer_change_gcode": ";AFTER_LAYER_CHANGE\n;[layer_z]",
    "machine_end_gcode": "G1 X-19 F3000 ; home X axis\nG1 Y1 F3000 ; home Y axis\nM104 S0 T0 ; turn off extruder\nM104 S0 T1 ; turn off extruder\nM104 S0 T2 ; turn off extruder\nM140 S0 ; turn off bed\nM106 S0 ; turn off fan\nM806 S0 ; turn of housing fan\nM84 ; disable motor\n",
    "machine_load_filament_time": "0",
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
      "2000",
      "20000"
    ],
    "machine_max_acceleration_y": [
      "2000",
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
    "machine_min_extruding_rate": [
      "0",
      "0"
    ],
    "machine_min_travel_rate": [
      "0",
      "0"
    ],
    "machine_pause_gcode": "PAUSE",
    "machine_start_gcode": "PRINT_START MATERIAL=[filament_type]\n",
    "machine_unload_filament_time": "0",
    "manual_filament_change": "0",
    "max_layer_height": [
      "2"
    ],
    "min_layer_height": [
      "0.1"
    ],
    "name": "fdm_tiq_common",
    "nozzle_hrc": "0",
    "nozzle_type": "undefine",
    "nozzle_volume": "0",
    "parking_pos_retraction": "92",
    "preferred_orientation": "0",
    "print_host": "http://10.0.1.200/",
    "print_host_webui": "",
    "printer_notes": "",
    "printer_settings_id": "fdm_tiq_common",
    "printer_structure": "undefine",
    "printer_technology": "FFF",
    "printhost_apikey": "",
    "printhost_authorization_type": "key",
    "printhost_cafile": "",
    "printhost_password": "",
    "printhost_port": "",
    "printhost_ssl_ignore_revoke": "0",
    "printhost_user": "",
    "printing_by_object_gcode": "",
    "purge_in_prime_tower": "1",
    "retract_before_wipe": [
      "70%"
    ],
    "retract_length_toolchange": [
      "2"
    ],
    "retract_lift_above": [
      "0"
    ],
    "retract_lift_below": [
      "0"
    ],
    "retract_lift_enforce": [
      "All Surfaces"
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
    "single_extruder_multi_material": "0",
    "support_air_filtration": "1",
    "support_chamber_temp_control": "1",
    "support_multi_bed_types": "0",
    "template_custom_gcode": "",
    "time_cost": "0",
    "time_lapse_gcode": "",
    "type": "machine",
    "upward_compatible_machine": [],
    "use_firmware_retraction": "0",
    "use_relative_e_distances": "1",
    "wipe": [
      "1"
    ],
    "wipe_distance": [
      "1"
    ],
    "z_hop": [
      "0.4"
    ],
    "z_hop_types": [
      "Normal Lift"
    ],
    "z_offset": "0"
  },
  "machine/iQ TiQ2 0.25 nozzle.json": {
    "change_filament_gcode": "G1 Z{layer_z+2} F900 ; safe distance while tool change\nG1 X32 Y3 F3000\nM109 S{nozzle_temperature[next_extruder]} T[next_extruder] ; set new tool temperature so it can start heating while changing\n",
    "deretraction_speed": [
      "30",
      "30"
    ],
    "disable_m73": "1",
    "emit_machine_limits_to_gcode": "0",
    "enable_filament_ramming": "0",
    "extruder_colour": [
      "#FCE94F",
      "#FCE94F"
    ],
    "extruder_offset": [
      "0x0",
      "0x0"
    ],
    "from": "system",
    "gcode_flavor": "marlin",
    "host_type": "simplyprint",
    "inherits": "fdm_tiq_common",
    "instantiation": "true",
    "long_retractions_when_cut": [
      "0",
      "0"
    ],
    "machine_end_gcode": "G1 X-19 F3000 ; home X axis\nG1 Y1 F3000 ; home Y axis\nM104 S0 T0 ; turn off extruder\nM104 S0 T1 ; turn off extruder\nM104 S0 T2 ; turn off extruder\nM140 S0 ; turn off bed\nM106 S0 ; turn off fan\nM806 S0 ; turn of housing fan\nM84 ; disable motor\n",
    "machine_max_speed_z": [
      "15",
      "12"
    ],
    "machine_pause_gcode": "M10710 S0",
    "machine_start_gcode": "T[initial_extruder]\nM109 S{nozzle_temperature_initial_layer[current_extruder]}\nG1 Z15 F900\nG1 X-19 Y1 F9000\nG1 X-19 Y45 F9000\nG1 Y1 F9000\nG1 Y45 F9000\nG1 Y1 F9000\nG1 Y45 F9000\nG1 X0",
    "max_layer_height": [
      "0.2",
      "0.2"
    ],
    "min_layer_height": [
      "0.08",
      "0.08"
    ],
    "name": "iQ TiQ2 0.25 Nozzle",
    "nozzle_diameter": [
      "0.25",
      "0.25"
    ],
    "print_host": "https://simplyprint.io/panel",
    "printable_area": [
      "0x0",
      "330x0",
      "330x330",
      "0x330"
    ],
    "printable_height": "300",
    "printer_model": "TiQ2",
    "printer_notes": "Machine file version 1.0 20251106",
    "printer_settings_id": "iQ TiQ2 0.25 Nozzle",
    "printer_variant": "0.25",
    "retract_before_wipe": [
      "70%",
      "70%"
    ],
    "retract_length_toolchange": [
      "10",
      "12"
    ],
    "retract_lift_above": [
      "0",
      "0"
    ],
    "retract_lift_below": [
      "0",
      "0"
    ],
    "retract_lift_enforce": [
      "All Surfaces",
      "All Surfaces"
    ],
    "retract_on_top_layer": [
      "1",
      "1"
    ],
    "retract_restart_extra": [
      "0",
      "0"
    ],
    "retract_restart_extra_toolchange": [
      "-0.2",
      "-0.2"
    ],
    "retract_when_changing_layer": [
      "1",
      "1"
    ],
    "retraction_distances_when_cut": [
      "18",
      "18"
    ],
    "retraction_length": [
      "0.8",
      "0.9"
    ],
    "retraction_minimum_travel": [
      "1",
      "1"
    ],
    "retraction_speed": [
      "30",
      "30"
    ],
    "thumbnails": "",
    "travel_slope": [
      "3",
      "3"
    ],
    "type": "machine",
    "wipe": [
      "1",
      "1"
    ],
    "wipe_distance": [
      "1",
      "1"
    ],
    "z_hop": [
      "0.25",
      "0.25"
    ],
    "z_hop_types": [
      "Normal Lift",
      "Normal Lift"
    ]
  },
  "machine/iQ TiQ2 0.4 nozzle.json": {
    "change_filament_gcode": "G1 Z{layer_z+2} F900 ; safe distance while tool change\nG1 X32 Y3 F3000\nM109 S{nozzle_temperature[next_extruder]} T[next_extruder] ; set new tool temperature so it can start heating while changing\n",
    "deretraction_speed": [
      "30",
      "30"
    ],
    "disable_m73": "1",
    "emit_machine_limits_to_gcode": "0",
    "enable_filament_ramming": "0",
    "extruder_colour": [
      "#FCE94F",
      "#FCE94F"
    ],
    "extruder_offset": [
      "0x0",
      "0x0"
    ],
    "from": "system",
    "gcode_flavor": "marlin",
    "host_type": "simplyprint",
    "inherits": "fdm_tiq_common",
    "instantiation": "true",
    "long_retractions_when_cut": [
      "0",
      "0"
    ],
    "machine_end_gcode": "G1 X-19 F3000 ; home X axis\nG1 Y1 F3000 ; home Y axis\nM104 S0 T0 ; turn off extruder\nM104 S0 T1 ; turn off extruder\nM104 S0 T2 ; turn off extruder\nM140 S0 ; turn off bed\nM106 S0 ; turn off fan\nM806 S0 ; turn of housing fan\nM84 ; disable motor\n",
    "machine_max_speed_z": [
      "15",
      "12"
    ],
    "machine_pause_gcode": "M10710 S0",
    "machine_start_gcode": "T[initial_extruder]\nM109 S{nozzle_temperature_initial_layer[current_extruder]}\nG1 Z15 F900\nG1 X-19 Y1 F9000\nG1 X-19 Y45 F9000\nG1 Y1 F9000\nG1 Y45 F9000\nG1 Y1 F9000\nG1 Y45 F9000\nG1 X0",
    "max_layer_height": [
      "0.32",
      "0.32"
    ],
    "min_layer_height": [
      "0.08",
      "0.08"
    ],
    "name": "iQ TiQ2 0.4 Nozzle",
    "nozzle_diameter": [
      "0.4",
      "0.4"
    ],
    "print_host": "https://simplyprint.io/panel",
    "printable_area": [
      "0x0",
      "330x0",
      "330x330",
      "0x330"
    ],
    "printable_height": "300",
    "printer_model": "TiQ2",
    "printer_notes": "Machine file version 1.1 20250812",
    "printer_settings_id": "iQ TiQ2 0.4 Nozzle",
    "printer_variant": "0.4",
    "retract_before_wipe": [
      "70%",
      "70%"
    ],
    "retract_length_toolchange": [
      "10",
      "12"
    ],
    "retract_lift_above": [
      "0",
      "0"
    ],
    "retract_lift_below": [
      "0",
      "0"
    ],
    "retract_lift_enforce": [
      "All Surfaces",
      "All Surfaces"
    ],
    "retract_on_top_layer": [
      "1",
      "1"
    ],
    "retract_restart_extra": [
      "0",
      "0"
    ],
    "retract_restart_extra_toolchange": [
      "-0.2",
      "-0.2"
    ],
    "retract_when_changing_layer": [
      "1",
      "1"
    ],
    "retraction_distances_when_cut": [
      "18",
      "18"
    ],
    "retraction_length": [
      "0.8",
      "0.9"
    ],
    "retraction_minimum_travel": [
      "1",
      "1"
    ],
    "retraction_speed": [
      "30",
      "30"
    ],
    "thumbnails": "",
    "travel_slope": [
      "3",
      "3"
    ],
    "type": "machine",
    "wipe": [
      "1",
      "1"
    ],
    "wipe_distance": [
      "1",
      "1"
    ],
    "z_hop": [
      "0.4",
      "0.4"
    ],
    "z_hop_types": [
      "Normal Lift",
      "Normal Lift"
    ]
  },
  "machine/iQ TiQ2 0.6 nozzle.json": {
    "change_filament_gcode": "G1 Z{layer_z+2} F900 ; safe distance while tool change\nG1 X32 Y3 F3000\nM109 S{nozzle_temperature[next_extruder]} T[next_extruder] ; set new tool temperature so it can start heating while changing\n",
    "deretraction_speed": [
      "30",
      "30"
    ],
    "disable_m73": "1",
    "emit_machine_limits_to_gcode": "0",
    "enable_filament_ramming": "0",
    "extruder_colour": [
      "#FCE94F",
      "#FCE94F"
    ],
    "extruder_offset": [
      "0x0",
      "0x0"
    ],
    "from": "system",
    "gcode_flavor": "marlin",
    "host_type": "simplyprint",
    "inherits": "fdm_tiq_common",
    "instantiation": "true",
    "long_retractions_when_cut": [
      "0",
      "0"
    ],
    "machine_end_gcode": "G1 X-19 F3000 ; home X axis\nG1 Y1 F3000 ; home Y axis\nM104 S0 T0 ; turn off extruder\nM104 S0 T1 ; turn off extruder\nM104 S0 T2 ; turn off extruder\nM140 S0 ; turn off bed\nM106 S0 ; turn off fan\nM806 S0 ; turn of housing fan\nM84 ; disable motor\n",
    "machine_max_speed_z": [
      "15",
      "12"
    ],
    "machine_pause_gcode": "M10710 S0",
    "machine_start_gcode": "T[initial_extruder]\nM109 S{nozzle_temperature_initial_layer[current_extruder]}\nG1 Z15 F900\nG1 X-19 Y1 F9000\nG1 X-19 Y45 F9000\nG1 Y1 F9000\nG1 Y45 F9000\nG1 Y1 F9000\nG1 Y45 F9000\nG1 X0",
    "max_layer_height": [
      "0.6",
      "0.6"
    ],
    "min_layer_height": [
      "0.08",
      "0.08"
    ],
    "name": "iQ TiQ2 0.6 Nozzle",
    "nozzle_diameter": [
      "0.6",
      "0.6"
    ],
    "print_host": "https://simplyprint.io/panel",
    "printable_area": [
      "0x0",
      "330x0",
      "330x330",
      "0x330"
    ],
    "printable_height": "300",
    "printer_model": "TiQ2",
    "printer_notes": "Machine file version 1.0 20251106",
    "printer_settings_id": "iQ TiQ2 0.6 Nozzle",
    "printer_variant": "0.6",
    "retract_before_wipe": [
      "70%",
      "70%"
    ],
    "retract_length_toolchange": [
      "10",
      "12"
    ],
    "retract_lift_above": [
      "0",
      "0"
    ],
    "retract_lift_below": [
      "0",
      "0"
    ],
    "retract_lift_enforce": [
      "All Surfaces",
      "All Surfaces"
    ],
    "retract_on_top_layer": [
      "1",
      "1"
    ],
    "retract_restart_extra": [
      "0",
      "0"
    ],
    "retract_restart_extra_toolchange": [
      "-0.2",
      "-0.2"
    ],
    "retract_when_changing_layer": [
      "1",
      "1"
    ],
    "retraction_distances_when_cut": [
      "18",
      "18"
    ],
    "retraction_length": [
      "0.8",
      "0.9"
    ],
    "retraction_minimum_travel": [
      "1",
      "1"
    ],
    "retraction_speed": [
      "30",
      "30"
    ],
    "thumbnails": "",
    "travel_slope": [
      "3",
      "3"
    ],
    "type": "machine",
    "wipe": [
      "1",
      "1"
    ],
    "wipe_distance": [
      "1",
      "1"
    ],
    "z_hop": [
      "0.6",
      "0.6"
    ],
    "z_hop_types": [
      "Normal Lift",
      "Normal Lift"
    ]
  },
  "machine/iQ TiQ2 0.8 nozzle.json": {
    "change_filament_gcode": "G1 Z{layer_z+2} F900 ; safe distance while tool change\nG1 X32 Y3 F3000\nM109 S{nozzle_temperature[next_extruder]} T[next_extruder] ; set new tool temperature so it can start heating while changing\n",
    "deretraction_speed": [
      "30",
      "30"
    ],
    "disable_m73": "1",
    "emit_machine_limits_to_gcode": "0",
    "enable_filament_ramming": "0",
    "extruder_colour": [
      "#FCE94F",
      "#FCE94F"
    ],
    "extruder_offset": [
      "0x0",
      "0x0"
    ],
    "from": "system",
    "gcode_flavor": "marlin",
    "host_type": "simplyprint",
    "inherits": "fdm_tiq_common",
    "instantiation": "true",
    "long_retractions_when_cut": [
      "0",
      "0"
    ],
    "machine_end_gcode": "G1 X-19 F3000 ; home X axis\nG1 Y1 F3000 ; home Y axis\nM104 S0 T0 ; turn off extruder\nM104 S0 T1 ; turn off extruder\nM104 S0 T2 ; turn off extruder\nM140 S0 ; turn off bed\nM106 S0 ; turn off fan\nM806 S0 ; turn of housing fan\nM84 ; disable motor\n",
    "machine_max_speed_z": [
      "15",
      "12"
    ],
    "machine_pause_gcode": "M10710 S0",
    "machine_start_gcode": "T[initial_extruder]\nM109 S{nozzle_temperature_initial_layer[current_extruder]}\nG1 Z15 F900\nG1 X-19 Y1 F9000\nG1 X-19 Y45 F9000\nG1 Y1 F9000\nG1 Y45 F9000\nG1 Y1 F9000\nG1 Y45 F9000\nG1 X0",
    "max_layer_height": [
      "0.8",
      "0.8"
    ],
    "min_layer_height": [
      "0.08",
      "0.08"
    ],
    "name": "iQ TiQ2 0.8 Nozzle",
    "nozzle_diameter": [
      "0.8",
      "0.8"
    ],
    "print_host": "https://simplyprint.io/panel",
    "printable_area": [
      "0x0",
      "330x0",
      "330x330",
      "0x330"
    ],
    "printable_height": "300",
    "printer_model": "TiQ2",
    "printer_notes": "Machine file version 1.0 20251106",
    "printer_settings_id": "iQ TiQ2 0.8 Nozzle",
    "printer_variant": "0.8",
    "retract_before_wipe": [
      "70%",
      "70%"
    ],
    "retract_length_toolchange": [
      "10",
      "12"
    ],
    "retract_lift_above": [
      "0",
      "0"
    ],
    "retract_lift_below": [
      "0",
      "0"
    ],
    "retract_lift_enforce": [
      "All Surfaces",
      "All Surfaces"
    ],
    "retract_on_top_layer": [
      "1",
      "1"
    ],
    "retract_restart_extra": [
      "0",
      "0"
    ],
    "retract_restart_extra_toolchange": [
      "-0.2",
      "-0.2"
    ],
    "retract_when_changing_layer": [
      "1",
      "1"
    ],
    "retraction_distances_when_cut": [
      "18",
      "18"
    ],
    "retraction_length": [
      "0.8",
      "0.9"
    ],
    "retraction_minimum_travel": [
      "1",
      "1"
    ],
    "retraction_speed": [
      "30",
      "30"
    ],
    "thumbnails": "",
    "travel_slope": [
      "3",
      "3"
    ],
    "type": "machine",
    "wipe": [
      "1",
      "1"
    ],
    "wipe_distance": [
      "1",
      "1"
    ],
    "z_hop": [
      "0.8",
      "0.8"
    ],
    "z_hop_types": [
      "Normal Lift",
      "Normal Lift"
    ]
  },
  "machine/iQ TiQ8 0.25 nozzle.json": {
    "change_filament_gcode": "G1 Z{layer_z+2} F900 ; safe distance while tool change\n{if next_extruder==0}G1 X30 Y-12 F9000{endif}\nM109 S{nozzle_temperature[next_extruder]} T[next_extruder] ; set new tool temperature so it can start heating while changing",
    "deretraction_speed": [
      "30",
      "30"
    ],
    "disable_m73": "1",
    "emit_machine_limits_to_gcode": "0",
    "enable_filament_ramming": "0",
    "extruder_colour": [
      "#FCE94F",
      "#FCE94F"
    ],
    "extruder_offset": [
      "0x0",
      "0x0"
    ],
    "from": "system",
    "gcode_flavor": "marlin",
    "host_type": "simplyprint",
    "inherits": "fdm_tiq_common",
    "instantiation": "true",
    "long_retractions_when_cut": [
      "0",
      "0"
    ],
    "machine_end_gcode": "G1 X10 F3000 ; home X axis\nG1 Y10 F3000 ; home Y axis\nM104 S0 T0 ; turn off extruder\nM104 S0 T1 ; turn off extruder\nM104 S0 T2 ; turn off extruder\nM140 S0 ; turn off bed\n{if nozzle_temperature_initial_layer[current_extruder]>350}M140 S80{endif} ; Keep bed hot for easy part removal from PEI sheet\nM106 S0 ; turn off fan\nM806 S0 ; turn of housing fan\nM84 ; disable motor\n",
    "machine_max_acceleration_x": [
      "1500",
      "1500"
    ],
    "machine_max_acceleration_y": [
      "1500",
      "1500"
    ],
    "machine_max_speed_z": [
      "15",
      "12"
    ],
    "machine_pause_gcode": "M10710 S0",
    "machine_start_gcode": "T[initial_extruder]\nM109 S{nozzle_temperature_initial_layer[current_extruder]}\n",
    "max_layer_height": [
      "0.25",
      "0.25"
    ],
    "min_layer_height": [
      "0.08",
      "0.08"
    ],
    "name": "iQ TiQ8 0.25 Nozzle",
    "nozzle_diameter": [
      "0.25",
      "0.25"
    ],
    "print_host": "https://simplyprint.io/panel",
    "printable_area": [
      "0x0",
      "500x0",
      "500x400",
      "0x400"
    ],
    "printable_height": "450",
    "printer_model": "TiQ8",
    "printer_notes": "Machine file version 1.0 20251106",
    "printer_settings_id": "iQ TiQ8 0.25 Nozzle",
    "printer_variant": "0.25",
    "retract_before_wipe": [
      "70%",
      "70%"
    ],
    "retract_length_toolchange": [
      "15",
      "15"
    ],
    "retract_lift_above": [
      "0",
      "0"
    ],
    "retract_lift_below": [
      "0",
      "0"
    ],
    "retract_lift_enforce": [
      "All Surfaces",
      "All Surfaces"
    ],
    "retract_on_top_layer": [
      "1",
      "1"
    ],
    "retract_restart_extra": [
      "0",
      "0"
    ],
    "retract_restart_extra_toolchange": [
      "-0.2",
      "-0.2"
    ],
    "retract_when_changing_layer": [
      "1",
      "1"
    ],
    "retraction_distances_when_cut": [
      "18",
      "18"
    ],
    "retraction_length": [
      "0.8",
      "0.9"
    ],
    "retraction_minimum_travel": [
      "1",
      "1"
    ],
    "retraction_speed": [
      "30",
      "30"
    ],
    "thumbnails": "",
    "travel_slope": [
      "3",
      "3"
    ],
    "type": "machine",
    "wipe": [
      "1",
      "1"
    ],
    "wipe_distance": [
      "1",
      "1"
    ],
    "z_hop": [
      "0.25",
      "0.25"
    ],
    "z_hop_types": [
      "Normal Lift",
      "Normal Lift"
    ]
  },
  "machine/iQ TiQ8 0.4 nozzle.json": {
    "change_filament_gcode": "G1 Z{layer_z+2} F900 ; safe distance while tool change\n{if next_extruder==0}G1 X30 Y-12 F9000{endif}\nM109 S{nozzle_temperature[next_extruder]} T[next_extruder] ; set new tool temperature so it can start heating while changing",
    "deretraction_speed": [
      "30",
      "30"
    ],
    "disable_m73": "1",
    "emit_machine_limits_to_gcode": "0",
    "enable_filament_ramming": "0",
    "extruder_colour": [
      "#FCE94F",
      "#FCE94F"
    ],
    "extruder_offset": [
      "0x0",
      "0x0"
    ],
    "from": "system",
    "gcode_flavor": "marlin",
    "host_type": "simplyprint",
    "inherits": "fdm_tiq_common",
    "instantiation": "true",
    "long_retractions_when_cut": [
      "0",
      "0"
    ],
    "machine_end_gcode": "G1 X10 F3000 ; home X axis\nG1 Y10 F3000 ; home Y axis\nM104 S0 T0 ; turn off extruder\nM104 S0 T1 ; turn off extruder\nM104 S0 T2 ; turn off extruder\nM140 S0 ; turn off bed\n{if nozzle_temperature_initial_layer[current_extruder]>350}M140 S80{endif} ; Keep bed hot for easy part removal from PEI sheet\nM106 S0 ; turn off fan\nM806 S0 ; turn of housing fan\nM84 ; disable motor\n",
    "machine_max_acceleration_x": [
      "1500",
      "1500"
    ],
    "machine_max_acceleration_y": [
      "1500",
      "1500"
    ],
    "machine_max_speed_z": [
      "15",
      "12"
    ],
    "machine_pause_gcode": "M10710 S0",
    "machine_start_gcode": "T[initial_extruder]\nM109 S{nozzle_temperature_initial_layer[current_extruder]}\n",
    "max_layer_height": [
      "0.32",
      "0.32"
    ],
    "min_layer_height": [
      "0.08",
      "0.08"
    ],
    "name": "iQ TiQ8 0.4 Nozzle",
    "nozzle_diameter": [
      "0.4",
      "0.4"
    ],
    "print_host": "https://simplyprint.io/panel",
    "printable_area": [
      "0x0",
      "500x0",
      "500x400",
      "0x400"
    ],
    "printable_height": "450",
    "printer_model": "TiQ8",
    "printer_notes": "Machine file version 1.1 20250516",
    "printer_settings_id": "iQ TiQ8 0.4 Nozzle",
    "printer_variant": "0.4",
    "retract_before_wipe": [
      "70%",
      "70%"
    ],
    "retract_length_toolchange": [
      "15",
      "15"
    ],
    "retract_lift_above": [
      "0",
      "0"
    ],
    "retract_lift_below": [
      "0",
      "0"
    ],
    "retract_lift_enforce": [
      "All Surfaces",
      "All Surfaces"
    ],
    "retract_on_top_layer": [
      "1",
      "1"
    ],
    "retract_restart_extra": [
      "0",
      "0"
    ],
    "retract_restart_extra_toolchange": [
      "-0.2",
      "-0.2"
    ],
    "retract_when_changing_layer": [
      "1",
      "1"
    ],
    "retraction_distances_when_cut": [
      "18",
      "18"
    ],
    "retraction_length": [
      "0.8",
      "0.9"
    ],
    "retraction_minimum_travel": [
      "1",
      "1"
    ],
    "retraction_speed": [
      "30",
      "30"
    ],
    "thumbnails": "",
    "travel_slope": [
      "3",
      "3"
    ],
    "type": "machine",
    "wipe": [
      "1",
      "1"
    ],
    "wipe_distance": [
      "1",
      "1"
    ],
    "z_hop": [
      "0.4",
      "0.4"
    ],
    "z_hop_types": [
      "Normal Lift",
      "Normal Lift"
    ]
  },
  "machine/iQ TiQ8 0.6 nozzle.json": {
    "change_filament_gcode": "G1 Z{layer_z+2} F900 ; safe distance while tool change\n{if next_extruder==0}G1 X30 Y-12 F9000{endif}\nM109 S{nozzle_temperature[next_extruder]} T[next_extruder] ; set new tool temperature so it can start heating while changing",
    "deretraction_speed": [
      "30",
      "30"
    ],
    "disable_m73": "1",
    "emit_machine_limits_to_gcode": "0",
    "enable_filament_ramming": "0",
    "extruder_colour": [
      "#FCE94F",
      "#FCE94F"
    ],
    "extruder_offset": [
      "0x0",
      "0x0"
    ],
    "from": "system",
    "gcode_flavor": "marlin",
    "host_type": "simplyprint",
    "inherits": "fdm_tiq_common",
    "instantiation": "true",
    "long_retractions_when_cut": [
      "0",
      "0"
    ],
    "machine_end_gcode": "G1 X10 F3000 ; home X axis\nG1 Y10 F3000 ; home Y axis\nM104 S0 T0 ; turn off extruder\nM104 S0 T1 ; turn off extruder\nM104 S0 T2 ; turn off extruder\nM140 S0 ; turn off bed\n{if nozzle_temperature_initial_layer[current_extruder]>350}M140 S80{endif} ; Keep bed hot for easy part removal from PEI sheet\nM106 S0 ; turn off fan\nM806 S0 ; turn of housing fan\nM84 ; disable motor\n",
    "machine_max_acceleration_x": [
      "1500",
      "1500"
    ],
    "machine_max_acceleration_y": [
      "1500",
      "1500"
    ],
    "machine_max_speed_z": [
      "15",
      "12"
    ],
    "machine_pause_gcode": "M10710 S0",
    "machine_start_gcode": "T[initial_extruder]\nM109 S{nozzle_temperature_initial_layer[current_extruder]}\n",
    "max_layer_height": [
      "0.6",
      "0.6"
    ],
    "min_layer_height": [
      "0.08",
      "0.08"
    ],
    "name": "iQ TiQ8 0.6 Nozzle",
    "nozzle_diameter": [
      "0.6",
      "0.6"
    ],
    "print_host": "https://simplyprint.io/panel",
    "printable_area": [
      "0x0",
      "500x0",
      "500x400",
      "0x400"
    ],
    "printable_height": "450",
    "printer_model": "TiQ8",
    "printer_notes": "Machine file version 1.0 20251106",
    "printer_settings_id": "iQ TiQ8 0.6 Nozzle",
    "printer_variant": "0.6",
    "retract_before_wipe": [
      "70%",
      "70%"
    ],
    "retract_length_toolchange": [
      "15",
      "15"
    ],
    "retract_lift_above": [
      "0",
      "0"
    ],
    "retract_lift_below": [
      "0",
      "0"
    ],
    "retract_lift_enforce": [
      "All Surfaces",
      "All Surfaces"
    ],
    "retract_on_top_layer": [
      "1",
      "1"
    ],
    "retract_restart_extra": [
      "0",
      "0"
    ],
    "retract_restart_extra_toolchange": [
      "-0.2",
      "-0.2"
    ],
    "retract_when_changing_layer": [
      "1",
      "1"
    ],
    "retraction_distances_when_cut": [
      "18",
      "18"
    ],
    "retraction_length": [
      "0.8",
      "0.9"
    ],
    "retraction_minimum_travel": [
      "1",
      "1"
    ],
    "retraction_speed": [
      "30",
      "30"
    ],
    "thumbnails": "",
    "travel_slope": [
      "3",
      "3"
    ],
    "type": "machine",
    "wipe": [
      "1",
      "1"
    ],
    "wipe_distance": [
      "1",
      "1"
    ],
    "z_hop": [
      "0.6",
      "0.6"
    ],
    "z_hop_types": [
      "Normal Lift",
      "Normal Lift"
    ]
  },
  "machine/iQ TiQ8 0.8 nozzle.json": {
    "change_filament_gcode": "G1 Z{layer_z+2} F900 ; safe distance while tool change\n{if next_extruder==0}G1 X30 Y-12 F9000{endif}\nM109 S{nozzle_temperature[next_extruder]} T[next_extruder] ; set new tool temperature so it can start heating while changing",
    "deretraction_speed": [
      "30",
      "30"
    ],
    "disable_m73": "1",
    "emit_machine_limits_to_gcode": "0",
    "enable_filament_ramming": "0",
    "extruder_colour": [
      "#FCE94F",
      "#FCE94F"
    ],
    "extruder_offset": [
      "0x0",
      "0x0"
    ],
    "from": "system",
    "gcode_flavor": "marlin",
    "host_type": "simplyprint",
    "inherits": "fdm_tiq_common",
    "instantiation": "true",
    "long_retractions_when_cut": [
      "0",
      "0"
    ],
    "machine_end_gcode": "G1 X10 F3000 ; home X axis\nG1 Y10 F3000 ; home Y axis\nM104 S0 T0 ; turn off extruder\nM104 S0 T1 ; turn off extruder\nM104 S0 T2 ; turn off extruder\nM140 S0 ; turn off bed\n{if nozzle_temperature_initial_layer[current_extruder]>350}M140 S80{endif} ; Keep bed hot for easy part removal from PEI sheet\nM106 S0 ; turn off fan\nM806 S0 ; turn of housing fan\nM84 ; disable motor\n",
    "machine_max_acceleration_x": [
      "1500",
      "1500"
    ],
    "machine_max_acceleration_y": [
      "1500",
      "1500"
    ],
    "machine_max_speed_z": [
      "15",
      "12"
    ],
    "machine_pause_gcode": "M10710 S0",
    "machine_start_gcode": "T[initial_extruder]\nM109 S{nozzle_temperature_initial_layer[current_extruder]}\n",
    "max_layer_height": [
      "0.8",
      "0.8"
    ],
    "min_layer_height": [
      "0.08",
      "0.08"
    ],
    "name": "iQ TiQ8 0.8 Nozzle",
    "nozzle_diameter": [
      "0.8",
      "0.8"
    ],
    "print_host": "https://simplyprint.io/panel",
    "printable_area": [
      "0x0",
      "500x0",
      "500x400",
      "0x400"
    ],
    "printable_height": "450",
    "printer_model": "TiQ8",
    "printer_notes": "Machine file version 1.0 20251106",
    "printer_settings_id": "iQ TiQ8 0.8 Nozzle",
    "printer_variant": "0.8",
    "retract_before_wipe": [
      "70%",
      "70%"
    ],
    "retract_length_toolchange": [
      "15",
      "15"
    ],
    "retract_lift_above": [
      "0",
      "0"
    ],
    "retract_lift_below": [
      "0",
      "0"
    ],
    "retract_lift_enforce": [
      "All Surfaces",
      "All Surfaces"
    ],
    "retract_on_top_layer": [
      "1",
      "1"
    ],
    "retract_restart_extra": [
      "0",
      "0"
    ],
    "retract_restart_extra_toolchange": [
      "-0.2",
      "-0.2"
    ],
    "retract_when_changing_layer": [
      "1",
      "1"
    ],
    "retraction_distances_when_cut": [
      "18",
      "18"
    ],
    "retraction_length": [
      "0.8",
      "0.9"
    ],
    "retraction_minimum_travel": [
      "1",
      "1"
    ],
    "retraction_speed": [
      "30",
      "30"
    ],
    "thumbnails": "",
    "travel_slope": [
      "3",
      "3"
    ],
    "type": "machine",
    "wipe": [
      "1",
      "1"
    ],
    "wipe_distance": [
      "1",
      "1"
    ],
    "z_hop": [
      "0.8",
      "0.8"
    ],
    "z_hop_types": [
      "Normal Lift",
      "Normal Lift"
    ]
  }
}

PROCESS = {
  "process/0.20mm Standard @iQ TiQ2 P1 - HPP4GF25 Grauts (0.4 Nozzle).json": {
    "bridge_flow": "1.07",
    "bridge_speed": "25",
    "brim_type": "no_brim",
    "compatible_printers": [
      "iQ TiQ2 0.4 Nozzle"
    ],
    "default_acceleration": "1500",
    "enable_extra_bridge_layer": "apply_to_all",
    "enable_prime_tower": "0",
    "enable_support": "1",
    "exclude_object": "0",
    "from": "system",
    "gcode_label_objects": "0",
    "inherits": "fdm_process_tiq_common",
    "initial_layer_infill_speed": "100",
    "inner_wall_acceleration": "1500",
    "inner_wall_speed": "100",
    "instantiation": "true",
    "internal_bridge_speed": "50%",
    "internal_solid_infill_speed": "60",
    "ironing_pattern": "concentric",
    "is_custom_defined": "0",
    "layer_height": "0.2",
    "name": "0.20mm Standard @iQ TiQ2 P1 - HPP4GF25 Grauts (0.4 Nozzle)",
    "notes": "Pre-Select:     FBA Time Delay: 0    EPC Factor: 0\n\nDeutsch P1 HPP4GF25\n\n1.   \u00dcberpr\u00fcfen Sie, dass sich das Grauts HPP4GF25 im linken Extruder befindet. Halten Sie das Filament trocken! Detailierte Trocknungsanleitung, siehe unten.\n\n2.   \u00dcberpr\u00fcfen Sie, dass sich eine 0,4 mm Wolfram-Kupfer D\u00fcse im linken Extruder befindet.\n\n3.   Verwenden Sie Magigoo Kleber f\u00fcr PPGF auf der PET-Folie, um eine bessere Haftung zu gew\u00e4hrleisten, im Singledruck in der Regel auf PET-Folie nicht erforderlich.\n\n4.   Reinigen Sie ggf. die D\u00fcse mit einer Messing-Drahtb\u00fcrste.\nNun sind sie bereit, um Ihren Druck zu starten.\n\n\nTipp: Am besten l\u00e4sst sich das Bauteil bei einer Druckplattentemperatur von 80\u00b0C entfernen, da dann der Kleber weich wird.\n\n\nEnglish P1 HPP4GF25\n\n1.   Check Left extruder filament: Grauts HPP4GF25 - Keep the filament dry!! Detailed drying instruction below.\n\n2.   Check left extruder nozzle: 0.4mm Wolfram\n\n3.   Check bed: PET with Magigoo glue for PPGF\n\n4.   Check nozzle: Clean it with brush\n\nWELLDONE! YOU ARE READY NOW TO START YOUR PRINT JOB!\n\n\nTip: The component is best removed at a printing plate temperature of 80\u00b0C, as this softens the adhesive.",
    "outer_wall_acceleration": "1500",
    "outer_wall_speed": "80",
    "prime_tower_width": "80",
    "print_settings_id": "0.20mm Standard @iQ TiQ2 P1 - HPP4GF25 Grauts (0.4 Nozzle)",
    "reduce_crossing_wall": "1",
    "skirt_height": "1",
    "skirt_loops": "2",
    "small_perimeter_speed": "30%",
    "small_perimeter_threshold": "5",
    "sparse_infill_density": "30%",
    "sparse_infill_pattern": "triangles",
    "sparse_infill_speed": "100",
    "support_angle": "0",
    "support_base_pattern": "default",
    "support_base_pattern_spacing": "1",
    "support_bottom_interface_spacing": "0.3",
    "support_bottom_z_distance": "0.24",
    "support_expansion": "0.5",
    "support_filament": "1",
    "support_interface_bottom_layers": "0",
    "support_interface_filament": "1",
    "support_interface_pattern": "rectilinear_interlaced",
    "support_interface_spacing": "0",
    "support_interface_top_layers": "3",
    "support_object_first_layer_gap": "0.3",
    "support_object_xy_distance": "0.35",
    "support_on_build_plate_only": "0",
    "support_speed": "100",
    "support_style": "snug",
    "support_top_z_distance": "0.2",
    "support_type": "normal(auto)",
    "top_shell_thickness": "0",
    "top_solid_infill_flow_ratio": "0.98",
    "top_surface_acceleration": "1500",
    "top_surface_speed": "80",
    "travel_acceleration": "1500",
    "tree_support_branch_diameter_angle": "10",
    "tree_support_branch_diameter_organic": "3",
    "tree_support_tip_diameter": "2",
    "type": "process",
    "version": "2.3.1.10",
    "wall_loops": "2"
  },
  "process/0.20mm Standard @iQ TiQ2 P1 - PACF Pro Fiberthree (0.4 Nozzle).json": {
    "bridge_flow": "1.07",
    "bridge_speed": "25",
    "brim_type": "no_brim",
    "compatible_printers": [
      "iQ TiQ2 0.4 Nozzle"
    ],
    "enable_support": "1",
    "exclude_object": "0",
    "from": "system",
    "gcode_label_objects": "0",
    "inherits": "fdm_process_tiq_common",
    "instantiation": "true",
    "internal_bridge_speed": "50%",
    "internal_solid_infill_speed": "60",
    "ironing_pattern": "concentric",
    "is_custom_defined": "0",
    "layer_height": "0.2",
    "name": "0.20mm Standard @iQ TiQ2 P1 - PACF Pro Fiberthree (0.4 Nozzle)",
    "prime_tower_width": "80",
    "print_settings_id": "0.20mm Standard @iQ TiQ2 P1 - PACF Pro Fiberthree (0.4 Nozzle)",
    "reduce_crossing_wall": "1",
    "skirt_height": "1",
    "skirt_loops": "2",
    "small_perimeter_speed": "30%",
    "small_perimeter_threshold": "5",
    "sparse_infill_density": "30%",
    "sparse_infill_pattern": "triangles",
    "support_angle": "45",
    "support_base_pattern": "rectilinear-grid",
    "support_base_pattern_spacing": "1",
    "support_bottom_interface_spacing": "0.3",
    "support_bottom_z_distance": "0.24",
    "support_expansion": "0.5",
    "support_filament": "0",
    "support_interface_filament": "0",
    "support_interface_pattern": "rectilinear_interlaced",
    "support_interface_spacing": "0",
    "support_object_xy_distance": "0.25",
    "support_on_build_plate_only": "1",
    "support_top_z_distance": "0.26",
    "support_type": "tree(auto)",
    "top_shell_thickness": "0",
    "top_solid_infill_flow_ratio": "0.98",
    "tree_support_branch_diameter_angle": "10",
    "tree_support_branch_diameter_organic": "3",
    "tree_support_tip_diameter": "2",
    "type": "process",
    "version": "2.2.0.4",
    "wall_loops": "2"
  },
  "process/0.20mm Standard @iQ TiQ2 P1 - PETG Polymax Polymaker (0.4 Nozzle).json": {
    "bottom_shell_layers": "4",
    "bottom_shell_thickness": "0.8",
    "bridge_flow": "1",
    "bridge_speed": "50",
    "brim_type": "no_brim",
    "compatible_printers": [
      "iQ TiQ2 0.4 Nozzle"
    ],
    "default_acceleration": "1500",
    "enable_extra_bridge_layer": "apply_to_all",
    "enable_overhang_speed": "0",
    "enable_prime_tower": "0",
    "enable_support": "1",
    "exclude_object": "0",
    "from": "system",
    "gap_infill_speed": "50",
    "gcode_label_objects": "0",
    "inherits": "fdm_process_tiq_common",
    "initial_layer_infill_speed": "25",
    "initial_layer_speed": "25",
    "initial_layer_travel_speed": "50%",
    "inner_wall_acceleration": "1500",
    "inner_wall_speed": "50",
    "instantiation": "true",
    "internal_bridge_speed": "150%",
    "internal_solid_infill_speed": "50",
    "name": "0.20mm Standard @iQ TiQ2 P1 - PETG Polymax Polymaker (0.4 Nozzle)",
    "notes": "Deutsch P1 Polymaker Polymax PETG Readme\n1.\t\u00dcberpr\u00fcfen Sie, dass sich das Polymaker Polymax PETG im linken Extruder befindet. Halten Sie das Filament trocken! Detailierte Trocknungsanleitung, siehe unten.\n2.\t\u00dcberpr\u00fcfen Sie, dass sich eine 0,4 mm Wolfram-Kupfer D\u00fcse im linken Extruder befindet.\n3.\tVerwenden Sie Magigoo Kleber auf der PET-Folie, um eine bessere Haftung zu gew\u00e4hrleisten. ( im Singledruck in der Regel auf PET-Folie nicht erforderlich)\n4.\tReinigen Sie ggf. die D\u00fcse mit einer Messing-Drahtb\u00fcrste.\nNun sind sie bereit, um Ihren Druck zu starten.\n\nAnleitung zum Trocknen von PETG:\nPETG-ESD ist hydrophil. Wenn Sie Stringing und Oozing an Ihrem Bauteil beobachten, ist dies ein Indiz daf\u00fcr, dass das Filament zu feucht ist. Um das Filament zu trocknen, belassen Sie die Spule in einem industriellen Ofen bei 70\u00b0C f\u00fcr 8 Stunden.\n\nEnglish P1 Polymaker Polymax PETG\n1.\tCheck Left extruder filament: Polymaker Polymax PETG - Keep the filament dry!! Detailed drying instruction below.\n2.\tCheck left extruder nozzle: 0.4mm Wolfram\n3.\tCheck bed: PET with Magigoo glue (not realy needed in a singelprint)\n4.\tCheck nozzle: Clean it with brush\nWELLDONE! YOU ARE READY NOW TO START YOUR PRINT JOB!\n\nFILAMENT DRYING INSTRUCTION\nPETG-ESD material is hydroscopic. If you feel you have stringing and oozing in your printed part, the filament have moisture in it.\nTo dry the filament, keep the spool in a industrial oven for 8 hours at 70\u00b0C.\n",
    "ooze_prevention": "0",
    "outer_wall_acceleration": "1500",
    "outer_wall_speed": "50",
    "print_settings_id": "0.20mm Standard @iQ TiQ2 P1 - PETG Polymax Polymaker (0.4 Nozzle)",
    "raft_first_layer_density": "100%",
    "raft_first_layer_expansion": "6",
    "reduce_crossing_wall": "0",
    "skirt_loops": "3",
    "slow_down_layers": "1",
    "small_perimeter_speed": "50",
    "small_perimeter_threshold": "0",
    "sparse_infill_density": "30%",
    "sparse_infill_pattern": "rectilinear",
    "sparse_infill_speed": "50",
    "support_angle": "0",
    "support_base_pattern": "rectilinear-grid",
    "support_base_pattern_spacing": "2.5",
    "support_bottom_interface_spacing": "0.5",
    "support_bottom_z_distance": "0.2",
    "support_expansion": "0",
    "support_filament": "0",
    "support_interface_filament": "0",
    "support_interface_pattern": "rectilinear_interlaced",
    "support_interface_spacing": "0",
    "support_interface_speed": "50",
    "support_interface_top_layers": "3",
    "support_line_width": "100%",
    "support_object_xy_distance": "0.35",
    "support_on_build_plate_only": "0",
    "support_speed": "50",
    "support_top_z_distance": "0.27",
    "support_type": "tree(auto)",
    "thick_internal_bridges": "0",
    "top_shell_thickness": "0.8",
    "top_solid_infill_flow_ratio": "1",
    "top_surface_acceleration": "1500",
    "top_surface_speed": "50",
    "travel_acceleration": "1500",
    "tree_support_branch_diameter_angle": "5",
    "tree_support_branch_diameter_organic": "8",
    "tree_support_tip_diameter": "0.8",
    "tree_support_wall_count": "2",
    "type": "process",
    "wall_direction": "ccw",
    "wall_loops": "3",
    "wall_sequence": "inner wall/outer wall"
  },
  "process/0.20mm Standard @iQ TiQ2 P2 - PACF Pro Fiberthree + VXL90 Xioneer (0.4 Nozzle).json": {
    "bridge_flow": "1.07",
    "bridge_speed": "25",
    "brim_type": "no_brim",
    "compatible_printers": [
      "iQ TiQ2 0.4 Nozzle"
    ],
    "enable_support": "1",
    "exclude_object": "0",
    "from": "system",
    "gap_infill_speed": "70",
    "gcode_label_objects": "0",
    "independent_support_layer_height": "0",
    "inherits": "fdm_process_tiq_common",
    "initial_layer_infill_speed": "75",
    "inner_wall_speed": "90",
    "instantiation": "true",
    "internal_bridge_speed": "50%",
    "internal_solid_infill_speed": "60",
    "ironing_pattern": "concentric",
    "is_custom_defined": "0",
    "layer_height": "0.2",
    "name": "0.20mm Standard @iQ TiQ2 P2 - PACF Pro Fiberthree + VXL90 Xioneer (0.4 Nozzle)",
    "notes": "Deutsch P2 PACF\n\n1.\tUeberpruefen Sie, dass sich das Fiberthree PACF Pro (100625) im linken Extruder befindet. Halten Sie das Filament trocken! Detailierte Trocknungsanleitung, siehe unten.\n2.\tueberpruefen Sie, dass sich eine 0,4 mm Wolfram-Kupfer Duese im linken Extruder befindet fuer PACF.\n3.\tueberpruefen Sie, dass sich eine 0,4 mm Wolfram-Kupfer Duese im rechten Extruder befindet fuer Xioneer VXL90 filament\n4.\tVerwenden Sie Magigoo PA Kleber auf der PET-Folie, um eine bessere Haftung zu gewaehrleisten.\n5.\tReinigen Sie ggf. die Duese mit einer Messing-Drahtbuerste.\nNun sind sie bereit, um Ihren Druck zu starten.\n\nTipp: Belassen Sie die Einstellung raft, damit sich das Bauteil einfach und ohne Beschaedigung der Folie vom Druckbett loesen laesst.\n\n\nAnleitung zum trocknen von PA-CF-Filament:\nNylon ist sehr hydrophil. Wenn Sie stringing und oozing an Ihrem Bauteil beobachten, ist dies ein Indiz dafuer, dass das Filament zu feucht ist.\nUm das Filament zu trocknen, belassen Sie die Spule in einem industriellen Trockner bei 75\u00b0C fuer 2-4 Tage mit 30 % Frischluftzirkulation.\n\n///// STUETZMATERIAL AUFLOESENDES VORGEHENSWEISE ///////\nVERBRAUCHSSTOFFE FUER DAS AUFLOESEN VON STUETZMATERIAL KOENNEN BEI innovatiQ ERWORBEN WERDEN.\n1. Lesen Sie die Sicherheitshinweise zu Ihrer Entnahmestation fuer Industriestuetzen.\n2. Brechen Sie die \"leicht zu entfernenden Stuetzen\" vorsichtig so weit wie moeglich vom Teil ab. Das spart Zeit und Reinigungsmittel beim Loesen.\n3. Das Verhaeltnis von \"Reinigungsmittel\" zu \"aufzuloesendem Traeger\" ist 1:1. Wenn Sie z. B. 100 g Traeger auf Ihrem Teil haben, muessen Sie 100 g Reinigungsmittel mit Wasser hinzufuegen.\n4. Die Solltemperatur der Aufloesestation zum Aufloesen von Xioneer VXL90 zusammen mit PACF betraegt 60\u00b0C. Ein ueberschreiten dieser Temperatur fuehrt zu einer Verformung des Werkstuecks.\n5. Fuer PACF wird eine Aufloesungszeit von etwa 5 bis 6 Stunden empfohlen.\n6. Nach dem Aufloesen ist die geloeste Fluessigkeit als alkalischer Industrieabfall zu entsorgen.\n7. Ausfuehrliche Informationen entnehmen Sie bitte den technischen Datenblaettern, der Betriebsanleitung und den Sicherheitsdatenblaettern von Xioneer VXL90 und Xioneer VXL EX detergent.\n\n\n\nEnglish P2 - PACF\n1.\tCheck Left extruder filament: innovatiQ PACF 100625 - Keep the filament dry!! Detailed drying instruction below.\n2.\tCheck left extruder nozzle: 0.4mm Wolfram for PACF\n3.\tCheck right extruder nozzle: 0.4mm Wolfram for Xioneer VXL90 filament\n4.\tCheck bed: PET with Magigoo PA glue\n5.\tCheck nozzle: Clean it with brush\nWELLDONE! YOU ARE READY NOW TO START YOUR PRINT JOB!\n\nTip for EASY part removal from print bed: Leave the raft-setting, to remove the part from the bed without damaging the foil.\n\n\nFILAMENT DRYING INSTRUCTION\nNylon material is highly hydroscopic. If you feel you have stringing and oozing in your printed part, the filament have moisture in it.\nTo dry the filament, keep the spool in a industrial oven for 2-4 days at 75\u00b0C with 30% fresh air intake circulation.\n\n///// SUPPORT DISSOLVING PROCEDURE ///////\nCONSUMABLES FOR DISSOLVING SUPPORT CAN BE PURCHASED FROM innovatiQ.\n1. Read the safety instructions of your Industrial support removal station.\n2. Carefully break-off the 'easy to remove supports' as much as possible from the part. This will save time and detergent in the dissolving process.\n3. The ratio of the 'detergent' to 'support to dissolve' is 1:1. Eg. If you have 100g of support on your part, you have to add 100g of detergent with water.\n4. The Set temperature of the dissolving station to dissolve Xioneer VXL90 together with PACF is 60\u00b0C. Exceeding this temperature will deform your part.\n5. For PACF, around 5 to 6 hours of dissolving time is recommeneded.\n6. After the dissolving process, dispose the dissolved liquid as alkaline industrial waste.\n7. For detailed information, please read the technical data sheets, operating instruction and safety data sheets of Xioneer VXL90 and Xioneer VXL EX detergent.",
    "outer_wall_speed": "70",
    "prime_tower_width": "80",
    "prime_volume": "80",
    "print_settings_id": "0.20mm Standard @iQ TiQ2 P2 - PACF Pro Fiberthree + VXL90 Xioneer (0.4 Nozzle)",
    "reduce_crossing_wall": "1",
    "skirt_height": "1",
    "skirt_loops": "2",
    "small_perimeter_speed": "30%",
    "small_perimeter_threshold": "5",
    "sparse_infill_density": "50%",
    "sparse_infill_pattern": "triangles",
    "sparse_infill_speed": "80",
    "support_angle": "45",
    "support_base_pattern": "rectilinear",
    "support_base_pattern_spacing": "1",
    "support_bottom_interface_spacing": "0.3",
    "support_bottom_z_distance": "0",
    "support_expansion": "1.7",
    "support_filament": "2",
    "support_interface_filament": "2",
    "support_interface_pattern": "rectilinear_interlaced",
    "support_interface_spacing": "0.1",
    "support_interface_speed": "50",
    "support_line_width": "100%",
    "support_object_xy_distance": "0.6",
    "support_on_build_plate_only": "0",
    "support_speed": "75",
    "support_style": "snug",
    "support_top_z_distance": "0.02",
    "support_type": "normal(auto)",
    "top_shell_thickness": "0",
    "top_solid_infill_flow_ratio": "1.01",
    "top_surface_speed": "75",
    "tree_support_branch_diameter_angle": "10",
    "tree_support_branch_diameter_organic": "3",
    "tree_support_tip_diameter": "2",
    "type": "process",
    "version": "2.2.0.4",
    "wall_generator": "classic",
    "wall_loops": "2",
    "wipe_tower_extra_spacing": "110%",
    "wipe_tower_max_purge_speed": "50"
  },
  "process/0.20mm Standard @iQ TiQ8 P1 - ABS Natur Material4Print (0.4 Nozzle).json": {
    "bottom_shell_layers": "4",
    "bridge_flow": "1.4",
    "bridge_speed": "100",
    "brim_object_gap": "0.05",
    "brim_type": "outer_only",
    "compatible_printers": [
      "iQ TiQ8 0.4 Nozzle"
    ],
    "default_acceleration": "600",
    "enable_overhang_speed": "0",
    "enable_prime_tower": "0",
    "enable_support": "1",
    "exclude_object": "0",
    "from": "system",
    "gcode_label_objects": "0",
    "independent_support_layer_height": "1",
    "inherits": "fdm_process_tiq_common",
    "initial_layer_infill_speed": "80",
    "initial_layer_speed": "80",
    "inner_wall_acceleration": "600",
    "inner_wall_speed": "140",
    "instantiation": "true",
    "internal_bridge_speed": "50%",
    "internal_solid_infill_speed": "50",
    "ironing_pattern": "concentric",
    "layer_height": "0.2",
    "name": "0.20mm Standard @iQ TiQ8 P1 - ABS Natur Material4Print (0.4 Nozzle)",
    "notes": "Process file version 1.0 20250620",
    "outer_wall_acceleration": "600",
    "outer_wall_speed": "90",
    "prime_tower_width": "80",
    "print_settings_id": "0.20mm Standard @iQ TiQ8 P1 - ABS Natur Material4Print (0.4 Nozzle)",
    "raft_first_layer_expansion": "3",
    "reduce_crossing_wall": "1",
    "skirt_height": "3",
    "skirt_loops": "2",
    "slow_down_layers": "1",
    "small_perimeter_speed": "5%",
    "small_perimeter_threshold": "0",
    "sparse_infill_acceleration": "50",
    "sparse_infill_density": "35%",
    "sparse_infill_pattern": "triangles",
    "sparse_infill_speed": "160",
    "support_angle": "45",
    "support_base_pattern": "default",
    "support_base_pattern_spacing": "3",
    "support_bottom_interface_spacing": "0",
    "support_bottom_z_distance": "0.5",
    "support_expansion": "1",
    "support_filament": "1",
    "support_interface_filament": "1",
    "support_interface_pattern": "auto",
    "support_interface_spacing": "0.2",
    "support_interface_speed": "100",
    "support_object_xy_distance": "0.04",
    "support_on_build_plate_only": "0",
    "support_speed": "300",
    "support_threshold_angle": "35",
    "support_top_z_distance": "0.2",
    "support_type": "normal(auto)",
    "top_shell_thickness": "0",
    "top_solid_infill_flow_ratio": "0.98",
    "top_surface_acceleration": "600",
    "top_surface_speed": "140",
    "travel_acceleration": "600",
    "travel_speed": "300",
    "tree_support_branch_diameter_angle": "10",
    "tree_support_branch_diameter_organic": "3",
    "tree_support_tip_diameter": "2",
    "type": "process",
    "wall_loops": "2"
  },
  "process/fdm_process_tiq_common.json": {
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
    "default_acceleration": "5000",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "0",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "1",
    "enable_support": "0",
    "exclude_object": "1",
    "filename_format": "{input_filename_base}_{layer_height}mm_{filament_type[initial_tool]}_{printer_model}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "100",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "25%",
    "initial_layer_acceleration": "500",
    "initial_layer_infill_speed": "105",
    "initial_layer_line_width": "120%",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "50",
    "inner_wall_acceleration": "5000",
    "inner_wall_line_width": "110%",
    "inner_wall_speed": "200",
    "instantiation": "false",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "120%",
    "internal_solid_infill_speed": "200",
    "ironing_flow": "10%",
    "ironing_spacing": "0.15",
    "ironing_speed": "30",
    "ironing_type": "no ironing",
    "layer_height": "0.2",
    "line_width": "110%",
    "max_travel_detour_distance": "0",
    "min_skirt_length": "4",
    "minimum_sparse_infill_area": "15",
    "name": "fdm_process_tiq_common",
    "ooze_prevention": "1",
    "outer_wall_acceleration": "3000",
    "outer_wall_line_width": "100%",
    "outer_wall_speed": "120",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "50",
    "overhang_3_4_speed": "30",
    "overhang_4_4_speed": "10",
    "preheat_steps": "1",
    "preheat_time": "30",
    "prime_tower_width": "60",
    "print_sequence": "by layer",
    "print_settings_id": "fdm_process_tiq_common",
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
    "sparse_infill_speed": "200",
    "spiral_mode": "0",
    "standby_temperature_delta": "-40",
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
    "top_surface_acceleration": "3000",
    "top_surface_line_width": "93.75%",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "100",
    "travel_acceleration": "7000",
    "travel_speed": "350",
    "tree_support_branch_angle": "30",
    "tree_support_wall_count": "0",
    "tree_support_with_infill": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "3",
    "wipe_tower_cone_angle": "25",
    "wipe_tower_extra_spacing": "150%",
    "wipe_tower_no_sparse_layers": "0",
    "wipe_tower_rotation_angle": "90",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  }
}

FILAMENT = {
  "filament/Fiberthree PACF Pro P1 @iQ TiQ2 0.4 Nozzle.json": {
    "activate_air_filtration": [
      "0"
    ],
    "activate_chamber_temp_control": [
      "0"
    ],
    "adaptive_pressure_advance": [
      "0"
    ],
    "adaptive_pressure_advance_bridges": [
      "0"
    ],
    "adaptive_pressure_advance_model": [
      "0,0,0\n0,0,0"
    ],
    "adaptive_pressure_advance_overhangs": [
      "0"
    ],
    "additional_cooling_fan_speed": [
      "0"
    ],
    "chamber_temperature": [
      "0"
    ],
    "close_fan_the_first_x_layers": [
      "3"
    ],
    "compatible_printers": [
      "iQ TiQ2 0.4 Nozzle"
    ],
    "compatible_printers_condition": "",
    "compatible_prints": [
      "0.20mm Standard @iQ TiQ2 P1 - PACF Pro Fiberthree (0.4 Nozzle)"
    ],
    "compatible_prints_condition": "",
    "complete_print_exhaust_fan_speed": [
      "80"
    ],
    "cool_plate_temp": [
      "105"
    ],
    "cool_plate_temp_initial_layer": [
      "105"
    ],
    "default_filament_colour": [
      "#000000"
    ],
    "dont_slow_down_outer_wall": [
      "0"
    ],
    "during_print_exhaust_fan_speed": [
      "60"
    ],
    "enable_overhang_bridge_fan": [
      "1"
    ],
    "enable_pressure_advance": [
      "0"
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
    "filament_cooling_final_speed": [
      "3.5"
    ],
    "filament_cooling_initial_speed": [
      "10"
    ],
    "filament_cooling_moves": [
      "2"
    ],
    "filament_cost": [
      "20"
    ],
    "filament_density": [
      "1.04"
    ],
    "filament_deretraction_speed": [
      "nil"
    ],
    "filament_diameter": [
      "1.75"
    ],
    "filament_end_gcode": [
      "; filament end gcode\n{if current_extruder==0}\nG1 Z{layer_z+2} F900 ; safe distance for T0 while tool change\nG1 X-17 Y1 F9000\nG1 X-17 Y45 F9000\nG1 Y1 F9000\nG1 Y45 F9000\n{endif}\n\n{if current_extruder==1}\n{if current_extruder==0}T1{endif}\nG1 X-23 Y3 F9000\nG1 Y45 F9000\nG1 Y3 F9000\nG1 Y45 F9000\n{endif}\n"
    ],
    "filament_flow_ratio": [
      "1.089"
    ],
    "filament_id": "IQM1",
    "filament_is_support": [
      "0"
    ],
    "filament_loading_speed": [
      "10"
    ],
    "filament_loading_speed_start": [
      "50"
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
      "1"
    ],
    "filament_multitool_ramming_flow": [
      "40"
    ],
    "filament_multitool_ramming_volume": [
      "10"
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
      "4"
    ],
    "filament_retraction_minimum_travel": [
      "nil"
    ],
    "filament_retraction_speed": [
      "40"
    ],
    "filament_settings_id": [
      "Fiberthree PACF Pro P1 @iQ TiQ2 0.4 Nozzle"
    ],
    "filament_shrink": [
      "100%"
    ],
    "filament_shrinkage_compensation_z": [
      "100%"
    ],
    "filament_soluble": [
      "0"
    ],
    "filament_stamping_distance": [
      "45"
    ],
    "filament_stamping_loading_speed": [
      "29"
    ],
    "filament_start_gcode": [
      "; Filament gcode\n{if current_extruder==0}\nG1 X-17 Y1 F9000\nG1 Y45 F9000\nG1 Y1 F9000\nG1 Y45 F9000\n{if layer_z==0}G1 Z{first_layer_height + 2.0}{endif}\n{if layer_z==0}G1 X[first_layer_print_min_0] Y[first_layer_print_min_1]{endif}\n{if layer_z==0}G1 Z{layer_z}{endif}\n{endif}\n\n{if current_extruder==1}\nG1 X-23 Y3 F9000\nG1 Y45 F9000\nG1 Y3 F9000\nG1 Y45 F9000\n{endif}\n"
    ],
    "filament_toolchange_delay": [
      "0"
    ],
    "filament_type": [
      "PACF Pro"
    ],
    "filament_unloading_speed": [
      "100"
    ],
    "filament_unloading_speed_start": [
      "100"
    ],
    "filament_vendor": [
      "iQ Materials"
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
      "75"
    ],
    "hot_plate_temp_initial_layer": [
      "75"
    ],
    "idle_temperature": [
      "250"
    ],
    "inherits": "fdm_filament_common",
    "instantiation": "true",
    "internal_bridge_fan_speed": [
      "-1"
    ],
    "name": "Fiberthree PACF Pro P1 @iQ TiQ2 0.4 Nozzle",
    "nozzle_temperature": [
      "265"
    ],
    "nozzle_temperature_initial_layer": [
      "265"
    ],
    "nozzle_temperature_range_high": [
      "270"
    ],
    "nozzle_temperature_range_low": [
      "250"
    ],
    "overhang_fan_speed": [
      "80"
    ],
    "overhang_fan_threshold": [
      "25%"
    ],
    "pellet_flow_coefficient": [
      "0.4157"
    ],
    "pressure_advance": [
      "0.02"
    ],
    "reduce_fan_stop_start_freq": [
      "1"
    ],
    "required_nozzle_HRC": [
      "0"
    ],
    "setting_id": "IQS1",
    "slow_down_for_layer_cooling": [
      "1"
    ],
    "slow_down_layer_time": [
      "3"
    ],
    "slow_down_min_speed": [
      "10"
    ],
    "supertack_plate_temp": [
      "35"
    ],
    "supertack_plate_temp_initial_layer": [
      "35"
    ],
    "support_material_interface_fan_speed": [
      "-1"
    ],
    "temperature_vitrification": [
      "110"
    ],
    "textured_cool_plate_temp": [
      "40"
    ],
    "textured_cool_plate_temp_initial_layer": [
      "40"
    ],
    "textured_plate_temp": [
      "105"
    ],
    "textured_plate_temp_initial_layer": [
      "105"
    ],
    "type": "filament"
  },
  "filament/Fiberthree PACF Pro P2 @iQ TiQ2 0.4 Nozzle.json": {
    "activate_air_filtration": [
      "0"
    ],
    "activate_chamber_temp_control": [
      "0"
    ],
    "adaptive_pressure_advance": [
      "0"
    ],
    "adaptive_pressure_advance_bridges": [
      "0"
    ],
    "adaptive_pressure_advance_model": [
      "0,0,0\n0,0,0"
    ],
    "adaptive_pressure_advance_overhangs": [
      "0"
    ],
    "additional_cooling_fan_speed": [
      "0"
    ],
    "chamber_temperature": [
      "0"
    ],
    "close_fan_the_first_x_layers": [
      "3"
    ],
    "compatible_printers": [
      "iQ TiQ2 0.4 Nozzle"
    ],
    "compatible_printers_condition": "",
    "compatible_prints": [
      "0.20mm Standard @iQ TiQ2 P2 - PACF Pro Fiberthree + VXL90 Xioneer (0.4 Nozzle)"
    ],
    "compatible_prints_condition": "",
    "complete_print_exhaust_fan_speed": [
      "80"
    ],
    "cool_plate_temp": [
      "105"
    ],
    "cool_plate_temp_initial_layer": [
      "105"
    ],
    "default_filament_colour": [
      "#000000"
    ],
    "dont_slow_down_outer_wall": [
      "0"
    ],
    "during_print_exhaust_fan_speed": [
      "60"
    ],
    "enable_overhang_bridge_fan": [
      "1"
    ],
    "enable_pressure_advance": [
      "0"
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
    "filament_cooling_final_speed": [
      "3.5"
    ],
    "filament_cooling_initial_speed": [
      "10"
    ],
    "filament_cooling_moves": [
      "2"
    ],
    "filament_cost": [
      "200"
    ],
    "filament_density": [
      "1.25"
    ],
    "filament_deretraction_speed": [
      "nil"
    ],
    "filament_diameter": [
      "1.75"
    ],
    "filament_end_gcode": [
      "; filament end gcode\n{if current_extruder==0}\nG1 Z{layer_z+2} F900 ; safe distance for T0 while tool change\nG1 X-17 Y1 F9000\nG1 X-17 Y45 F9000\nG1 Y1 F9000\nG1 Y45 F9000\n{endif}\n\n{if current_extruder==1}\n{if current_extruder==0}T1{endif}\nG1 X-23 Y3 F9000\nG1 Y45 F9000\nG1 Y3 F9000\nG1 Y45 F9000\n{endif}"
    ],
    "filament_flow_ratio": [
      "1.1"
    ],
    "filament_id": "IQM7",
    "filament_is_support": [
      "0"
    ],
    "filament_loading_speed": [
      "10"
    ],
    "filament_loading_speed_start": [
      "50"
    ],
    "filament_long_retractions_when_cut": [
      "nil"
    ],
    "filament_max_volumetric_speed": [
      "8"
    ],
    "filament_minimal_purge_on_wipe_tower": [
      "15"
    ],
    "filament_multitool_ramming": [
      "0"
    ],
    "filament_multitool_ramming_flow": [
      "40"
    ],
    "filament_multitool_ramming_volume": [
      "10"
    ],
    "filament_notes": [
      "Filament file version 1.0 20251103"
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
      "4"
    ],
    "filament_retraction_minimum_travel": [
      "nil"
    ],
    "filament_retraction_speed": [
      "40"
    ],
    "filament_settings_id": [
      "Fiberthree PACF Pro P2 @iQ TiQ2 0.4 Nozzle"
    ],
    "filament_shrink": [
      "100%"
    ],
    "filament_shrinkage_compensation_z": [
      "100%"
    ],
    "filament_soluble": [
      "0"
    ],
    "filament_stamping_distance": [
      "45"
    ],
    "filament_stamping_loading_speed": [
      "29"
    ],
    "filament_start_gcode": [
      "; Filament gcode\n{if current_extruder==0}\nG1 X-17 Y1 F9000\nG1 Y45 F9000\nG1 Y1 F9000\nG1 Y45 F9000\n{if layer_z==0}G1 Z{first_layer_height + 2.0}{endif}\n{if layer_z==0}G1 X[first_layer_print_min_0] Y[first_layer_print_min_1]{endif}\n{if layer_z==0}G1 Z{layer_z}{endif}\n{endif}\n\n{if current_extruder==1}\nG1 X-23 Y3 F9000\nG1 Y45 F9000\nG1 Y3 F9000\nG1 Y45 F9000\n{endif}"
    ],
    "filament_toolchange_delay": [
      "0"
    ],
    "filament_type": [
      "PACF Pro"
    ],
    "filament_unloading_speed": [
      "100"
    ],
    "filament_unloading_speed_start": [
      "100"
    ],
    "filament_vendor": [
      "iQ Materials"
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
      "100"
    ],
    "hot_plate_temp_initial_layer": [
      "100"
    ],
    "idle_temperature": [
      "240"
    ],
    "inherits": "fdm_filament_common",
    "instantiation": "true",
    "internal_bridge_fan_speed": [
      "-1"
    ],
    "is_custom_defined": "0",
    "name": "Fiberthree PACF Pro P2 @iQ TiQ2 0.4 Nozzle",
    "nozzle_temperature": [
      "275"
    ],
    "nozzle_temperature_initial_layer": [
      "275"
    ],
    "nozzle_temperature_range_high": [
      "275"
    ],
    "nozzle_temperature_range_low": [
      "250"
    ],
    "overhang_fan_speed": [
      "80"
    ],
    "overhang_fan_threshold": [
      "25%"
    ],
    "pellet_flow_coefficient": [
      "0.4157"
    ],
    "pressure_advance": [
      "0.02"
    ],
    "reduce_fan_stop_start_freq": [
      "1"
    ],
    "required_nozzle_HRC": [
      "0"
    ],
    "setting_id": "IQS7",
    "slow_down_for_layer_cooling": [
      "1"
    ],
    "slow_down_layer_time": [
      "3"
    ],
    "slow_down_min_speed": [
      "10"
    ],
    "supertack_plate_temp": [
      "35"
    ],
    "supertack_plate_temp_initial_layer": [
      "35"
    ],
    "support_material_interface_fan_speed": [
      "-1"
    ],
    "temperature_vitrification": [
      "110"
    ],
    "textured_cool_plate_temp": [
      "40"
    ],
    "textured_cool_plate_temp_initial_layer": [
      "40"
    ],
    "textured_plate_temp": [
      "105"
    ],
    "textured_plate_temp_initial_layer": [
      "105"
    ],
    "type": "filament",
    "version": "2.3.1.10"
  },
  "filament/Grauts HPP4GF25 P1 @iQ TiQ2 0.4 Nozzle.json": {
    "activate_air_filtration": [
      "0"
    ],
    "activate_chamber_temp_control": [
      "0"
    ],
    "adaptive_pressure_advance": [
      "0"
    ],
    "adaptive_pressure_advance_bridges": [
      "0"
    ],
    "adaptive_pressure_advance_model": [
      "0,0,0\n0,0,0"
    ],
    "adaptive_pressure_advance_overhangs": [
      "0"
    ],
    "additional_cooling_fan_speed": [
      "0"
    ],
    "chamber_temperature": [
      "0"
    ],
    "close_fan_the_first_x_layers": [
      "3"
    ],
    "compatible_printers": [
      "iQ TiQ2 0.4 Nozzle"
    ],
    "compatible_printers_condition": "",
    "compatible_prints": [
      "0.20mm Standard @iQ TiQ2 P1 - HPP4GF25 Grauts (0.4 Nozzle)"
    ],
    "compatible_prints_condition": "",
    "complete_print_exhaust_fan_speed": [
      "80"
    ],
    "cool_plate_temp": [
      "105"
    ],
    "cool_plate_temp_initial_layer": [
      "105"
    ],
    "default_filament_colour": [
      "#000000"
    ],
    "dont_slow_down_outer_wall": [
      "0"
    ],
    "during_print_exhaust_fan_speed": [
      "60"
    ],
    "enable_overhang_bridge_fan": [
      "1"
    ],
    "enable_pressure_advance": [
      "0"
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
    "filament_cooling_final_speed": [
      "3.5"
    ],
    "filament_cooling_initial_speed": [
      "10"
    ],
    "filament_cooling_moves": [
      "2"
    ],
    "filament_cost": [
      "70.58"
    ],
    "filament_density": [
      "1.09"
    ],
    "filament_deretraction_speed": [
      "nil"
    ],
    "filament_diameter": [
      "1.75"
    ],
    "filament_end_gcode": [
      "; filament end gcode\n{if current_extruder==0}\nG1 Z{layer_z+2} F900 ; safe distance for T0 while tool change\nG1 X-17 Y1 F9000\nG1 X-17 Y45 F9000\nG1 Y1 F9000\nG1 Y45 F9000\n{endif}\n\n{if current_extruder==1}\n{if current_extruder==0}T1{endif}\nG1 X-23 Y3 F9000\nG1 Y45 F9000\nG1 Y3 F9000\nG1 Y45 F9000\n{endif}\n"
    ],
    "filament_flow_ratio": [
      "0.926"
    ],
    "filament_id": "IQM1",
    "filament_is_support": [
      "0"
    ],
    "filament_loading_speed": [
      "10"
    ],
    "filament_loading_speed_start": [
      "50"
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
      "1"
    ],
    "filament_multitool_ramming_flow": [
      "40"
    ],
    "filament_multitool_ramming_volume": [
      "10"
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
      "4"
    ],
    "filament_retraction_minimum_travel": [
      "nil"
    ],
    "filament_retraction_speed": [
      "40"
    ],
    "filament_settings_id": [
      "Grauts HPP4GF25 P1 @iQ TiQ2 0.4 Nozzle"
    ],
    "filament_shrink": [
      "98.994%"
    ],
    "filament_shrinkage_compensation_z": [
      "99%"
    ],
    "filament_soluble": [
      "0"
    ],
    "filament_stamping_distance": [
      "45"
    ],
    "filament_stamping_loading_speed": [
      "29"
    ],
    "filament_start_gcode": [
      "; Filament gcode\n{if current_extruder==0}\nG1 X-17 Y1 F9000\nG1 Y45 F9000\nG1 Y1 F9000\nG1 Y45 F9000\n{if layer_z==0}G1 Z{first_layer_height + 2.0}{endif}\n{if layer_z==0}G1 X[first_layer_print_min_0] Y[first_layer_print_min_1]{endif}\n{if layer_z==0}G1 Z{layer_z}{endif}\n{endif}\n\n{if current_extruder==1}\nG1 X-23 Y3 F9000\nG1 Y45 F9000\nG1 Y3 F9000\nG1 Y45 F9000\n{endif}\n"
    ],
    "filament_toolchange_delay": [
      "0"
    ],
    "filament_type": [
      "HPP4GF25"
    ],
    "filament_unloading_speed": [
      "100"
    ],
    "filament_unloading_speed_start": [
      "100"
    ],
    "filament_vendor": [
      "iQ Materials"
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
      "110"
    ],
    "hot_plate_temp_initial_layer": [
      "110"
    ],
    "idle_temperature": [
      "180"
    ],
    "inherits": "fdm_filament_common",
    "instantiation": "true",
    "internal_bridge_fan_speed": [
      "-1"
    ],
    "is_custom_defined": "0",
    "name": "Grauts HPP4GF25 P1 @iQ TiQ2 0.4 Nozzle",
    "nozzle_temperature": [
      "220"
    ],
    "nozzle_temperature_initial_layer": [
      "220"
    ],
    "nozzle_temperature_range_high": [
      "280"
    ],
    "nozzle_temperature_range_low": [
      "220"
    ],
    "overhang_fan_speed": [
      "80"
    ],
    "overhang_fan_threshold": [
      "25%"
    ],
    "pellet_flow_coefficient": [
      "0.4157"
    ],
    "pressure_advance": [
      "0.02"
    ],
    "reduce_fan_stop_start_freq": [
      "1"
    ],
    "required_nozzle_HRC": [
      "0"
    ],
    "setting_id": "IQS1",
    "slow_down_for_layer_cooling": [
      "1"
    ],
    "slow_down_layer_time": [
      "3"
    ],
    "slow_down_min_speed": [
      "10"
    ],
    "supertack_plate_temp": [
      "35"
    ],
    "supertack_plate_temp_initial_layer": [
      "35"
    ],
    "support_material_interface_fan_speed": [
      "-1"
    ],
    "temperature_vitrification": [
      "127"
    ],
    "textured_cool_plate_temp": [
      "40"
    ],
    "textured_cool_plate_temp_initial_layer": [
      "40"
    ],
    "textured_plate_temp": [
      "105"
    ],
    "textured_plate_temp_initial_layer": [
      "105"
    ],
    "type": "filament",
    "version": "2.3.1.10"
  },
  "filament/Material4Print ABS Natur P1 @iQ TiQ8 0.4 Nozzle.json": {
    "activate_air_filtration": [
      "0"
    ],
    "activate_chamber_temp_control": [
      "1"
    ],
    "adaptive_pressure_advance": [
      "0"
    ],
    "adaptive_pressure_advance_bridges": [
      "0"
    ],
    "adaptive_pressure_advance_model": [
      "0,0,0\n0,0,0"
    ],
    "adaptive_pressure_advance_overhangs": [
      "0"
    ],
    "additional_cooling_fan_speed": [
      "0"
    ],
    "chamber_temperature": [
      "75"
    ],
    "close_fan_the_first_x_layers": [
      "1000"
    ],
    "compatible_printers": [
      "iQ TiQ8 0.4 Nozzle"
    ],
    "compatible_printers_condition": "",
    "compatible_prints": [
      "0.20mm Standard @iQ TiQ8 P1 - ABS Natur Material4Print (0.4 Nozzle)"
    ],
    "compatible_prints_condition": "",
    "complete_print_exhaust_fan_speed": [
      "70"
    ],
    "cool_plate_temp": [
      "105"
    ],
    "cool_plate_temp_initial_layer": [
      "105"
    ],
    "default_filament_colour": [
      "#FFFFFF"
    ],
    "dont_slow_down_outer_wall": [
      "0"
    ],
    "during_print_exhaust_fan_speed": [
      "60"
    ],
    "enable_overhang_bridge_fan": [
      "0"
    ],
    "enable_pressure_advance": [
      "0"
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
      "0"
    ],
    "fan_min_speed": [
      "0"
    ],
    "filament_cooling_final_speed": [
      "3.5"
    ],
    "filament_cooling_initial_speed": [
      "10"
    ],
    "filament_cooling_moves": [
      "2"
    ],
    "filament_cost": [
      "20"
    ],
    "filament_density": [
      "1.04"
    ],
    "filament_deretraction_speed": [
      "30"
    ],
    "filament_diameter": [
      "1.75"
    ],
    "filament_end_gcode": [
      "; filament end gcode"
    ],
    "filament_flow_ratio": [
      "0.926"
    ],
    "filament_id": "IQM2",
    "filament_is_support": [
      "0"
    ],
    "filament_loading_speed": [
      "10"
    ],
    "filament_loading_speed_start": [
      "50"
    ],
    "filament_long_retractions_when_cut": [
      "nil"
    ],
    "filament_max_volumetric_speed": [
      "14"
    ],
    "filament_minimal_purge_on_wipe_tower": [
      "15"
    ],
    "filament_multitool_ramming": [
      "1"
    ],
    "filament_multitool_ramming_flow": [
      "40"
    ],
    "filament_multitool_ramming_volume": [
      "10"
    ],
    "filament_notes": [
      "Filament file version 1.0 20250620"
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
      "0.4"
    ],
    "filament_retraction_minimum_travel": [
      "nil"
    ],
    "filament_retraction_speed": [
      "30"
    ],
    "filament_settings_id": [
      "Material4Print ABS Natur P1 @iQ TiQ8 0.4 Nozzle"
    ],
    "filament_shrink": [
      "99.2%"
    ],
    "filament_shrinkage_compensation_z": [
      "99.18%"
    ],
    "filament_soluble": [
      "0"
    ],
    "filament_stamping_distance": [
      "45"
    ],
    "filament_stamping_loading_speed": [
      "29"
    ],
    "filament_start_gcode": [
      "M109 S{nozzle_temperature_initial_layer[current_extruder]}\nG1 x-12 Y-13 Z44 F4000\nG4 P400\nG1 X-55\nG1 X-13 Y-4\nG1 X-51 Y-26\nG1 X-12 Y-13\nG1 X-55\nG1 X-13 Y-4\nG1 X-51 Y-26\nG1 X-12 Y-13\nG1 x-12 Y-13 F4000; Filament gcode\n{if layer_z==0}G1 Z{first_layer_height + 2.0}{endif}\n{if layer_z==0}G1 X[first_layer_print_min_0] Y[first_layer_print_min_1]{endif}\n{if layer_z==0}G1 Z{layer_z}{endif}\n",
      "; Filament gcode\n"
    ],
    "filament_toolchange_delay": [
      "0"
    ],
    "filament_type": [
      "ABS Material4Print Natur"
    ],
    "filament_unloading_speed": [
      "100"
    ],
    "filament_unloading_speed_start": [
      "100"
    ],
    "filament_vendor": [
      "iQ Materials"
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
      "105"
    ],
    "hot_plate_temp_initial_layer": [
      "105"
    ],
    "idle_temperature": [
      "0"
    ],
    "inherits": "fdm_filament_common",
    "instantiation": "true",
    "internal_bridge_fan_speed": [
      "-1"
    ],
    "name": "Material4Print ABS Natur P1 @iQ TiQ8 0.4 Nozzle",
    "nozzle_temperature": [
      "240"
    ],
    "nozzle_temperature_initial_layer": [
      "240"
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
    "pellet_flow_coefficient": [
      "0.4157"
    ],
    "pressure_advance": [
      "0.02"
    ],
    "reduce_fan_stop_start_freq": [
      "0"
    ],
    "required_nozzle_HRC": [
      "0"
    ],
    "setting_id": "IQS2",
    "slow_down_for_layer_cooling": [
      "0"
    ],
    "slow_down_layer_time": [
      "0"
    ],
    "slow_down_min_speed": [
      "10"
    ],
    "supertack_plate_temp": [
      "0"
    ],
    "supertack_plate_temp_initial_layer": [
      "0"
    ],
    "support_material_interface_fan_speed": [
      "-1"
    ],
    "temperature_vitrification": [
      "110"
    ],
    "textured_cool_plate_temp": [
      "40"
    ],
    "textured_cool_plate_temp_initial_layer": [
      "40"
    ],
    "textured_plate_temp": [
      "105"
    ],
    "textured_plate_temp_initial_layer": [
      "105"
    ],
    "type": "filament"
  },
  "filament/Polymaker PETG Polymax black P1 @iQ TiQ2 0.4 Nozzle.json": {
    "activate_air_filtration": [
      "0"
    ],
    "activate_chamber_temp_control": [
      "0"
    ],
    "adaptive_pressure_advance": [
      "0"
    ],
    "adaptive_pressure_advance_bridges": [
      "0"
    ],
    "adaptive_pressure_advance_model": [
      "0,0,0\n0,0,0"
    ],
    "adaptive_pressure_advance_overhangs": [
      "0"
    ],
    "additional_cooling_fan_speed": [
      "0"
    ],
    "chamber_temperature": [
      "0"
    ],
    "close_fan_the_first_x_layers": [
      "1000"
    ],
    "compatible_printers": [
      "iQ TiQ2 0.4 Nozzle"
    ],
    "compatible_printers_condition": "",
    "compatible_prints": [
      "0.20mm Standard @iQ TiQ2 P1 - PETG Polymax Polymaker (0.4 Nozzle)"
    ],
    "compatible_prints_condition": "",
    "complete_print_exhaust_fan_speed": [
      "70"
    ],
    "cool_plate_temp": [
      "0"
    ],
    "cool_plate_temp_initial_layer": [
      "0"
    ],
    "default_filament_colour": [
      "#000000"
    ],
    "dont_slow_down_outer_wall": [
      "0"
    ],
    "during_print_exhaust_fan_speed": [
      "70"
    ],
    "enable_overhang_bridge_fan": [
      "0"
    ],
    "enable_pressure_advance": [
      "0"
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
    "filament_cooling_final_speed": [
      "3.4"
    ],
    "filament_cooling_initial_speed": [
      "2.2"
    ],
    "filament_cooling_moves": [
      "4"
    ],
    "filament_cost": [
      "29.99"
    ],
    "filament_density": [
      "1.25"
    ],
    "filament_deretraction_speed": [
      "nil"
    ],
    "filament_diameter": [
      "1.75"
    ],
    "filament_end_gcode": [
      "; filament end gcode\n{if current_extruder==0}\nG1 Z{layer_z+2} F900 ; safe distance for T0 while tool change\nG1 X-17 Y1 F9000\nG1 X-17 Y45 F9000\nG1 Y1 F9000\nG1 Y45 F9000\n{endif}\n\n{if current_extruder==1}\n{if current_extruder==0}T1{endif}\nG1 X-23 Y3 F9000\nG1 Y45 F9000\nG1 Y3 F9000\nG1 Y45 F9000\n{endif}\n"
    ],
    "filament_flow_ratio": [
      "0.9405"
    ],
    "filament_id": "IQM3",
    "filament_is_support": [
      "0"
    ],
    "filament_loading_speed": [
      "28"
    ],
    "filament_loading_speed_start": [
      "3"
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
      "10"
    ],
    "filament_multitool_ramming_volume": [
      "10"
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
      "0.4"
    ],
    "filament_retraction_minimum_travel": [
      "nil"
    ],
    "filament_retraction_speed": [
      "nil"
    ],
    "filament_settings_id": [
      "Polymaker PETG Polymax black P1 @iQ TiQ2 0.4 Nozzle"
    ],
    "filament_shrink": [
      "100%"
    ],
    "filament_shrinkage_compensation_z": [
      "100%"
    ],
    "filament_soluble": [
      "0"
    ],
    "filament_stamping_distance": [
      "0"
    ],
    "filament_stamping_loading_speed": [
      "0"
    ],
    "filament_start_gcode": [
      "; Filament gcode\n{if current_extruder==0}\nG1 X-17 Y1 F9000\nG1 Y45 F9000\nG1 Y1 F9000\nG1 Y45 F9000\n{if layer_z==0}G1 Z{first_layer_height + 2.0}{endif}\n{if layer_z==0}G1 X[first_layer_print_min_0] Y[first_layer_print_min_1]{endif}\n{if layer_z==0}G1 Z{layer_z}{endif}\n{endif}\n\n{if current_extruder==1}\nG1 X-23 Y3 F9000\nG1 Y45 F9000\nG1 Y3 F9000\nG1 Y45 F9000\n{endif}\n"
    ],
    "filament_toolchange_delay": [
      "0"
    ],
    "filament_type": [
      "PETG Polymax"
    ],
    "filament_unloading_speed": [
      "90"
    ],
    "filament_unloading_speed_start": [
      "100"
    ],
    "filament_vendor": [
      "iQ Materials"
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
      "70"
    ],
    "hot_plate_temp_initial_layer": [
      "80"
    ],
    "idle_temperature": [
      "210"
    ],
    "inherits": "fdm_filament_common",
    "instantiation": "true",
    "internal_bridge_fan_speed": [
      "-1"
    ],
    "ironing_fan_speed": [
      "-1"
    ],
    "name": "Polymaker PETG Polymax black P1 @iQ TiQ2 0.4 Nozzle",
    "nozzle_temperature": [
      "240"
    ],
    "nozzle_temperature_initial_layer": [
      "250"
    ],
    "nozzle_temperature_range_high": [
      "240"
    ],
    "nozzle_temperature_range_low": [
      "230"
    ],
    "overhang_fan_speed": [
      "100"
    ],
    "overhang_fan_threshold": [
      "95%"
    ],
    "pellet_flow_coefficient": [
      "0.4157"
    ],
    "pressure_advance": [
      "0.02"
    ],
    "reduce_fan_stop_start_freq": [
      "0"
    ],
    "required_nozzle_HRC": [
      "3"
    ],
    "settings_id": "IQS3",
    "slow_down_for_layer_cooling": [
      "1"
    ],
    "slow_down_layer_time": [
      "8"
    ],
    "slow_down_min_speed": [
      "10"
    ],
    "supertack_plate_temp": [
      "70"
    ],
    "supertack_plate_temp_initial_layer": [
      "70"
    ],
    "support_material_interface_fan_speed": [
      "-1"
    ],
    "temperature_vitrification": [
      "76"
    ],
    "textured_cool_plate_temp": [
      "40"
    ],
    "textured_cool_plate_temp_initial_layer": [
      "40"
    ],
    "textured_plate_temp": [
      "60"
    ],
    "textured_plate_temp_initial_layer": [
      "60"
    ],
    "type": "filament"
  },
  "filament/VXL90 TiQ2 P2 @iQ TiQ2 0.4 Nozzle.json": {
    "close_fan_the_first_x_layers": [
      "3"
    ],
    "compatible_printers": [
      "iQ TiQ2 0.4 Nozzle"
    ],
    "compatible_prints": [
      "0.20mm Standard @iQ TiQ2 P2 - PACF Pro Fiberthree + VXL90 Xioneer (0.4 Nozzle)"
    ],
    "complete_print_exhaust_fan_speed": [
      "70"
    ],
    "default_filament_colour": [
      "#FFFFFF"
    ],
    "during_print_exhaust_fan_speed": [
      "70"
    ],
    "enable_pressure_advance": [
      "0"
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
    "filament_cooling_final_speed": [
      "3.5"
    ],
    "filament_cooling_initial_speed": [
      "10"
    ],
    "filament_cooling_moves": [
      "2"
    ],
    "filament_cost": [
      "150"
    ],
    "filament_density": [
      "1.1"
    ],
    "filament_diameter": [
      "1.75"
    ],
    "filament_end_gcode": [
      "; filament end gcode\n{if current_extruder==0}\nG1 Z{layer_z+2} F900 ; safe distance for T0 while tool change\nG1 X-17 Y1 F9000\nG1 X-17 Y45 F9000\nG1 Y1 F9000\nG1 Y45 F9000\n{endif}\n\n{if current_extruder==1}\n{if current_extruder==0}T1{endif}\nG1 X-23 Y3 F9000\nG1 Y45 F9000\nG1 Y3 F9000\nG1 Y45 F9000\n{endif}"
    ],
    "filament_flow_ratio": [
      "1"
    ],
    "filament_id": "IQM1011",
    "filament_is_support": [
      "1"
    ],
    "filament_loading_speed": [
      "10"
    ],
    "filament_loading_speed_start": [
      "50"
    ],
    "filament_max_volumetric_speed": [
      "12"
    ],
    "filament_notes": [
      "Filament file version 1.0 20251103"
    ],
    "filament_retraction_length": [
      "4"
    ],
    "filament_retraction_speed": [
      "nil"
    ],
    "filament_settings_id": [
      "VXL90 TiQ2 P2 @iQ TiQ2 0.4 Nozzle"
    ],
    "filament_soluble": [
      "1"
    ],
    "filament_stamping_distance": [
      "45"
    ],
    "filament_stamping_loading_speed": [
      "29"
    ],
    "filament_start_gcode": [
      "; Filament gcode\n{if current_extruder==0}\nG1 X-17 Y1 F9000\nG1 Y45 F9000\nG1 Y1 F9000\nG1 Y45 F9000\n{if layer_z==0}G1 Z{first_layer_height + 2.0}{endif}\n{if layer_z==0}G1 X[first_layer_print_min_0] Y[first_layer_print_min_1]{endif}\n{if layer_z==0}G1 Z{layer_z}{endif}\n{endif}\n\n{if current_extruder==1}\nG1 X-23 Y3 F9000\nG1 Y45 F9000\nG1 Y3 F9000\nG1 Y45 F9000\n{endif}"
    ],
    "filament_toolchange_delay": [
      "0"
    ],
    "filament_type": [
      "VXL90 Xioneer"
    ],
    "filament_unloading_speed": [
      "100"
    ],
    "filament_unloading_speed_start": [
      "100"
    ],
    "filament_vendor": [
      "iQ Materials"
    ],
    "from": "system",
    "hot_plate_temp": [
      "100"
    ],
    "hot_plate_temp_initial_layer": [
      "100"
    ],
    "idle_temperature": [
      "205"
    ],
    "inherits": "fdm_filament_common",
    "instantiation": "true",
    "is_custom_defined": "0",
    "name": "VXL90 TiQ2 P2 @iQ TiQ2 0.4 Nozzle",
    "nozzle_temperature": [
      "235"
    ],
    "nozzle_temperature_initial_layer": [
      "235"
    ],
    "nozzle_temperature_range_high": [
      "250"
    ],
    "nozzle_temperature_range_low": [
      "220"
    ],
    "overhang_fan_speed": [
      "80"
    ],
    "overhang_fan_threshold": [
      "25%"
    ],
    "setting_id": "IQS1011",
    "slow_down_layer_time": [
      "3"
    ],
    "slow_down_min_speed": [
      "10"
    ],
    "temperature_vitrification": [
      "110"
    ],
    "type": "filament",
    "version": "2.3.1.10"
  },
  "filament/fdm_filament_common.json": {
    "activate_air_filtration": [
      "0"
    ],
    "activate_chamber_temp_control": [
      "0"
    ],
    "additional_cooling_fan_speed": [
      "70"
    ],
    "chamber_temperature": [
      "0"
    ],
    "close_fan_the_first_x_layers": [
      "1"
    ],
    "complete_print_exhaust_fan_speed": [
      "70"
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
      "70"
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
      "60"
    ],
    "fan_max_speed": [
      "0"
    ],
    "fan_min_speed": [
      "0"
    ],
    "filament_cooling_final_speed": [
      "3.4"
    ],
    "filament_cooling_initial_speed": [
      "2.2"
    ],
    "filament_cooling_moves": [
      "4"
    ],
    "filament_cost": [
      "5"
    ],
    "filament_density": [
      "1.24"
    ],
    "filament_deretraction_speed": [
      "nil"
    ],
    "filament_diameter": [
      "2.8"
    ],
    "filament_end_gcode": [
      "; filament end gcode \nM106 P3 S0\n"
    ],
    "filament_flow_ratio": [
      "1"
    ],
    "filament_is_support": [
      "0"
    ],
    "filament_load_time": [
      "0"
    ],
    "filament_loading_speed": [
      "28"
    ],
    "filament_loading_speed_start": [
      "3"
    ],
    "filament_max_volumetric_speed": [
      "300"
    ],
    "filament_minimal_purge_on_wipe_tower": [
      "15"
    ],
    "filament_multitool_ramming": [
      "0"
    ],
    "filament_multitool_ramming_flow": [
      "10"
    ],
    "filament_multitool_ramming_volume": [
      "10"
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
    "filament_retraction_length": [
      "nil"
    ],
    "filament_retraction_minimum_travel": [
      "nil"
    ],
    "filament_retraction_speed": [
      "nil"
    ],
    "filament_shrink": [
      "100%"
    ],
    "filament_soluble": [
      "0"
    ],
    "filament_start_gcode": [
      "; filament start gcode\n{if  (bed_temperature[current_extruder] >45)||(bed_temperature_initial_layer[current_extruder] >45)}M106 P3 S255\n{elsif(bed_temperature[current_extruder] >35)||(bed_temperature_initial_layer[current_extruder] >35)}M106 P3 S180\n{endif}\n\n{if activate_air_filtration[current_extruder] && support_air_filtration}\nM106 P3 S{during_print_exhaust_fan_speed_num[current_extruder]} \n{endif}"
    ],
    "filament_toolchange_delay": [
      "0"
    ],
    "filament_unload_time": [
      "0"
    ],
    "filament_unloading_speed": [
      "90"
    ],
    "filament_unloading_speed_start": [
      "100"
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
      "1"
    ],
    "hot_plate_temp_initial_layer": [
      "60"
    ],
    "instantiation": "false",
    "name": "fdm_filament_common",
    "nozzle_temperature": [
      "220"
    ],
    "nozzle_temperature_initial_layer": [
      "220"
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
      "0.4"
    ],
    "reduce_fan_stop_start_freq": [
      "0"
    ],
    "required_nozzle_HRC": [
      "3"
    ],
    "slow_down_for_layer_cooling": [
      "1"
    ],
    "slow_down_layer_time": [
      "30"
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
  }
}

MISC = {}

ASSETS = [
  "TiQ2.stl",
  "TiQ2_cover.png",
  "TiQ2_texture.png",
  "TiQ8.stl",
  "TiQ8_cover.png",
  "TiQ8_texture.png"
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
