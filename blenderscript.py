import bpy
import mathutils
from math import radians
from os.path import join

S = bpy.context.scene

renderFolder = "D:/MyRenderFolder/"
logFile = "D:/MyRenderFolder/logs.txt"

obj = bpy.data.objects["model"]
cam = bpy.data.objects["Camera"]

numAngles = 4
rotAngle  = 360 / numAngles

origCamPos = cam.location
camPosArr = []

for i in range(numAngles):
    for j in range(-5, 5):
        deltaY = j * 0.1 + origCamPos.y
        camPosArr.append(deltaY)
        cam.location = mathutils.Vector((origCamPos.x, deltaY, origCamPos.z))

        angle = i * rotAngle
        obj.rotation_euler.z = radians( angle )

        fileName = "angle_{a}_cam_{f}".format( a = angle, f = j )
        fileName += S.render.file_extension
        bpy.context.scene.render.filepath = join( renderFolder, fileName )

        bpy.ops.render.render(write_still = True)

with open(logFile, 'w') as f:
    f.write(camPosArr)