from __future__ import annotations

VENDOR = "Raise3D"
INDEX = {
  "description": "Raise3D configurations",
  "filament_list": [],
  "force_update": "0",
  "machine_list": [
    {
      "name": "fdm_machine_common",
      "sub_path": "machine/fdm_machine_common.json"
    },
    {
      "name": "Raise3D Pro3 0.4 nozzle (Dual)",
      "sub_path": "machine/Raise3D Pro3 0.4 nozzle (Dual).json"
    },
    {
      "name": "Raise3D Pro3 0.4 nozzle (Left)",
      "sub_path": "machine/Raise3D Pro3 0.4 nozzle (Left).json"
    },
    {
      "name": "Raise3D Pro3 0.4 nozzle (Right)",
      "sub_path": "machine/Raise3D Pro3 0.4 nozzle (Right).json"
    },
    {
      "name": "Raise3D Pro3 Plus 0.4 nozzle (Dual)",
      "sub_path": "machine/Raise3D Pro3 Plus 0.4 nozzle (Dual).json"
    },
    {
      "name": "Raise3D Pro3 Plus 0.4 nozzle (Left)",
      "sub_path": "machine/Raise3D Pro3 Plus 0.4 nozzle (Left).json"
    },
    {
      "name": "Raise3D Pro3 Plus 0.4 nozzle (Right)",
      "sub_path": "machine/Raise3D Pro3 Plus 0.4 nozzle (Right).json"
    }
  ],
  "machine_model_list": [
    {
      "name": "Raise3D Pro3",
      "sub_path": "machine/Raise3D Pro3.json"
    },
    {
      "name": "Raise3D Pro3 Plus",
      "sub_path": "machine/Raise3D Pro3 Plus.json"
    }
  ],
  "name": "Raise3D",
  "process_list": [
    {
      "name": "fdm_process_common",
      "sub_path": "process/fdm_process_common.json"
    },
    {
      "name": "0.10mm Fine @Raise3D Pro3",
      "sub_path": "process/0.10mm Fine @Raise3D Pro3.json"
    },
    {
      "name": "0.10mm Fine @Raise3D Pro3Plus",
      "sub_path": "process/0.10mm Fine @Raise3D Pro3Plus.json"
    },
    {
      "name": "0.20mm Standard @Raise3D Pro3",
      "sub_path": "process/0.20mm Standard @Raise3D Pro3.json"
    },
    {
      "name": "0.20mm Standard @Raise3D Pro3Plus",
      "sub_path": "process/0.20mm Standard @Raise3D Pro3Plus.json"
    },
    {
      "name": "0.25mm Draft @Raise3D Pro3",
      "sub_path": "process/0.25mm Draft @Raise3D Pro3.json"
    },
    {
      "name": "0.25mm Draft @Raise3D Pro3Plus",
      "sub_path": "process/0.25mm Draft @Raise3D Pro3Plus.json"
    }
  ],
  "url": "",
  "version": "02.03.01.10"
}

