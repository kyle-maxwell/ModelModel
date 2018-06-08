import bpy
import mathutils
import json
import random
import numpy as np
from sys import argv
from math import radians
from os.path import join, abspath, exists
import os

# Get random color to put as background color
# Use to create a baseline background
def get_color():
    return np.append(np.random.rand(3), 1)

def unlink_files(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
            exit()

def main(model_path):
    # Init variables

    # Change this to change how many pictures you take
    # Number of pictures will be NUM_ANGLES^2
    NUM_ANGLES = 15

    # Get scene and set render resolution
    S = bpy.context.scene
    WIDTH = 256
    HEIGHT = 256
    S.render.resolution_x = WIDTH
    S.render.resolution_y = HEIGHT
    S.render.resolution_percentage = 100

    # Parent data folder
    model_name = os.path.splitext(os.path.basename(model_path))[0]
    render_folder = abspath(join("data/models/", model_name))
    if not exists(render_folder):
        os.makedirs(render_folder)

    unlink_files(abspath(render_folder))

    # Delete all previous files in render folder
    for the_file in os.listdir(render_folder):
        file_path = os.path.join(render_folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
            exit()

    random.seed()
   
    # Get object and camera (camera is unnecessary as of now)
    obj = bpy.data.objects["model"]
    # cam = bpy.data.objects["Camera"]

    rot_angle  = 360 / NUM_ANGLES
    vert_angle = 180 / NUM_ANGLES

    count = 0

    # Rotation around vertical axis (horizontal rotaton)
    for i in range(NUM_ANGLES):
        # Rotation around horizontal axis (vertical rotation)
        for j in range(int(-NUM_ANGLES/2)+1, int(NUM_ANGLES/2)+1):
            vert = j * vert_angle
            obj.rotation_euler.y = radians( vert )

            rot = i * rot_angle
            obj.rotation_euler.z = radians( rot )

            print('Processing image {} with rot {} and vert {}'.format(count, rot, vert))

            file_name = "angle_{}_cam_{}.{}".format(rot, vert, S.render.file_extension)

            bpy.context.scene.render.filepath = join(render_folder, file_name)
            bpy.ops.render.render(write_still=True)
            count += 1

main(argv[2])
