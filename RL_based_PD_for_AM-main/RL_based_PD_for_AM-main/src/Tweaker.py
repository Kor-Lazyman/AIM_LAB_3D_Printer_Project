# ORIGINAL CODE: https://github.com/ChristophSchranz/Tweaker-3/blob/master/Tweaker.py

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from time import time

from MeshTweaker import Tweak
import FileHandler


class Arguments:
    # def __init__(self, trimesh_model):
    # APPLY TRIMESH MESH RATHER THAN FILE HANDLER

    def __init__(self):
        self.inputfile = 'demo_object.stl'
        self.outputfile = 'demo_object_tweaked.stl'
        self.verbose = True
        self.show_progress = False
        self.convert = False
        self.output_type = False
        self.extended_mode = False
        self.version = False
        self.result = False
        self.favside = None
        self.volume = False


def getargs():
    return Arguments()


def cli(args):
    global FileHandler
    # Get the command line arguments. Run in IDE for demo tweaking.
    stime = time()
    try:
        args = getargs()
        if args is None:
            sys.exit()
    except:
        raise

    try:
        FileHandler = FileHandler.FileHandler()
        objs = FileHandler.load_mesh(args.inputfile)
        if objs is None:
            sys.exit()
    except (KeyboardInterrupt, SystemExit):
        raise SystemExit("Error, loading mesh from file failed!")

    # Start of tweaking.
    if args.verbose:
        print("Calculating the optimal orientation:\n  {}"
              .format(args.inputfile.split(os.sep)[-1]))

    c = 0
    info = dict()
    for part, content in objs.items():
        mesh = content["mesh"]
        info[part] = dict()
        if args.convert:
            info[part]["matrix"] = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        else:
            try:
                cstime = time()
                x = Tweak(mesh, args.extended_mode, args.verbose,
                          args.show_progress, args.favside, args.volume)
                info[part]["matrix"] = x.matrix
                info[part]["tweaker_stats"] = x
            except (KeyboardInterrupt, SystemExit):
                raise SystemExit("\nError, tweaking process failed!")

            # List tweaking results
            if args.result or args.verbose:
                print("Result-stats:")
                print(" Tweaked Z-axis: \t{}".format(x.alignment))
                print(" Axis {}, \tangle: {}".format(
                    x.rotation_axis, x.rotation_angle))
                print(""" Rotation matrix: 
            {:2f}\t{:2f}\t{:2f}
            {:2f}\t{:2f}\t{:2f}
            {:2f}\t{:2f}\t{:2f}""".format(x.matrix[0][0], x.matrix[0][1], x.matrix[0][2],
                                          x.matrix[1][0], x.matrix[1][1], x.matrix[1][2],
                                          x.matrix[2][0], x.matrix[2][1], x.matrix[2][2]))
                print(" Unprintability: \t{}".format(x.unprintability))

                print("Found result:    \t{:2f} s\n".format(time() - cstime))

    if not args.result:
        try:
            FileHandler.write_mesh(
                objs, info, args.outputfile, args.output_type)
        except FileNotFoundError:
            raise FileNotFoundError(
                "Output File '{}' not found.".format(args.outputfile))

    # Success message
    if args.verbose:
        print("Tweaking took:  \t{:2f} s".format(time() - stime))
        print("Successfully Rotated!")

    return x.matrix
