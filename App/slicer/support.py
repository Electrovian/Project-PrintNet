"""Support generation utilities."""

from dataclasses import dataclass
import math
from typing import Dict, List, Optional, Sequence, Tuple

from .geometry import (Island2D, LineSegment2D, Point2D, ensure_winding,
                       islands_difference, islands_intersection, islands_union,
                       offset_islands, point_in_polygon, polygons_with_holes)
from .gcode.writer import SliceSettings
from .mesh import MeshModel
from . import infill

@dataclass
class SupportColumn:
    x: float
    y: float
    z_base: float
    z_top: float

@dataclass
class SupportLayerPlan:
    z: float
    base_lines: List[LineSegment2D]
    interface_lines: List[LineSegment2D]
    is_interface: bool

@dataclass
class SupportPlan:
    layers: List[SupportLayerPlan]
    tree_branches: List["TreeSupportBranch"]

@dataclass
class TreeSupportBranch:
    points: List[Tuple[float, float, float]]

@dataclass
class _TreeNode:
    x: float
    y: float
    z: float
    parent: Optional["_TreeNode"] = None

def overhang_mask(mesh: MeshModel, overhang_angle: float) -> List[Island2D]:
    triangles = mesh.overhang_triangles(overhang_angle)
    polygons: List[List[Point2D]] = []
    for tri in triangles:
        polygons.append([(tri[0][0], tri[0][1]),
                         (tri[1][0], tri[1][1]),
                         (tri[2][0], tri[2][1])])
    return polygons_with_holes(polygons)

def _point_in_island(point: Point2D, island: Island2D) -> bool:
    outer, holes = island
    if not point_in_polygon(point, outer):
        return False
    for hole in holes:
        if point_in_polygon(point, hole):
            return False
    return True

def _triangle_centroid(tri: Sequence[Tuple[float, float, float]]) -> Tuple[float, float, float]:
    cx = (tri[0][0] + tri[1][0] + tri[2][0]) / 3.0
    cy = (tri[0][1] + tri[1][1] + tri[2][1]) / 3.0
    cz = (tri[0][2] + tri[1][2] + tri[2][2]) / 3.0
    return (cx, cy, cz)

def _cluster_points(points: Sequence[Tuple[float, float, float]],
                    radius: float) -> List[Tuple[float, float, float]]:
    clusters: List[List[Tuple[float, float, float]]] = []
    centers: List[Tuple[float, float]] = []
    counts: List[int] = []
    r2 = radius * radius
    for point in points:
        added = False
        for idx, center in enumerate(centers):
            dx = point[0] - center[0]
            dy = point[1] - center[1]
            if dx * dx + dy * dy <= r2:
                clusters[idx].append(point)
                counts[idx] += 1
                count = counts[idx]
                centers[idx] = (
                    center[0] + (point[0] - center[0]) / count,
                    center[1] + (point[1] - center[1]) / count,
                )
                added = True
                break
        if not added:
            clusters.append([point])
            centers.append((point[0], point[1]))
            counts.append(1)
    results: List[Tuple[float, float, float]] = []
    for cluster, center in zip(clusters, centers):
        x, y = center
        z = max(p[2] for p in cluster)
        results.append((x, y, z))
    return results

def _cluster_nodes(nodes: Sequence[_TreeNode],
                   radius: float) -> List[List[_TreeNode]]:
    clusters: List[List[_TreeNode]] = []
    centers: List[Tuple[float, float]] = []
    counts: List[int] = []
    r2 = radius * radius
    for node in nodes:
        added = False
        for idx, center in enumerate(centers):
            dx = node.x - center[0]
            dy = node.y - center[1]
            if dx * dx + dy * dy <= r2:
                clusters[idx].append(node)
                counts[idx] += 1
                count = counts[idx]
                centers[idx] = (
                    center[0] + (node.x - center[0]) / count,
                    center[1] + (node.y - center[1]) / count,
                )
                added = True
                break
        if not added:
            clusters.append([node])
            centers.append((node.x, node.y))
            counts.append(1)
    return clusters

