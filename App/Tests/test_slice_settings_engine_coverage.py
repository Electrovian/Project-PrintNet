import ast
import os
import sys
from pathlib import Path


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def _parse_py(path: Path) -> ast.AST:
    text = path.read_text(encoding="utf-8-sig", errors="ignore")
    return ast.parse(text)


def _slice_settings_fields(tree: ast.AST) -> list[str]:
    for node in getattr(tree, "body", []):
        if not isinstance(node, ast.ClassDef) or node.name != "SliceSettings":
            continue
        fields: list[str] = []
        for stmt in node.body:
            if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
                fields.append(stmt.target.id)
        return fields
    return []


def test_slice_settings_fields_are_handled_by_engine():
    project_root = Path(ROOT)
    slicer_root = project_root / "slicer_v2"
    writer_path = slicer_root / "legacy_gcode_writer.py"

    writer_tree = _parse_py(writer_path)
    fields = _slice_settings_fields(writer_tree)
    assert fields, "SliceSettings dataclass fields not found."

    handled: set[str] = set()

    # 1) Settings consumed by engine modules via `settings.<field>` or `self.settings.<field>`.
    for path in slicer_root.rglob("*.py"):
        tree = _parse_py(path)

        class _EngineRefVisitor(ast.NodeVisitor):
            def visit_Attribute(self, node):
                if isinstance(node.ctx, ast.Load):
                    if isinstance(node.value, ast.Name) and node.value.id == "settings":
                        handled.add(node.attr)
                    if (
                        isinstance(node.value, ast.Attribute)
                        and node.value.attr == "settings"
                        and isinstance(node.value.value, ast.Name)
                        and node.value.value.id == "self"
                    ):
                        handled.add(node.attr)
                self.generic_visit(node)

        _EngineRefVisitor().visit(tree)

    # 2) Fields normalized or transformed in SliceSettings itself via `self.<field>`.
    for node in getattr(writer_tree, "body", []):
        if not isinstance(node, ast.ClassDef) or node.name != "SliceSettings":
            continue

        class _SelfRefVisitor(ast.NodeVisitor):
            def visit_Attribute(self, node):
                if (
                    isinstance(node.ctx, ast.Load)
                    and isinstance(node.value, ast.Name)
                    and node.value.id == "self"
                    and node.attr in fields
                ):
                    handled.add(node.attr)
                self.generic_visit(node)

        _SelfRefVisitor().visit(node)
        break

    uncovered = sorted(field for field in fields if field not in handled)
    assert not uncovered, f"Uncovered SliceSettings fields: {uncovered}"
