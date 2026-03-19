from __future__ import annotations

# source: profiles/M3D.json
DATA = {'description': 'Configuration for M3D printers',
 'filament_list': [],
 'force_update': '0',
 'machine_list': [{'name': 'fdm_machine_common', 'sub_path': 'machine/fdm_machine_common.json'},
                  {'name': 'M3D Enabler D8500 MM', 'sub_path': 'machine/M3D Enabler D8500 MM.json'}],
 'machine_model_list': [{'name': 'M3D Enabler D8500 MM Model', 'sub_path': 'machine/M3D Enabler D8500 MM Model.json'}],
 'name': 'M3D',
 'process_list': [{'name': 'fdm_process_common', 'sub_path': 'process/fdm_process_common.json'},
                  {'name': '0.15mm MM @D8500', 'sub_path': 'process/0.15mm MM @D8500.json'},
                  {'name': '0.20mm MM @D8500', 'sub_path': 'process/0.20mm MM @D8500.json'}],
 'version': '1.0.0'}
