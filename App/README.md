# OpenSlicer (Prototype)

OpenSlicer is a **prototype** open‑source 3D printing slicer and print manager.

This version is intentionally lightweight: it has a functional PyQt GUI,
STL preview, a very simple demo slicer that generates a single‑layer
outline, and stubs for Airtable and OctoPrint integration.  
It is meant as a starting point and architecture reference, **not** a
production slicer.

## Features

- Dark UI inspired by modern slicers (Creality / Bambu style).
- Drag‑and‑drop STL loading.
- 3D preview of the model.
- Basic slicing demo that writes a simple square outline G‑code.
- Settings panel for layer height, infill %, etc. (currently used only
  by the demo slicer).
- Job queue panel (local only by default).
- Architecture hooks for:
  - Airtable job fetching / status update.
  - OctoPrint upload & print start.
  - Printer configuration from `Printer Information.xlsx`.

## Limitations

- The slicing engine is **minimal** and only generates a single outline
  at the model’s bounding box as a proof‑of‑concept.
- Real infill, supports, multi‑layer path planning, etc. are **not**
  implemented yet.
- Airtable and OctoPrint calls are safe stubs until you add real
  credentials in config.

---

## Installation (Windows + Visual Studio Code)

1. **Install Python 3.10+**  
   Download from python.org and check **“Add Python to PATH”** during
   installation.

2. **Install Git (optional but recommended)**  
   So you can manage this project as a repo later.

3. **Open the folder in VS Code**

   - Start **Visual Studio Code**.
   - `File -> Open Folder...` and select the `OpenSlicer` folder.

4. **Create a virtual environment (recommended)**

   In VS Code, open a terminal (``Ctrl+` ``) and run:

   ```bash
   python -m venv .venv
   ```

   Then activate it:

   - PowerShell:

     ```bash
     .venv\Scripts\Activate
     ```

   VS Code should then detect the `.venv` interpreter.

5. **Install dependencies**

   In the same terminal:

   ```bash
   pip install -r requirements.txt
   ```

6. **(Optional) Add `Printer Information.xlsx`**

   Place your `Printer Information.xlsx` file in the **root** of this
   project (next to `main.py`).  
   The loader is tolerant; if the file is missing it will just create a
   dummy printer configuration.

7. **Run the app**

   In VS Code:

   - Open `main.py`.
   - Press `F5` (Run with Debugging) or run:

     ```bash
     python main.py
     ```

   A window titled **OpenSlicer** should appear.  
   Drag an STL file onto the build plate area or use **File → Open STL**.

---

## Very quick user guide

- **Load model**: drag & drop an STL file into the window or use the menu.
- **Inspect**: rotate (left mouse), pan (right mouse), zoom (wheel).
- **Settings**: adjust layer height / infill on the right panel.
- **Slice**: click the **Slice** button in the toolbar.
- **Preview**: the G‑code outline appears as a wireframe square.
- **Print**:
  - Configure OctoPrint URL and API key in `config/printer_config.py`
    or your Excel.
  - Click **Send to Printer** (demo prints the G‑code path to console
    unless fully wired).

This codebase is intentionally small and heavily commented so you can
grow it into a full slicer (multi‑layer geometry, real infill, supports,
Airtable workflow, etc.).
