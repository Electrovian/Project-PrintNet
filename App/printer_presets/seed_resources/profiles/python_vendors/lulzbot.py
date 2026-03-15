from __future__ import annotations

VENDOR = "Lulzbot"
INDEX = {
  "description": "Lulzbot configurations",
  "filament_list": [
    {
      "name": "Lulzbot 2.85mm ABS",
      "sub_path": "filament/Lulzbot 2.85mm ABS.json"
    },
    {
      "name": "Lulzbot 2.85mm PETG",
      "sub_path": "filament/Lulzbot 2.85mm PETG.json"
    },
    {
      "name": "Lulzbot 2.85mm PLA",
      "sub_path": "filament/Lulzbot 2.85mm PLA.json"
    }
  ],
  "force_update": "0",
  "machine_list": [
    {
      "name": "fdm_machine_common",
      "sub_path": "machine/fdm_machine_common.json"
    },
    {
      "name": "Lulzbot Taz 4 or 5 0.5 nozzle",
      "sub_path": "machine/Lulzbot Taz 4 or 5 0.5 nozzle.json"
    },
    {
      "name": "Lulzbot Taz 6 0.5 nozzle",
      "sub_path": "machine/Lulzbot Taz 6 0.5 nozzle.json"
    },
    {
      "name": "Lulzbot Taz Pro Common",
      "sub_path": "machine/Lulzbot Taz Pro Common.json"
    },
    {
      "name": "Lulzbot Taz Pro Dual 0.5 nozzle",
      "sub_path": "machine/Lulzbot Taz Pro Dual 0.5 nozzle.json"
    },
    {
      "name": "Lulzbot Taz Pro S 0.5 nozzle",
      "sub_path": "machine/Lulzbot Taz Pro S 0.5 nozzle.json"
    }
  ],
  "machine_model_list": [
    {
      "name": "Lulzbot Taz 4 or 5",
      "sub_path": "machine/Lulzbot Taz 4 or 5.json"
    },
    {
      "name": "Lulzbot Taz 6",
      "sub_path": "machine/Lulzbot Taz 6.json"
    },
    {
      "name": "Lulzbot Taz Pro Dual",
      "sub_path": "machine/Lulzbot Taz Pro Dual.json"
    },
    {
      "name": "Lulzbot Taz Pro S",
      "sub_path": "machine/Lulzbot Taz Pro S.json"
    }
  ],
  "name": "Lulzbot",
  "process_list": [
    {
      "name": "fdm_process_common",
      "sub_path": "process/fdm_process_common.json"
    },
    {
      "name": "0.25mm Standard @Lulzbot Taz 4 or 5",
      "sub_path": "process/0.25mm Standard @Lulzbot Taz 4 or 5.json"
    },
    {
      "name": "0.25mm Standard @Lulzbot Taz 6",
      "sub_path": "process/0.25mm Standard @Lulzbot Taz 6.json"
    },
    {
      "name": "0.25mm Standard @Lulzbot Taz Pro Dual",
      "sub_path": "process/0.25mm Standard @Lulzbot Taz Pro Dual.json"
    },
    {
      "name": "0.25mm Standard @Lulzbot Taz Pro S",
      "sub_path": "process/0.25mm Standard @Lulzbot Taz Pro S.json"
    },
    {
      "name": "0.18mm High Detail @Lulzbot Taz 4 or 5",
      "sub_path": "process/0.18mm High Detail @Lulzbot Taz 4 or 5.json"
    },
    {
      "name": "0.18mm High Detail @Lulzbot Taz 6",
      "sub_path": "process/0.18mm High Detail @Lulzbot Taz 6.json"
    },
    {
      "name": "0.18mm High Detail @Lulzbot Taz Pro Dual",
      "sub_path": "process/0.18mm High Detail @Lulzbot Taz Pro Dual.json"
    },
    {
      "name": "0.18mm High Detail @Lulzbot Taz Pro S",
      "sub_path": "process/0.18mm High Detail @Lulzbot Taz Pro S.json"
    }
  ],
  "url": "https://ohai.lulzbot.com/group/taz-6/",
  "version": "02.03.01.10"
}

