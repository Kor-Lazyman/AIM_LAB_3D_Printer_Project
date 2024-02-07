import sys
import os
from time import time
import MeshTweaker
from MeshTweaker import Tweak
import FileHandler
import numpy as np
import trimesh
class Utility():
    def __init__(self):
        self.test_start='Ori' # Ori means using Tweaker first, Tri means using Trimesh first
        self.file_name='death_star' # input filename what you want to change
        self.file_type='stl' #input form of file
        self.curpath = os.path.dirname(os.path.realpath(self.file_name))
        self.result=True
        self.Root = self.curpath + os.sep +self.file_name+'.'+self.file_type
        self.outputfile =self.curpath + os.sep +self.file_name+ "_tweaked"+'.stl'

    # trimesh's bounds를 (xMin, xMax, yMin, yMax, zMin, zMax)로 변형 
    def align_bounds(self,bounds):
        temp = []
        for i in range(len(bounds)):
            aa = bounds[i]
            for j in range(len(aa)):
                jj = aa[j]
                temp.append(jj)
        align_bound = [temp[0], temp[3], temp[1], temp[4], temp[2], temp[5]]
        return align_bound 
    
    #Create_Trimesh
    def create_trimesh(self,objs):
        faces=[]
        vertices =[]
        for y in range(len(objs[0]['mesh'])):
       
            if objs[0]['mesh'][y] not in vertices:
             vertices.append(objs[0]['mesh'][y])
            if y%3==2:
                tmp=[]
                for z in range(3):
                    tmp.append(vertices.index(objs[0]['mesh'][y-(2-z)]))
                faces.append(tmp)
        
        faces=np.array(faces)
        vertices=np.array(vertices)
        return trimesh.Trimesh(faces=faces,vertices=vertices)

    def create_obj(self,sliced_meshes):
        obj={0:{'mesh':[],'name':['binary file']}}
        for x in range(len(sliced_meshes.faces)):
            for y in range(3):
                obj[0]['mesh'].append(sliced_meshes.vertices[sliced_meshes.faces[x][y]])
  
        return obj
    
    # Print tweak result
    def Print_Result(self,x):
        if Utility.result:
                print("Result-stats:")
                print(" Tweaked Z-axis: \t{}".format(x.alignment))
                print(" Axis {}, \tangle: {}".format(x.rotation_axis, x.rotation_angle))
                print(""" Rotation matrix: 
            {:2f}\t{:2f}\t{:2f}
            {:2f}\t{:2f}\t{:2f}
            {:2f}\t{:2f}\t{:2f}""".format(x.matrix[0][0], x.matrix[0][1], x.matrix[0][2],
                                          x.matrix[1][0], x.matrix[1][1], x.matrix[1][2],
                                          x.matrix[2][0], x.matrix[2][1], x.matrix[2][2]))
                print(" Unprintability: \t{}".format(x.unprintability))

                print("Found result:    \t{:2f} s\n".format(time() - cstime))

Utility=Utility()
FileHandler = FileHandler.FileHandler()

if Utility.test_start=='Ori':

    # Get the command line arguments. Run in IDE for demo tweaking.
    stime = time()
    try:
        if Utility is None:
            sys.exit()
    except:
        pass

    try:
        
        objs = FileHandler.load_mesh(Utility.Root)
        if objs is None:
            sys.exit()
    except(KeyboardInterrupt, SystemExit):
        pass 

    # Start of tweaking.
    if Utility.result:
        print("Calculating the optimal orientation:\n  {}"
              .format(Utility.Root.split(os.sep)[-1]))

    c = 0
    info = dict()
    for part, content in objs.items():
        mesh = content["mesh"]
        info[part] = dict()
        try:
            cstime = time()
            x = Tweak(mesh, True, True, False, False, False)
            info[part]["matrix"] = x.matrix
            info[part]["tweaker_stats"] = x
        except (KeyboardInterrupt, SystemExit):
            pass 
    
    Utility.Print_Result(x)   
    FileHandler.write_mesh(objs, info, Utility.outputfile, '.stl')
    print("Tweaking took:  \t{:2f} s".format(time() - stime))
    print("Successfully Rotated!")
   
    #Start Trimesh
    mesh=Utility.create_trimesh(objs)#Makes mesh 
    
    # 평면의 원점과 법선 벡터 정의
    slice_origin = mesh.center_mass  # 평면의 원점
    slice_normal = mesh.vertices[0]  # 평면의 법선 벡터 
    sliced_meshes = mesh.slice_plane(plane_origin=slice_origin, plane_normal=slice_normal)

elif Utility.test_start=='Tri':
    mesh=trimesh.load(Utility.Root)

    #자를 평면을 선택
    slice_origin = mesh.center_mass  # 평면의 원점
    slice_normal = mesh.vertices[0]  # 평면의 법선 벡터 
    #자르기
    sliced_meshes = mesh.slice_plane(plane_origin=slice_origin, plane_normal=slice_normal)
    sliced_meshes.export('sliced.stl')
   

    # Get the command line arguments. Run in IDE for demo tweaking.
    stime = time()
    try:
        if Utility is None:
            sys.exit()
    except:
        pass


    c = 0
    info = dict()
    obj=Utility.create_obj(sliced_meshes)
    for part, content in obj.items():
        mesh = content["mesh"]
        info[part] = dict()
        try:
            cstime = time()
            x = Tweak(mesh, True, True, False, False, False)
            info[part]["matrix"] = x.matrix
            info[part]["tweaker_stats"] = x
        except (KeyboardInterrupt, SystemExit):
            pass 
        
    # Print tweak result
    Utility.Print_Result(x) 
        
    FileHandler.write_mesh(obj, info, Utility.outputfile, '.stl')
    print("Tweaking took:  \t{:2f} s".format(time() - stime))
    print("Successfully Rotated!")