def generate_support_columns(mesh: MeshModel,
                             settings: SliceSettings) -> List[SupportColumn]:
    mask_islands = overhang_mask(mesh, settings.overhang_angle)
    if settings.support_xy_gap > 0.0 and mask_islands:
        mask_islands = offset_islands(mask_islands, -settings.support_xy_gap)
    if not mask_islands:
        return []

    triangles = mesh.overhang_triangles(settings.overhang_angle)
    points_xyz: List[Tuple[float, float, float]] = []
    for tri in triangles:
        points_xyz.append(_triangle_centroid(tri))

    if not points_xyz:
        return []

    filtered_xyz: List[Tuple[float, float, float]] = []
    for x, y, z in points_xyz:
        if z <= settings.layer_height * 0.5:
            continue
        for island in mask_islands:
            if _point_in_island((x, y), island):
                filtered_xyz.append((x, y, z))
                break
    if not filtered_xyz:
        return []

    clusters = _cluster_points(filtered_xyz, radius=settings.support_spacing)
    columns: List[SupportColumn] = []
    for x, y, z in clusters:
        z_top = z - settings.support_z_gap
        if z_top <= 0.0:
            continue
        columns.append(SupportColumn(x=x, y=y, z_base=0.0, z_top=z_top))
    return columns

def _merge_islands(*groups: Sequence[Island2D]) -> List[Island2D]:
    merged: List[Island2D] = []
    for group in groups:
        merged.extend(group)
    return islands_union(merged)

def _support_density_from_spacing(settings: SliceSettings) -> float:
    width = settings.support_line_width or settings.extrusion_width
    spacing = max(0.1, float(settings.support_spacing))
    if width <= 0.0:
        return 0.0
    return max(0.05, min(1.0, width / spacing))

def _support_patterns(settings: SliceSettings) -> Tuple[str, str]:
    base_pattern = getattr(settings, "support_pattern", "rectilinear")
    interface_pattern = getattr(settings, "support_interface_pattern", base_pattern)
    return base_pattern, interface_pattern

def _circle_loop(cx: float, cy: float, radius: float, steps: int = 12) -> List[Tuple[float, float]]:
    if radius <= 0.0:
        return []
    points = []
    for i in range(steps):
        angle = (2.0 * math.pi * i) / steps
        points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    points.append(points[0])
    return ensure_winding(points, clockwise=True)

def _circle_lines(cx: float, cy: float, radius: float, steps: int = 12) -> List[LineSegment2D]:
    loop = _circle_loop(cx, cy, radius, steps=steps)
    if not loop:
        return []
    return [(loop[i], loop[i + 1]) for i in range(len(loop) - 1)]

def _allowed_overhang_offset(settings: SliceSettings, layer_height: float) -> float:
    angle = max(1.0, min(89.0, float(settings.overhang_angle)))
    tan_val = math.tan(math.radians(angle))
    if tan_val <= 1e-6:
        return 0.0
    return max(0.0, float(layer_height) / tan_val)

def _support_masks_by_layer(layer_islands: Sequence[Sequence[Island2D]],
                            z_heights: Sequence[float],
                            settings: SliceSettings) -> List[List[Island2D]]:
    if not layer_islands:
        return []
    layer_count = len(layer_islands)
    masks: List[List[Island2D]] = [[] for _ in range(layer_count)]
    base_footprint: List[Island2D] = []
    if settings.support_build_plate_only:
        all_islands: List[Island2D] = []
        for layer in layer_islands:
            all_islands.extend(layer)
        base_footprint = islands_union(all_islands) if all_islands else []
    gap_layers = max(0, int(math.ceil(settings.support_z_gap / max(settings.layer_height, 1e-6))))
    pending: List[Island2D] = []

    for idx in range(layer_count - 1, 0, -1):
        current = layer_islands[idx]
        below = layer_islands[idx - 1]
        allowed_offset = _allowed_overhang_offset(settings, z_heights[idx] - z_heights[idx - 1])
        expanded_below = offset_islands(below, allowed_offset) if allowed_offset > 0.0 else list(below)
        unsupported = islands_difference(current, expanded_below)
        if settings.support_xy_gap > 0.0 and unsupported:
            unsupported = offset_islands(unsupported, -settings.support_xy_gap)
        pending = _merge_islands(pending, unsupported)
        if base_footprint and pending:
            pending = islands_intersection(pending, base_footprint)

        target_idx = idx - gap_layers
        if target_idx < 0:
            continue
        masks[target_idx] = _merge_islands(masks[target_idx], pending)
        if base_footprint and masks[target_idx]:
            masks[target_idx] = islands_intersection(masks[target_idx], base_footprint)

    return masks