MACHINE = {
  "machine/Lulzbot Taz 4 or 5 0.5 nozzle.json": {
    "auxiliary_fan": "0",
    "before_layer_change_gcode": "G92 E0; reset relative extrusion",
    "change_filament_gcode": "M400\nM600 B10 X115 Y-10 Z10\nM190 S{bed_temperature[0]}\nM109 S{temperature[0]}",
    "default_filament_profile": [
      "Lulzbot 2.85mm PLA"
    ],
    "default_print_profile": "0.25mm Standard @Lulzbot Taz 4 or 5",
    "deretraction_speed": [
      "40"
    ],
    "emit_machine_limits_to_gcode": "0",
    "from": "system",
    "inherits": "fdm_machine_common",
    "instantiation": "true",
    "layer_change_gcode": "; LAYER:{layer_num}\nM117 Layer: {layer_num +1} / [total_layer_count]",
    "machine_end_gcode": ";End G-Code Begin\nM400; wait for moves to finish\nM140 S0; disable hotend\nM104 S0; disable bed heater\nM107; disable fans\nG91; relative positioning\nG1 E-1 F300; filament retraction to release pressure\nG1 Z0.5 E-5 X-20 Y-20 F3000; lift up and retract even more filament\nM77;stopGLCD timer\nG90;absolute positioning\nG1 X0 Y250;move to cooling position\nM84;disable steppers\nM117 Print Complete.;print complete message",
    "machine_max_acceleration_extruding": [
      "500",
      "500"
    ],
    "machine_max_acceleration_retracting": [
      "1000",
      "1000"
    ],
    "machine_max_acceleration_travel": [
      "1250",
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
    "machine_pause_gcode": "M600 B10",
    "machine_start_gcode": ";This G-Code has been generated specifically for the Lulzbot Taz 4 and 5 - translated from CuraLE 4.13.10 by Wrathernaut\nM73 P0; clear GLCD progress bar\nM75; start GLCD timer\nM140 S{bed_temperature_initial_layer[0]}; start bed heating up\nG90; absolute positioning\nM107; disable fans\nM82; set extruder to absolute mode\nG28 X0 Y0; home X and Y\nG28 Z0; home Z\nG1 Z15.0 F175; move extruder up\nM117 Heating...; progress indicator message on LCD\nM109 R{nozzle_temperature_initial_layer[0]}; wait for extruder to reach printing temp\nM190 R{bed_temperature_initial_layer[0]}; wait for bed to reach printing temp\nG92 E0; set extruder position to 0\nG1 F200 E0; prime the nozzle with filament\nG92 E0; re-set extruder position to 0\nG1 F175; set travel speed\nM203 X192 Y208 Z3; set limits on travel speed\nM117 TAZ Printing...; progress indicator message on LCD\n;Start G-Code End",
    "max_layer_height": [
      "0.4"
    ],
    "min_layer_height": [
      "0.08"
    ],
    "name": "Lulzbot Taz 4 or 5 0.5 nozzle",
    "nozzle_diameter": [
      "0.5"
    ],
    "nozzle_type": "undefine",
    "printable_area": [
      "0x0",
      "280x0",
      "280x280",
      "0x280"
    ],
    "printable_height": "250",
    "printer_model": "Lulzbot Taz 4 or 5",
    "printer_settings_id": "Lulzbot4-5",
    "retract_before_wipe": [
      "70%"
    ],
    "retract_length_toolchange": [
      "1"
    ],
    "retraction_length": [
      "5"
    ],
    "retraction_minimum_travel": [
      "2"
    ],
    "scan_first_layer": "0",
    "setting_id": "LZ004",
    "single_extruder_multi_material": "1",
    "type": "machine"
  },
  "machine/Lulzbot Taz 4 or 5.json": {
    "bed_model": "taz_4_or_5_build_plate.stl",
    "bed_texture": "lulzbot_logo.png",
    "default_materials": "Lulzbot 2.85mm ABS;Lulzbot 2.85mm PETG;Lulzbot 2.85mm PLA",
    "family": "Lulzbot",
    "hotend_model": "",
    "machine_tech": "FFF",
    "model_id": "Lulzbot-Taz-4-5",
    "name": "Lulzbot Taz 4 or 5",
    "nozzle_diameter": "0.5",
    "type": "machine_model"
  },
  "machine/Lulzbot Taz 6 0.5 nozzle.json": {
    "auxiliary_fan": "0",
    "before_layer_change_gcode": "G92 E0; reset relative extrusion",
    "change_filament_gcode": "M400\nM600 B10 X115 Y-10 Z10\nM190 S{bed_temperature[0]}\nM109 S{temperature[0]}",
    "default_filament_profile": [
      "Lulzbot 2.85mm PLA"
    ],
    "default_print_profile": "0.25mm Standard @Lulzbot Taz 6",
    "deretraction_speed": [
      "40"
    ],
    "emit_machine_limits_to_gcode": "0",
    "from": "system",
    "inherits": "fdm_machine_common",
    "instantiation": "true",
    "layer_change_gcode": "; LAYER:{layer_num}\nM117 Layer: {layer_num +1} / [total_layer_count]",
    "machine_end_gcode": ";End G-Code Begin\nM400; wait for moves to finish\nM140 S0; start bed cooling\nM104 S0; disable hotend\nM107; disable fans\nG91; relative positioning\nG1 E-1 F300; filament retraction to release pressure\nG1 Z20 E-5 X-20 Y-20 F3000; lift up and retract even more filament\nG1 E6; re-prime extruder\nG90; absolute positioning\nG1 Y280 F3000; present finished print\nM77; stop GLCD timer\nM84; disable steppers\nG90; absolute positioning\nM117 Print Complete.; print complete message\n;End G-Code End",
    "machine_max_acceleration_extruding": [
      "500",
      "500"
    ],
    "machine_max_acceleration_retracting": [
      "1000",
      "1000"
    ],
    "machine_max_acceleration_travel": [
      "1250",
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
    "machine_pause_gcode": "M600 B10",
    "machine_start_gcode": ";This G-Code has been translated from LulzBot's CuraLE (v4.13.10) startup GCODE for Taz 6 Single Extruder by Wrathernaut\nM73 P0; clear GLCD progress bar\nM75; start GLCD timer\nM107; disable fans\nM420 S; disable leveling matrix\nG90; absolute positioning\nM82; set extruder to absolute mode\nG92 E0; set extruder position to 0\nM140 S{bed_temperature_initial_layer[0]}; start bed heating up (w)\nG28 XY; home X and Y\nG1 X-19 Y258 F1000; move to safe homing position\nM109 {if filament_type[0] == \"PLA\"}R180\n{elsif filament_type[0] == \"ABS\"}R190\n{elsif filament_type[0] == \"ABS-GF\"}R190\n{elsif filament_type[0] == \"ASA\"}R190\n{elsif filament_type[0] == \"ASA-Aero\"}R190\n{elsif filament_type[0] == \"BVOH\"}R170\n{elsif filament_type[0] == \"EVA\"}R170\n{elsif filament_type[0] == \"PA\"}R220\n{elsif filament_type[0] == \"PA-CF\"}R220\n{elsif filament_type[0] == \"PA-GF\"}R220\n{elsif filament_type[0] == \"PA6-CF\"}R220\n{elsif filament_type[0] == \"PA11-CF\"}R220\n{elsif filament_type[0] == \"ASA-Aero\"}R170\n{elsif filament_type[0] == \"PC\"}R220\n{elsif filament_type[0] == \"PC-CF\"}R220\n{elsif filament_type[0] == \"PCTG\"}R180\n{elsif filament_type[0] == \"PE\"}R190\n{elsif filament_type[0] == \"PE-CF\"}R190\n{elsif filament_type[0] == \"PET-CF\"}R190\n{elsif filament_type[0] == \"PETG\"}R190\n{elsif filament_type[0] == \"PETG-CF10\"}R190\n{elsif filament_type[0] == \"PHA\"}R180\n{elsif filament_type[0] == \"PLA-AERO\"}R180\n{elsif filament_type[0] == \"PLA-CF\"}R180\n{elsif filament_type[0] == \"PP\"}R180\n{elsif filament_type[0] == \"PP-CF\"}R180\n{elsif filament_type[0] == \"PP-GF\"}R180\n{elsif filament_type[0] == \"PPS\"}R180\n{elsif filament_type[0] == \"PPS-CF\"}R180\n{elsif filament_type[0] == \"PVA\"}R180\n{elsif filament_type[0] == \"PVB\"}R180\n{elsif filament_type[0] == \"SBS\"}R180\n{elsif filament_type[0] == \"TPU\"}R180\n{elsif filament_type[0] == \"FLEX\"}R180\n{elsif filament_type[0] == \"PET\"}R170\n{elsif filament_type[0] == \"HIPS\"}R170\n{elsif filament_type[0] == \"NYLON\"}R220\n{else}R190; unknown filament type soften temp before homing Z{endif}\nG28 Z; home Z\nG1 E-15 F100; retract filament\nM109 {if filament_type[0] == \"PLA\"}R180\n{elsif filament_type[0] == \"ABS\"}R190\n{elsif filament_type[0] == \"ABS-GF\"}R190\n{elsif filament_type[0] == \"ASA\"}R190\n{elsif filament_type[0] == \"ASA-Aero\"}R190\n{elsif filament_type[0] == \"BVOH\"}R170\n{elsif filament_type[0] == \"EVA\"}R170\n{elsif filament_type[0] == \"PA\"}R220\n{elsif filament_type[0] == \"PA-CF\"}R220\n{elsif filament_type[0] == \"PA-GF\"}R220\n{elsif filament_type[0] == \"PA6-CF\"}R220\n{elsif filament_type[0] == \"PA11-CF\"}R220\n{elsif filament_type[0] == \"ASA-Aero\"}R170\n{elsif filament_type[0] == \"PC\"}R220\n{elsif filament_type[0] == \"PC-CF\"}R220\n{elsif filament_type[0] == \"PCTG\"}R190\n{elsif filament_type[0] == \"PE\"}R190\n{elsif filament_type[0] == \"PE-CF\"}R190\n{elsif filament_type[0] == \"PET-CF\"}R190\n{elsif filament_type[0] == \"PETG\"}R190\n{elsif filament_type[0] == \"PETG-CF10\"}R190\n{elsif filament_type[0] == \"PHA\"}R180\n{elsif filament_type[0] == \"PLA-AERO\"}R180\n{elsif filament_type[0] == \"PLA-CF\"}R180\n{elsif filament_type[0] == \"PP\"}R180\n{elsif filament_type[0] == \"PP-CF\"}R180\n{elsif filament_type[0] == \"PP-GF\"}R180\n{elsif filament_type[0] == \"PPS\"}R180\n{elsif filament_type[0] == \"PPS-CF\"}R180\n{elsif filament_type[0] == \"PVA\"}R180\n{elsif filament_type[0] == \"PVB\"}R180\n{elsif filament_type[0] == \"SBS\"}R180\n{elsif filament_type[0] == \"TPU\"}R180\n{elsif filament_type[0] == \"FLEX\"}R180\n{elsif filament_type[0] == \"PET\"}R170\n{elsif filament_type[0] == \"HIPS\"}R180\n{elsif filament_type[0] == \"NYLON\"}R220\n{else}R170; unknown filament type wipe temp{endif}\n;M206 X0 Y0 Z0; uncomment to adjust wipe position (+X ~ nozzle moves left)(+Y ~ nozzle moves forward)(+Z ~ nozzle moves down)\nG12; wiping sequence\nM206 X0 Y0 Z0; reseting stock nozzle position ### CAUTION: changing this line can affect print quality ###\nG1 Z10 F5000; raise nozzle after wipe\nM109 {if filament_type[0] == \"PLA\"}R160\n{elsif filament_type[0] == \"ABS\"}R170\n{elsif filament_type[0] == \"ABS-GF\"}R170\n{elsif filament_type[0] == \"ASA\"}R170\n{elsif filament_type[0] == \"ASA-Aero\"}R170\n{elsif filament_type[0] == \"BVOH\"}R170\n{elsif filament_type[0] == \"EVA\"}R170\n{elsif filament_type[0] == \"PA\"}R200\n{elsif filament_type[0] == \"PA-CF\"}R200\n{elsif filament_type[0] == \"PA-GF\"}R170\n{elsif filament_type[0] == \"PA6-CF\"}R170\n{elsif filament_type[0] == \"PA11-CF\"}R200\n{elsif filament_type[0] == \"ASA-Aero\"}R170\n{elsif filament_type[0] == \"PC\"}R200\n{elsif filament_type[0] == \"PC-CF\"}R200\n{elsif filament_type[0] == \"PCTG\"}R180\n{elsif filament_type[0] == \"PE\"}R180\n{elsif filament_type[0] == \"PE-CF\"}R180\n{elsif filament_type[0] == \"PET-CF\"}R170\n{elsif filament_type[0] == \"PETG\"}R170\n{elsif filament_type[0] == \"PETG-CF10\"}R170\n{elsif filament_type[0] == \"PHA\"}R180\n{elsif filament_type[0] == \"PLA-AERO\"}R180\n{elsif filament_type[0] == \"PLA-CF\"}R180\n{elsif filament_type[0] == \"PP\"}R180\n{elsif filament_type[0] == \"PP-CF\"}R180\n{elsif filament_type[0] == \"PP-GF\"}R180\n{elsif filament_type[0] == \"PPS\"}R180\n{elsif filament_type[0] == \"PPS-CF\"}R180\n{elsif filament_type[0] == \"PVA\"}R160\n{elsif filament_type[0] == \"PVB\"}R160\n{elsif filament_type[0] == \"SBS\"}R180\n{elsif filament_type[0] == \"TPU\"}R160\n{elsif filament_type[0] == \"FLEX\"}R160\n{elsif filament_type[0] == \"PET\"}R170\n{elsif filament_type[0] == \"HIPS\"}R160\n{elsif filament_type[0] == \"NYLON\"}R200\n{else}R170; unknown filament type probe temp{endif}\nG1 X-10 Y293 F4000; move above first probe point\nM204 S100; set probing acceleration\nG29; start auto-leveling sequence\nM420 S1; enable leveling matrix\nM204 S500; restore standard acceleration\nG1 X0 Y0 Z15 F5000; move up off last probe point\nG4 S1; pause\nM400; wait for moves to finish\nM117 Heating...; progress indicator message on LCD\nM109 R{nozzle_temperature_initial_layer[0]}; wait for extruder to reach printing temp (w)\nM190 R{bed_temperature_initial_layer[0]}; wait for bed to reach printing temp\nG1 Z2 E0 F75; prime tiny bit of filament into the nozzle\nM117 TAZ 6 Printing...; progress indicator message on LCD\n;Start G-Code End",
    "max_layer_height": [
      "0.4"
    ],
    "min_layer_height": [
      "0.08"
    ],
    "name": "Lulzbot Taz 6 0.5 nozzle",
    "nozzle_diameter": [
      "0.5"
    ],
    "nozzle_type": "undefine",
    "printable_area": [
      "0x0",
      "280x0",
      "280x280",
      "0x280"
    ],
    "printable_height": "250",
    "printer_model": "Lulzbot Taz 6",
    "printer_settings_id": "Lulzbot",
    "retract_before_wipe": [
      "70%"
    ],
    "retract_length_toolchange": [
      "1"
    ],
    "retraction_length": [
      "5"
    ],
    "retraction_minimum_travel": [
      "2"
    ],
    "scan_first_layer": "0",
    "setting_id": "LZ006",
    "single_extruder_multi_material": "1",
    "type": "machine"
  },
  "machine/Lulzbot Taz 6.json": {
    "bed_model": "taz_6_build_plate.stl",
    "bed_texture": "lulzbot_logo.png",
    "default_materials": "Lulzbot 2.85mm ABS;Lulzbot 2.85mm PETG;Lulzbot 2.85mm PLA",
    "family": "Lulzbot",
    "hotend_model": "",
    "machine_tech": "FFF",
    "model_id": "Lulzbot-Taz-6",
    "name": "Lulzbot Taz 6",
    "nozzle_diameter": "0.5",
    "type": "machine_model"
  },
  "machine/Lulzbot Taz Pro Common.json": {
    "auxiliary_fan": "0",
    "before_layer_change_gcode": ";BEFORE_LAYER_CHANGE\n;[layer_z]\nG92 E0; reset relative extrusion",
    "change_filament_gcode": "",
    "cooling_tube_length": "0",
    "cooling_tube_retraction": "0",
    "deretraction_speed": [
      "10"
    ],
    "emit_machine_limits_to_gcode": "1",
    "extra_loading_move": "0",
    "from": "system",
    "inherits": "fdm_machine_common",
    "instantiation": "false",
    "layer_change_gcode": ";AFTER_LAYER_CHANGE\n;LAYER:{layer_num}\n;[layer_z]\nM117 Layer: {layer_num +1} / [total_layer_count]",
    "machine_load_filament_time": "1",
    "machine_max_acceleration_extruding": [
      "1000",
      "1000"
    ],
    "machine_max_acceleration_retracting": [
      "3000",
      "3000"
    ],
    "machine_max_acceleration_travel": [
      "500",
      "500"
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
      "100",
      "100"
    ],
    "machine_max_jerk_e": [
      "10",
      "10"
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
      "300",
      "300"
    ],
    "machine_max_speed_y": [
      "300",
      "300"
    ],
    "machine_max_speed_z": [
      "25",
      "25"
    ],
    "machine_pause_gcode": "M600 B10",
    "machine_tool_change_time": "3",
    "machine_unload_filament_time": "1",
    "max_layer_height": [
      "0.38",
      "0.38"
    ],
    "min_layer_height": [
      "0.08",
      "0.08"
    ],
    "name": "Lulzbot Taz Pro Common",
    "nozzle_type": "undefine",
    "parking_pos_retraction": "0",
    "printable_area": [
      "0x0",
      "280x0",
      "280x280",
      "0x280"
    ],
    "printable_height": "280",
    "printer_model": "Lulzbot Taz Pro Common",
    "printer_settings_id": "LulzbotPro-Common",
    "printer_structure": "i3",
    "retract_before_wipe": [
      "70%",
      "70%"
    ],
    "retract_length_toolchange": [
      "1",
      "1"
    ],
    "retraction_length": [
      "1",
      "1"
    ],
    "retraction_minimum_travel": [
      "1",
      "1"
    ],
    "retraction_speed": [
      "10"
    ],
    "scan_first_layer": "0",
    "setting_id": "LZPC001",
    "support_air_filtration": "0",
    "support_chamber_temp_control": "0",
    "support_multi_bed_types": "1",
    "type": "machine"
  },
  "machine/Lulzbot Taz Pro Dual 0.5 nozzle.json": {
    "default_filament_profile": [
      "Lulzbot 2.85mm PLA"
    ],
    "default_print_profile": "0.25mm Standard @Lulzbot Taz Pro Dual",
    "extruders_count": "2",
    "from": "system",
    "inherits": "Lulzbot Taz Pro Common",
    "instantiation": "true",
    "machine_end_gcode": "M400; wait for moves to finish\nM140 S0; start cooling bed\nM107; fans off\nG91 ; relative positioning\nG1 E-1 F300 ; retract the filament a bit before lifting the nozzle, to release some of the pressure\nG1 Z25 E-1 X20 Y20 F2000; move Z up a bit and retract filament even more\nM104 S{nozzle_temperature[0]} T0 ; T0 to print temp\nM104 S{nozzle_temperature[1]} T1 ; T1 to print temp\nG90 ; absolute positioning\nG0 X285 Y-30 F3000; move to cooling position\nG91 ; relative positioning\nM117 Purging for next print;progress indicator message\nT0\nM109 S{nozzle_temperature[0]}; wait for temp\nG92 E0; set extruder position to purge amount\nG1 E15 F75; purge\nM400; wait for purge\nM104 S0 ; T0 hotend off\nT1\nM109 S{nozzle_temperature[1]}; wait for temp\nG92 E0; set extruder position to purge amount\nG1 E15 F75; purge\nM400; wait for purge\nM104 S0 ; T1 hotend off\nT0\nM117 Cooling, please wait;progress indicator message\nM190 S0; cool off bed\nG0 Y280 F3000 ; present finished print\nM77; stop GLCD timer\nM18 X Y E; turn off x y and e axis\nG90 ; absolute positioning\nM117 Print complete; progress indicator message",
    "machine_start_gcode": ";This G-Code has been translated from Cura startup from CuraLE 4.13.10 to EONSlicer by Wrathernaut\nT0\nM82; absolute extrusion mode\nM73 P0; clear GLCD progress bar\nM75; start GLCD timer\nM107; disable fans\nG90; absolute positioning\nM420 S0; disable previous leveling matrix\nM140 S{bed_temperature_initial_layer[initial_tool]}; begin bed temping up (w)\nM104 {if filament_type[initial_tool] == \"PLA\"}S180\n{elsif filament_type[initial_tool] == \"ABS\"}S190\n{elsif filament_type[initial_tool] == \"ABS-GF\"}S190\n{elsif filament_type[initial_tool] == \"ASA\"}S190\n{elsif filament_type[initial_tool] == \"ASA-Aero\"}S190\n{elsif filament_type[initial_tool] == \"BVOH\"}S170\n{elsif filament_type[initial_tool] == \"EVA\"}S170\n{elsif filament_type[initial_tool] == \"PA\"}R220\n{elsif filament_type[initial_tool] == \"PA-CF\"}R220\n{elsif filament_type[initial_tool] == \"PA-GF\"}R220\n{elsif filament_type[initial_tool] == \"PA6-CF\"}R220\n{elsif filament_type[initial_tool] == \"PA11-CF\"}R220\n{elsif filament_type[initial_tool] == \"ASA-Aero\"}S170\n{elsif filament_type[initial_tool] == \"PC\"}R220\n{elsif filament_type[initial_tool] == \"PC-CF\"}R220\n{elsif filament_type[initial_tool] == \"PCTG\"}S180\n{elsif filament_type[initial_tool] == \"PE\"}S190\n{elsif filament_type[initial_tool] == \"PE-CF\"}S190\n{elsif filament_type[initial_tool] == \"PET-CF\"}S190\n{elsif filament_type[initial_tool] == \"PETG\"}S190\n{elsif filament_type[initial_tool] == \"PETG-CF10\"}S190\n{elsif filament_type[initial_tool] == \"PHA\"}S180\n{elsif filament_type[initial_tool] == \"PLA-AERO\"}S180\n{elsif filament_type[initial_tool] == \"PLA-CF\"}S180\n{elsif filament_type[initial_tool] == \"PP\"}S180\n{elsif filament_type[initial_tool] == \"PP-CF\"}S180\n{elsif filament_type[initial_tool] == \"PP-GF\"}S180\n{elsif filament_type[initial_tool] == \"PPS\"}S180\n{elsif filament_type[initial_tool] == \"PPS-CF\"}S180\n{elsif filament_type[initial_tool] == \"PVA\"}S180\n{elsif filament_type[initial_tool] == \"PVB\"}S180\n{elsif filament_type[initial_tool] == \"SBS\"}S180\n{elsif filament_type[initial_tool] == \"TPU\"}S180\n{elsif filament_type[initial_tool] == \"FLEX\"}S180\n{elsif filament_type[initial_tool] == \"PET\"}S170\n{elsif filament_type[initial_tool] == \"HIPS\"}S170\n{elsif filament_type[initial_tool] == \"NYLON\"}R220\n{else}S190; unknown filament type soften temp before homing Z\n{endif}G28; home\nG0 X50 Y25 Z10 F2000\nM117 Heating...\nM109 {if filament_type[0] == \"PLA\"}R180\n{elsif filament_type[0] == \"ABS\"}R190\n{elsif filament_type[0] == \"ABS-GF\"}R190\n{elsif filament_type[0] == \"ASA\"}R190\n{elsif filament_type[0] == \"ASA-Aero\"}R190\n{elsif filament_type[0] == \"BVOH\"}R170\n{elsif filament_type[0] == \"EVA\"}R170\n{elsif filament_type[0] == \"PA\"}R220\n{elsif filament_type[0] == \"PA-CF\"}R220\n{elsif filament_type[0] == \"PA-GF\"}R220\n{elsif filament_type[0] == \"PA6-CF\"}R220\n{elsif filament_type[0] == \"PA11-CF\"}R220\n{elsif filament_type[0] == \"ASA-Aero\"}R170\n{elsif filament_type[0] == \"PC\"}R220\n{elsif filament_type[0] == \"PC-CF\"}R220\n{elsif filament_type[0] == \"PCTG\"}R180\n{elsif filament_type[0] == \"PE\"}R190\n{elsif filament_type[0] == \"PE-CF\"}R190\n{elsif filament_type[0] == \"PET-CF\"}R190\n{elsif filament_type[0] == \"PETG\"}R190\n{elsif filament_type[0] == \"PETG-CF10\"}R190\n{elsif filament_type[0] == \"PHA\"}R180\n{elsif filament_type[0] == \"PLA-AERO\"}R180\n{elsif filament_type[0] == \"PLA-CF\"}R180\n{elsif filament_type[0] == \"PP\"}R180\n{elsif filament_type[0] == \"PP-CF\"}R180\n{elsif filament_type[0] == \"PP-GF\"}R180\n{elsif filament_type[0] == \"PPS\"}R180\n{elsif filament_type[0] == \"PPS-CF\"}R180\n{elsif filament_type[0] == \"PVA\"}R180\n{elsif filament_type[0] == \"PVB\"}R180\n{elsif filament_type[0] == \"SBS\"}R180\n{elsif filament_type[0] == \"TPU\"}R180\n{elsif filament_type[0] == \"FLEX\"}R180\n{elsif filament_type[0] == \"PET\"}R170\n{elsif filament_type[0] == \"HIPS\"}R170\n{elsif filament_type[0] == \"NYLON\"}R220\n{else}R190; unknown filament type soften temp before homing Z{endif}\nM82; set extruder to absolute mode\nG92 E0; set extruder to zero\nG1 E-7 F100; retract 7mm of filament on first extruder\nM106; turn on fans to speed cooling\nM117 Wiping...\nM109 {if filament_type[0] == \"PLA\"}R180\n{elsif filament_type[0] == \"ABS\"}R190\n{elsif filament_type[0] == \"ABS-GF\"}R190\n{elsif filament_type[0] == \"ASA\"}R190\n{elsif filament_type[0] == \"ASA-Aero\"}R190\n{elsif filament_type[0] == \"BVOH\"}R170\n{elsif filament_type[0] == \"EVA\"}R170\n{elsif filament_type[0] == \"PA\"}R220\n{elsif filament_type[0] == \"PA-CF\"}R220\n{elsif filament_type[0] == \"PA-GF\"}R220\n{elsif filament_type[0] == \"PA6-CF\"}R220\n{elsif filament_type[0] == \"PA11-CF\"}R220\n{elsif filament_type[0] == \"ASA-Aero\"}R170\n{elsif filament_type[0] == \"PC\"}R220\n{elsif filament_type[0] == \"PC-CF\"}R220\n{elsif filament_type[0] == \"PCTG\"}R190\n{elsif filament_type[0] == \"PE\"}R190\n{elsif filament_type[0] == \"PE-CF\"}R190\n{elsif filament_type[0] == \"PET-CF\"}R190\n{elsif filament_type[0] == \"PETG\"}R190\n{elsif filament_type[0] == \"PETG-CF10\"}R190\n{elsif filament_type[0] == \"PHA\"}R180\n{elsif filament_type[0] == \"PLA-AERO\"}R180\n{elsif filament_type[0] == \"PLA-CF\"}R180\n{elsif filament_type[0] == \"PP\"}R180\n{elsif filament_type[0] == \"PP-CF\"}R180\n{elsif filament_type[0] == \"PP-GF\"}R180\n{elsif filament_type[0] == \"PPS\"}R180\n{elsif filament_type[0] == \"PPS-CF\"}R180\n{elsif filament_type[0] == \"PVA\"}R180\n{elsif filament_type[0] == \"PVB\"}R180\n{elsif filament_type[0] == \"SBS\"}R180\n{elsif filament_type[0] == \"TPU\"}R180\n{elsif filament_type[0] == \"FLEX\"}R180\n{elsif filament_type[0] == \"PET\"}R170\n{elsif filament_type[0] == \"HIPS\"}R180\n{elsif filament_type[0] == \"NYLON\"}R220\n{else}R170; unknown filament type wipe temp{endif}\nM109 {if filament_type[0] == \"PLA\"}R160\n{elsif filament_type[0] == \"ABS\"}R170\n{elsif filament_type[0] == \"ABS-GF\"}R170\n{elsif filament_type[0] == \"ASA\"}R170\n{elsif filament_type[0] == \"ASA-Aero\"}R170\n{elsif filament_type[0] == \"BVOH\"}R170\n{elsif filament_type[0] == \"EVA\"}R170\n{elsif filament_type[0] == \"PA\"}R200\n{elsif filament_type[0] == \"PA-CF\"}R200\n{elsif filament_type[0] == \"PA-GF\"}R170\n{elsif filament_type[0] == \"PA6-CF\"}R170\n{elsif filament_type[0] == \"PA11-CF\"}R200\n{elsif filament_type[0] == \"ASA-Aero\"}R170\n{elsif filament_type[0] == \"PC\"}R200\n{elsif filament_type[0] == \"PC-CF\"}R200\n{elsif filament_type[0] == \"PCTG\"}R180\n{elsif filament_type[0] == \"PE\"}R180\n{elsif filament_type[0] == \"PE-CF\"}R180\n{elsif filament_type[0] == \"PET-CF\"}R170\n{elsif filament_type[0] == \"PETG\"}R170\n{elsif filament_type[0] == \"PETG-CF10\"}R170\n{elsif filament_type[0] == \"PHA\"}R180\n{elsif filament_type[0] == \"PLA-AERO\"}R180\n{elsif filament_type[0] == \"PLA-CF\"}R180\n{elsif filament_type[0] == \"PP\"}R180\n{elsif filament_type[0] == \"PP-CF\"}R180\n{elsif filament_type[0] == \"PP-GF\"}R180\n{elsif filament_type[0] == \"PPS\"}R180\n{elsif filament_type[0] == \"PPS-CF\"}R180\n{elsif filament_type[0] == \"PVA\"}R160\n{elsif filament_type[0] == \"PVB\"}R160\n{elsif filament_type[0] == \"SBS\"}R180\n{elsif filament_type[0] == \"TPU\"}R160\n{elsif filament_type[0] == \"FLEX\"}R160\n{elsif filament_type[0] == \"PET\"}R170\n{elsif filament_type[0] == \"HIPS\"}R160\n{elsif filament_type[0] == \"NYLON\"}R200\n{else}R170; unknown filament type probe temp{endif}; cool to probe temp\nG12; wipe sequence\nM107; turn off fan\nG29; probe sequence (for auto-leveling)\nM420 S1; enable leveling matrix\nT{initial_tool}; ensure we're using the first extruder\nM104 S{first_layer_temperature[initial_tool]}; set extruder temp\nG0 X5 Y15 Z10 F5000; move to start location\nM400; clear buffer\nM117 Heating...\nM109 R{first_layer_temperature[initial_tool]}; set extruder temp and waitnM190 R{bed_temperature_initial_layer[initial_tool]}; get bed temping up during first layer\nG1 Z2 E0 F75; raise head and 0 extruder\nM82; set to absolute mode\nM400; clear buffer\nM300 T; play sound at start of first layer\nM117 Printing ...\n;Start G-Code End",
    "name": "Lulzbot Taz Pro Dual 0.5 nozzle",
    "nozzle_diameter": [
      "0.5",
      "0.5"
    ],
    "printer_model": "Lulzbot Taz Pro Dual",
    "printer_settings_id": "LulzbotPro-Dual",
    "setting_id": "LZPD001",
    "single_extruder_multi_material": "0",
    "type": "machine"
  },
  "machine/Lulzbot Taz Pro Dual.json": {
    "bed_model": "taz_pro_dual_build_plate.stl",
    "bed_texture": "Taz_Pro_Dual_printbed.png",
    "default_materials": "Lulzbot 2.85mm ABS;Lulzbot 2.85mm PETG;Lulzbot 2.85mm PLA",
    "family": "Lulzbot",
    "hotend_model": "",
    "machine_tech": "FFF",
    "model_id": "Lulzbot-Taz-Pro-Dual",
    "name": "Lulzbot Taz Pro Dual",
    "nozzle_diameter": "0.5",
    "type": "machine_model"
  },
  "machine/Lulzbot Taz Pro S 0.5 nozzle.json": {
    "default_filament_profile": [
      "Generic PLA @System"
    ],
    "default_print_profile": "0.25mm Standard @Lulzbot Taz Pro S",
    "extruders_count": "1",
    "from": "system",
    "inherits": "Lulzbot Taz Pro Common",
    "instantiation": "true",
    "machine_end_gcode": "M400; wait for moves to finish\nM140 S0; start cooling bed\nM107; fans off\nG91 ; relative positioning\nG1 E-1 F300 ; retract the filament a bit before lifting the nozzle, to release some of the pressure\nG1 Z25 E-1 X20 Y20 F2000; move Z up a bit and retract filament even more\nM104 S{nozzle_temperature[0]} T0 ; T0 to print temp\nM104 S{nozzle_temperature[1]} T1 ; T1 to print temp\nG90 ; absolute positioning\nG0 X285 Y-30 F3000; move to cooling position\nG91 ; relative positioning\nM117 Purging for next print;progress indicator message\nT0\nM109 S{nozzle_temperature[0]}; wait for temp\nG92 E0; set extruder position to purge amount\nG1 E15 F75; purge\nM400; wait for purge\nM104 S0 ; T0 hotend off\nT1\nM109 S{nozzle_temperature[1]}; wait for temp\nG92 E0; set extruder position to purge amount\nG1 E15 F75; purge\nM400; wait for purge\nM104 S0 ; T1 hotend off\nT0\nM117 Cooling, please wait;progress indicator message\nM190 S0; cool off bed\nG0 Y280 F3000 ; present finished print\nM77; stop GLCD timer\nM18 X Y E; turn off x y and e axis\nG90 ; absolute positioning\nM117 Print complete; progress indicator message",
    "machine_start_gcode": ";This G-Code has been translated from Cura startup from CuraLE 4.13.10 to EONSlicer by Wrathernaut\nG4 S1 ; delay for 1 seconds to display file name\nM140 S{bed_temperature_initial_layer[initial_tool]}; begin bed temping up (w)\nM104 {if filament_type[initial_tool] == \"PLA\"}S180\n{elsif filament_type[initial_tool] == \"ABS\"}S190\n{elsif filament_type[initial_tool] == \"ABS-GF\"}S190\n{elsif filament_type[initial_tool] == \"ASA\"}S190\n{elsif filament_type[initial_tool] == \"ASA-Aero\"}S190\n{elsif filament_type[initial_tool] == \"BVOH\"}S170\n{elsif filament_type[initial_tool] == \"EVA\"}S170\n{elsif filament_type[initial_tool] == \"PA\"}R220\n{elsif filament_type[initial_tool] == \"PA-CF\"}R220\n{elsif filament_type[initial_tool] == \"PA-GF\"}R220\n{elsif filament_type[initial_tool] == \"PA6-CF\"}R220\n{elsif filament_type[initial_tool] == \"PA11-CF\"}R220\n{elsif filament_type[initial_tool] == \"ASA-Aero\"}S170\n{elsif filament_type[initial_tool] == \"PC\"}R220\n{elsif filament_type[initial_tool] == \"PC-CF\"}R220\n{elsif filament_type[initial_tool] == \"PCTG\"}S180\n{elsif filament_type[initial_tool] == \"PE\"}S190\n{elsif filament_type[initial_tool] == \"PE-CF\"}S190\n{elsif filament_type[initial_tool] == \"PET-CF\"}S190\n{elsif filament_type[initial_tool] == \"PETG\"}S190\n{elsif filament_type[initial_tool] == \"PETG-CF10\"}S190\n{elsif filament_type[initial_tool] == \"PHA\"}S180\n{elsif filament_type[initial_tool] == \"PLA-AERO\"}S180\n{elsif filament_type[initial_tool] == \"PLA-CF\"}S180\n{elsif filament_type[initial_tool] == \"PP\"}S180\n{elsif filament_type[initial_tool] == \"PP-CF\"}S180\n{elsif filament_type[initial_tool] == \"PP-GF\"}S180\n{elsif filament_type[initial_tool] == \"PPS\"}S180\n{elsif filament_type[initial_tool] == \"PPS-CF\"}S180\n{elsif filament_type[initial_tool] == \"PVA\"}S180\n{elsif filament_type[initial_tool] == \"PVB\"}S180\n{elsif filament_type[initial_tool] == \"SBS\"}S180\n{elsif filament_type[initial_tool] == \"TPU\"}S180\n{elsif filament_type[initial_tool] == \"FLEX\"}S180\n{elsif filament_type[initial_tool] == \"PET\"}S170\n{elsif filament_type[initial_tool] == \"HIPS\"}S170\n{elsif filament_type[initial_tool] == \"NYLON\"}R220\n{else}S190; unknown filament type soften temp before homing Z\n{endif}G28O; home all axes (if needed)\nM73 P0 ; clear LCD progress bar\nM75; start LCD print timer\nM107;disable fans\nM420 S0; disable leveling matrix\n{if enable_pressure_advance == 1}M900 K{pressure_advance[0]}; set pressure advance\n{endif}G90; absolute positioning\nM82; set extruder to absolute mode\nG92 E0; set extruder position to 0\nG0 X145 Y187 Z156 F3000; move away from endstops\nM117 Heating Nozzle...; progress indicator message on LCD\nM109 {if filament_type[0] == \"PLA\"}R180\n{elsif filament_type[0] == \"ABS\"}R190\n{elsif filament_type[0] == \"ABS-GF\"}R190\n{elsif filament_type[0] == \"ASA\"}R190\n{elsif filament_type[0] == \"ASA-Aero\"}R190\n{elsif filament_type[0] == \"BVOH\"}R170\n{elsif filament_type[0] == \"EVA\"}R170\n{elsif filament_type[0] == \"PA\"}R220\n{elsif filament_type[0] == \"PA-CF\"}R220\n{elsif filament_type[0] == \"PA-GF\"}R220\n{elsif filament_type[0] == \"PA6-CF\"}R220\n{elsif filament_type[0] == \"PA11-CF\"}R220\n{elsif filament_type[0] == \"ASA-Aero\"}R170\n{elsif filament_type[0] == \"PC\"}R220\n{elsif filament_type[0] == \"PC-CF\"}R220\n{elsif filament_type[0] == \"PCTG\"}R180\n{elsif filament_type[0] == \"PE\"}R190\n{elsif filament_type[0] == \"PE-CF\"}R190\n{elsif filament_type[0] == \"PET-CF\"}R190\n{elsif filament_type[0] == \"PETG\"}R190\n{elsif filament_type[0] == \"PETG-CF10\"}R190\n{elsif filament_type[0] == \"PHA\"}R180\n{elsif filament_type[0] == \"PLA-AERO\"}R180\n{elsif filament_type[0] == \"PLA-CF\"}R180\n{elsif filament_type[0] == \"PP\"}R180\n{elsif filament_type[0] == \"PP-CF\"}R180\n{elsif filament_type[0] == \"PP-GF\"}R180\n{elsif filament_type[0] == \"PPS\"}R180\n{elsif filament_type[0] == \"PPS-CF\"}R180\n{elsif filament_type[0] == \"PVA\"}R180\n{elsif filament_type[0] == \"PVB\"}R180\n{elsif filament_type[0] == \"SBS\"}R180\n{elsif filament_type[0] == \"TPU\"}R180\n{elsif filament_type[0] == \"FLEX\"}R180\n{elsif filament_type[0] == \"PET\"}R170\n{elsif filament_type[0] == \"HIPS\"}R170\n{elsif filament_type[0] == \"NYLON\"}R220\n{else}R190; unknown filament type soften temp before homing Z{endif};soften filament before retraction\nG1 E-7 F75; retract filament\nG92 E-12 ; set extruder position to -12 to account for 5mm retract at end of previous print\nM109 {if filament_type[0] == \"PLA\"}R180\n{elsif filament_type[0] == \"ABS\"}R190\n{elsif filament_type[0] == \"ABS-GF\"}R190\n{elsif filament_type[0] == \"ASA\"}R190\n{elsif filament_type[0] == \"ASA-Aero\"}R190\n{elsif filament_type[0] == \"BVOH\"}R170\n{elsif filament_type[0] == \"EVA\"}R170\n{elsif filament_type[0] == \"PA\"}R220\n{elsif filament_type[0] == \"PA-CF\"}R220\n{elsif filament_type[0] == \"PA-GF\"}R220\n{elsif filament_type[0] == \"PA6-CF\"}R220\n{elsif filament_type[0] == \"PA11-CF\"}R220\n{elsif filament_type[0] == \"ASA-Aero\"}R170\n{elsif filament_type[0] == \"PC\"}R220\n{elsif filament_type[0] == \"PC-CF\"}R220\n{elsif filament_type[0] == \"PCTG\"}R190\n{elsif filament_type[0] == \"PE\"}R190\n{elsif filament_type[0] == \"PE-CF\"}R190\n{elsif filament_type[0] == \"PET-CF\"}R190\n{elsif filament_type[0] == \"PETG\"}R190\n{elsif filament_type[0] == \"PETG-CF10\"}R190\n{elsif filament_type[0] == \"PHA\"}R180\n{elsif filament_type[0] == \"PLA-AERO\"}R180\n{elsif filament_type[0] == \"PLA-CF\"}R180\n{elsif filament_type[0] == \"PP\"}R180\n{elsif filament_type[0] == \"PP-CF\"}R180\n{elsif filament_type[0] == \"PP-GF\"}R180\n{elsif filament_type[0] == \"PPS\"}R180\n{elsif filament_type[0] == \"PPS-CF\"}R180\n{elsif filament_type[0] == \"PVA\"}R180\n{elsif filament_type[0] == \"PVB\"}R180\n{elsif filament_type[0] == \"SBS\"}R180\n{elsif filament_type[0] == \"TPU\"}R180\n{elsif filament_type[0] == \"FLEX\"}R180\n{elsif filament_type[0] == \"PET\"}R170\n{elsif filament_type[0] == \"HIPS\"}R180\n{elsif filament_type[0] == \"NYLON\"}R220\n{else}R170; unknown filament type wipe temp{endif};wait for extruder to reach wiping temp\nM104 {if filament_type[0] == \"PLA\"}R160\n{elsif filament_type[0] == \"ABS\"}R170\n{elsif filament_type[0] == \"ABS-GF\"}R170\n{elsif filament_type[0] == \"ASA\"}R170\n{elsif filament_type[0] == \"ASA-Aero\"}R170\n{elsif filament_type[0] == \"BVOH\"}R170\n{elsif filament_type[0] == \"EVA\"}R170\n{elsif filament_type[0] == \"PA\"}R200\n{elsif filament_type[0] == \"PA-CF\"}R200\n{elsif filament_type[0] == \"PA-GF\"}R170\n{elsif filament_type[0] == \"PA6-CF\"}R170\n{elsif filament_type[0] == \"PA11-CF\"}R200\n{elsif filament_type[0] == \"ASA-Aero\"}R170\n{elsif filament_type[0] == \"PC\"}R200\n{elsif filament_type[0] == \"PC-CF\"}R200\n{elsif filament_type[0] == \"PCTG\"}R180\n{elsif filament_type[0] == \"PE\"}R180\n{elsif filament_type[0] == \"PE-CF\"}R180\n{elsif filament_type[0] == \"PET-CF\"}R170\n{elsif filament_type[0] == \"PETG\"}R170\n{elsif filament_type[0] == \"PETG-CF10\"}R170\n{elsif filament_type[0] == \"PHA\"}R180\n{elsif filament_type[0] == \"PLA-AERO\"}R180\n{elsif filament_type[0] == \"PLA-CF\"}R180\n{elsif filament_type[0] == \"PP\"}R180\n{elsif filament_type[0] == \"PP-CF\"}R180\n{elsif filament_type[0] == \"PP-GF\"}R180\n{elsif filament_type[0] == \"PPS\"}R180\n{elsif filament_type[0] == \"PPS-CF\"}R180\n{elsif filament_type[0] == \"PVA\"}R160\n{elsif filament_type[0] == \"PVB\"}R160\n{elsif filament_type[0] == \"SBS\"}R180\n{elsif filament_type[0] == \"TPU\"}R160\n{elsif filament_type[0] == \"FLEX\"}R160\n{elsif filament_type[0] == \"PET\"}R170\n{elsif filament_type[0] == \"HIPS\"}R160\n{elsif filament_type[0] == \"NYLON\"}R200\n{else}R170; unknown filament type probe temp{endif}; start cooling to probe temp during wipe\nM106 S255 ; turn fan on to help drop temp\n; Use M206 below to adjust nozzle wipe position (Replace \"z_offset\" to adjust Z value)\n; X ~ (+)left/(-)right, Y ~ (+)front/(-)back, Z ~ (+)down/(-)up\nM206 X0 Y0 Z[z_offset] ; restoring offsets and adjusting offset if AST285 is enabled\nM117 Wiping Nozzle...;progress indicator on LCD\nG12; wiping sequence\nM206 X0 Y0 Z0 ; reseting stock nozzle position # # #  CAUTION:  changing this line can affect print quality # # #\nM107; turn off part cooling fan\nM104 {if filament_type[0] == \"PLA\"}R160\n{elsif filament_type[0] == \"ABS\"}R170\n{elsif filament_type[0] == \"ABS-GF\"}R170\n{elsif filament_type[0] == \"ASA\"}R170\n{elsif filament_type[0] == \"ASA-Aero\"}R170\n{elsif filament_type[0] == \"BVOH\"}R170\n{elsif filament_type[0] == \"EVA\"}R170\n{elsif filament_type[0] == \"PA\"}R200\n{elsif filament_type[0] == \"PA-CF\"}R200\n{elsif filament_type[0] == \"PA-GF\"}R170\n{elsif filament_type[0] == \"PA6-CF\"}R170\n{elsif filament_type[0] == \"PA11-CF\"}R200\n{elsif filament_type[0] == \"ASA-Aero\"}R170\n{elsif filament_type[0] == \"PC\"}R200\n{elsif filament_type[0] == \"PC-CF\"}R200\n{elsif filament_type[0] == \"PCTG\"}R180\n{elsif filament_type[0] == \"PE\"}R180\n{elsif filament_type[0] == \"PE-CF\"}R180\n{elsif filament_type[0] == \"PET-CF\"}R170\n{elsif filament_type[0] == \"PETG\"}R170\n{elsif filament_type[0] == \"PETG-CF10\"}R170\n{elsif filament_type[0] == \"PHA\"}R180\n{elsif filament_type[0] == \"PLA-AERO\"}R180\n{elsif filament_type[0] == \"PLA-CF\"}R180\n{elsif filament_type[0] == \"PP\"}R180\n{elsif filament_type[0] == \"PP-CF\"}R180\n{elsif filament_type[0] == \"PP-GF\"}R180\n{elsif filament_type[0] == \"PPS\"}R180\n{elsif filament_type[0] == \"PPS-CF\"}R180\n{elsif filament_type[0] == \"PVA\"}R160\n{elsif filament_type[0] == \"PVB\"}R160\n{elsif filament_type[0] == \"SBS\"}R180\n{elsif filament_type[0] == \"TPU\"}R160\n{elsif filament_type[0] == \"FLEX\"}R160\n{elsif filament_type[0] == \"PET\"}R170\n{elsif filament_type[0] == \"HIPS\"}R160\n{elsif filament_type[0] == \"NYLON\"}R200\n{else}R170; unknown filament type probe temp{endif}; set probe temp\nM117 Leveling Print Bed...; progress indicator message on LCD\nG29; start auto-leveling sequence\nM420 S1; enable leveling matrix\nG1 X5 Y15 Z10 F8000; move up off last probe point\nG4 S1; pause\nM400 wait for moves to finish\nM117 Final Heating... Please Wait.\nM109 S{first_layer_temperature[initial_tool]}; set extruder temp and wait\nM190 R{bed_temperature_initial_layer[initial_tool]}; get bed temping up during first layer\nG1 Z2 E0 F75; prime tiny bit of filament into the nozzle\nM300 T; play sound at start of first layer\nM117 Printing ...\n;Start G-Code End",
    "name": "Lulzbot Taz Pro S 0.5 nozzle",
    "nozzle_diameter": [
      "0.5"
    ],
    "printer_model": "Lulzbot Taz Pro S",
    "printer_settings_id": "LulzbotPro-S",
    "setting_id": "LZPS001",
    "single_extruder_multi_material": "1",
    "type": "machine"
  },
  "machine/Lulzbot Taz Pro S.json": {
    "bed_model": "taz_pro_dual_build_plate.stl",
    "bed_texture": "lulzbot_logo.png",
    "default_materials": "Generic PLA @System, Generic PETG @System, Generic ABS @System",
    "extruder_clearance_height_to_lid": "280",
    "extruder_clearance_height_to_rod": "36",
    "extruder_clearance_radius": "62",
    "family": "Lulzbot",
    "hotend_model": "",
    "machine_load_filament_time": "20",
    "machine_tech": "FFF",
    "machine_tool_change_time": "5",
    "machine_unload_filament_time": "20",
    "manual_filament_change": "1",
    "model_id": "Lulzbot-Taz-Pro-S",
    "name": "Lulzbot Taz Pro S",
    "nozzle_diameter": "0.5",
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
    "gcode_flavor": "marlin2",
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
      "0.5"
    ],
    "printable_height": "250",
    "printer_settings_id": "",
    "printer_technology": "FFF",
    "printer_variant": "0.5",
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
  "process/0.18mm High Detail @Lulzbot Taz 4 or 5.json": {
    "compatible_printers": [
      "Lulzbot Taz 4 or 5 0.5 nozzle"
    ],
    "from": "system",
    "inherits": "0.25mm Standard @Lulzbot Taz 4 or 5",
    "instantiation": "true",
    "layer_height": "0.18",
    "name": "0.18mm High Detail @Lulzbot Taz 4 or 5",
    "setting_id": "LZH04",
    "type": "process"
  },
  "process/0.18mm High Detail @Lulzbot Taz 6.json": {
    "compatible_printers": [
      "Lulzbot Taz 6 0.5 nozzle"
    ],
    "from": "system",
    "inherits": "0.25mm Standard @Lulzbot Taz 6",
    "instantiation": "true",
    "layer_height": "0.18",
    "name": "0.18mm High Detail @Lulzbot Taz 6",
    "setting_id": "LZH06",
    "type": "process"
  },
  "process/0.18mm High Detail @Lulzbot Taz Pro Dual.json": {
    "compatible_printers": [
      "Lulzbot Taz Pro Dual 0.5 nozzle"
    ],
    "from": "system",
    "inherits": "0.25mm Standard @Lulzbot Taz Pro Dual",
    "instantiation": "true",
    "layer_height": "0.18",
    "name": "0.18mm High Detail @Lulzbot Taz Pro Dual",
    "setting_id": "LZHPD01",
    "type": "process"
  },
  "process/0.18mm High Detail @Lulzbot Taz Pro S.json": {
    "compatible_printers": [
      "Lulzbot Taz Pro S 0.5 nozzle"
    ],
    "from": "system",
    "inherits": "0.25mm Standard @Lulzbot Taz Pro S",
    "instantiation": "true",
    "layer_height": "0.18",
    "name": "0.18mm High Detail @Lulzbot Taz Pro S",
    "setting_id": "LZHPS01",
    "type": "process"
  },
  "process/0.25mm Standard @Lulzbot Taz 4 or 5.json": {
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
      "Lulzbot Taz 4 or 5 0.5 nozzle"
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
    "gap_infill_speed": "30",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "25%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "0",
    "initial_layer_infill_speed": "35%",
    "initial_layer_line_width": "0.50",
    "initial_layer_print_height": "0.425",
    "initial_layer_speed": "35%",
    "inner_wall_acceleration": "0",
    "inner_wall_line_width": "0.50",
    "inner_wall_speed": "40",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0",
    "internal_solid_infill_speed": "40",
    "ironing_flow": "15%",
    "ironing_spacing": "0.1",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.25",
    "line_width": "0.5",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.25mm Standard @Lulzbot Taz 4 or 5",
    "outer_wall_acceleration": "0",
    "outer_wall_line_width": "0.5",
    "outer_wall_speed": "40",
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
    "setting_id": "LZS04",
    "skirt_distance": "3",
    "skirt_height": "1",
    "skirt_loops": "2",
    "sparse_infill_density": "20%",
    "sparse_infill_line_width": "0.50",
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
    "support_line_width": "0.5",
    "support_object_xy_distance": "60%",
    "support_on_build_plate_only": "0",
    "support_speed": "40",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.19",
    "support_type": "normal(auto)",
    "top_shell_layers": "5",
    "top_shell_thickness": "1.0",
    "top_surface_acceleration": "0",
    "top_surface_line_width": "0.5",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "30",
    "travel_acceleration": "0",
    "travel_speed": "150",
    "tree_support_branch_angle": "40",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "2",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/0.25mm Standard @Lulzbot Taz 6.json": {
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
      "Lulzbot Taz 6 0.5 nozzle"
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
    "gap_infill_speed": "30",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "25%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "0",
    "initial_layer_infill_speed": "35%",
    "initial_layer_line_width": "0.50",
    "initial_layer_print_height": "0.425",
    "initial_layer_speed": "35%",
    "inner_wall_acceleration": "0",
    "inner_wall_line_width": "0.50",
    "inner_wall_speed": "40",
    "instantiation": "true",
    "interface_shells": "0",
    "internal_solid_infill_line_width": "0",
    "internal_solid_infill_speed": "40",
    "ironing_flow": "15%",
    "ironing_spacing": "0.1",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.25",
    "line_width": "0.5",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.25mm Standard @Lulzbot Taz 6",
    "outer_wall_acceleration": "0",
    "outer_wall_line_width": "0.5",
    "outer_wall_speed": "40",
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
    "setting_id": "LZS06",
    "skirt_distance": "3",
    "skirt_height": "1",
    "skirt_loops": "2",
    "sparse_infill_density": "20%",
    "sparse_infill_line_width": "0.50",
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
    "support_line_width": "0.5",
    "support_object_xy_distance": "60%",
    "support_on_build_plate_only": "0",
    "support_speed": "40",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.19",
    "support_type": "normal(auto)",
    "top_shell_layers": "5",
    "top_shell_thickness": "1.0",
    "top_surface_acceleration": "0",
    "top_surface_line_width": "0.5",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "30",
    "travel_acceleration": "0",
    "travel_speed": "150",
    "tree_support_branch_angle": "40",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "2",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/0.25mm Standard @Lulzbot Taz Pro Dual.json": {
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
      "Lulzbot Taz Pro Dual 0.5 nozzle"
    ],
    "compatible_printers_condition": "",
    "default_acceleration": "0",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "1",
    "enable_support": "0",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "30",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "25%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "0",
    "initial_layer_infill_speed": "15",
    "initial_layer_line_width": "0.50",
    "initial_layer_print_height": "0.35",
    "initial_layer_speed": "15",
    "inner_wall_acceleration": "0",
    "inner_wall_line_width": "0.50",
    "inner_wall_speed": "35",
    "instantiation": "true",
    "interface_shells": "0",
    "interlocking_beam": "1",
    "interlocking_beam_width": "1",
    "internal_solid_infill_line_width": "0",
    "internal_solid_infill_speed": "45",
    "ironing_flow": "15%",
    "ironing_spacing": "0.1",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.25",
    "line_width": "0.5",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.25mm Standard @Lulzbot Taz Pro Dual",
    "ooze_prevention": "1",
    "outer_wall_acceleration": "0",
    "outer_wall_line_width": "0.5",
    "outer_wall_speed": "35",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "20",
    "overhang_3_4_speed": "15",
    "overhang_4_4_speed": "10",
    "preheat_steps": "1",
    "preheat_time": "35",
    "prime_tower_width": "30",
    "print_sequence": "by layer",
    "print_settings_id": "",
    "raft_layers": "0",
    "reduce_crossing_wall": "0",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "seam_position": "aligned",
    "setting_id": "LZSPD01",
    "skirt_distance": "3",
    "skirt_height": "1",
    "skirt_loops": "2",
    "sparse_infill_density": "20%",
    "sparse_infill_line_width": "0.50",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "45",
    "spiral_mode": "0",
    "standby_temperature_delta": "-25",
    "support_base_pattern": "rectilinear",
    "support_base_pattern_spacing": "0.2",
    "support_filament": "0",
    "support_interface_bottom_layers": "-1",
    "support_interface_filament": "0",
    "support_interface_loop_pattern": "0",
    "support_interface_spacing": "0.2",
    "support_interface_speed": "100%",
    "support_interface_top_layers": "3",
    "support_line_width": "0.5",
    "support_object_xy_distance": "60%",
    "support_on_build_plate_only": "0",
    "support_speed": "40",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.19",
    "support_type": "normal(auto)",
    "top_shell_layers": "5",
    "top_shell_thickness": "1.25",
    "top_surface_acceleration": "0",
    "top_surface_line_width": "0.5",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "35",
    "travel_acceleration": "0",
    "travel_speed": "175",
    "tree_support_branch_angle": "40",
    "tree_support_wall_count": "0",
    "type": "process",
    "wall_infill_order": "inner wall/outer wall/infill",
    "wall_loops": "2",
    "wipe_tower_no_sparse_layers": "0",
    "xy_contour_compensation": "0",
    "xy_hole_compensation": "0"
  },
  "process/0.25mm Standard @Lulzbot Taz Pro S.json": {
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
      "Lulzbot Taz Pro S 0.5 nozzle"
    ],
    "compatible_printers_condition": "",
    "default_acceleration": "0",
    "detect_overhang_wall": "1",
    "detect_thin_wall": "1",
    "draft_shield": "disabled",
    "elefant_foot_compensation": "0.1",
    "enable_arc_fitting": "0",
    "enable_prime_tower": "1",
    "enable_support": "0",
    "filename_format": "{input_filename_base}_{filament_type[initial_tool]}_{print_time}.gcode",
    "from": "system",
    "gap_infill_speed": "30",
    "infill_combination": "0",
    "infill_direction": "45",
    "infill_wall_overlap": "25%",
    "inherits": "fdm_process_common",
    "initial_layer_acceleration": "0",
    "initial_layer_infill_speed": "15",
    "initial_layer_line_width": "0.50",
    "initial_layer_print_height": "0.425",
    "initial_layer_speed": "15",
    "inner_wall_acceleration": "0",
    "inner_wall_line_width": "0.50",
    "inner_wall_speed": "30",
    "instantiation": "true",
    "interface_shells": "0",
    "interlocking_beam": "1",
    "interlocking_beam_width": "1",
    "internal_solid_infill_line_width": "0",
    "internal_solid_infill_speed": "40",
    "ironing_flow": "15%",
    "ironing_spacing": "0.1",
    "ironing_speed": "15",
    "ironing_type": "no ironing",
    "layer_height": "0.25",
    "line_width": "0.5",
    "max_travel_detour_distance": "0",
    "minimum_sparse_infill_area": "10",
    "name": "0.25mm Standard @Lulzbot Taz Pro S",
    "ooze_prevention": "1",
    "outer_wall_acceleration": "0",
    "outer_wall_line_width": "0.5",
    "outer_wall_speed": "30",
    "overhang_1_4_speed": "0",
    "overhang_2_4_speed": "20",
    "overhang_3_4_speed": "15",
    "overhang_4_4_speed": "10",
    "preheat_steps": "1",
    "preheat_time": "35",
    "prime_tower_width": "30",
    "print_sequence": "by layer",
    "print_settings_id": "",
    "raft_layers": "0",
    "reduce_crossing_wall": "0",
    "reduce_infill_retraction": "1",
    "resolution": "0.012",
    "seam_position": "aligned",
    "setting_id": "LZSPS01",
    "skirt_distance": "3",
    "skirt_height": "1",
    "skirt_loops": "2",
    "sparse_infill_density": "20%",
    "sparse_infill_line_width": "0.50",
    "sparse_infill_pattern": "crosshatch",
    "sparse_infill_speed": "45",
    "spiral_mode": "0",
    "standby_temperature_delta": "-25",
    "support_base_pattern": "rectilinear",
    "support_base_pattern_spacing": "0.2",
    "support_filament": "0",
    "support_interface_bottom_layers": "-1",
    "support_interface_filament": "0",
    "support_interface_loop_pattern": "0",
    "support_interface_spacing": "0.2",
    "support_interface_speed": "100%",
    "support_interface_top_layers": "3",
    "support_line_width": "0.5",
    "support_object_xy_distance": "60%",
    "support_on_build_plate_only": "0",
    "support_speed": "40",
    "support_style": "grid",
    "support_threshold_angle": "30",
    "support_top_z_distance": "0.19",
    "support_type": "normal(auto)",
    "top_shell_layers": "5",
    "top_shell_thickness": "1.25",
    "top_surface_acceleration": "0",
    "top_surface_line_width": "0.5",
    "top_surface_pattern": "monotonicline",
    "top_surface_speed": "30",
    "travel_acceleration": "0",
    "travel_speed": "175",
    "tree_support_branch_angle": "40",
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
    "bridge_flow": "0.95",
    "bridge_no_support": "0",
    "bridge_speed": "25",
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
    "sparse_infill_pattern": "alignedrectilinear",
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
  "filament/Lulzbot 2.85mm ABS.json": {
    "compatible_printers": [
      "Lulzbot Taz 6 0.5 nozzle",
      "Lulzbot Taz 4 or 5 0.5 nozzle",
      "Lulzbot Taz Pro Dual 0.5 nozzle"
    ],
    "filament_diameter": [
      "2.85"
    ],
    "filament_id": "GFB99",
    "filament_max_volumetric_speed": [
      "6"
    ],
    "from": "system",
    "inherits": "Generic ABS @System",
    "instantiation": "true",
    "name": "Lulzbot 2.85mm ABS",
    "setting_id": "GFSA04",
    "type": "filament"
  },
  "filament/Lulzbot 2.85mm PETG.json": {
    "compatible_printers": [
      "Lulzbot Taz 6 0.5 nozzle",
      "Lulzbot Taz 4 or 5 0.5 nozzle",
      "Lulzbot Taz Pro Dual 0.5 nozzle"
    ],
    "filament_diameter": [
      "2.85"
    ],
    "filament_id": "GFG99",
    "filament_max_volumetric_speed": [
      "6"
    ],
    "from": "system",
    "inherits": "Generic PETG @System",
    "instantiation": "true",
    "name": "Lulzbot 2.85mm PETG",
    "setting_id": "GFSG99",
    "type": "filament"
  },
  "filament/Lulzbot 2.85mm PLA.json": {
    "compatible_printers": [
      "Lulzbot Taz 6 0.5 nozzle",
      "Lulzbot Taz 4 or 5 0.5 nozzle",
      "Lulzbot Taz Pro Dual 0.5 nozzle"
    ],
    "filament_diameter": [
      "2.85"
    ],
    "filament_id": "GFL99",
    "filament_max_volumetric_speed": [
      "8"
    ],
    "from": "system",
    "inherits": "Generic PLA @System",
    "instantiation": "true",
    "name": "Lulzbot 2.85mm PLA",
    "setting_id": "GFSL99",
    "type": "filament"
  }
}

MISC = {}

ASSETS = [
  "Lulzbot Taz 4 or 5_cover.png",
  "Lulzbot Taz 6_cover.png",
  "Lulzbot Taz Mini 2_cover.png",
  "Lulzbot Taz Pro Dual_cover.png",
  "Lulzbot Taz Pro S_cover.png",
  "Lulzbot Taz Workhorse_cover.png",
  "lulzbot_logo.png",
  "taz_4_or_5_build_plate.stl",
  "taz_6_build_plate.stl",
  "taz_pro_dual_build_plate.stl",
  "Taz_Pro_Dual_printbed.png"
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
