import os
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHART_DIR = ROOT / "deploy" / "helm" / "printnet"
TEMPLATES_DIR = CHART_DIR / "templates"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class KubernetesPackagingTests(unittest.TestCase):
    def test_chart_scaffold_exists(self):
        required = [
            CHART_DIR / "Chart.yaml",
            CHART_DIR / "values.yaml",
            CHART_DIR / "values-k3d.yaml",
            TEMPLATES_DIR / "_helpers.tpl",
            TEMPLATES_DIR / "backend-deployment.yaml",
            TEMPLATES_DIR / "frontend-deployment.yaml",
            TEMPLATES_DIR / "worker-deployment.yaml",
            TEMPLATES_DIR / "ingress.yaml",
        ]
        for path in required:
            with self.subTest(path=str(path)):
                self.assertTrue(path.exists(), msg=f"missing required chart artifact: {path}")

    def test_chart_metadata_and_values_contract(self):
        chart_text = _read(CHART_DIR / "Chart.yaml")
        self.assertIn("apiVersion: v2", chart_text)
        self.assertIn("name: printnet", chart_text)

        values_text = _read(CHART_DIR / "values.yaml")
        required_keys = [
            "backend:",
            "worker:",
            "frontend:",
            "redis:",
            "mongo:",
            "ingress:",
            "queueWorkerMaxJobsPerTick:",
            "queueWorkerHeartbeatTtlSeconds:",
        ]
        for key in required_keys:
            with self.subTest(key=key):
                self.assertIn(key, values_text)

    def test_template_kinds_cover_core_stack(self):
        expected_kind_by_file = {
            "namespace.yaml": "kind: Namespace",
            "backend-configmap.yaml": "kind: ConfigMap",
            "backend-secret.yaml": "kind: Secret",
            "backend-deployment.yaml": "kind: Deployment",
            "backend-service.yaml": "kind: Service",
            "worker-deployment.yaml": "kind: Deployment",
            "frontend-deployment.yaml": "kind: Deployment",
            "frontend-service.yaml": "kind: Service",
            "redis-deployment.yaml": "kind: Deployment",
            "redis-service.yaml": "kind: Service",
            "mongo-statefulset.yaml": "kind: StatefulSet",
            "mongo-service.yaml": "kind: Service",
            "ingress.yaml": "kind: Ingress",
        }
        for file_name, kind_marker in expected_kind_by_file.items():
            path = TEMPLATES_DIR / file_name
            text = _read(path)
            with self.subTest(file=file_name):
                self.assertIn(kind_marker, text)

    def test_k3d_script_and_smoke_scripts_exist(self):
        scripts = [
            ROOT / "scripts" / "k3d-deploy.ps1",
            ROOT / "scripts" / "run-kubernetes-packaging-smoke.ps1",
            ROOT / "scripts" / "test-kubernetes-packaging-unit.ps1",
            ROOT / "scripts" / "test-kubernetes-packaging-integration.ps1",
        ]
        for path in scripts:
            with self.subTest(path=str(path)):
                self.assertTrue(path.exists(), msg=f"missing script: {path}")

        k3d_text = _read(ROOT / "scripts" / "k3d-deploy.ps1")
        self.assertIn("k3d", k3d_text.lower())
        self.assertIn("helm upgrade --install", k3d_text)


if __name__ == "__main__":
    unittest.main()
