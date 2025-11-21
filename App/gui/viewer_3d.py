from PyQt5 import QtWidgets
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
import trimesh

class Viewer3D(gl.GLViewWidget):
    """Simple 3D viewer using pyqtgraph's OpenGL view.

    Supports STL visualization and basic orbit controls.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBackgroundColor((20, 22, 26))
        self.opts['distance'] = 300
        self.mesh_item = None

        # Add a grid for the build plate
        g = gl.GLGridItem()
        g.setSize(200, 200, 0)
        g.setSpacing(10, 10, 1)
        g.translate(0, 0, 0)
        g.setColor((80, 80, 80, 255))
        self.addItem(g)

    def clear_mesh(self):
        if self.mesh_item is not None:
            self.removeItem(self.mesh_item)
            self.mesh_item = None

    def load_stl(self, path: str):
        self.clear_mesh()
        mesh = trimesh.load(path, force="mesh")
        if not isinstance(mesh, trimesh.Trimesh):
            mesh = trimesh.util.concatenate(mesh.dump())

        vertices = mesh.vertices
        faces = mesh.faces

        md = gl.MeshData(vertexes=vertices, faces=faces)
        color = (0.0, 0.9, 0.4, 0.9)  # green accent
        self.mesh_item = gl.GLMeshItem(meshdata=md, smooth=False,
                                       color=color, shader='shaded')
        self.addItem(self.mesh_item)

        # Auto-center camera
        mn, mx = mesh.bounds
        center = (mn + mx) / 2.0
        size = np.max(mx - mn)
        self.opts['center'] = pg.Vector(*center)
        self.opts['distance'] = max(size * 2, 200)
        self.update()
