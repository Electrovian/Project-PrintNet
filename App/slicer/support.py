"""Support generation utilities."""

from dataclasses import dataclass
import math
from typing import Dict, List, Optional, Sequence, Tuple

from .geometry import (Island2D, LineSegment2D, Point2D, offset_islands,
                       point_in_polygon, polygons_with_holes)
from .gcode import SliceSettings
from .mesh import MeshModel
from . import infill

@dataclass
class SupportColumn:
    x: float
    y: float
    z_base: float
    z_top: float

@dataclass
class SupportInterfaceLayer:
    z: float
    lines: List[LineSegment2D]

@dataclass
class SupportPlan:
    mask_islands: List[Island2D]
    columns: List[SupportColumn]
    interface_layers: List[SupportInterfaceLayer]
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

def _cluster_points(points: Sequence[Tuple[float, float, float]],
                    radius: float) -> List[Tuple[float, float, float]]:
    clusters: List[List[Tuple[float, float, float]]] = []
    r2 = radius * radius
    for point in points:
        added = False
        for cluster in clusters:
            cx = sum(p[0] for p in cluster) / len(cluster)
            cy = sum(p[1] for p in cluster) / len(cluster)
            dx = point[0] - cx
            dy = point[1] - cy
            if dx * dx + dy * dy <= r2:
                cluster.append(point)
                added = True
                break
        if not added:
            clusters.append([point])
    results: List[Tuple[float, float, float]] = []
    for cluster in clusters:
        x = sum(p[0] for p in cluster) / len(cluster)
        y = sum(p[1] for p in cluster) / len(cluster)
        z = max(p[2] for p in cluster)
        results.append((x, y, z))
    return results

def _cluster_nodes(nodes: Sequence[_TreeNode],
                   radius: float) -> List[List[_TreeNode]]:
    clusters: List[List[_TreeNode]] = []
    r2 = radius * radius
    for node in nodes:
        added = False
        for cluster in clusters:
            cx = sum(n.x for n in cluster) / len(cluster)
            cy = sum(n.y for n in cluster) / len(cluster)
            dx = node.x - cx
            dy = node.y - cy
            if dx * dx + dy * dy <= r2:
                cluster.append(node)
                added = True
                break
        if not added:
            clusters.append([node])
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
        cx = (tri[0][0] + tri[1][0] + tri[2][0]) / 3.0
        cy = (tri[0][1] + tri[1][1] + tri[2][1]) / 3.0
        cz = (tri[0][2] + tri[1][2] + tri[2][2]) / 3.0
        points_xyz.append((cx, cy, cz))

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

def generate_support_interfaces(mask_islands: Sequence[Island2D],
                                z_heights: Sequence[float],
                                settings: SliceSettings,
                                top_z: float) -> List[SupportInterfaceLayer]:
    if not mask_islands or settings.interface_layers <= 0:
        return []
    interface_layers = max(0, settings.interface_layers)
    threshold = top_z - interface_layers * settings.layer_height
    layers: List[SupportInterfaceLayer] = []
    for index, z in enumerate(z_heights):
        if z < threshold or z > top_z:
            continue
        lines = infill.rectilinear_infill(list(mask_islands),
                                          density=settings.interface_density,
                                          angle_deg=settings.infill_angle,
                                          layer_index=index,
                                          extrusion_width=settings.extrusion_width,
                                          alternate=True)
        if lines:
            layers.append(SupportInterfaceLayer(z=float(z), lines=lines))
    return layers

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
        cx = (tri[0][0] + tri[1][0] + tri[2][0]) / 3.0
        cy = (tri[0][1] + tri[1][1] + tri[2][1]) / 3.0
        cz = (tri[0][2] + tri[1][2] + tri[2][2]) / 3.0
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

def generate_support_plan(mesh: MeshModel,
                          z_heights: Sequence[float],
                          settings: SliceSettings) -> SupportPlan:
    mask_islands = overhang_mask(mesh, settings.overhang_angle)
    if settings.support_xy_gap > 0.0 and mask_islands:
        mask_islands = offset_islands(mask_islands, -settings.support_xy_gap)

    columns: List[SupportColumn] = []
    tree_branches: List[TreeSupportBranch] = []
    if settings.support_style in ("tree", "trees"):
        tree_branches = generate_tree_supports(mesh, settings)
    else:
        columns = generate_support_columns(mesh, settings)

    top_z = max((column.z_top for column in columns), default=0.0)
    interface_layers = generate_support_interfaces(mask_islands,
                                                   z_heights,
                                                   settings,
                                                   top_z)
    return SupportPlan(mask_islands=mask_islands,
                       columns=columns,
                       interface_layers=interface_layers,
                       tree_branches=tree_branches)
