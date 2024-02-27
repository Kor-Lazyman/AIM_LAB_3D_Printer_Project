import trimesh
import os
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


# 예시 사용
if __name__ == "__main__":
    current_dir = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.path.dirname(current_dir)
    mesh_path = os.path.join(parent_dir, 'models', 'StanfordBunny.stl')
    export_dir = os.path.join(parent_dir, 'results')

    processor = MeshProcessor(mesh_path)
    center_point = processor.mesh.centroid  # + (0, 0, 200)
    x_normal = [1, 0, 0]
    y_normal = [0, 1, 0]
    z_normal = [0, 0, 1]

    meshes = processor.trimesh_cut(center_point, z_normal)

    if len(meshes) > 0:
        i = 1
        for mesh in meshes:
            print("Mesh{} Validation (Watertight): ".format(i), mesh.is_watertight)
            print("Mesh{} Volume: ".format(i), mesh.volume)
            # processor.trimesh_visualize(mesh)
            processor.pyvista_visualize(mesh)
            processor.export_mesh_as_stl(mesh, os.path.join(
                export_dir, 'bunny{}.stl'.format(i)))
            i += 1
