# Project-PrintNet Architecture Analysis

## Overview
This document provides a comprehensive architectural analysis of the OpenSlicer application, mapping out the core logic flow, component interactions, and design patterns used throughout the codebase.

## System Architecture Diagram

```mermaid
flowchart TB
    subgraph "Application Entry Point"
        A[main.py] --> B[QApplication]
        A --> C[SplashScreen]
        A --> D[ActivityLogger]
        A --> E[CrashReporter]
    end
    
    subgraph "Configuration Layer"
        F[printer_config.py]
        G[defaults.py]
        H[performance.py]
        I[printers_catalog.py]
        F --> J[Load Printer Config]
        F --> K[Airtable Config]
    end
    
    subgraph "Main Window & UI"
        L[MainWindow]
        M[MainController]
        N[PrepareView]
        O[PreviewView]
        P[DeviceView]
        Q[ControlView]
        R[FilesView]
        S[ActivityView]
        T[SharedView]
        
        L --> M
        M --> N
        M --> O
        M --> P
        M --> Q
        M --> R
        M --> S
        M --> T
    end
    
    subgraph "3D Viewer & Model Management"
        U[viewer_3d.py]
        V[MeshModel]
        W[Trimesh]
        AA[model_panel.py]
        AB[arrange_utils.py]
        AC[auto_orient.py]
        
        U --> V
        V --> W
        U --> AA
        U --> AB
        U --> AC
    end
    
    subgraph "Settings & Configuration"
        AD[settings_panel/]
        AE[SliceSettings]
        AF[FirmwareProfile]
        
        AD --> AE
        AE --> AF
    end
    
    subgraph "Worker Thread Management"
        AG[workers.py]
        AH[QThreadPool]
        AI[WorkerSignals]
        
        AG --> AH
        AG --> AI
    end
    
    A --> F
    A --> L
    L --> U
    M --> AG
    M --> AD
    
    subgraph "Slicer Core - Entry Points"
        BA[slicer/emit.py]
        BB[slice_file]
        BC[slice_mesh_model]
        BD[slice_trimesh]
        
        BA --> BB
        BA --> BC
        BA --> BD
    end
    
    subgraph "Slicer Planning"
        BE[slicer/plan.py]
        BF[PrintPlan]
        BG[LayerPlan]
        BH[LayerPerimeters]
        BI[LayerInfill]
        BJ[build_z_heights]
        BK[generate_layer_perimeters]
        BL[generate_layer_plans]
        
        BE --> BF
        BF --> BG
        BG --> BH
        BG --> BI
        BE --> BJ
        BE --> BK
        BE --> BL
    end
    
    subgraph "Support Structures"
        BM[slicer/raft.py]
        BN[slicer/supports.py]
        BO[RaftLayer]
        BP[BrimPlan]
        BQ[SkirtPlan]
        BR[BridgeInfill]
        BS[IroningPass]
        BT[support.py]
        BU[SupportPlan]
        BV[SupportColumn]
        BW[TreeSupportBranch]
        
        BM --> BO
        BM --> BP
        BM --> BQ
        BN --> BR
        BN --> BS
        BT --> BU
        BU --> BV
        BU --> BW
    end
    
    subgraph "Geometry Operations"
        CA[slicer/geometry.py]
        CB[Polygon2D]
        CC[Island2D]
        CD[LineSegment2D]
        CE[pyclipper]
        CF[offset_islands]
        CG[clip_lines_to_island]
        CH[gap_fill_lines]
        CI[thin_wall_lines]
        
        CA --> CB
        CA --> CC
        CA --> CD
        CA --> CE
        CA --> CF
        CA --> CG
        CA --> CH
        CA --> CI
    end
    
    subgraph "Infill Generation"
        CJ[slicer/infill.py]
        CK[rectilinear_infill]
        CL[grid_infill]
        CM[triangle_infill]
        CN[honeycomb_infill]
        
        CJ --> CK
        CJ --> CL
        CJ --> CM
        CJ --> CN
    end
    
    subgraph "Path Planning"
        CO[slicer/path_planner.py]
        CP[Toolpath]
        CQ[ArcFit]
        CR[BridgeRegion]
        CS[apply_seam_placement]
        CT[fit_arc]
        CU[detect_bridges]
        CV[optimize_travel]
        
        CO --> CP
        CO --> CQ
        CO --> CR
        CO --> CS
        CO --> CT
        CO --> CU
        CO --> CV
    end
    
    subgraph "G-Code Generation"
        DA[gcode/writer.py]
        DB[GCodeWriter]
        DC[gcode/preview.py]
        DD[parse_gcode_preview_file]
        DE[gcode/stats.py]
        DF[estimate_gcode_file]
        
        DA --> DB
        DC --> DD
        DE --> DF
    end
    
    M --> BD
    BD --> BL
    BL --> BF
    BF --> BM
    BF --> BN
    BF --> BT
    BL --> CA
    BL --> CJ
    BL --> CO
    BF --> DA
    DB --> DC
    DB --> DE
    
    subgraph "Mesh Operations"
        EA[slicer/mesh.py]
        EB[MeshModel]
        EC[slice_at_z]
        ED[overhang_triangles]
        EE[bbox]
        
        EA --> EB
        EB --> EC
        EB --> ED
        EB --> EE
    end
    
    BD --> EA
    BL --> EA
    
    subgraph "Integration Layer"
        FA[integrations/printer_manager.py]
        FB[PrinterManager]
        FC[OctoPrint Integration]
        FD[Airtable Integration]
        
        FA --> FB
        FB --> FC
        FB --> FD
    end
    
    M --> FA
    
    subgraph "GUI Utilities"
        GA[gui/popups/]
        GB[gui/widgets/]
        GC[preview_utils.py]
        GD[selection_utils.py]
        GE[theme.py]
        GF[shortcuts.py]
        
        M --> GA
        M --> GB
        M --> GC
        M --> GD
        M --> GE
        M --> GF
    end
    
    style A fill:#ff6b6b
    style L fill:#4ecdc4
    style BA fill:#ffe66d
    style BE fill:#ffe66d
    style DA fill:#95e1d3
    style U fill:#4ecdc4
    style M fill:#4ecdc4
```

