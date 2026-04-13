from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np


def _vec3_tuple(value: Any, default: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> tuple[float, float, float]:
    try:
        arr = np.asarray(value if value is not None else default, dtype=float).reshape(-1)
    except Exception:
        arr = np.asarray(default, dtype=float).reshape(-1)
    if arr.size != 3:
        arr = np.asarray(default, dtype=float).reshape(-1)
    return (float(arr[0]), float(arr[1]), float(arr[2]))


def _listify_vertices(value: Any) -> list[list[float]]:
    arr = np.asarray(value, dtype=float)
    if arr.ndim != 2 or arr.shape[1] != 3:
        raise ValueError("Invalid vertex array")
    return [[float(x), float(y), float(z)] for x, y, z in arr.tolist()]


def _listify_faces(value: Any) -> list[list[int]]:
    arr = np.asarray(value, dtype=int)
    if arr.ndim != 2 or arr.shape[1] != 3:
        raise ValueError("Invalid face array")
    return [[int(a), int(b), int(c)] for a, b, c in arr.tolist()]


@dataclass
class PlateState:
    id: int
    name: str
    order: int
    locked: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": int(self.id),
            "name": str(self.name or "").strip() or f"{int(self.order) + 1:02d}",
            "order": int(self.order),
            "locked": bool(self.locked),
            "metadata": dict(self.metadata or {}),
        }


@dataclass
class PartState:
    id: int
    name: str
    vertices: list[list[float]]
    faces: list[list[int]]
    kind: str = "mesh"
    source_path: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": int(self.id),
            "name": str(self.name or "").strip() or f"Part {int(self.id)}",
            "vertices": [[float(v) for v in row] for row in self.vertices],
            "faces": [[int(v) for v in row] for row in self.faces],
            "kind": str(self.kind or "mesh"),
            "source_path": str(self.source_path or ""),
            "metadata": dict(self.metadata or {}),
        }


@dataclass
class ObjectState:
    id: int
    name: str
    part_ids: list[int]
    source_path: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": int(self.id),
            "name": str(self.name or "").strip() or f"Object {int(self.id)}",
            "part_ids": [int(pid) for pid in self.part_ids],
            "source_path": str(self.source_path or ""),
            "metadata": dict(self.metadata or {}),
        }


@dataclass
class InstanceState:
    id: int
    object_id: int
    plate_id: int
    name: str = ""
    scale: tuple[float, float, float] = (1.0, 1.0, 1.0)
    rotation: tuple[float, float, float] = (0.0, 0.0, 0.0)
    offset: tuple[float, float, float] = (0.0, 0.0, 0.0)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": int(self.id),
            "object_id": int(self.object_id),
            "plate_id": int(self.plate_id),
            "name": str(self.name or ""),
            "scale": [float(v) for v in self.scale],
            "rotation": [float(v) for v in self.rotation],
            "offset": [float(v) for v in self.offset],
            "metadata": dict(self.metadata or {}),
        }


@dataclass
class ToolState:
    active_tool: str = "move"
    active_editor: str = ""
    assembly_mode: bool = False
    assembly_explosion_ratio: float = 1.0
    assembly_offsets: dict[str, list[float]] = field(default_factory=dict)
    adaptive_layer_ranges: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    annotations: dict[str, dict[str, Any]] = field(default_factory=dict)
    emboss_payloads: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    measure_payload: dict[str, Any] = field(default_factory=dict)
    cut_payload: dict[str, Any] = field(default_factory=dict)
    boolean_payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "active_tool": str(self.active_tool or "move"),
            "active_editor": str(self.active_editor or ""),
            "assembly_mode": bool(self.assembly_mode),
            "assembly_explosion_ratio": float(self.assembly_explosion_ratio),
            "assembly_offsets": {str(key): list(value or []) for key, value in dict(self.assembly_offsets or {}).items()},
            "adaptive_layer_ranges": {
                str(key): [dict(item or {}) for item in (value or [])]
                for key, value in dict(self.adaptive_layer_ranges or {}).items()
            },
            "annotations": {str(key): dict(value or {}) for key, value in dict(self.annotations or {}).items()},
            "emboss_payloads": {
                str(key): [dict(item or {}) for item in (value or [])]
                for key, value in dict(self.emboss_payloads or {}).items()
            },
            "measure_payload": dict(self.measure_payload or {}),
            "cut_payload": dict(self.cut_payload or {}),
            "boolean_payload": dict(self.boolean_payload or {}),
        }


