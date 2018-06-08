import cv2
import numpy as np
import random
import sys
from os.path import abspath, join
import os
from subprocess import run

class Background:
    def __init__(self, width, height, folder):
        self.seed = random.seed()
        self.w = width
        self.h = height
        self.folder = folder
        self.load_imgs()

    def load_imgs(self):
        print("Loading background images")
        files = os.listdir(self.folder)
        self.images = []
        for i, f in enumerate(files):
            #image = bpy.data.images.load(abspath(join(self.folder, f)))
            image = cv2.imread(abspath(join(self.folder, f)));
            image = cv2.resize(image, (self.w, self.h))
            self.images.append(image)

    def get_img(self):
        n = random.randint(0, len(self.images) - 1)
        return self.images[n]


def overlay_img(im, bkgd, name):
    obj = np.zeros(im.shape)
    for i in range(len(obj)):
        for j in range(len(obj[0])):
            if(im[i][j][3] == 0):
                obj[i][j][:3] = bkgd[i][j]
                obj[i][j][3] = 1
            else:
                obj[i][j] = im[i][j]
    cv2.imwrite(name, np.delete(obj, 3, axis=-1))


def overlay_folder(w, h, im_folder, bkgd):
    num_overlays = 6
    im_files = os.listdir(abspath(im_folder))
    #Make 5 overlays for each image of the object
    count = 0
    for i, f in enumerate(im_files):
        name = abspath(join(im_folder,f))
        im = cv2.imread(name, cv2.IMREAD_UNCHANGED) # To get alpha values
        for j in range(num_overlays - 1):
            print("Image {}{}".format(j,i))
            new_name = abspath(join(im_folder,str(count)+f))
            overlay_img(im, bkgd.get_img(), new_name)
            count += 1
        print("Image {}{}".format(j,i))
        overlay_img(im, bkgd.get_img(), name)


def main(argv):
    w = 256
    h = 256
    blender_exe = argv[1]
    bkgd_folder = argv[2]
    obj_folder = argv[3]

    for obj in os.listdir(obj_folder):
        proc = run([blender_exe, '-b', join(obj_folder, obj), '--python', 'blenderscript.py'])
        proc.check_returncode()

    im_folder = 'data'
    bkgd = Background(int(w), int(h), bkgd_folder)
    for fold in os.listdir(im_folder):
        print("Processing {}".format(fold)) 
        overlay_folder(w, h, join(im_folder, fold), bkgd)

main(sys.argv)
