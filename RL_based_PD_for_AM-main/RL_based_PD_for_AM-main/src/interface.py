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
        self.file_name='demo_object' # input filename what you want to change
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
    def create_trimesh(self,obj):
        meshes=[]

        for x in range(len(obj.keys())):

            #중복된 좌표가 있을 수 있으나 시간, 메모리, 데이터의 사이즈를 고려 중복유지가 합리적
            vertices = np.array(obj[x]['mesh'])

            # faces 배열 생성
            num_triangles = len(vertices) // 3
            faces = np.arange(len(vertices)).reshape(num_triangles, 3)

            # Trimesh 객체 생성 
            mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
            meshes.append(mesh)
        

        return meshes

    def create_obj(self,sliced_meshes_lst):
        # obj형식을 stl형식의 리스트로 변형
        
        obj={}

        for x in range(len(sliced_meshes_lst)): #Parts별 obj생성
            #Tweaker obj 기본 자료구조
            obj[x]={'mesh':[],'name':['binary file']}
            for face in sliced_meshes_lst[x].faces:
                #x y z 좌표 3개가 하나의 삼각형을 이룸
                obj[x]['mesh'].append([sliced_meshes_lst[x].vertices[face[0]][0],sliced_meshes_lst[x].vertices[face[0]][1],sliced_meshes_lst[x].vertices[face[0]][2]])
                obj[x]['mesh'].append([sliced_meshes_lst[x].vertices[face[1]][0],sliced_meshes_lst[x].vertices[face[1]][1],sliced_meshes_lst[x].vertices[face[1]][2]])
                obj[x]['mesh'].append([sliced_meshes_lst[x].vertices[face[2]][0],sliced_meshes_lst[x].vertices[face[2]][1],sliced_meshes_lst[x].vertices[face[2]][2]])
        
        return obj
    # Print tweak result
    def Print_Result(self,x,cstime):
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

    def rot(self,objs):
        
        # Start of tweaking.
        if self.result:
            print("Calculating the optimal orientation:\n  {}"
                  .format(self.Root.split(os.sep)[-1]))
        stime = time()
        try:
            if Utility is None:
                sys.exit()
        except:
            pass
        if objs==None:
            try:

                objs = FileHandler.load_mesh(self.Root)
                if objs is None:
                    sys.exit()

            except(KeyboardInterrupt, SystemExit):
              pass 
        else:
            pass
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
    
            Utility.Print_Result(x,cstime)   
            print("Tweaking took:  \t{:2f} s".format(time() - stime))
            print("Successfully Rotated!")
        
        return objs
    
    def Trim(self,meshes,vectors,part):

            if meshes == None:
                mesh=trimesh.load(self.Root)
                sliced_meshes_lst=[]

                plane_origin = vectors[0]
                plane_normal = vectors[1]

                sliced_mesh=mesh.slice_plane(plane_origin=plane_origin, plane_normal=plane_normal)
                
                if  sliced_mesh.faces.shape[0] != 0:
                    sliced_meshes_lst.append(sliced_mesh)
        
                else:
                    pass
        
                plane_normal = [vectors[1][0],vectors[1][1],-vectors[1][2]]
        
                sliced_mesh=mesh.slice_plane(plane_origin=plane_origin, plane_normal=plane_normal)
        
        
                if sliced_mesh.faces.shape[0] != 0:
                    sliced_meshes_lst.append(sliced_mesh)
        
                else:
                    pass

                return sliced_meshes_lst
        
            else:  
                if part >len(meshes)-1:
                    print("Out of Range")
                    return meshes
                
                else:
                    mesh=meshes[part]
                    print("=========")
                    sliced_meshes_lst=meshes

                    plane_origin = vectors[0]
                    plane_normal = vectors[1]

                    sliced_mesh=mesh.slice_plane(plane_origin=plane_origin, plane_normal=plane_normal)

                    if  sliced_mesh.faces.shape[0] != 0:
                        sliced_meshes_lst.append(sliced_mesh)
        
                    else:
                        pass
        
                    plane_normal = [vectors[1][0],vectors[1][1],-vectors[1][2]]
        
                    sliced_mesh=mesh.slice_plane(plane_origin=plane_origin, plane_normal=plane_normal)
        
        
                    if sliced_mesh.faces.shape[0] != 0:
                        sliced_meshes_lst.append(sliced_mesh)
        
                    else:
                        pass

                    return sliced_meshes_lst
                
class Act:

    Utility=Utility()
    FileHandler = FileHandler.FileHandler()

    def Ori(self,vectors,part):
        objs=None
        objs=Utility.rot(objs)

        #Start Trimesh
        mesh=Utility.create_trimesh(objs)#Makes mesh 
        sliced_meshes_lst=Utility.Trim(mesh,vectors,part)

        return sliced_meshes_lst
        

    def Tri(self,vectors,part):
        mesh=None
        sliced_meshes_lst=Utility.Trim(mesh,vectors,part)
        print(sliced_meshes_lst)
        if sliced_meshes_lst != None:
            obj=Utility.create_obj(sliced_meshes_lst)
            obj=Utility.rot(obj)

        else:
            obj=None

        return obj
 

Utility=Utility()
FileHandler = FileHandler.FileHandler()
Act=Act()

vectors=[[30,50,100],[0,0,1]]#[원점 / 법선벡터]
part=30#어떤 부품을 자를지
if Utility.test_start=="Ori":
    sliced_meshes_lst=Act.Ori(vectors,part)
    print(sliced_meshes_lst)

else:
    obj=Act.Tri(vectors,part)
    
