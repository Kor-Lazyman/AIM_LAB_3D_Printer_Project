import trimesh
import numpy as np
import pyvista as pv
import interface

class MeshProcessor:
    def __init__(self):
        pass
    
    def load_mesh(self,mesh_path):
        mesh_path = mesh_path
        self.mesh = trimesh.load(mesh_path)

    def reverse_plane_normal(self, plane_normal):
        return [-x for x in plane_normal]

    def trimesh_cut(self, mesh,plane_point, plane_normal):
        checked1=True
        checked2=True
        reverse_plane = self.reverse_plane_normal(plane_normal)

        sliced_mesh_one = mesh.slice_plane(
            plane_origin=plane_point, plane_normal=plane_normal, cap=True)
        sliced_mesh_theother = mesh.slice_plane(
            plane_origin=plane_point, plane_normal=reverse_plane, cap=True)
        
        #print(sliced_mesh_one)
        #print(sliced_mesh_theother)
        if sliced_mesh_one.faces.shape !=(0,3):
            meshes_one=sliced_mesh_one.split()
            if len(meshes_one)== 0:
                meshes_one = [sliced_mesh_one]
        else:
            checked1=False
            

        if sliced_mesh_theother.faces.shape !=(0,3):
            meshes_theother = sliced_mesh_theother.split()
            if len(meshes_theother)== 0:
                meshes_theother = [sliced_mesh_theother]
        else:
            checked2=False
        
       
        
        if checked1==True and checked2==True:
             meshes = np.concatenate((meshes_one, meshes_theother))
             #print(meshes)
             return meshes, True
        if checked1==True and checked2==False :
            meshes_one=sliced_mesh_one.split()
            if len(meshes_one)== 0:
                meshes_one = [sliced_mesh_one]
            print("Mesh 2 is broken")
            return meshes_one, False
        if checked2==True and checked1==False:
            meshes_theother = sliced_mesh_theother.split()
            if len(meshes_theother)== 0:
                meshes_theother = [sliced_mesh_theother]

            print("Mesh 1 is broken")
            return meshes_theother, False
            
        # meshes = meshes_one + meshes_theother
       
       

    def export_mesh_as_stl(self, mesh, file_path):
        mesh.export(file_path, file_type='stl')

    @staticmethod
    def trimesh_visualize(mesh):
        #mesh.show()
        pass
    @staticmethod
    def pyvista_visualize(tri_mesh, color='lightblue'):
        py_mesh = pv.wrap(tri_mesh)
        plotter = pv.Plotter()
        plotter.add_mesh(py_mesh, color=color, show_edges=True)
        plotter.show()