## Component Interaction Flow

```mermaid
sequenceDiagram
    participant User
    participant MainWindow
    participant MainController
    participant Viewer3D
    participant Worker
    participant SlicerEmit
    participant LayerPlan
    participant Geometry
    participant Infill
    participant PathPlanner
    participant GCodeWriter
    participant PreviewView
    
    User->>MainWindow: Load STL File
    MainWindow->>Viewer3D: load_model()
    Viewer3D->>Viewer3D: Create MeshModel
    Viewer3D-->>MainWindow: Model Loaded
    
    User->>MainWindow: Adjust Settings
    MainWindow->>MainController: Update SliceSettings
    
    User->>MainWindow: Click Slice
    MainController->>Worker: Create Worker Thread
    Worker->>SlicerEmit: slice_trimesh()
    
    SlicerEmit->>LayerPlan: generate_layer_plans()
    LayerPlan->>Geometry: slice_at_z()
    Geometry-->>LayerPlan: 2D Polygons
    
    LayerPlan->>Geometry: offset_islands()
    LayerPlan->>Geometry: gap_fill_lines()
    LayerPlan->>Geometry: thin_wall_lines()
    
    LayerPlan->>Infill: generate_infill()
    Infill->>Geometry: clip_lines_to_island()
    Infill-->>LayerPlan: Infill Lines
    
    LayerPlan->>PathPlanner: optimize_travel()
    PathPlanner->>PathPlanner: detect_bridges()
    PathPlanner->>PathPlanner: apply_seam_placement()
    PathPlanner->>PathPlanner: fit_arc()
    PathPlanner-->>LayerPlan: Optimized Paths
    
    LayerPlan-->>SlicerEmit: PrintPlan
    
    SlicerEmit->>GCodeWriter: write_header()
    SlicerEmit->>GCodeWriter: write_layer()
    GCodeWriter->>GCodeWriter: perimeter_loop()
    GCodeWriter->>GCodeWriter: infill_lines()
    GCodeWriter->>GCodeWriter: retract()
    GCodeWriter->>GCodeWriter: travel()
    SlicerEmit->>GCodeWriter: write_footer()
    GCodeWriter-->>SlicerEmit: G-Code File Path
    
    SlicerEmit-->>Worker: Success
    Worker-->>MainController: Slice Complete
    MainController->>PreviewView: Load G-Code Preview
    PreviewView->>PreviewView: parse_gcode_preview_file()
    PreviewView-->>MainWindow: Preview Ready
    MainWindow-->>User: Display Preview
```

## Data Flow Architecture

