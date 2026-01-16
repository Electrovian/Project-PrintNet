from __future__ import annotations

from typing import Any, TYPE_CHECKING

from PyQt5 import QtCore, QtGui, QtWidgets


class StrengthSectionMixin:
    if TYPE_CHECKING:
        def __getattr__(self, name: str) -> Any: ...

    def _build_strength_page(self):
        layout = self._build_page("strength")

        section, section_layout = self._section("Walls")
        self.wall_loops_spin = self._make_int_spin(self._defaults.perimeter_count, 1, 10)
        self._add_row("strength", section, section_layout, "Wall loops", self.wall_loops_spin,
                      "Number of perimeter walls.")
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Top/bottom shells")
        self.top_shell_layers_spin = self._make_int_spin(self._defaults.top_layers, 0, 20, suffix="layers")
        self._add_row("strength", section, section_layout, "Top shell layers", self.top_shell_layers_spin,
                      "Number of top layers.")
        self.bottom_shell_layers_spin = self._make_int_spin(self._defaults.bottom_layers, 0, 20, suffix="layers")
        self._add_row("strength", section, section_layout, "Bottom shell layers", self.bottom_shell_layers_spin,
                      "Number of bottom layers.")
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Infill")
        self.infill_density_spin = self._make_int_spin(int(self._defaults.infill_percent), 0, 100, suffix="%")
        self._add_row("strength", section, section_layout, "Sparse infill density", self.infill_density_spin,
                      "Density of sparse infill.")
        self.infill_pattern_combo = self._make_combo(
            [
                ("Grid", "grid"),
                ("Rectilinear", "rectilinear"),
                ("Triangle", "triangle"),
            ]
        )
        self._set_combo_value(self.infill_pattern_combo, self._defaults.infill_pattern)
        self._add_row("strength", section, section_layout, "Sparse infill pattern", self.infill_pattern_combo,
                      "Infill pattern for non-solid regions.")
        layout.insertWidget(layout.count() - 1, section)

