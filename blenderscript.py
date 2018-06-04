import bpy
import mathutils
import json
import numpy as np
from math import radians
from os.path import join
import os

# NOTE: Blender cannot run just in the background for this script
# Run this command: blender.exe test.blend --python blenderscript.py

# Get random color to put as background color
def get_color():
    return np.append(np.random.rand(3), 1)

# Init variables

# Change this to change how many pictures you take
# Number of pictures will be NUM_ANGLES^2
NUM_ANGLES = 2

S = bpy.context.scene
WIDTH = 256
HEIGHT = 256
S.render.resolution_x = WIDTH
S.render.resolution_y = HEIGHT
S.render.resolution_percentage = 100
renderFolder = "D:/MyRenderFolder/"

# Create folder to render to
for the_file in os.listdir(renderFolder):
    file_path = os.path.join(renderFolder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)
        exit()

# Create nodes to get render info
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree
links = tree.links

# Clear all existing nodes, don't care about them
for n in tree.nodes:
    tree.nodes.remove(n)

# Create input render layer and set a location (only for visual Blender, might be able to remove)
rend_lyr = tree.nodes.new('CompositorNodeRLayers')
rend_lyr.location = 185, 285

# Create output node (the Viewer node that lets us get pixel values)
viewer = tree.nodes.new('CompositorNodeViewer')
viewer.location = 750, 210
viewer.use_alpha = True # Guy said false here, but we need the alpha to do proper blending

# Link the two nodes
links.new(rend_lyr.outputs[0], viewer.inputs[0])

# Get object and camera (camera is unnecessary as of now)
obj = bpy.data.objects["model"]
cam = bpy.data.objects["Camera"]

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
        file_name = "angle_{a}_cam_{f}".format( a = rot, f = vert)
        bpy.ops.render.render()
        pixels = bpy.data.images['Viewer Node'].pixels

        # Do numpy stuff to copy values of bkgd image into places where alpha is full
        # Need rendered image and bkgd image to be same size for this to work
        # For now, just make the background a solid random color
        pixel_arr = np.array(pixels[:])
        pixel_arr = pixel_arr.reshape((WIDTH * HEIGHT, 4))
        pixel_arr[pixel_arr[...,3]==0] = get_color()

        image = bpy.data.images.new(file_name, width=WIDTH, height=HEIGHT)
        image.pixels = pixel_arr.flatten()
        file_name += S.render.file_extension
        image.filepath_raw = join(renderFolder, file_name)
        image.file_format = 'PNG'
        image.save()
        count += 1