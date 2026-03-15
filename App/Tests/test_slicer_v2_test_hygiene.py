import ast
import os
from pathlib import Path
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

TESTS_DIR = Path(__file__).resolve().parent


def _iter_v2_test_files() -> list[Path]:
    files = sorted(TESTS_DIR.glob("test_slicer_v2_*.py"))
    return [path for path in files if path.name != Path(__file__).name]


def _parse(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8-sig"))


def _decorator_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        root = _decorator_name(node.value)
        return f"{root}.{node.attr}" if root else node.attr
    if isinstance(node, ast.Call):
        return _decorator_name(node.func)
    return ""


def _iter_test_functions(tree: ast.Module):
    for class_node in tree.body:
        if not isinstance(class_node, ast.ClassDef):
            continue
        for fn in class_node.body:
            if isinstance(fn, ast.FunctionDef) and fn.name.startswith("test_"):
                yield class_node, fn


def _count_asserts(fn: ast.FunctionDef) -> int:
    count = 0
    for node in ast.walk(fn):
        if isinstance(node, ast.Assert):
            count += 1
            continue
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if (
                isinstance(node.func.value, ast.Name)
                and node.func.value.id == "self"
                and node.func.attr.startswith("assert")
            ):
                count += 1
    return count


class TestSlicerV2TestHygiene(unittest.TestCase):
    def test_no_skip_or_xfail_decorators(self) -> None:
        banned = {
            "unittest.expectedFailure",
            "unittest.skip",
            "unittest.skipIf",
            "unittest.skipUnless",
            "pytest.mark.skip",
            "pytest.mark.skipif",
            "pytest.mark.xfail",
        }
        violations: list[str] = []
        for path in _iter_v2_test_files():
            tree = _parse(path)
            for class_node, fn in _iter_test_functions(tree):
                for decorator in fn.decorator_list:
                    name = _decorator_name(decorator)
                    if name in banned:
                        violations.append(
                            f"{path.name}:{fn.lineno} {class_node.name}.{fn.name} uses @{name}"
                        )
        self.assertEqual(violations, [])

    def test_each_test_method_has_assertion(self) -> None:
        violations: list[str] = []
        for path in _iter_v2_test_files():
            tree = _parse(path)
            for class_node, fn in _iter_test_functions(tree):
                if _count_asserts(fn) == 0:
                    violations.append(f"{path.name}:{fn.lineno} {class_node.name}.{fn.name}")
        self.assertEqual(violations, [])

    def test_no_bare_except_in_test_methods(self) -> None:
        violations: list[str] = []
        for path in _iter_v2_test_files():
            tree = _parse(path)
            for class_node, fn in _iter_test_functions(tree):
                for node in ast.walk(fn):
                    if isinstance(node, ast.ExceptHandler) and node.type is None:
                        violations.append(
                            f"{path.name}:{node.lineno} {class_node.name}.{fn.name} uses bare except"
                        )
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
