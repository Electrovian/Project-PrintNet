from __future__ import annotations


class SlicerV2Error(ValueError):
    """Base slicer_v2 error class."""


class SlicerV2ValidationError(SlicerV2Error):
    """Raised when pre/post pipeline validation fails."""


class SlicerV2StageError(SlicerV2Error):
    """Raised when a slicer_v2 stage fails."""


class SlicerV2CancelledError(SlicerV2Error):
    """Raised when slicer_v2 execution is cancelled."""


class SlicerV2SettingsNormalizationError(SlicerV2Error):
    """Raised when slicer_v2 settings normalization fails."""


class SlicerV2GeometryError(SlicerV2Error):
    """Raised when slicer_v2 geometry primitives/utility validation fails."""


class SlicerV2PolygonPipelineError(SlicerV2Error):
    """Raised when slicer_v2 polygon offset/cleanup pipeline fails."""


class SlicerV2MeshSlicingError(SlicerV2Error):
    """Raised when slicer_v2 mesh slicing/contour assembly fails."""


class SlicerV2AdaptiveLayerError(SlicerV2Error):
    """Raised when slicer_v2 adaptive layer planning fails."""


class SlicerV2IslandGraphError(SlicerV2Error):
    """Raised when slicer_v2 island graph/adjacency modeling fails."""


class SlicerV2PerimeterClassicError(SlicerV2Error):
    """Raised when slicer_v2 classic perimeter planning fails."""


class SlicerV2PerimeterVariableError(SlicerV2Error):
    """Raised when slicer_v2 variable-width perimeter planning fails."""


class SlicerV2InfillPatternError(SlicerV2Error):
    """Raised when slicer_v2 infill pattern planning fails."""


class SlicerV2SolidBridgeError(SlicerV2Error):
    """Raised when slicer_v2 solid-layer and bridge planning fails."""


class SlicerV2SupportPlanningError(SlicerV2Error):
    """Raised when slicer_v2 support planning fails."""


class SlicerV2TravelPlanningError(SlicerV2Error):
    """Raised when slicer_v2 travel planning/combing fails."""


class SlicerV2ExtrusionFlowError(SlicerV2Error):
    """Raised when slicer_v2 extrusion volume/flow modeling fails."""


class SlicerV2GCodeEmissionError(SlicerV2Error):
    """Raised when slicer_v2 G-code semantic emission fails."""


class SlicerV2GCodeValidationError(SlicerV2Error):
    """Raised when slicer_v2 G-code validation/sanity checks fail."""
