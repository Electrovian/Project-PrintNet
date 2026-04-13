from __future__ import annotations

from PyQt5 import QtCore, QtTest, QtWidgets


def snapshot_top_level_widgets(app: QtWidgets.QApplication | None = None) -> set[int]:
    resolved_app = app or QtWidgets.QApplication.instance()
    if resolved_app is None:
        return set()
    return {id(widget) for widget in resolved_app.topLevelWidgets() if widget is not None}


def drain_qt_events(
    app: QtWidgets.QApplication | None,
    *,
    wait_ms: int = 0,
    passes: int = 2,
) -> None:
    if app is None:
        return
    total_passes = max(1, int(passes))
    delay_ms = max(0, int(wait_ms))
    for index in range(total_passes):
        app.processEvents()
        QtCore.QCoreApplication.sendPostedEvents(None, QtCore.QEvent.DeferredDelete)
        app.processEvents()
        if delay_ms > 0 and index == 0:
            QtTest.QTest.qWait(delay_ms)
    app.processEvents()
    QtCore.QCoreApplication.sendPostedEvents(None, QtCore.QEvent.DeferredDelete)
    app.processEvents()


def dispose_created_top_levels(
    app: QtWidgets.QApplication | None,
    baseline_widget_ids: set[int] | None,
    *objects: object,
    wait_ms: int = 40,
) -> None:
    resolved_app = app or QtWidgets.QApplication.instance()
    candidates: list[object] = []
    seen_ids: set[int] = set()

    def _add(obj: object | None) -> None:
        if obj is None:
            return
        obj_id = id(obj)
        if obj_id in seen_ids:
            return
        seen_ids.add(obj_id)
        candidates.append(obj)

    for obj in objects:
        _add(obj)

    baseline_ids = set(baseline_widget_ids or ())
    if resolved_app is not None:
        for widget in resolved_app.topLevelWidgets():
            if widget is not None and id(widget) not in baseline_ids:
                _add(widget)

    for obj in candidates:
        hide = getattr(obj, "hide", None)
        if callable(hide):
            try:
                hide()
            except Exception:
                pass
        close = getattr(obj, "close", None)
        if callable(close):
            try:
                close()
            except Exception:
                pass

    for obj in candidates:
        delete_later = getattr(obj, "deleteLater", None)
        if callable(delete_later):
            try:
                delete_later()
            except Exception:
                pass

    drain_qt_events(resolved_app, wait_ms=wait_ms, passes=3)
