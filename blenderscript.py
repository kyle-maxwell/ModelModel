import bpy
import mathutils
import json
import random
import numpy as np
from math import radians
from os.path import join
import os

class Background:
    def __init__(self, w, h):
        self.seed = random.seed()
        self.width = w
        self.height = h

    def load_imgs(self):
        print("Loading background images into blender")
        folder = "Background/"
        files = os.listdir(folder)
        self.images = []
        for i, f in enumerate(files):
            image = bpy.data.images.load(os.path.abspath(os.path.join(folder, f)))
            image.scale(self.width, self.height)
            self.images.append(np.array(image.pixels).reshape((self.height, self.width, 4)))

    def get_img(self):
        n = random.randint(0, len(self.images) - 1)
        return self.images[n]


# Get random color to put as background color
def get_color():
    return np.append(np.random.rand(3), 1)

# Takes two numpy arrays of pixel values and overlays them based on alpha values of obj
def overlay_imgs(obj, bkgd):
    for i in range(len(obj)):
        for j in range(len(obj[0])):
            if(obj[i][j][3] == 0):
                obj[i][j] = bkgd[i][j]

# Init variables

# Change this to change how many pictures you take
# Number of pictures will be NUM_ANGLES^2
NUM_ANGLES = 10

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

# Create background image generator
bkgd = Background(WIDTH, HEIGHT)
bkgd.load_imgs()

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

        # Copy pixel values of bkgd image into obj image using alpha values
        pixel_arr = np.array(pixels[:])
        pixel_arr = pixel_arr.reshape((HEIGHT, WIDTH, 4))
        overlay_imgs(pixel_arr, bkgd.get_img())

        # Save image
        image = bpy.data.images.new(file_name, width=WIDTH, height=HEIGHT)
        image.pixels = pixel_arr.flatten()
        file_name += S.render.file_extension
        image.filepath_raw = join(renderFolder, file_name)
        image.file_format = 'PNG'
        image.save()
        bpy.data.images.remove(image)
        count += 1