```mermaid
flowchart LR
    subgraph "Input Data"
        A[STL File]
        B[User Settings]
        C[Printer Config]
    end
    
    subgraph "Model Representation"
        D[Trimesh Object]
        E[MeshModel Wrapper]
        F[Vertex Data]
        G[Face Data]
    end
    
    subgraph "2D Slicing"
        H[Z-Height Layers]
        I[Raw Polygons]
        J[Islands with Holes]
        K[Perimeter Shells]
    end
    
    subgraph "Feature Generation"
        L[Perimeter Paths]
        M[Infill Lines]
        N[Support Structures]
        O[Raft/Brim/Skirt]
        P[Thin Walls]
        Q[Gap Fill]
        R[Bridge Detection]
        S[Ironing Paths]
    end
    
    subgraph "Path Optimization"
        T[Travel Optimization]
        U[Seam Placement]
        V[Arc Fitting]
        W[Combing]
        X[Retraction Planning]
    end
    
    subgraph "G-Code Output"
        Y[Movement Commands]
        Z[Extrusion Commands]
        AA[Temperature Control]
        AB[Fan Control]
        AC[Final G-Code File]
    end
    
    A --> D
    D --> E
    E --> F
    E --> G
    B --> H
    C --> H
    F --> H
    G --> H
    H --> I
    I --> J
    J --> K
    
    K --> L
    K --> M
    K --> N
    K --> O
    K --> P
    K --> Q
    K --> R
    K --> S
    
    L --> T
    M --> T
    N --> T
    O --> T
    
    T --> U
    U --> V
    V --> W
    W --> X
    
    X --> Y
    X --> Z
    B --> AA
    B --> AB
    Y --> AC
    Z --> AC
    AA --> AC
    AB --> AC
```

## Key Design Patterns

### 1. **Model-View-Controller (MVC) Pattern**
- **Model**: `MeshModel`, `SliceSettings`, configuration data
- **View**: All GUI components (`MainWindow`, `PrepareView`, `PreviewView`, etc.)
- **Controller**: `MainController` orchestrates interactions between views and models

### 2. **Worker Thread Pattern**
- Uses `QThreadPool` and `QRunnable` for background processing
- `Worker` class encapsulates long-running operations (slicing, file loading)
- `WorkerSignals` provide thread-safe communication back to the main thread

### 3. **Dataclass Configuration Pattern**
- `SliceSettings`, `PrintPlan`, `LayerPlan`, etc. use Python dataclasses
- Immutable configuration objects passed through the pipeline
- Type-safe settings management

### 4. **Pipeline/Chain Pattern**
- Slicing follows a clear pipeline: Mesh → Layers → Perimeters → Infill → Paths → G-Code
- Each stage transforms data and passes to the next
- Pure functions enable easy testing and debugging

### 5. **Strategy Pattern**
- Multiple infill patterns (rectilinear, grid, triangle, honeycomb)
- Different firmware profiles (Marlin, Klipper)
- Configurable seam placement strategies
- Support structure strategies (pillar vs. tree)

### 6. **Builder Pattern**
- `GCodeWriter` builds G-Code incrementally
- `PrintPlan` constructed through multiple builder functions
- Layered construction of complex objects

### 7. **Adapter Pattern**
- `MeshModel` wraps `trimesh.Trimesh` with slicer-specific functionality
- `pyclipper` integration through geometry utility functions
- OctoPrint and Airtable adapters for external service integration

## Core Processing Flow

### Stage 1: Initialization
1. Application starts with `main.py`
2. Configuration loaded from Excel/defaults
3. Main window and views initialized
4. 3D viewer ready for model loading

### Stage 2: Model Loading
1. User loads STL file (drag-drop or file dialog)
2. `Trimesh` parses STL into vertices and faces
3. `MeshModel` wrapper provides slicing utilities
4. Model displayed in `Viewer3D` with OpenGL

### Stage 3: Pre-Slice Configuration
1. User adjusts settings in `settings_panel`
2. Settings compiled into `SliceSettings` dataclass
3. Printer configuration loaded
4. Validation of settings performed

### Stage 4: Slicing (Worker Thread)
1. **Z-Height Generation**: `build_z_heights()` creates layer heights
2. **Layer Slicing**: `slice_at_z()` intersects mesh with Z-planes
3. **Perimeter Generation**: 
   - `generate_layer_perimeters()` creates shells
   - Offset operations for multiple perimeters
   - Hole compensation applied
4. **Infill Generation**:
   - Pattern generator creates fill lines
   - Lines clipped to interior regions
   - Density and angle applied
5. **Support Generation**:
   - Overhang detection
   - Tree or pillar support creation
   - Interface layers generated