MACHINE = {
  "machine/Raise3D Pro3 0.4 nozzle (Dual).json": {
    "auxiliary_fan": "0",
    "before_layer_change_gcode": "; before layer [layer_num] change\nG92 E0\n{if layer_z <= initial_layer_print_height + layer_height * 2}\nM140 S{max(bed_temperature_initial_layer_single, bed_temperature_initial_layer_single)}\n{else}\nM140 S{max(bed_temperature[0], bed_temperature[1])}\n{endif}\n{if (filament_type[0] ==\"PLA\" or filament_type[0] ==\"PETG\")}\n{if layer_z >= initial_layer_print_height + layer_height * 2}\nM106 P2 S150\n{elsif layer_z >= initial_layer_print_height + layer_height * 1}\nM106 P2 S100\n{else}\nM106 P2 S0\n{endif}\n{endif}",
    "change_filament_gcode": "",
    "default_filament_profile": [
      "Generic PLA @System"
    ],
    "default_print_profile": "0.20mm Standard @Raise3D Pro3",
    "deretraction_speed": [
      "0",
      "0"
    ],
    "extruder_colour": [
      "#FCE94F",
      "#FCE94F"
    ],
    "extruder_offset": [
      "0x0",
      "0x0"
    ],
    "from": "system",
    "inherits": "fdm_machine_common",
    "instantiation": "true",
    "layer_change_gcode": ";AFTER_LAYER_CHANGE\n;[layer_z]",
    "machine_end_gcode": "M221 T0 S100\nM104 S0\nM140 S0\nM107\nM106 P2 S0\nG91\nG1 E-1 F300\nG1 Z+0.5 E-5 X-20 Y-20 F9000.00\nG28 X0 Y0\nM84\nG90",
    "machine_max_acceleration_e": [
      "3000",
      "3000"
    ],
    "machine_max_acceleration_extruding": [
      "1000",
      "300"
    ],
    "machine_max_acceleration_retracting": [
      "3000",
      "1500"
    ],
    "machine_max_acceleration_travel": [
      "1500",
      "500"
    ],
    "machine_max_acceleration_x": [
      "1000",
      "1000"
    ],
    "machine_max_acceleration_y": [
      "1000",
      "1000"
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
      "5",
      "5"
    ],
    "machine_max_jerk_y": [
      "5",
      "5"
    ],
    "machine_max_jerk_z": [
      "0.4",
      "0.4"
    ],
    "machine_max_speed_e": [
      "120",
      "120"
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
    "machine_pause_gcode": "; pause print\nM2000",
    "machine_start_gcode": ";Bounding Box: {digits(first_layer_print_min[0],0,2)} {if(first_layer_print_max[0]>300)}{300}{else}{digits(first_layer_print_max[0],0,2)}{endif} {digits(first_layer_print_min[1],0,2)} {if(first_layer_print_max[1]>300)}{300}{else}{digits(first_layer_print_max[1],0,2)}{endif}\n\nM104 T0 S{nozzle_temperature_initial_layer[0] - 30} ; raise extruder one temp\nM104 T1 S{nozzle_temperature_initial_layer[1] - 30} ; raise extruder two temp\nM190 S{max(bed_temperature_initial_layer_single, bed_temperature_initial_layer_single)} ; wait for bed temp\nM109 T1 S{nozzle_temperature_initial_layer[1]} ; wait for extruder two temp\nT1\nG21\nG90\nM82\nM107\nM106 P2 S0\nG1 Z0.3 F500\nG92 E0\nG1 Z0.3 F400\nG1 X60 Y{random(2,8)} F1000\nG1 X110 Y{random(2,8)} E30 F200\nG1 Z0.3 E15 F200\nG92 E0\nG1 Z10 F2000 ; move up from purge line\nG1 X170 F2000 ; move away from purge line\nM104 T1 S{nozzle_temperature_initial_layer[1] - 30} ; lower extruder two temp\nM109 T0 S{nozzle_temperature_initial_layer[0]} ; wait for extruder one temp\nT0\nG1 Z0.3 F400\nG1 X220 Y{random(2,8)} F1000\nG1 X270 Y{random(2,8)} E18 F200\nG1 Z5 E15 F200\nG92 E0\nG1 Z10 F2000 ; move up from purge line\nG1 Y30 F2000 ; move away from purge line\nM104 T0 S{nozzle_temperature_initial_layer[1] - 30} ; lower extruder one temp\nG92 E0\nG1 X{(first_layer_print_max[0] + first_layer_print_min[0])/2} Y{(first_layer_print_max[1] + first_layer_print_min[1])/2} Z{initial_layer_print_height} ; move to center of print\nM117 Printing...",
    "max_layer_height": [
      "0.4",
      "0.4"
    ],
    "min_layer_height": [
      "0.1",
      "0.1"
    ],
    "name": "Raise3D Pro3 0.4 nozzle (Dual)",
    "nozzle_diameter": [
      "0.4",
      "0.4"
    ],
    "nozzle_type": "hardened_steel",
    "printable_area": [
      "0x0",
      "340x0",
      "340x300",
      "0x300"
    ],
    "printable_height": "300",
    "printer_model": "Raise3D Pro3",
    "printer_settings_id": "Raise3D",
    "retract_before_wipe": [
      "0%",
      "0%"
    ],
    "retract_length_toolchange": [
      "2",
      "2"
    ],
    "retract_restart_extra": [
      "0",
      "0"
    ],
    "retract_restart_extra_toolchange": [
      "0",
      "0"
    ],
    "retract_when_changing_layer": [
      "1",
      "1"
    ],
    "retraction_length": [
      "0.5",
      "0.5"
    ],
    "retraction_minimum_travel": [
      "0.6",
      "0.6"
    ],
    "retraction_speed": [
      "40",
      "40"
    ],
    "scan_first_layer": "0",
    "setting_id": "GM001",
    "single_extruder_multi_material": "1",
    "toolchange_gcode": "; layer [layer_num] tool change\n{if layer_z < initial_layer_print_height + layer_height * 2}\nM104 T[current_extruder] S{nozzle_temperature_initial_layer[current_extruder] - 30}\nM109 T[next_extruder] S{nozzle_temperature_initial_layer[next_extruder]}\n{else}\nM104 T[current_extruder] S{nozzle_temperature[current_extruder] - 30}\nM109 T[next_extruder] S{nozzle_temperature[next_extruder]}\n{endif}",
    "type": "machine",
    "wipe": [
      "1",
      "1"
    ]
  },
  "machine/Raise3D Pro3 0.4 nozzle (Left).json": {
    "auxiliary_fan": "0",
    "before_layer_change_gcode": "; before layer [layer_num] change\nG92 E0\n{if layer_z <= initial_layer_print_height + layer_height * 2}\nM109 T0 S{nozzle_temperature_initial_layer[0]}\nM140 S[bed_temperature_initial_layer_single]\n{else}\nM109 T0 S{nozzle_temperature[0]}\nM140 S{bed_temperature[0]}\n{endif}\n{if (filament_type[0] ==\"PLA\" or filament_type[0] ==\"PETG\")}\n{if layer_z >= initial_layer_print_height + layer_height * 2}\nM106 P2 S150\n{elsif layer_z >= initial_layer_print_height + layer_height * 1}\nM106 P2 S100\n{else}\nM106 P2 S0\n{endif}\n{endif}",
    "change_filament_gcode": "",
    "default_filament_profile": [
      "Generic PLA @System"
    ],
    "default_print_profile": "0.20mm Standard @Raise3D Pro3",
    "deretraction_speed": [
      "0",
      "0"
    ],
    "extruder_colour": [
      "#FCE94F",
      "#FCE94F"
    ],
    "extruder_offset": [
      "0x0",
      "0x0"
    ],
    "from": "system",
    "inherits": "fdm_machine_common",
    "instantiation": "true",
    "layer_change_gcode": ";AFTER_LAYER_CHANGE\n;[layer_z]",
    "machine_end_gcode": "M1002\nM221 T0 S100\nM104 S0\nM140 S0\nM107\nM106 P2 S0\nG91\nG1 E-1 F300\nG1 Z+0.5 E-5 X-20 Y-20 F9000.00\nG28 X0 Y0\nM84\nG90\n",
    "machine_max_acceleration_e": [
      "3000",
      "3000"
    ],
    "machine_max_acceleration_extruding": [
      "1000",
      "300"
    ],
    "machine_max_acceleration_retracting": [
      "3000",
      "1500"
    ],
    "machine_max_acceleration_travel": [
      "1500",
      "500"
    ],
    "machine_max_acceleration_x": [
      "1000",
      "1000"
    ],
    "machine_max_acceleration_y": [
      "1000",
      "1000"
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
      "5",
      "5"
    ],
    "machine_max_jerk_y": [
      "5",
      "5"
    ],
    "machine_max_jerk_z": [
      "0.4",
      "0.4"
    ],
    "machine_max_speed_e": [
      "120",
      "120"
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
    "machine_pause_gcode": "; pause print\nM2000",
    "machine_start_gcode": ";Bounding Box: {digits(first_layer_print_min[0],0,2)} {if(first_layer_print_max[0]>300)}{300}{else}{digits(first_layer_print_max[0],0,2)}{endif} {digits(first_layer_print_min[1],0,2)} {if(first_layer_print_max[1]>300)}{300}{else}{digits(first_layer_print_max[1],0,2)}{endif}\n\nM104 T0 S{nozzle_temperature_initial_layer[0] - 20} ; raise left extruder temp\nM140 S[bed_temperature_initial_layer_single] ; raise bed temp\nM190 S[bed_temperature_initial_layer_single] ; wait for bed temp\nM109 T0 S{nozzle_temperature_initial_layer[0] - 20} ; wait for left extruder temp\nM104 T0 S[nozzle_temperature_initial_layer] ; set left extruder temp\nM109 T0 S[nozzle_temperature_initial_layer] ; wait for left extruder temp\nT0\nG21\nG90\nM82\nM107\nM106 P2 S0\nG1 Z0.3 F500\nG92 E0\nG1 Z0.3 F400\nG1 X100 Y{random(2,8)} F1000\nG1 X170 Y{random(2,8)} E15 F200\nG1 Z5 E15 F200\nG92 E0\nG1 Z10 F2000 ; move up from purge line\nG1 Y30 F2000 ; move away from purge line\nG1 X{(first_layer_print_max[0] + first_layer_print_min[0])/2} Y{(first_layer_print_max[1] + first_layer_print_min[1])/2} Z{initial_layer_print_height} ; move to center of print\nM117 Printing...\nM1001",
    "max_layer_height": [
      "0.4",
      "0.4"
    ],
    "min_layer_height": [
      "0.1",
      "0.1"
    ],
    "name": "Raise3D Pro3 0.4 nozzle (Left)",
    "nozzle_diameter": [
      "0.4",
      "0.4"
    ],
    "nozzle_type": "hardened_steel",
    "printable_area": [
      "0x0",
      "340x0",
      "340x300",
      "0x300"
    ],
    "printable_height": "300",
    "printer_model": "Raise3D Pro3",
    "printer_settings_id": "Raise3D",
    "retract_before_wipe": [
      "0%",
      "0%"
    ],
    "retract_length_toolchange": [
      "2",
      "2"
    ],
    "retract_restart_extra": [
      "0",
      "0"
    ],
    "retract_restart_extra_toolchange": [
      "0",
      "0"
    ],
    "retract_when_changing_layer": [
      "1",
      "1"
    ],
    "retraction_length": [
      "0.5",
      "0.5"
    ],
    "retraction_minimum_travel": [
      "0.6",
      "0.6"
    ],
    "retraction_speed": [
      "40",
      "40"
    ],
    "scan_first_layer": "0",
    "setting_id": "GM001",
    "single_extruder_multi_material": "1",
    "toolchange_gcode": "; layer [layer_num] tool change",
    "type": "machine",
    "wipe": [
      "1",
      "1"
    ]
  },
  "machine/Raise3D Pro3 0.4 nozzle (Right).json": {
    "auxiliary_fan": "0",
    "before_layer_change_gcode": "; before layer [layer_num] change\nG92 E0\n{if layer_z <= initial_layer_print_height + layer_height * 2}\nM109 T1 S{nozzle_temperature_initial_layer[1]}\nM140 S[bed_temperature_initial_layer_single]\n{else}\nM109 T1 S{nozzle_temperature[1]}\nM140 S{bed_temperature[1]}\n{endif}\n{if (filament_type[0] ==\"PLA\" or filament_type[0] ==\"PETG\")}\n{if layer_z >= initial_layer_print_height + layer_height * 2}\nM106 P2 S150\n{elsif layer_z >= initial_layer_print_height + layer_height * 1}\nM106 P2 S100\n{else}\nM106 P2 S0\n{endif}\n{endif}",
    "change_filament_gcode": "",
    "default_filament_profile": [
      "Generic PLA @System"
    ],
    "default_print_profile": "0.20mm Standard @Raise3D Pro3",
    "deretraction_speed": [
      "0",
      "0"
    ],
    "extruder_colour": [
      "#FCE94F",
      "#FCE94F"
    ],
    "extruder_offset": [
      "0x0",
      "0x0"
    ],
    "from": "system",
    "inherits": "fdm_machine_common",
    "instantiation": "true",
    "layer_change_gcode": ";AFTER_LAYER_CHANGE\n;[layer_z]",
    "machine_end_gcode": "M1002\nM221 T0 S100\nM104 S0\nM140 S0\nM107\nM106 P2 S0\nG91\nG1 E-1 F300\nG1 Z+0.5 E-5 X-20 Y-20 F9000.00\nG28 X0 Y0\nM84\nG90\nM106 P2 S0\n",
    "machine_max_acceleration_e": [
      "3000",
      "3000"
    ],
    "machine_max_acceleration_extruding": [
      "1000",
      "300"
    ],
    "machine_max_acceleration_retracting": [
      "3000",
      "1500"
    ],
    "machine_max_acceleration_travel": [
      "1500",
      "500"
    ],
    "machine_max_acceleration_x": [
      "1000",
      "1000"
    ],
    "machine_max_acceleration_y": [
      "1000",
      "1000"
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
      "5",
      "5"
    ],
    "machine_max_jerk_y": [
      "5",
      "5"
    ],
    "machine_max_jerk_z": [
      "0.4",
      "0.4"
    ],
    "machine_max_speed_e": [
      "120",
      "120"
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
    "machine_pause_gcode": "; pause print\nM2000",
    "machine_start_gcode": ";Bounding Box: {digits(first_layer_print_min[0],0,2)} {if(first_layer_print_max[0]>300)}{300}{else}{digits(first_layer_print_max[0],0,2)}{endif} {digits(first_layer_print_min[1],0,2)} {if(first_layer_print_max[1]>300)}{300}{else}{digits(first_layer_print_max[1],0,2)}{endif}\n\nM104 T1 S{nozzle_temperature_initial_layer[1] - 20} ; raise right extruder temp\nM140 S[bed_temperature_initial_layer_single] ; raise bed temp\nM190 S[bed_temperature_initial_layer_single] ; wait for bed temp\nM109 T1 S{nozzle_temperature_initial_layer[1] - 20} ; wait for right extruder temp\nM104 T1 S{nozzle_temperature_initial_layer[1]} ; set right extruder temp\nM109 T1 S{nozzle_temperature_initial_layer[1]} ; wait for right extruder temp\nT1\nG21\nG90\nM82\nM107\nM106 P2 S0\nG1 Z0.3 F500\nG92 E0\nG1 Z0.3 F400\nG1 X100 Y{random(2,8)} F1000\nG1 X170 Y{random(2,8)} E15 F200\nG1 Z5 E15 F200\nG92 E0\nG1 Z10 F2000 ; move up from purge line\nG1 Y30 F2000 ; move away from purge line\nG1 X{(first_layer_print_max[0] + first_layer_print_min[0])/2} Y{(first_layer_print_max[1] + first_layer_print_min[1])/2} Z{initial_layer_print_height} ; move to center of print\nM117 Printing...\nM1001",
    "max_layer_height": [
      "0.4",
      "0.4"
    ],
    "min_layer_height": [
      "0.1",
      "0.1"
    ],
    "name": "Raise3D Pro3 0.4 nozzle (Right)",
    "nozzle_diameter": [
      "0.4",
      "0.4"
    ],
    "nozzle_type": "hardened_steel",
    "printable_area": [
      "0x0",
      "340x0",
      "340x300",
      "0x300"
    ],
    "printable_height": "300",
    "printer_model": "Raise3D Pro3",
    "printer_settings_id": "Raise3D",
    "retract_before_wipe": [
      "0%",
      "0%"
    ],
    "retract_length_toolchange": [
      "2",
      "2"
    ],
    "retract_restart_extra": [
      "0",
      "0"
    ],
    "retract_restart_extra_toolchange": [
      "0",
      "0"
    ],
    "retract_when_changing_layer": [
      "1",
      "1"
    ],
    "retraction_length": [
      "0.5",
      "0.5"
    ],
    "retraction_minimum_travel": [
      "0.6",
      "0.6"
    ],
    "retraction_speed": [
      "40",
      "40"
    ],
    "scan_first_layer": "0",
    "setting_id": "GM001",
    "single_extruder_multi_material": "1",
    "toolchange_gcode": "; layer [layer_num] tool change",
    "type": "machine",
    "wipe": [
      "1",
      "1"
    ]
  },
  "machine/Raise3D Pro3 Plus 0.4 nozzle (Dual).json": {
    "auxiliary_fan": "0",
    "before_layer_change_gcode": "; before layer [layer_num] change\n{if layer_z <= initial_layer_print_height + layer_height * 2}\nM140 S{max(bed_temperature_initial_layer_single, bed_temperature_initial_layer_single)}\n{else}\nM140 S{max(bed_temperature[0], bed_temperature[1])}\n{endif}\n{if (filament_type[0] ==\"PLA\" or filament_type[0] ==\"PETG\")}\n{if layer_z >= initial_layer_print_height + layer_height * 2}\nM106 P2 S150\n{elsif layer_z >= initial_layer_print_height + layer_height * 1}\nM106 P2 S100\n{else}\nM106 P2 S0\n{endif}\n{endif}",
    "change_filament_gcode": "",
    "default_filament_profile": [
      "Generic PLA @System"
    ],
    "default_print_profile": "0.20mm Standard @Raise3D Pro3Plus",
    "deretraction_speed": [
      "0",
      "0"
    ],
    "extruder_colour": [
      "#FCE94F",
      "#FCE94F"
    ],
    "extruder_offset": [
      "0x0",
      "0x0"
    ],
    "from": "system",
    "inherits": "fdm_machine_common",
    "instantiation": "true",
    "layer_change_gcode": ";AFTER_LAYER_CHANGE\n;[layer_z]",
    "machine_end_gcode": "M221 T0 S100\nM104 S0\nM140 S0\nM107\nM106 P2 S0\nG91\nG1 E-1 F300\nG1 Z+0.5 E-5 X-20 Y-20 F9000.00\nG28 X0 Y0\nM84\nG90",
    "machine_max_acceleration_e": [
      "3000",
      "3000"
    ],
    "machine_max_acceleration_extruding": [
      "1000",
      "300"
    ],
    "machine_max_acceleration_retracting": [
      "3000",
      "1500"
    ],
    "machine_max_acceleration_travel": [
      "1500",
      "500"
    ],
    "machine_max_acceleration_x": [
      "1000",
      "1000"
    ],
    "machine_max_acceleration_y": [
      "1000",
      "1000"
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
      "5",
      "5"
    ],
    "machine_max_jerk_y": [
      "5",
      "5"
    ],
    "machine_max_jerk_z": [
      "0.4",
      "0.4"
    ],
    "machine_max_speed_e": [
      "120",
      "120"
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
    "machine_pause_gcode": "; pause print\nM2000",
    "machine_start_gcode": ";Bounding Box: {digits(first_layer_print_min[0],0,2)} {if(first_layer_print_max[0]>300)}{300}{else}{digits(first_layer_print_max[0],0,2)}{endif} {digits(first_layer_print_min[1],0,2)} {if(first_layer_print_max[1]>300)}{300}{else}{digits(first_layer_print_max[1],0,2)}{endif}\n\nM104 T0 S{nozzle_temperature_initial_layer[0] - 30} ; raise extruder one temp\nM104 T1 S{nozzle_temperature_initial_layer[1] - 30} ; raise extruder two temp\nM190 S{max(bed_temperature_initial_layer_single, bed_temperature_initial_layer_single)} ; wait for bed temp\nM109 T1 S{nozzle_temperature_initial_layer[1]} ; wait for extruder two temp\nT1\nG21\nG90\nM82\nM107\nM106 P2 S0\nG1 Z0.3 F500\nG92 E0\nG1 Z0.3 F400\nG1 X60 Y{random(2,8)} F1000\nG1 X110 Y{random(2,8)} E30 F200\nG1 Z0.3 E15 F200\nG92 E0\nG1 Z10 F2000 ; move up from purge line\nG1 X170 F2000 ; move away from purge line\nM104 T1 S{nozzle_temperature_initial_layer[1] - 30} ; lower extruder two temp\nM109 T0 S{nozzle_temperature_initial_layer[0]} ; wait for extruder one temp\nT0\nG1 Z0.3 F400\nG1 X220 Y{random(2,8)} F1000\nG1 X270 Y{random(2,8)} E18 F200\nG1 Z5 E15 F200\nG92 E0\nG1 Z10 F2000 ; move up from purge line\nG1 Y30 F2000 ; move away from purge line\nM104 T0 S{nozzle_temperature_initial_layer[1] - 30} ; lower extruder one temp\nG92 E0\nG1 X{(first_layer_print_max[0] + first_layer_print_min[0])/2} Y{(first_layer_print_max[1] + first_layer_print_min[1])/2} Z{initial_layer_print_height} ; move to center of print\nM117 Printing...",
    "max_layer_height": [
      "0.4",
      "0.4"
    ],
    "min_layer_height": [
      "0.1",
      "0.1"
    ],
    "name": "Raise3D Pro3 Plus 0.4 nozzle (Dual)",
    "nozzle_diameter": [
      "0.4",
      "0.4"
    ],
    "nozzle_type": "hardened_steel",
    "printable_area": [
      "0x0",
      "340x0",
      "340x300",
      "0x300"
    ],
    "printable_height": "605",
    "printer_model": "Raise3D Pro3 Plus",
    "printer_settings_id": "Raise3D",
    "retract_before_wipe": [
      "0%",
      "0%"
    ],
    "retract_length_toolchange": [
      "2",
      "2"
    ],
    "retract_restart_extra": [
      "0",
      "0"
    ],
    "retract_restart_extra_toolchange": [
      "0",
      "0"
    ],
    "retract_when_changing_layer": [
      "1",
      "1"
    ],
    "retraction_length": [
      "0.5",
      "0.5"
    ],
    "retraction_minimum_travel": [
      "0.6",
      "0.6"
    ],
    "retraction_speed": [
      "40",
      "40"
    ],
    "scan_first_layer": "0",
    "setting_id": "GM001",
    "single_extruder_multi_material": "1",
    "toolchange_gcode": "; layer [layer_num] tool change\n{if layer_z < initial_layer_print_height + layer_height * 2}\nM104 T[current_extruder] S{nozzle_temperature_initial_layer[current_extruder] - 30}\nM109 T[next_extruder] S{nozzle_temperature_initial_layer[next_extruder]}\n{else}\nM104 T[current_extruder] S{nozzle_temperature[current_extruder] - 30}\nM109 T[next_extruder] S{nozzle_temperature[next_extruder]}\n{endif}",
    "type": "machine",
    "wipe": [
      "1",
      "1"
    ]
  },
  "machine/Raise3D Pro3 Plus 0.4 nozzle (Left).json": {
    "auxiliary_fan": "0",
    "before_layer_change_gcode": "; before layer [layer_num] change\n{if layer_z <= initial_layer_print_height + layer_height * 2}\nM109 T0 S{nozzle_temperature_initial_layer[0]}\nM140 S[bed_temperature_initial_layer_single]\n{else}\nM109 T0 S{nozzle_temperature[0]}\nM140 S{bed_temperature[0]}\n{endif}\n{if (filament_type[0] ==\"PLA\" or filament_type[0] ==\"PETG\")}\n{if layer_z >= initial_layer_print_height + layer_height * 2}\nM106 P2 S150\n{elsif layer_z >= initial_layer_print_height + layer_height * 1}\nM106 P2 S100\n{else}\nM106 P2 S0\n{endif}\n{endif}",
    "change_filament_gcode": "",
    "default_filament_profile": [
      "Generic PLA @System"
    ],
    "default_print_profile": "0.20mm Standard @Raise3D Pro3Plus",
    "deretraction_speed": [
      "0",
      "0"
    ],
    "extruder_colour": [
      "#FCE94F",
      "#FCE94F"
    ],
    "extruder_offset": [
      "0x0",
      "0x0"
    ],
    "from": "system",
    "inherits": "fdm_machine_common",
    "instantiation": "true",
    "layer_change_gcode": ";AFTER_LAYER_CHANGE\n;[layer_z]",
    "machine_end_gcode": "M1002\nM221 T0 S100\nM104 S0\nM140 S0\nM107\nM106 P2 S0\nG91\nG1 E-1 F300\nG1 Z+0.5 E-5 X-20 Y-20 F9000.00\nG28 X0 Y0\nM84\nG90\n",
    "machine_max_acceleration_e": [
      "3000",
      "3000"
    ],
    "machine_max_acceleration_extruding": [
      "1000",
      "300"
    ],
    "machine_max_acceleration_retracting": [
      "3000",
      "1500"
    ],
    "machine_max_acceleration_travel": [
      "1500",
      "500"
    ],
    "machine_max_acceleration_x": [
      "1000",
      "1000"
    ],
    "machine_max_acceleration_y": [
      "1000",
      "1000"
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
      "5",
      "5"
    ],
    "machine_max_jerk_y": [
      "5",
      "5"
    ],
    "machine_max_jerk_z": [
      "0.4",
      "0.4"
    ],
    "machine_max_speed_e": [
      "120",
      "120"
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
    "machine_pause_gcode": "; pause print\nM2000",
    "machine_start_gcode": ";Bounding Box: {digits(first_layer_print_min[0],0,2)} {if(first_layer_print_max[0]>300)}{300}{else}{digits(first_layer_print_max[0],0,2)}{endif} {digits(first_layer_print_min[1],0,2)} {if(first_layer_print_max[1]>300)}{300}{else}{digits(first_layer_print_max[1],0,2)}{endif}\n\nM104 T0 S{nozzle_temperature_initial_layer[0] - 20} ; raise left extruder temp\nM140 S[bed_temperature_initial_layer_single] ; raise bed temp\nM190 S{bed_temperature_initial_layer_single} ; wait for bed temp\nM109 T0 S{nozzle_temperature_initial_layer[0] - 20} ; wait for left extruder temp\nM104 T0 S[nozzle_temperature_initial_layer] ; set left extruder temp\nM109 T0 S[nozzle_temperature_initial_layer] ; wait for left extruder temp\nT0\nG21\nG90\nM82\nM107\nM106 P2 S0\nG1 Z0.3 F500\nG92 E0\nG1 Z0.3 F400\nG1 X100 Y{random(2,8)} F1000\nG1 X170 Y{random(2,8)} E15 F200\nG1 Z5 E15 F200\nG92 E0\nG1 Z10 F2000 ; move up from purge line\nG1 Y30 F2000 ; move away from purge line\nG1 X{(first_layer_print_max[0] + first_layer_print_min[0])/2} Y{(first_layer_print_max[1] + first_layer_print_min[1])/2} Z{initial_layer_print_height} ; move to center of print\nM117 Printing...\nM1001",
    "max_layer_height": [
      "0.4",
      "0.4"
    ],
    "min_layer_height": [
      "0.1",
      "0.1"
    ],
    "name": "Raise3D Pro3 Plus 0.4 nozzle (Left)",
    "nozzle_diameter": [
      "0.4",
      "0.4"
    ],
    "nozzle_type": "hardened_steel",
    "printable_area": [
      "0x0",
      "340x0",
      "340x300",
      "0x300"
    ],
    "printable_height": "605",
    "printer_model": "Raise3D Pro3 Plus",
    "printer_settings_id": "Raise3D",
    "retract_before_wipe": [
      "0%",
      "0%"
    ],
    "retract_length_toolchange": [
      "2",
      "2"
    ],
    "retract_restart_extra": [
      "0",
      "0"
    ],
    "retract_restart_extra_toolchange": [
      "0",
      "0"
    ],
    "retract_when_changing_layer": [
      "1",
      "1"
    ],
    "retraction_length": [
      "0.5",
      "0.5"
    ],
    "retraction_minimum_travel": [
      "0.6",
      "0.6"
    ],
    "retraction_speed": [
      "40",
      "40"
    ],
    "scan_first_layer": "0",
    "setting_id": "GM001",
    "single_extruder_multi_material": "1",
    "toolchange_gcode": "; layer [layer_num] tool change",
    "type": "machine",
    "wipe": [
      "1",
      "1"
    ]
  },
  "machine/Raise3D Pro3 Plus 0.4 nozzle (Right).json": {
    "auxiliary_fan": "0",
    "before_layer_change_gcode": "; before layer [layer_num] change\n{if layer_z <= initial_layer_print_height + layer_height * 2}\nM109 T1 S{nozzle_temperature_initial_layer[1]}\nM140 S[bed_temperature_initial_layer_single]\n{else}\nM109 T1 S{nozzle_temperature[1]}\nM140 S{bed_temperature[1]}\n{endif}\n{if (filament_type[0] ==\"PLA\" or filament_type[0] ==\"PETG\")}\n{if layer_z >= initial_layer_print_height + layer_height * 2}\nM106 P2 S150\n{elsif layer_z >= initial_layer_print_height + layer_height * 1}\nM106 P2 S100\n{else}\nM106 P2 S0\n{endif}\n{endif}",
    "change_filament_gcode": "",
    "default_filament_profile": [
      "Generic PLA @System"
    ],
    "default_print_profile": "0.20mm Standard @Raise3D Pro3Plus",
    "deretraction_speed": [
      "0",
      "0"
    ],
    "extruder_colour": [
      "#FCE94F",
      "#FCE94F"
    ],
    "extruder_offset": [
      "0x0",
      "0x0"
    ],
    "from": "system",
    "inherits": "fdm_machine_common",
    "instantiation": "true",
    "layer_change_gcode": ";AFTER_LAYER_CHANGE\n;[layer_z]",
    "machine_end_gcode": "M1002\nM221 T0 S100\nM104 S0\nM140 S0\nM107\nM106 P2 S0\nG91\nG1 E-1 F300\nG1 Z+0.5 E-5 X-20 Y-20 F9000.00\nG28 X0 Y0\nM84\nG90\nM106 P2 S0\n",
    "machine_max_acceleration_e": [
      "3000",
      "3000"
    ],
    "machine_max_acceleration_extruding": [
      "1000",
      "300"
    ],
    "machine_max_acceleration_retracting": [
      "3000",
      "1500"
    ],
    "machine_max_acceleration_travel": [
      "1500",
      "500"
    ],
    "machine_max_acceleration_x": [
      "1000",
      "1000"
    ],
    "machine_max_acceleration_y": [
      "1000",
      "1000"
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
      "5",
      "5"
    ],
    "machine_max_jerk_y": [
      "5",
      "5"
    ],
    "machine_max_jerk_z": [
      "0.4",
      "0.4"
    ],
    "machine_max_speed_e": [
      "120",
      "120"
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
    "machine_pause_gcode": "; pause print\nM2000",
    "machine_start_gcode": ";Bounding Box: {digits(first_layer_print_min[0],0,2)} {if(first_layer_print_max[0]>300)}{300}{else}{digits(first_layer_print_max[0],0,2)}{endif} {digits(first_layer_print_min[1],0,2)} {if(first_layer_print_max[1]>300)}{300}{else}{digits(first_layer_print_max[1],0,2)}{endif}\n\nM104 T1 S{nozzle_temperature_initial_layer[1] - 20} ; raise right extruder temp\nM140 S[bed_temperature_initial_layer_single] ; raise bed temp\nM190 S[bed_temperature_initial_layer_single] ; wait for bed temp\nM109 T1 S{nozzle_temperature_initial_layer[1] - 20} ; wait for right extruder temp\nM104 T1 S{nozzle_temperature_initial_layer[1]} ; set right extruder temp\nM109 T1 S{nozzle_temperature_initial_layer[1]} ; wait for right extruder temp\nT1\nG21\nG90\nM82\nM107\nM106 P2 S0\nG1 Z0.3 F500\nG92 E0\nG1 Z0.3 F400\nG1 X100 Y{random(2,8)} F1000\nG1 X170 Y{random(2,8)} E15 F200\nG1 Z5 E15 F200\nG92 E0\nG1 Z10 F2000 ; move up from purge line\nG1 Y30 F2000 ; move away from purge line\nG1 X{(first_layer_print_max[0] + first_layer_print_min[0])/2} Y{(first_layer_print_max[1] + first_layer_print_min[1])/2} Z{initial_layer_print_height} ; move to center of print\nM117 Printing...\nM1001",
    "max_layer_height": [
      "0.4",
      "0.4"
    ],
    "min_layer_height": [
      "0.1",
      "0.1"
    ],
    "name": "Raise3D Pro3 Plus 0.4 nozzle (Right)",
    "nozzle_diameter": [
      "0.4",
      "0.4"
    ],
    "nozzle_type": "hardened_steel",
    "printable_area": [
      "0x0",
      "340x0",
      "340x300",
      "0x300"
    ],
    "printable_height": "605",
    "printer_model": "Raise3D Pro3 Plus",
    "printer_settings_id": "Raise3D",
    "retract_before_wipe": [
      "0%",
      "0%"
    ],
    "retract_length_toolchange": [
      "2",
      "2"
    ],
    "retract_restart_extra": [
      "0",
      "0"
    ],
    "retract_restart_extra_toolchange": [
      "0",
      "0"
    ],
    "retract_when_changing_layer": [
      "1",
      "1"
    ],
    "retraction_length": [
      "0.5",
      "0.5"
    ],
    "retraction_minimum_travel": [
      "0.6",
      "0.6"
    ],
    "retraction_speed": [
      "40",
      "40"
    ],
    "scan_first_layer": "0",
    "setting_id": "GM001",
    "single_extruder_multi_material": "1",
    "toolchange_gcode": "; layer [layer_num] tool change",
    "type": "machine",
    "wipe": [
      "1",
      "1"
    ]
  },
  "machine/Raise3D Pro3 Plus.json": {
    "bed_model": "raise3d_pro3plus_buildplate_model.stl",
    "bed_texture": "raise3d_pro3plus_buildplate_texture.png",
    "default_materials": "Generic ASA @System;Generic PETG @System;Generic PLA @System;Generic PVA @System;Generic TPU @System",
    "family": "Raise3D",
    "hotend_model": "",
    "machine_tech": "FFF",
    "model_id": "Raise3D-Pro3-Plus",
    "name": "Raise3D Pro3 Plus",
    "nozzle_diameter": "0.4",
    "type": "machine_model"
  },
  "machine/Raise3D Pro3.json": {
    "bed_model": "raise3d_pro3_buildplate_model.stl",
    "bed_texture": "raise3d_pro3_buildplate_texture.png",
    "default_materials": "Generic ASA @System;Generic PETG @System;Generic PLA @System;Generic PVA @System;Generic TPU @System",
    "family": "Raise3D",
    "hotend_model": "",
    "machine_tech": "FFF",
    "model_id": "Raise3D-Pro3",
    "name": "Raise3D Pro3",
    "nozzle_diameter": "0.4",
    "type": "machine_model"
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
    "machine_end_gcode": "",
    "machine_max_acceleration_e": [
      "5000"
    ],
    "machine_max_acceleration_extruding": [
      "500"
    ],
    "machine_max_acceleration_retracting": [
      "1000"
    ],
    "machine_max_acceleration_x": [
      "500"
    ],
    "machine_max_acceleration_y": [
      "500"
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
    "machine_start_gcode": "",
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
  "process/0.10mm Fine @Raise3D Pro3.json": {
    "adaptive_layer_height": "1",
    "bottom_shell_layers": "6",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.95",
    "bridge_no_support": "0",
    "bridge_speed": "10",
    "brim_object_gap": "0",
    "brim_width": "5",
    "compatible_printers": [
      "Raise3D Pro3 0.4 nozzle (Dual)",
      "Raise3D Pro3 0.4 nozzle (Left)",
      "Raise3D Pro3 0.4 nozzle (Right)"
    ],
    "compatible_printers_condition": "",
    "default_acceleration": "0",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "25",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "25%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "0",
    "initial_layer_infill_speed": "35%",
    "initial_layer_line_width": "0.4",
    "initial_layer_print_height": "0.3",
    "initial_layer_speed": "35%",
    "inner_wall_acceleration": "0",
    "inner_wall_line_width": "0.4",
    "inner_wall_speed": "20",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0.4",
    "internal_solid_infill_speed": "70",
    "ironing_flow": "5%",
    "ironing_spacing": "0.1",
    "ironing_speed": "10",
    "ironing_type": "no ironing",
    "layer_height": "0.1",
    "line_width": "0.4",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.10mm Fine @Raise3D Pro3",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "15",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "20",
    "overhang_3_4_speed": "15",
    "overhang_4_4_speed": "10",
    "prime_tower_width": "40",
    "print_sequence": "by layer",
    "print_settings_id": "",
    "raft_layers": "0",
    "reduce_crossing_wall": "0",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "seam_position": "aligned",
    "setting_id": "GP004",
    "skirt_distance": "3",
    "skirt_height": "1",
    "skirt_loops": "2",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.4",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "60",
    "spiral_mode": "0",
    "standby_temperature_delta": "-20",
    "support_base_pattern": "rectilinear",
    "support_base_pattern_spacing": "0.1",
    "support_filament": "0",
    "support_interface_bottom_layers": "-1",
    "support_interface_filament": "0",
    "support_interface_loop_pattern": "0",
    "support_interface_spacing": "0.1",
    "support_interface_speed": "100%",
    "support_interface_top_layers": "3",
    "support_line_width": "0.38",
    "support_object_xy_distance": "60%",
    "support_on_build_plate_only": "0",
    "support_speed": "60",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.08",
    "support_type": "normal(auto)",
    "top_shell_layers": "5",
    "top_shell_thickness": "0.8",
    "top_surface_acceleration": "0",
    "top_surface_line_width": "0.38",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "35",
    "travel_acceleration": "0",
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
  "process/0.10mm Fine @Raise3D Pro3Plus.json": {
    "adaptive_layer_height": "1",
    "bottom_shell_layers": "6",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.95",
    "bridge_no_support": "0",
    "bridge_speed": "10",
    "brim_object_gap": "0",
    "brim_width": "5",
    "compatible_printers": [
      "Raise3D Pro3 Plus 0.4 nozzle (Dual)",
      "Raise3D Pro3 Plus 0.4 nozzle (Left)",
      "Raise3D Pro3 Plus 0.4 nozzle (Right)"
    ],
    "compatible_printers_condition": "",
    "default_acceleration": "0",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "25",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "25%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "0",
    "initial_layer_infill_speed": "35%",
    "initial_layer_line_width": "0.4",
    "initial_layer_print_height": "0.3",
    "initial_layer_speed": "35%",
    "inner_wall_acceleration": "0",
    "inner_wall_line_width": "0.4",
    "inner_wall_speed": "20",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0.4",
    "internal_solid_infill_speed": "70",
    "ironing_flow": "5%",
    "ironing_spacing": "0.1",
    "ironing_speed": "10",
    "ironing_type": "no ironing",
    "layer_height": "0.1",
    "line_width": "0.4",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.10mm Fine @Raise3D Pro3Plus",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "15",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "20",
    "overhang_3_4_speed": "15",
    "overhang_4_4_speed": "10",
    "prime_tower_width": "40",
    "print_sequence": "by layer",
    "print_settings_id": "",
    "raft_layers": "0",
    "reduce_crossing_wall": "0",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "seam_position": "aligned",
    "setting_id": "GP004",
    "skirt_distance": "3",
    "skirt_height": "1",
    "skirt_loops": "2",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.4",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "60",
    "spiral_mode": "0",
    "standby_temperature_delta": "-20",
    "support_base_pattern": "rectilinear",
    "support_base_pattern_spacing": "0.1",
    "support_filament": "0",
    "support_interface_bottom_layers": "-1",
    "support_interface_filament": "0",
    "support_interface_loop_pattern": "0",
    "support_interface_spacing": "0.1",
    "support_interface_speed": "100%",
    "support_interface_top_layers": "3",
    "support_line_width": "0.38",
    "support_object_xy_distance": "60%",
    "support_on_build_plate_only": "0",
    "support_speed": "60",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.08",
    "support_type": "normal(auto)",
    "top_shell_layers": "5",
    "top_shell_thickness": "0.8",
    "top_surface_acceleration": "0",
    "top_surface_line_width": "0.38",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "35",
    "travel_acceleration": "0",
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
  "process/0.20mm Standard @Raise3D Pro3.json": {
    "adaptive_layer_height": "1",
    "bottom_shell_layers": "5",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.95",
    "bridge_no_support": "0",
    "bridge_speed": "10",
    "brim_object_gap": "0",
    "brim_width": "5",
    "compatible_printers": [
      "Raise3D Pro3 0.4 nozzle (Dual)",
      "Raise3D Pro3 0.4 nozzle (Left)",
      "Raise3D Pro3 0.4 nozzle (Right)"
    ],
    "compatible_printers_condition": "",
    "default_acceleration": "0",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "25",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "25%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "0",
    "initial_layer_infill_speed": "35%",
    "initial_layer_line_width": "0.4",
    "initial_layer_print_height": "0.3",
    "initial_layer_speed": "35%",
    "inner_wall_acceleration": "0",
    "inner_wall_line_width": "0.4",
    "inner_wall_speed": "30",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0.4",
    "internal_solid_infill_speed": "70",
    "ironing_flow": "5%",
    "ironing_spacing": "0.1",
    "ironing_speed": "10",
    "ironing_type": "no ironing",
    "layer_height": "0.2",
    "line_width": "0.4",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.20mm Standard @Raise3D Pro3",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "25",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "20",
    "overhang_3_4_speed": "15",
    "overhang_4_4_speed": "10",
    "prime_tower_width": "40",
    "print_sequence": "by layer",
    "print_settings_id": "",
    "raft_layers": "0",
    "reduce_crossing_wall": "0",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "seam_position": "aligned",
    "setting_id": "GP004",
    "skirt_distance": "3",
    "skirt_height": "1",
    "skirt_loops": "2",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.4",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "60",
    "spiral_mode": "0",
    "standby_temperature_delta": "-20",
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
    "support_speed": "60",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.19",
    "support_type": "normal(auto)",
    "top_shell_layers": "5",
    "top_shell_thickness": "0.8",
    "top_surface_acceleration": "0",
    "top_surface_line_width": "0.38",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "35",
    "travel_acceleration": "0",
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
  "process/0.20mm Standard @Raise3D Pro3Plus.json": {
    "adaptive_layer_height": "1",
    "bottom_shell_layers": "5",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.95",
    "bridge_no_support": "0",
    "bridge_speed": "10",
    "brim_object_gap": "0",
    "brim_width": "5",
    "compatible_printers": [
      "Raise3D Pro3 Plus 0.4 nozzle (Dual)",
      "Raise3D Pro3 Plus 0.4 nozzle (Left)",
      "Raise3D Pro3 Plus 0.4 nozzle (Right)"
    ],
    "compatible_printers_condition": "",
    "default_acceleration": "0",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "25",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "25%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "0",
    "initial_layer_infill_speed": "35%",
    "initial_layer_line_width": "0.4",
    "initial_layer_print_height": "0.3",
    "initial_layer_speed": "35%",
    "inner_wall_acceleration": "0",
    "inner_wall_line_width": "0.4",
    "inner_wall_speed": "30",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0.4",
    "internal_solid_infill_speed": "70",
    "ironing_flow": "5%",
    "ironing_spacing": "0.1",
    "ironing_speed": "10",
    "ironing_type": "no ironing",
    "layer_height": "0.2",
    "line_width": "0.4",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.20mm Standard @Raise3D Pro3Plus",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "25",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "20",
    "overhang_3_4_speed": "15",
    "overhang_4_4_speed": "10",
    "prime_tower_width": "40",
    "print_sequence": "by layer",
    "print_settings_id": "",
    "raft_layers": "0",
    "reduce_crossing_wall": "0",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "seam_position": "aligned",
    "setting_id": "GP004",
    "skirt_distance": "3",
    "skirt_height": "1",
    "skirt_loops": "2",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.4",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "60",
    "spiral_mode": "0",
    "standby_temperature_delta": "-20",
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
    "support_speed": "60",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.19",
    "support_type": "normal(auto)",
    "top_shell_layers": "5",
    "top_shell_thickness": "0.8",
    "top_surface_acceleration": "0",
    "top_surface_line_width": "0.38",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "35",
    "travel_acceleration": "0",
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
  "process/0.25mm Draft @Raise3D Pro3.json": {
    "adaptive_layer_height": "1",
    "bottom_shell_layers": "3",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.95",
    "bridge_no_support": "0",
    "bridge_speed": "10",
    "brim_object_gap": "0",
    "brim_width": "5",
    "compatible_printers": [
      "Raise3D Pro3 0.4 nozzle (Dual)",
      "Raise3D Pro3 0.4 nozzle (Left)",
      "Raise3D Pro3 0.4 nozzle (Right)"
    ],
    "compatible_printers_condition": "",
    "default_acceleration": "0",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "25",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "25%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "0",
    "initial_layer_infill_speed": "35%",
    "initial_layer_line_width": "0.4",
    "initial_layer_print_height": "0.3",
    "initial_layer_speed": "35%",
    "inner_wall_acceleration": "0",
    "inner_wall_line_width": "0.4",
    "inner_wall_speed": "30",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0.4",
    "internal_solid_infill_speed": "70",
    "ironing_flow": "5%",
    "ironing_spacing": "0.1",
    "ironing_speed": "10",
    "ironing_type": "no ironing",
    "layer_height": "0.25",
    "line_width": "0.4",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.25mm Draft @Raise3D Pro3",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "35",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "20",
    "overhang_3_4_speed": "15",
    "overhang_4_4_speed": "10",
    "prime_tower_width": "40",
    "print_sequence": "by layer",
    "print_settings_id": "",
    "raft_layers": "0",
    "reduce_crossing_wall": "0",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "seam_position": "aligned",
    "setting_id": "GP004",
    "skirt_distance": "3",
    "skirt_height": "1",
    "skirt_loops": "2",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.4",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "60",
    "spiral_mode": "0",
    "standby_temperature_delta": "-20",
    "support_base_pattern": "rectilinear",
    "support_base_pattern_spacing": "0.25",
    "support_filament": "0",
    "support_interface_bottom_layers": "-1",
    "support_interface_filament": "0",
    "support_interface_loop_pattern": "0",
    "support_interface_spacing": "0.25",
    "support_interface_speed": "100%",
    "support_interface_top_layers": "3",
    "support_line_width": "0.38",
    "support_object_xy_distance": "60%",
    "support_on_build_plate_only": "0",
    "support_speed": "60",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.24",
    "support_type": "normal(auto)",
    "top_shell_layers": "3",
    "top_shell_thickness": "0.8",
    "top_surface_acceleration": "0",
    "top_surface_line_width": "0.38",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "35",
    "travel_acceleration": "0",
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
  "process/0.25mm Draft @Raise3D Pro3Plus.json": {
    "adaptive_layer_height": "1",
    "bottom_shell_layers": "3",
    "bottom_shell_thickness": "0",
    "bottom_surface_pattern": "monotonic",
    "bridge_flow": "0.95",
    "bridge_no_support": "0",
    "bridge_speed": "10",
    "brim_object_gap": "0",
    "brim_width": "5",
    "compatible_printers": [
      "Raise3D Pro3 Plus 0.4 nozzle (Dual)",
      "Raise3D Pro3 Plus 0.4 nozzle (Left)",
      "Raise3D Pro3 Plus 0.4 nozzle (Right)"
    ],
    "compatible_printers_condition": "",
    "default_acceleration": "0",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "25",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "25%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "0",
    "initial_layer_infill_speed": "35%",
    "initial_layer_line_width": "0.4",
    "initial_layer_print_height": "0.3",
    "initial_layer_speed": "35%",
    "inner_wall_acceleration": "0",
    "inner_wall_line_width": "0.4",
    "inner_wall_speed": "30",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0.4",
    "internal_solid_infill_speed": "70",
    "ironing_flow": "5%",
    "ironing_spacing": "0.1",
    "ironing_speed": "10",
    "ironing_type": "no ironing",
    "layer_height": "0.25",
    "line_width": "0.4",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.25mm Draft @Raise3D Pro3Plus",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "35",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "20",
    "overhang_3_4_speed": "15",
    "overhang_4_4_speed": "10",
    "prime_tower_width": "40",
    "print_sequence": "by layer",
    "print_settings_id": "",
    "raft_layers": "0",
    "reduce_crossing_wall": "0",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "seam_position": "aligned",
    "setting_id": "GP004",
    "skirt_distance": "3",
    "skirt_height": "1",
    "skirt_loops": "2",
    "sparse_infill_density": "15%",
    "sparse_infill_line_width": "0.4",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "60",
    "spiral_mode": "0",
    "standby_temperature_delta": "-20",
    "support_base_pattern": "rectilinear",
    "support_base_pattern_spacing": "0.25",
    "support_filament": "0",
    "support_interface_bottom_layers": "-1",
    "support_interface_filament": "0",
    "support_interface_loop_pattern": "0",
    "support_interface_spacing": "0.25",
    "support_interface_speed": "100%",
    "support_interface_top_layers": "3",
    "support_line_width": "0.38",
    "support_object_xy_distance": "60%",
    "support_on_build_plate_only": "0",
    "support_speed": "60",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.24",
    "support_type": "normal(auto)",
    "top_shell_layers": "3",
    "top_shell_thickness": "0.8",
    "top_surface_acceleration": "0",
    "top_surface_line_width": "0.38",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "35",
    "travel_acceleration": "0",
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
  "process/fdm_process_common.json": {
    "adaptive_layer_height": "0",
    "bridge_flow": "0.95",
    "bridge_no_support": "0",
    "bridge_speed": "10",
    "brim_width": "5",
    "compatible_printers": [],
    "default_acceleration": "0",
    "detect_overhang_wall": "0",
    "detect_thin_wall": "0",
    "elefant_foot_compensation": "0.1",
    "enable_prime_tower": "0",
    "enable_support": "0",
    "filename_format": "{input_filename_base}.gcode",
    "from": "system",
    "gap_infill_speed": "25",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "25%",
    "initial_layer_line_width": "0.4",
    "initial_layer_print_height": "0.2",
    "initial_layer_speed": "15",
    "inner_wall_line_width": "0.4",
    "inner_wall_speed": "40",
    "instantiation": "false",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0.4",
    "internal_solid_infill_speed": "60",
    "line_width": "0.4",
    "minimum_sparse_infill_area": "0",
    "name": "fdm_process_common",
    "outer_wall_line_width": "0.4",
    "outer_wall_speed": "25",
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
    "sparse_infill_line_width": "0.4",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "70",
    "spiral_mode": "0",
    "standby_temperature_delta": "-20",
    "support_base_pattern": "rectilinear",
    "support_base_pattern_spacing": "2",
    "support_filament": "0",
    "support_interface_filament": "0",
    "support_interface_loop_pattern": "0",
    "support_interface_spacing": "0",
    "support_interface_speed": "80",
    "support_interface_top_layers": "2",
    "support_line_width": "0.38",
    "support_object_xy_distance": "0.5",
    "support_on_build_plate_only": "0",
    "support_speed": "40",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.2",
    "top_surface_line_width": "0.4",
    "top_surface_speed": "35",
    "travel_speed": "150",
    "type": "process",
    "wall_loops": "3",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  }
}

FILAMENT = {}

MISC = {}

ASSETS = [
  "Raise3D Pro3 Plus_cover.png",
  "Raise3D Pro3_cover.png",
  "raise3d_pro3_buildplate_model.stl",
  "raise3d_pro3_buildplate_texture.png",
  "raise3d_pro3plus_buildplate_model.stl",
  "raise3d_pro3plus_buildplate_texture.png"
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
