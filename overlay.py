import cv2
import numpy as np
import random
import sys
from os.path import abspath, join
import os

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


def overlay_img(obj, bkgd, name):
    for i in range(len(obj)):
        for j in range(len(obj[0])):
            if(obj[i][j][3] == 0):
                obj[i][j][:3] = bkgd[i][j]
                obj[i][j][3] = 1
    cv2.imwrite(name, np.delete(obj, 3, axis=-1))


def overlay_folder(w, h, im_folder, bkgd):
    num_overlays = 6
    im_files = os.listdir(abspath(im_folder))
    #Make 5 overlays for each image of the object
    count = 0
    for j in range(0,num_overlays-1):
        for i, f in enumerate(im_files):
            print("Image {}{}".format(j,i))
            name = abspath(join(im_folder,f))
            im = cv2.imread(name, cv2.IMREAD_UNCHANGED) # To get alpha values
            name = abspath(join(im_folder,str(count)+f))
            overlay_img(im, bkgd.get_img(), name)
            count += 1
    #One last time to overwrite original... Now we have 6 each
    for i, f in enumerate(im_files):
        print("Image {}{}".format(j,i))
        name = abspath(join(im_folder,f))
        im = cv2.imread(name, cv2.IMREAD_UNCHANGED) # To get alpha values
        overlay_img(im, bkgd.get_img(), name)


def main(argv):
    w = argv[1]
    h = argv[2]
    bkgd_folder = argv[3]
    im_folders = argv[4:]
    bkgd = Background(int(w), int(h), bkgd_folder)
    for obj in im_folders:
        print("Processing {}".format(obj))
        for fold in os.listdir(abspath(obj)): 
            overlay_folder(w, h, join(obj, fold), bkgd)

main(sys.argv)
