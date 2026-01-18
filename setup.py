#!/usr/bin/env python
"""
Setup script for EON-OpenSlicer.
This is primarily for development and compatibility purposes.
Production builds should use Briefcase via pyproject.toml.
"""
from setuptools import setup, find_packages

with open("App/requirements.txt") as f:
    desktop_requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

# Mobile requirements (Toga)
mobile_requirements = [
    "toga>=0.4.0",
    "briefcase>=0.3.0",
]

setup(
    name="EON-OpenSlicer",
    version="1.0.0",
    description="A centralized 3D printing lab management system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="EON-OpenSlicer Team",
    author_email="koskima@mail.uc.edu",
    url="https://github.com/Electrovian/Project-EON-OpenSlicer",
    packages=["App"] + ["App." + pkg for pkg in find_packages("App")],
    package_dir={"App": "App"},
    install_requires=[
        "requests>=2.31",
        "numpy>=1.24",
    ],
    extras_require={
        "desktop": desktop_requirements,
        "mobile": mobile_requirements,
        "dev": desktop_requirements + mobile_requirements + [
            "pytest>=7.0",
            "pyinstaller>=5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "eon-openslicer=__main__:main",
        ],
    },
    python_requires=">=3.12",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Manufacturing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Graphics :: 3D Modeling",
    ],
)
