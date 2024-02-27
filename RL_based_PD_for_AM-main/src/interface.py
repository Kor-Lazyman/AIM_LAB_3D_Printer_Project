import sys
import os
import time
import struct
import MeshTweaker
from MeshTweaker import Tweak
import FileHandler
import numpy as np
import trimesh
from config import *
FileHandler=FileHandler.FileHandler()
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
            vertices = np.array(obj[x])

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
            print(sliced_meshes_lst)
            for face in sliced_meshes_lst[x].faces:
                #x y z 좌표 3개가 하나의 삼각형을 이룸
                obj[x]['mesh'].append([sliced_meshes_lst[x].vertices[face[0]][0],sliced_meshes_lst[x].vertices[face[0]][1],sliced_meshes_lst[x].vertices[face[0]][2]])
                obj[x]['mesh'].append([sliced_meshes_lst[x].vertices[face[1]][0],sliced_meshes_lst[x].vertices[face[1]][1],sliced_meshes_lst[x].vertices[face[1]][2]])
                obj[x]['mesh'].append([sliced_meshes_lst[x].vertices[face[2]][0],sliced_meshes_lst[x].vertices[face[2]][1],sliced_meshes_lst[x].vertices[face[2]][2]])
        
        return obj

    def orientation(self,objs):
        total_x=0
        sup_vol={}
        # Start of tweaking.
        if self.result:
            print("Calculating the optimal orientation:\n  {}"
                  .format(self.Root.split(os.sep)[-1]))
        stime = time.time()
        c = 0
        self.info = dict()

        for part, content in objs.items():
            mesh = content["mesh"]
            self.info[part] = dict()
            try:
                cstime = time.time()
                x = Tweak(mesh, EXTENDED, True, False, False, False)
                self.info[part]["matrix"] = x.matrix
                self.info[part]["tweaker_stats"] = x
                print(x)

            except (KeyboardInterrupt, SystemExit):
                pass 
    
            print("Tweaking took:  \t{:2f} s".format(time.time() - stime))
            print("Successfully Rotated!")
            sup_vol[part]=x.overhang
        meshes={}
        for part, content in objs.items():
                mesh = objs[part]["mesh"]
                mesh = self.rotate_bin_stl(self.info[part]["matrix"], mesh)
                meshes[part]=mesh
        return meshes,sup_vol
    
    
    def rotate_bin_stl(self, rotation_matrix, content):
        mesh = np.array(content, dtype=np.float64)

        if len(mesh[0]) == 3:
            row_number = int(len(content) / 3)

        mesh = np.matmul(mesh, rotation_matrix)
        mesh=mesh.reshape(len(content),3)

        return mesh
