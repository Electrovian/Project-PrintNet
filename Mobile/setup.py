from pathlib import Path

from setuptools import find_packages, setup


def _read_requirements(path: Path) -> list[str]:
    if not path.exists():
        return []
    lines = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        lines.append(line)
    return lines


BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent
APP_ROOT = REPO_ROOT / "App"


setup(
    name="eon-openslicer",
    version="0.1.0",
    description="EON-OpenSlicer desktop and mobile entry points",
    package_dir={"": str(REPO_ROOT)},
    packages=find_packages(where=str(REPO_ROOT), include=["App", "App.*"]),
    include_package_data=True,
    install_requires=_read_requirements(APP_ROOT / "requirements.txt"),
    extras_require={
        "mobile": _read_requirements(BASE_DIR / "requirements-mobile.txt"),
    },
    entry_points={
        "console_scripts": [
            "eon-openslicer=App.__main__:main",
        ]
    },
)
