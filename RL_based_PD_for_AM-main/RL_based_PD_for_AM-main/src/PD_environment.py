from config import *
import numpy as np
import mesh_processor as mp
import os
import Tweaker as twk
import interface 

current_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.dirname(current_dir)
mesh_path = os.path.join(parent_dir, IMPORT_DIR, INPUT_MODEL)
export_dir = os.path.join(parent_dir, EXPORT_DIR)


def create_env():
    
    # Import the initial model
    processor = mp.MeshProcessor()
    processor.load_mesh(mesh_path)
    '''
    center_point = processor.mesh.centroid + (0, 0, 200)
    z_normal = [0, 0, 1]
    initial_model = processor.trimesh_cut(
        center_point, z_normal)  # THIS CODE SHOULD BE SIMPLIFIED
    '''
    # Determine the build orientation of the initial model
    #deter_build_orientation(initial_model)

    part_volume = processor.mesh.volume
    concavity = part_volume - processor.mesh.convex_hull.volume
    bounding_box = processor.mesh.bounding_box.extents
    support_volume = 0  # THIS SHOULD BE OBTAINED FROM THE CODE
    
    '''
    print("Initial model ==== ")
    print("Validation (Watertight): ", processor.mesh.is_watertight)
    print("Volume: ", part_volume)
    print("concavity: ", concavity)
    print("bounding_box: ", bounding_box)
    print("support_volume: ", support_volume)
    '''
    #processor.pyvista_visualize(processor.mesh)

    # Create a PD tree
    PD_tree = {1: {"Vol": part_volume, "BB-X": bounding_box[0],"BB-Y": bounding_box[1],"BB-Z": bounding_box[2],
                     "Conc": concavity, "SupVol": support_volume,"Mesh":processor.mesh}}

    # Create a list of decomposed parts
    part_list = [1]

    return PD_tree, part_list

'''
def cap_current_state(PD_tree, decomposed_parts):
    # Capture the current state of the PD environment
    # BUILD ORIENTATION DETERMINATION

    return state
'''

def deter_build_orientation(trimesh_model):

    Utility=interface.Utility()
    build_orientation,reward,sup_vol=Utility.orientation(Utility.create_obj(trimesh_model))

    # SET THE CURRENT BUILD ORIENTATION TO THE DEFAULT

    return build_orientation,reward,sup_vol


def decompose_parts(ACTION, part_list, PD_tree):
    
    Utility=interface.Utility()
    MeshProcessor=mp.MeshProcessor()
    Part=part_list[round(ACTION[0])]
    
    for key in PD_tree.keys():
        if key == Part:
            part_volume = PD_tree[key]["Vol"]
            bb_x = PD_tree[key]["BB-X"]
            bb_y = PD_tree[key]["BB-Y"]
            bb_z = PD_tree[key]["BB-Z"]
            concavity = PD_tree[key]["Conc"]
            support_volume = PD_tree[key]["SupVol"]
    
    # ACTION[0] : PART ID of the part to be decomposed
    # ACTION[1] : CUTTING PLANE COORDINATE & ANGLE
    '''        
    mesh_path = os.path.join(export_dir, ACTION[0], ".stl")
    processor = mp.MeshProcessor(mesh_path)
    '''
    start_point = [ACTION[1],ACTION[2],ACTION[3]]
    plain_normal=[ACTION[4],ACTION[5],ACTION[6]]

    meshes,check = MeshProcessor.trimesh_cut(PD_tree[Part]['Mesh'],start_point, plain_normal)

    obj,reward,sup_vol=deter_build_orientation(meshes)
    
    #Cal Reward

    meshes=Utility.create_trimesh(obj)
    
    # Remove the decomposed part from the part list
    
    
    
    if len(meshes) > 0 and check==True:
        i = 1
        for mesh in meshes:
            
            print("Mesh{} Validation (Watertight): ".format(i), mesh.is_watertight)
            print("Mesh{} Volume: ".format(i), mesh.volume)
            # mp.processor.pyvista_visualize(mesh)
            PartID = Part*10+i
            i += 1

            # Update the PD tree
            PD_tree[PartID] = {"Vol": mesh.volume, "BB-X":mesh.bounding_box.extents[0],"BB-Y": mesh.bounding_box.extents[1],"BB-Z": mesh.bounding_box.extents[2],
                               "Conc": mesh.volume - mesh.convex_hull.volume, "SupVol":sup_vol[i-2],"Mesh":mesh}

            # Update the list of decomposed parts
            part_list.append(PartID)
        part_list.remove(Part)
    else:
        pass

    
    return PD_tree, part_list,reward




def cal_reward(min_volume_of_surrport_struct):
    # Calculate the reward based on the current state
    
    return -min_volume_of_surrport_struct
'''
PD_tree, part_list=create_env()
PD_tree, part_list,reward=decompose_parts([1,0,0,0,-20,-20,100],part_list,PD_tree)
PD_tree, part_list,reward=decompose_parts([12,0,0,0,-200,-20,100],part_list,PD_tree)
'''