class SceneState:
    VERSION = 2

    def __init__(self):
        self.plates: dict[int, PlateState] = {}
        self.objects: dict[int, ObjectState] = {}
        self.parts: dict[int, PartState] = {}
        self.instances: dict[int, InstanceState] = {}
        self.selected_plate_id: int | None = None
        self.selected_entity_ids: list[int] = []
        self.tool_state = ToolState()
        self._next_plate_id = 1
        self._next_object_id = 1
        self._next_part_id = 1
        self._next_instance_id = 1
        self.ensure_default_plate()

    def ensure_default_plate(self) -> int:
        if self.plates:
            if self.selected_plate_id in self.plates:
                return int(self.selected_plate_id)
            plate_id = min(self.plates.keys(), key=lambda key: self.plates[key].order)
            self.selected_plate_id = int(plate_id)
            return int(plate_id)
        plate = self.create_plate()
        self.selected_plate_id = int(plate.id)
        return int(plate.id)

    def _default_plate_name(self, order: int) -> str:
        return f"{int(order) + 1:02d}"

    def create_plate(self, name: str | None = None) -> PlateState:
        plate_id = int(self._next_plate_id)
        self._next_plate_id += 1
        order = len(self.plates)
        plate = PlateState(
            id=plate_id,
            name=str(name or self._default_plate_name(order)).strip() or self._default_plate_name(order),
            order=order,
        )
        self.plates[plate_id] = plate
        self.selected_plate_id = plate_id
        return plate

    def reorder_plates(self) -> None:
        ordered = sorted(self.plates.values(), key=lambda plate: (plate.order, plate.id))
        for order, plate in enumerate(ordered):
            plate.order = int(order)
            if not str(plate.name or "").strip():
                plate.name = self._default_plate_name(order)

    def delete_plate(self, plate_id: int) -> bool:
        plate_id = int(plate_id)
        if plate_id not in self.plates or len(self.plates) <= 1:
            return False
        instance_ids = [iid for iid, instance in self.instances.items() if int(instance.plate_id) == plate_id]
        for instance_id in instance_ids:
            self.remove_instance(instance_id, prune_orphans=True)
        del self.plates[plate_id]
        self.reorder_plates()
        remaining = sorted(self.plates.values(), key=lambda plate: (plate.order, plate.id))
        if remaining:
            self.selected_plate_id = int(remaining[min(len(remaining) - 1, 0)].id)
        else:
            self.selected_plate_id = None
        self.selected_entity_ids = [iid for iid in self.selected_entity_ids if iid in self.instances]
        self.ensure_default_plate()
        return True

    def set_selected_plate(self, plate_id: int | None) -> int | None:
        if plate_id is None:
            self.selected_plate_id = None
            return None
        plate_id = int(plate_id)
        if plate_id in self.plates:
            self.selected_plate_id = plate_id
        return self.selected_plate_id

    def create_object(
        self,
        name: str,
        source_path: str,
        parts: list[dict[str, Any]],
        metadata: dict[str, Any] | None = None,
    ) -> ObjectState:
        object_id = int(self._next_object_id)
        self._next_object_id += 1
        part_ids: list[int] = []
        for raw_part in parts:
            part_id = int(self._next_part_id)
            self._next_part_id += 1
            vertices = _listify_vertices(raw_part.get("vertices", []))
            faces = _listify_faces(raw_part.get("faces", []))
            part = PartState(
                id=part_id,
                name=str(raw_part.get("name", "") or f"Part {len(part_ids) + 1}"),
                vertices=vertices,
                faces=faces,
                kind=str(raw_part.get("kind", "mesh") or "mesh"),
                source_path=str(raw_part.get("source_path", source_path) or source_path or ""),
                metadata=dict(raw_part.get("metadata") or {}),
            )
            self.parts[part_id] = part
            part_ids.append(part_id)
        obj = ObjectState(
            id=object_id,
            name=str(name or "").strip() or f"Object {object_id}",
            part_ids=part_ids,
            source_path=str(source_path or ""),
            metadata=dict(metadata or {}),
        )
        self.objects[object_id] = obj
        return obj

    def create_instance(
        self,
        object_id: int,
        *,
        plate_id: int | None = None,
        name: str = "",
        scale: Any = (1.0, 1.0, 1.0),
        rotation: Any = (0.0, 0.0, 0.0),
        offset: Any = (0.0, 0.0, 0.0),
        metadata: dict[str, Any] | None = None,
    ) -> InstanceState:
        if object_id not in self.objects:
            raise KeyError(f"Unknown object id {object_id}")
        resolved_plate_id = int(plate_id if plate_id is not None else self.ensure_default_plate())
        if resolved_plate_id not in self.plates:
            raise KeyError(f"Unknown plate id {resolved_plate_id}")
        instance_id = int(self._next_instance_id)
        self._next_instance_id += 1
        instance = InstanceState(
            id=instance_id,
            object_id=int(object_id),
            plate_id=resolved_plate_id,
            name=str(name or ""),
            scale=_vec3_tuple(scale, (1.0, 1.0, 1.0)),
            rotation=_vec3_tuple(rotation, (0.0, 0.0, 0.0)),
            offset=_vec3_tuple(offset, (0.0, 0.0, 0.0)),
            metadata=dict(metadata or {}),
        )
        self.instances[instance_id] = instance
        self.selected_plate_id = resolved_plate_id
        self.selected_entity_ids = [instance_id]
        return instance

    def add_imported_object(
        self,
        name: str,
        source_path: str,
        parts: list[dict[str, Any]],
        *,
        plate_id: int | None = None,
        object_metadata: dict[str, Any] | None = None,
        instance_metadata: dict[str, Any] | None = None,
    ) -> InstanceState:
        obj = self.create_object(name=name, source_path=source_path, parts=parts, metadata=object_metadata)
        return self.create_instance(obj.id, plate_id=plate_id, metadata=instance_metadata)

    def remove_instance(self, instance_id: int, prune_orphans: bool = True) -> bool:
        instance_id = int(instance_id)
        instance = self.instances.get(instance_id)
        if instance is None:
            return False
        object_id = int(instance.object_id)
        del self.instances[instance_id]
        self.selected_entity_ids = [iid for iid in self.selected_entity_ids if iid != instance_id]
        if prune_orphans and not any(int(item.object_id) == object_id for item in self.instances.values()):
            self.remove_object(object_id)
        if self.selected_entity_ids:
            selected = self.selected_entity_ids[0]
            current = self.instances.get(selected)
            if current is not None:
                self.selected_plate_id = int(current.plate_id)
        return True

    def remove_object(self, object_id: int) -> bool:
        object_id = int(object_id)
        obj = self.objects.get(object_id)
        if obj is None:
            return False
        instance_ids = [iid for iid, instance in self.instances.items() if int(instance.object_id) == object_id]
        for instance_id in instance_ids:
            if instance_id in self.instances:
                del self.instances[instance_id]
        for part_id in list(obj.part_ids):
            self.parts.pop(int(part_id), None)
        del self.objects[object_id]
        self.selected_entity_ids = [iid for iid in self.selected_entity_ids if iid in self.instances]
        return True

    def get_plate_instance_ids(self, plate_id: int | None = None) -> list[int]:
        resolved_plate_id = int(plate_id if plate_id is not None else self.ensure_default_plate())
        return [
            int(instance.id)
            for instance in sorted(self.instances.values(), key=lambda item: item.id)
            if int(instance.plate_id) == resolved_plate_id
        ]

    def get_all_instance_ids(self) -> list[int]:
        return [int(instance.id) for instance in sorted(self.instances.values(), key=lambda item: item.id)]

    def get_plate_ids(self) -> list[int]:
        ordered = sorted(self.plates.values(), key=lambda plate: (plate.order, plate.id))
        return [int(plate.id) for plate in ordered]

    def get_plate(self, plate_id: int | None = None) -> PlateState | None:
        if plate_id is None:
            if self.selected_plate_id is None:
                return None
            plate_id = self.selected_plate_id
        return self.plates.get(int(plate_id))

    def get_object(self, object_id: int) -> ObjectState | None:
        return self.objects.get(int(object_id))

    def get_instance(self, instance_id: int) -> InstanceState | None:
        return self.instances.get(int(instance_id))

    def get_object_parts(self, object_id: int) -> list[PartState]:
        obj = self.objects.get(int(object_id))
        if obj is None:
            return []
        return [self.parts[pid] for pid in obj.part_ids if pid in self.parts]

    def object_mesh_arrays(self, object_id: int) -> tuple[np.ndarray, np.ndarray, list[tuple[int, int, int]]]:
        parts = self.get_object_parts(int(object_id))
        if not parts:
            return (
                np.zeros((0, 3), dtype=float),
                np.zeros((0, 3), dtype=int),
                [],
            )
        vertices_list: list[np.ndarray] = []
        faces_list: list[np.ndarray] = []
        face_ranges: list[tuple[int, int, int]] = []
        vert_offset = 0
        face_offset = 0
        for part in parts:
            vertices = np.asarray(part.vertices, dtype=float)
            faces = np.asarray(part.faces, dtype=int)
            if vertices.ndim != 2 or vertices.shape[1] != 3 or faces.ndim != 2 or faces.shape[1] != 3:
                continue
            vertices_list.append(vertices)
            faces_list.append(faces + vert_offset)
            start = face_offset
            stop = face_offset + int(len(faces))
            face_ranges.append((int(part.id), int(start), int(stop)))
            vert_offset += int(len(vertices))
            face_offset = stop
        if not vertices_list or not faces_list:
            return (
                np.zeros((0, 3), dtype=float),
                np.zeros((0, 3), dtype=int),
                [],
            )
        return (
            np.vstack(vertices_list),
            np.vstack(faces_list),
            face_ranges,
        )

    def duplicate_instance(self, instance_id: int, *, offset: Any = (10.0, 10.0, 0.0)) -> InstanceState:
        instance = self.get_instance(instance_id)
        if instance is None:
            raise KeyError(f"Unknown instance id {instance_id}")
        delta = _vec3_tuple(offset, (10.0, 10.0, 0.0))
        return self.create_instance(
            int(instance.object_id),
            plate_id=int(instance.plate_id),
            name=str(instance.name or ""),
            scale=instance.scale,
            rotation=instance.rotation,
            offset=(
                float(instance.offset[0] + delta[0]),
                float(instance.offset[1] + delta[1]),
                float(instance.offset[2] + delta[2]),
            ),
            metadata=dict(instance.metadata or {}),
        )

    def prune_orphan_objects(self) -> None:
        live_objects = {int(instance.object_id) for instance in self.instances.values()}
        for object_id in list(self.objects.keys()):
            if object_id not in live_objects:
                self.remove_object(object_id)

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": int(self.VERSION),
            "plates": [self.plates[plate_id].to_dict() for plate_id in self.get_plate_ids()],
            "objects": [self.objects[object_id].to_dict() for object_id in sorted(self.objects.keys())],
            "parts": [self.parts[part_id].to_dict() for part_id in sorted(self.parts.keys())],
            "instances": [self.instances[instance_id].to_dict() for instance_id in self.get_all_instance_ids()],
            "selected_plate_id": int(self.selected_plate_id) if self.selected_plate_id is not None else None,
            "selected_entity_ids": [int(item_id) for item_id in self.selected_entity_ids if item_id in self.instances],
            "tool_state": self.tool_state.to_dict(),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any] | None) -> SceneState:
        scene = cls()
        scene.plates.clear()
        scene.objects.clear()
        scene.parts.clear()
        scene.instances.clear()
        scene.selected_plate_id = None
        scene.selected_entity_ids = []
        scene.tool_state = ToolState()
        scene._next_plate_id = 1
        scene._next_object_id = 1
        scene._next_part_id = 1
        scene._next_instance_id = 1

        data = dict(payload or {})
        for raw_plate in data.get("plates", []) or []:
            if not isinstance(raw_plate, dict):
                continue
            plate = PlateState(
                id=int(raw_plate.get("id", scene._next_plate_id)),
                name=str(raw_plate.get("name", "") or ""),
                order=int(raw_plate.get("order", len(scene.plates))),
                locked=bool(raw_plate.get("locked", False)),
                metadata=dict(raw_plate.get("metadata") or {}),
            )
            scene.plates[plate.id] = plate
            scene._next_plate_id = max(scene._next_plate_id, int(plate.id) + 1)

        for raw_part in data.get("parts", []) or []:
            if not isinstance(raw_part, dict):
                continue
            part = PartState(
                id=int(raw_part.get("id", scene._next_part_id)),
                name=str(raw_part.get("name", "") or ""),
                vertices=_listify_vertices(raw_part.get("vertices", [])),
                faces=_listify_faces(raw_part.get("faces", [])),
                kind=str(raw_part.get("kind", "mesh") or "mesh"),
                source_path=str(raw_part.get("source_path", "") or ""),
                metadata=dict(raw_part.get("metadata") or {}),
            )
            scene.parts[part.id] = part
            scene._next_part_id = max(scene._next_part_id, int(part.id) + 1)

        for raw_object in data.get("objects", []) or []:
            if not isinstance(raw_object, dict):
                continue
            obj = ObjectState(
                id=int(raw_object.get("id", scene._next_object_id)),
                name=str(raw_object.get("name", "") or ""),
                part_ids=[int(pid) for pid in list(raw_object.get("part_ids", []) or []) if int(pid) in scene.parts],
                source_path=str(raw_object.get("source_path", "") or ""),
                metadata=dict(raw_object.get("metadata") or {}),
            )
            scene.objects[obj.id] = obj
            scene._next_object_id = max(scene._next_object_id, int(obj.id) + 1)

        for raw_instance in data.get("instances", []) or []:
            if not isinstance(raw_instance, dict):
                continue
            object_id = int(raw_instance.get("object_id", 0))
            plate_id = int(raw_instance.get("plate_id", 0))
            if object_id not in scene.objects or plate_id not in scene.plates:
                continue
            instance = InstanceState(
                id=int(raw_instance.get("id", scene._next_instance_id)),
                object_id=object_id,
                plate_id=plate_id,
                name=str(raw_instance.get("name", "") or ""),
                scale=_vec3_tuple(raw_instance.get("scale"), (1.0, 1.0, 1.0)),
                rotation=_vec3_tuple(raw_instance.get("rotation"), (0.0, 0.0, 0.0)),
                offset=_vec3_tuple(raw_instance.get("offset"), (0.0, 0.0, 0.0)),
                metadata=dict(raw_instance.get("metadata") or {}),
            )
            scene.instances[instance.id] = instance
            scene._next_instance_id = max(scene._next_instance_id, int(instance.id) + 1)

        raw_tool_state = data.get("tool_state")
        if isinstance(raw_tool_state, dict):
            scene.tool_state = ToolState(
                active_tool=str(raw_tool_state.get("active_tool", "move") or "move"),
                active_editor=str(raw_tool_state.get("active_editor", "") or ""),
                assembly_mode=bool(raw_tool_state.get("assembly_mode", False)),
                assembly_explosion_ratio=float(raw_tool_state.get("assembly_explosion_ratio", 1.0) or 1.0),
                assembly_offsets={str(key): list(value or []) for key, value in dict(raw_tool_state.get("assembly_offsets") or {}).items()},
                adaptive_layer_ranges={
                    str(key): [dict(item or {}) for item in (value or [])]
                    for key, value in dict(raw_tool_state.get("adaptive_layer_ranges") or {}).items()
                },
                annotations={str(key): dict(value or {}) for key, value in dict(raw_tool_state.get("annotations") or {}).items()},
                emboss_payloads={
                    str(key): [dict(item or {}) for item in (value or [])]
                    for key, value in dict(raw_tool_state.get("emboss_payloads") or {}).items()
                },
                measure_payload=dict(raw_tool_state.get("measure_payload") or {}),
                cut_payload=dict(raw_tool_state.get("cut_payload") or {}),
                boolean_payload=dict(raw_tool_state.get("boolean_payload") or {}),
            )

        selected_plate_id = data.get("selected_plate_id")
        if selected_plate_id is not None and int(selected_plate_id) in scene.plates:
            scene.selected_plate_id = int(selected_plate_id)
        selected_entity_ids = [int(item_id) for item_id in list(data.get("selected_entity_ids", []) or []) if int(item_id) in scene.instances]
        scene.selected_entity_ids = selected_entity_ids
        scene.ensure_default_plate()
        scene.reorder_plates()
        return scene

