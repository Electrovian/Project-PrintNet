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


setup(
    name="eon-openslicer",
    version="0.1.0",
    description="EON-OpenSlicer desktop and mobile entry points",
    packages=find_packages(),
    include_package_data=True,
    install_requires=_read_requirements(Path("App/requirements.txt")),
    extras_require={
        "mobile": _read_requirements(Path("Mobile/requirements-mobile.txt")),
    },
    entry_points={
        "console_scripts": [
            "eon-openslicer=App.__main__:main",
        ]
    },
)