def _interface_layer_indices(masks: Sequence[Sequence[Island2D]],
                             interface_layers: int) -> set[int]:
    indices = [idx for idx, mask in enumerate(masks) if mask]
    if not indices:
        return set()
    interface_layers = max(0, int(interface_layers))
    if interface_layers <= 0:
        return set()
    return set(indices[-interface_layers:])

def _tree_lines_by_layer(branches: Sequence[TreeSupportBranch],
                         z_heights: Sequence[float],
                         settings: SliceSettings) -> List[List[LineSegment2D]]:
    if not branches:
        return [[] for _ in z_heights]
    radius = max(settings.support_line_width or settings.extrusion_width, 0.2) * 0.6
    steps = max(8, int(round(2.0 * math.pi * radius / 0.6)))
    lines_by_layer: List[List[LineSegment2D]] = [[] for _ in z_heights]

    for branch in branches:
        points = list(branch.points)
        if len(points) < 2:
            continue
        points = sorted(points, key=lambda pt: pt[2])
        for idx, z in enumerate(z_heights):
            if z < points[0][2] - 1e-6 or z > points[-1][2] + 1e-6:
                continue
            for j in range(1, len(points)):
                z0 = points[j - 1][2]
                z1 = points[j][2]
                if (z0 <= z <= z1) or (z1 <= z <= z0):
                    if abs(z1 - z0) < 1e-6:
                        t = 0.0
                    else:
                        t = (z - z0) / (z1 - z0)
                    x = points[j - 1][0] + (points[j][0] - points[j - 1][0]) * t
                    y = points[j - 1][1] + (points[j][1] - points[j - 1][1]) * t
                    lines_by_layer[idx].extend(_circle_lines(x, y, radius, steps=steps))
                    break
    return lines_by_layer

def generate_tree_supports(mesh: MeshModel,
                           settings: SliceSettings) -> List[TreeSupportBranch]:
    mask_islands = overhang_mask(mesh, settings.overhang_angle)
    if settings.support_xy_gap > 0.0 and mask_islands:
        mask_islands = offset_islands(mask_islands, -settings.support_xy_gap)
    if not mask_islands:
        return []

    triangles = mesh.overhang_triangles(settings.overhang_angle)
    points_xyz: List[Tuple[float, float, float]] = []
    for tri in triangles:
        cx, cy, cz = _triangle_centroid(tri)
        for island in mask_islands:
            if _point_in_island((cx, cy), island):
                points_xyz.append((cx, cy, cz))
                break

    if not points_xyz:
        return []

    step = settings.layer_height
    if step <= 0.0:
        return []

    nodes_by_level: Dict[int, List[_TreeNode]] = {}
    for x, y, z in points_xyz:
        z_top = z - settings.support_z_gap
        if z_top <= step * 0.5:
            continue
        level = int(math.ceil(z_top / step))
        z_snapped = level * step
        nodes_by_level.setdefault(level, []).append(_TreeNode(x=x, y=y, z=z_snapped))

    if not nodes_by_level:
        return []

    max_level = max(nodes_by_level.keys())
    max_dx = math.tan(math.radians(settings.tree_branch_angle)) * step
    merge_distance = settings.tree_merge_distance

    for level in range(max_level, 0, -1):
        nodes = nodes_by_level.get(level, [])
        if not nodes:
            continue
        clusters = _cluster_nodes(nodes, merge_distance)
        next_level = level - 1
        for cluster in clusters:
            cx = sum(node.x for node in cluster) / len(cluster)
            cy = sum(node.y for node in cluster) / len(cluster)
            moved_points: List[Tuple[float, float]] = []
            for node in cluster:
                dx = cx - node.x
                dy = cy - node.y
                dist = math.hypot(dx, dy)
                if dist > max_dx and dist > 0.0:
                    scale = max_dx / dist
                    moved_points.append((node.x + dx * scale, node.y + dy * scale))
                else:
                    moved_points.append((cx, cy))
            parent_x = sum(p[0] for p in moved_points) / len(moved_points)
            parent_y = sum(p[1] for p in moved_points) / len(moved_points)
            needs_split = False
            for node in cluster:
                if math.hypot(parent_x - node.x, parent_y - node.y) > max_dx + 1e-6:
                    needs_split = True
                    break
            if needs_split:
                for node, (px, py) in zip(cluster, moved_points):
                    parent = _TreeNode(x=px, y=py, z=next_level * step)
                    node.parent = parent
                    nodes_by_level.setdefault(next_level, []).append(parent)
            else:
                parent = _TreeNode(x=parent_x, y=parent_y, z=next_level * step)
                for node in cluster:
                    node.parent = parent
                nodes_by_level.setdefault(next_level, []).append(parent)

    branches: List[TreeSupportBranch] = []
    seen: set = set()
    all_nodes: List[_TreeNode] = []
    parent_ids: set = set()
    for level_nodes in nodes_by_level.values():
        all_nodes.extend(level_nodes)
        for node in level_nodes:
            if node.parent is not None:
                parent_ids.add(id(node.parent))

    leaves = [node for node in all_nodes if id(node) not in parent_ids and node.parent is not None]
    for node in leaves:
        points: List[Tuple[float, float, float]] = [(node.x, node.y, node.z)]
        current = node
        while current.parent is not None:
            current = current.parent
            points.append((current.x, current.y, current.z))
        points = list(reversed(points))
        key = tuple((round(p[0], 4), round(p[1], 4), round(p[2], 4)) for p in points)
        if key in seen or len(points) < 2:
            continue
        seen.add(key)
        branches.append(TreeSupportBranch(points=points))
    return branches

