import bpy
import mathutils
import json
import numpy as np
from math import radians
from os.path import join
import os

S = bpy.context.scene

renderFolder = "D:/MyRenderFolder/"
logFile = "D:/MyRenderFolder/logs.txt"

for the_file in os.listdir(renderFolder):
    file_path = os.path.join(renderFolder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)
        exit()

obj = bpy.data.objects["model"]
cam = bpy.data.objects["Camera"]

numAngles = 30
rotAngle  = 360 / numAngles
vertRotAngle = 180 / numAngles

for i in range(numAngles):
    for j in range(int(-numAngles/2)+1, int(numAngles/2)+1):
        vertAngle = j * vertRotAngle
        obj.rotation_euler.y = radians( vertAngle )

        angle = i * rotAngle
        obj.rotation_euler.z = radians( angle )

        fileName = "angle_{a}_cam_{f}".format( a = angle, f = vertAngle)
        fileName += S.render.file_extension
        bpy.context.scene.render.filepath = join( renderFolder, fileName )

        bpy.ops.render.render(write_still = True)