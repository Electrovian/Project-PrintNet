DEFAULTS = {
    "app": {
        "title": "EON-OpenSlicer",
        "language": "en",
        "size": (1280, 720),
        "status_ready": "Ready",
    },
    "viewer": {
        "default_view": {"distance": 300.0, "elevation": 30.0, "azimuth": 45.0},
        "grid_size": (250, 200, 0),
        "grid_spacing": (10, 10, 1),
        "snap_enabled": False,
        "snap_step": 1.0,
    },
    "printer": {
        "name": "MakerGear M3-SE",
        "bed_size": (250, 200),
        "max_height": 200,
        "nozzle_clearance": 10,
    },
    "ui": {
        "topbar_margins": (8, 4, 8, 4),
        "topbar_spacing": 6,
        "action_panel_margins": (10, 8, 10, 8),
        "action_panel_spacing": 6,
        "action_panel_margin": 16,
    },
    "settings_panel": {
        "layer_height": {"min": 0.05, "max": 1.0, "step": 0.05, "default": 0.2},
        "infill": {"min": 0, "max": 100, "default": 15},
        "speed": {"min": 10, "max": 200, "default": 60.0},
    },
    "performance": {
        "max_threads": None,
        "max_slice_cache_mb": None,
    },
    "popups": {
        "min_width": 420,
        "arrange_min_width": 340,
        "spin_width": 86,
        "move": {"min": -9999.0, "max": 9999.0, "step": 0.5, "decimals": 2},
        "rotate": {"min": -360.0, "max": 360.0, "step": 1.0, "decimals": 2},
        "scale": {"min": 1.0, "max": 500.0, "default": 100.0, "step": 1.0, "decimals": 2},
        "size": {"min": 0.0, "max": 99999.0, "step": 1.0, "decimals": 2},
        "arrange": {
            "spacing_min": 0,
            "spacing_max": 20,
            "spacing_default": 0,
            "auto_spacing": 5.0,
            "spacing_base": 3.0,
        },
    },
}
