"""Slicing engine package.

This prototype implements a very small demo slicer. The architecture is
laid out so you can extend it into a real multi-layer engine later.

Modules:
- mesh: STL loading and mesh wrapper.
- geometry: geometric utilities (currently minimal).
- slicer: high-level slice function.
- infill, support, path_planner: hooks for expansion.
- gcode: G-code writer / time estimator.
"""
