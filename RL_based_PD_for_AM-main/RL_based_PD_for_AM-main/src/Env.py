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
    processor = mp.MeshProcessor(mesh_path)
    center_point = processor.mesh.centroid + (0, 0, 200)
    z_normal = [0, 0, 1]
    initial_model = processor.trimesh_cut(
        center_point, z_normal)  # THIS CODE SHOULD BE SIMPLIFIED
    # Determine the build orientation of the initial model
    deter_build_orientation(initial_model)

    part_volume = initial_model.volume
    concavity = part_volume - initial_model.convex_hull.volume
    bounding_box = initial_model.bounding_box.extents
    support_volume = 0  # THIS SHOULD BE OBTAINED FROM THE CODE

    print("Initial model ==== ")
    print("Validation (Watertight): ", initial_model.is_watertight)
    print("Volume: ", part_volume)
    print("concavity: ", concavity)
    print("bounding_box: ", bounding_box)
    print("support_volume: ", support_volume)
    processor.pyvista_visualize(initial_model)

    # Create a PD tree
    PD_tree = {"1": {"Vol": part_volume, "BB": bounding_box,
                     "Conc": concavity, "SupVol": support_volume}}

    # Create a list of decomposed parts
    part_list = [PD_tree["1"]]

    return PD_tree, part_list


def cap_current_state(PD_tree, decomposed_parts):
    # Capture the current state of the PD environment
    # BUILD ORIENTATION DETERMINATION

    return state


def deter_build_orientation(trimesh_model):
    args = twk.getargs(trimesh_model)
    build_orientation = twk.cli(args)

    # SET THE CURRENT BUILD ORIENTATION TO THE DEFAULT

    return build_orientation


def decompose_parts(action, part_list, PD_tree):

    for key in PD_tree.keys():
        if key == ACTION[0]:
            part_volume = PD_tree[key]["Vol"]
            bounding_box = PD_tree[key]["BB"]
            concavity = PD_tree[key]["Conc"]
            support_volume = PD_tree[key]["SupVol"]
    # ACTION[0] : PART ID of the part to be decomposed
    # ACTION[1] : CUTTING PLANE COORDINATE & ANGLE
    mesh_path = os.path.join(export_dir, ACTION[0], ".stl")
    processor = mp.MeshProcessor(mesh_path)
    center_point = processor.mesh.centroid + ACTION[1]
    x_normal = [1, 0, 0]
    y_normal = [0, 1, 0]
    z_normal = [0, 0, 1]
    meshes = mp.processor.trimesh_cut(center_point, z_normal)

    # Remove the decomposed part from the part list
    part_list.remove(PD_tree[ACTION[0]])

    if len(meshes) > 0:
        i = 1
        for mesh in meshes:
            print("Mesh{} Validation (Watertight): ".format(i), mesh.is_watertight)
            print("Mesh{} Volume: ".format(i), mesh.volume)
            # mp.processor.pyvista_visualize(mesh)
            PartID = ACTION[0] + "_" + str(i)
            mp.processor.export_mesh_as_stl(mesh, os.path.join(
                export_dir, PartID, '.stl'))
            i += 1

            # Update the PD tree
            PD_tree[PartID] = {"Vol": part_volume, "BB": bounding_box,
                               "Conc": concavity, "SupVol": support_volume}

            # Update the list of decomposed parts
            part_list.append(PD_tree[PartID])

    return PD_tree, part_list


def cal_reward(next_state):
    # Calculate the reward based on the current state

    return reward