6. **Special Features**:
   - Thin wall detection
   - Gap fill computation
   - Bridge detection
   - Ironing path generation
7. **Path Planning**:
   - Travel path optimization
   - Seam placement
   - Arc fitting
   - Combing within boundaries

### Stage 5: G-Code Generation
1. `GCodeWriter` initialized with settings
2. Header written (start G-Code, temperatures)
3. For each layer:
   - Write raft/brim/skirt (if applicable)
   - Write perimeters (outer → inner or inner → outer)
   - Write infill
   - Write support structures
   - Handle retractions and travels
4. Footer written (end G-Code, cooldown)
5. File saved to disk

### Stage 6: Preview & Output
1. G-Code parsed for preview
2. Path visualization in 3D viewer
3. Statistics computed (time, material)
4. User can send to printer or save

## Key File Responsibilities

| File/Module | Responsibility |
|------------|---------------|
| `main.py` | Application entry point, initialization |
| `gui/main_window.py` | Main application window container |
| `gui/Windows/controller/*.py` | Business logic orchestration |
| `gui/viewer_3d.py` | 3D model visualization with OpenGL |
| `gui/settings_panel/` | User interface for slice settings |
| `slicer/slicer/emit.py` | Main slicing entry point |
| `slicer/slicer/plan.py` | Layer planning and perimeter generation |
| `slicer/geometry.py` | 2D geometric operations (clipper wrapper) |
| `slicer/infill.py` | Infill pattern generation |
| `slicer/support.py` | Support structure generation |
| `slicer/path_planner.py` | Path optimization and planning |
| `slicer/gcode/writer.py` | G-Code file generation |
| `slicer/mesh.py` | 3D mesh operations and slicing |
| `config/printer_config.py` | Printer configuration loading |
| `integrations/printer_manager.py` | External printer communication |

## Geometry Processing Pipeline

```mermaid
flowchart TD
    A[3D Mesh] --> B[Slice at Z-Heights]
    B --> C[Raw 2D Polygons]
    C --> D[Union Overlapping Polygons]
    D --> E[Identify Islands with Holes]
    E --> F[Apply Hole Compensation]
    F --> G[Offset for Perimeters]
    G --> H[Shell Generation Loop]
    H --> I{More Shells?}
    I -->|Yes| G
    I -->|No| J[Inner Region Extraction]
    J --> K[Thin Wall Detection]
    J --> L[Gap Fill Detection]
    J --> M[Infill Region]
    M --> N[Generate Infill Lines]
    N --> O[Clip to Region]
    O --> P[Final Paths]
    K --> P
    L --> P
```

## Settings Hierarchy

```mermaid
flowchart TD
    A[User Input] --> B[settings_panel UI]
    B --> C[SliceSettings Dataclass]
    D[Printer Config] --> C
    E[defaults.py] --> C
    F[FirmwareProfile] --> C
    
    C --> G[Layer Settings]
    C --> H[Perimeter Settings]
    C --> I[Infill Settings]
    C --> J[Support Settings]
    C --> K[Speed Settings]
    C --> L[Material Settings]
    C --> M[Advanced Settings]
    
    G --> N[layer_height, first_layer_height, etc.]
    H --> O[wall_count, line_width, seam_position, etc.]
    I --> P[infill_percent, pattern, angle, etc.]
    J --> Q[support_type, density, interface, etc.]
    K --> R[print_speed, travel_speed, bridge_speed, etc.]
    L --> S[nozzle_diameter, filament_density, temperature, etc.]
    M --> T[arc_fitting, combing, retraction, etc.]
```

## Summary of Architectural Strengths

1. **Clear Separation of Concerns**: GUI, slicing logic, and configuration are well separated
2. **Extensibility**: Strategy patterns make it easy to add new infill patterns, support types, etc.
3. **Type Safety**: Extensive use of dataclasses and type hints
4. **Testability**: Pure functions and clear interfaces enable unit testing
5. **Performance**: Worker threads prevent UI blocking during long operations
6. **Modularity**: Each module has a single, clear responsibility

## Areas for Potential Optimization

1. **Geometry Operations**: Heavy use of pyclipper could be optimized with caching
2. **Path Planning**: Travel optimization could use more sophisticated algorithms (TSP solvers)
3. **Memory Usage**: Large meshes could benefit from streaming/chunking
4. **Preview Generation**: Incremental preview updates during slicing
5. **Settings Validation**: More comprehensive validation before slicing starts
