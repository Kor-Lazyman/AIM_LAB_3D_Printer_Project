import trimesh
import numpy as np
import pyvista as pv


class MeshProcessor:
    def __init__(self, mesh_path):
        self.mesh_path = mesh_path
        self.mesh = trimesh.load(mesh_path)

    def reverse_plane_normal(self, plane_normal):
        return [-x for x in plane_normal]

    def trimesh_cut(self, plane_point, plane_normal):
        reverse_plane = self.reverse_plane_normal(plane_normal)

        sliced_mesh_one = self.mesh.slice_plane(
            plane_origin=plane_point, plane_normal=plane_normal, cap=True)
        sliced_mesh_theother = self.mesh.slice_plane(
            plane_origin=plane_point, plane_normal=reverse_plane, cap=True)

        meshes_one = sliced_mesh_one.split()
        meshes_theother = sliced_mesh_theother.split()

        # meshes = meshes_one + meshes_theother
        meshes = np.concatenate((meshes_one, meshes_theother))
        return meshes

    def export_mesh_as_stl(self, mesh, file_path):
        mesh.export(file_path, file_type='stl')

    @staticmethod
    def trimesh_visualize(mesh):
        mesh.show()

    @staticmethod
    def pyvista_visualize(tri_mesh, color='lightblue'):
        py_mesh = pv.wrap(tri_mesh)
        plotter = pv.Plotter()
        plotter.add_mesh(py_mesh, color=color, show_edges=True)
        plotter.show()