def generate_support_plan(mesh: Optional[MeshModel],
                          z_heights: Sequence[float],
                          settings: SliceSettings,
                          layer_islands: Optional[Sequence[Sequence[Island2D]]] = None
                          ) -> SupportPlan:
    if not settings.support_enabled:
        return SupportPlan(layers=[], tree_branches=[])
    if not z_heights:
        return SupportPlan(layers=[], tree_branches=[])
    if layer_islands is None:
        if mesh is None:
            return SupportPlan(layers=[], tree_branches=[])
        layer_islands = [mesh.slice_layer(z) for z in z_heights]

    support_style = str(getattr(settings, "support_style", "pillars") or "pillars").strip().lower()
    support_type = str(getattr(settings, "support_type", "") or "").strip().lower()
    if support_type in ("tree", "trees", "organic", "hybrid"):
        support_style = "tree"
    elif support_type in ("normal", "auto", "default") and support_style in ("tree", "trees"):
        support_style = "pillars"

    support_masks = _support_masks_by_layer(layer_islands, z_heights, settings)
    interface_layers = _interface_layer_indices(support_masks, settings.interface_layers)
    base_pattern, interface_pattern = _support_patterns(settings)
    base_density = _support_density_from_spacing(settings)

    support_layers: List[SupportLayerPlan] = []
    tree_branches: List[TreeSupportBranch] = []
    tree_lines: List[List[LineSegment2D]] = [[] for _ in z_heights]
    if support_style in ("tree", "trees"):
        if mesh is not None:
            tree_branches = generate_tree_supports(mesh, settings)
        tree_lines = _tree_lines_by_layer(tree_branches, z_heights, settings)

    for idx, z in enumerate(z_heights):
        base_lines: List[LineSegment2D] = []
        interface_lines: List[LineSegment2D] = []
        is_interface = idx in interface_layers
        mask = support_masks[idx] if idx < len(support_masks) else []

        if support_style in ("tree", "trees"):
            base_lines = tree_lines[idx]
            if is_interface and mask:
                interface_lines = infill.generate_infill(
                    mask,
                    density=settings.interface_density,
                    angle_deg=settings.infill_angle,
                    layer_index=idx,
                    extrusion_width=settings.support_line_width or settings.extrusion_width,
                    pattern=interface_pattern,
                    alternate=True,
                )
        else:
            if mask:
                density = settings.interface_density if is_interface else base_density
                pattern = interface_pattern if is_interface else base_pattern
                lines = infill.generate_infill(
                    mask,
                    density=density,
                    angle_deg=settings.infill_angle,
                    layer_index=idx,
                    extrusion_width=settings.support_line_width or settings.extrusion_width,
                    pattern=pattern,
                    alternate=True,
                )
                if is_interface:
                    interface_lines = lines
                else:
                    base_lines = lines

        if base_lines or interface_lines:
            support_layers.append(SupportLayerPlan(
                z=float(z),
                base_lines=base_lines,
                interface_lines=interface_lines,
                is_interface=is_interface,
            ))

    return SupportPlan(layers=support_layers,
                       tree_branches=tree_branches)
