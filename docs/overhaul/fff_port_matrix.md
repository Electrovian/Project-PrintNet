# FFF Port Matrix (Python-first)

## Scope
- Source anchors:
`overhaul/eon_engine_mirror/src/libslic3r`
`overhaul/eon_engine_mirror/src/libvgcode`
`overhaul/eon_engine_mirror/src/slic3r`
- Active target:
`App/slicer_v2`
- Done definition:
Corpus parity with tolerance gates (not bit-identical G-code).

## FFF Matrix
| Subsystem | C++ Source | Python Target | Status | Notes |
| --- | --- | --- | --- | --- |
| Layer/island adjacency | `libslic3r/Algorithm`, `libslic3r/Print*` | `App/slicer_v2/island_graph.py` | `ported` | Vertical adjacency + layer graph are exercised in existing tests. |
| Region expansion / split | `libslic3r/Algorithm/RegionExpansion.*`, `LineSplit.*` | `App/slicer_v2/region_expansion.py`, `App/slicer_v2/line_split.py` | `ported` | Core wave propagation and clipped segment logic present. |
| Infill patterns | `libslic3r/Fill/*` | `App/slicer_v2/infill_patterns.py` | `partial` | Broad pattern coverage; combine-infill parity metadata is additive and still evolving. |
| Bridge planning | `libslic3r/Fill/Fill*`, bridge internals | `App/slicer_v2/solid_bridges.py`, `App/slicer_v2/bridges.py` | `partial` | Multi-island span graph + strip metrics implemented; full bridge detector parity still open. |
| Arachne variable width | `libslic3r/Arachne/*` | `App/slicer_v2/perimeter_variable.py` | `partial` | Half-edge redistribution and carryover exist; full junction/beading parity is not complete. |
| Tree supports | `libslic3r/Support/*` | `App/slicer_v2/support_planning.py`, `App/slicer_v2/supports.py` | `partial` | Parent/trunk weighted scoring and route-aware heuristics present; still marked MVP lineage. |
| Travel planning | `libslic3r/GCode` travel routing | `App/slicer_v2/travel_planning.py`, `App/slicer_v2/travel.py` | `partial` | Avoid-crossing style combing and detour constraints present. |
| G-code emission/validation | `libslic3r/GCode/*` | `App/slicer_v2/gcode.py`, `gcode_emission.py`, `gcode_validation.py` | `partial` | Core semantics + validation present; advanced processors remain deferred. |
| Settings normalization | `libslic3r/Preset*`, config layers | `App/slicer_v2/settings.py` | `ported` | Alias/coercion/clamp matrix is broad and test-covered. |
| Corpus parity harness | n/a (port infrastructure) | `App/testing/fff_parity.py` | `ported` | Deterministic metrics + tolerance comparator over corpus manifest. |

## CLI Parity Track
- Status:
`Profiles+Compat First` in progress.
- Target modules:
`App/slicer_v2/cli.py`, `App/slicer_v2/profile_compat.py`, `App/slicer_v2/cli_contract.py`
- Current focus:
Profile loading/merge, compatibility lookup (`downward_check`), deterministic `result.json` contract.
- Deferred in this phase:
3MF project parity, multi-plate assemble orchestration, thumbnail/OpenGL generation, pipe callback parity.

## Deferred Queue (Non-FFF / Lower Priority)
| Area | Source | Status | Prereq |
| --- | --- | --- | --- |
| SLA toolchain | `libslic3r/SLA/*` | `missing` | FFF parity gate stable |
| Full format parity | `libslic3r/Format/*` | `partial` | FFF parity gate stable |
| Viewer renderer parity | `libvgcode/*` | `missing` | FFF parity + UI integration plan |
| Desktop GUI behavior parity | `src/slic3r/*` | `deferred` | Connector and UX strategy alignment |

## Parity Gate Metrics
- Exact:
`layer_count`, `stage_order`, `stage_presence`, normalized settings digest.
- Tolerance:
Path counts `max(2, 5%)`, path lengths `7%`, bridge candidate/support ratio `<= 0.08` abs delta, tree branch/trunk counts `<= 10%`.
- Hard gate:
No G-code validation hard errors on corpus output.
