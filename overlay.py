import cv2
import numpy as np
import random
import sys
from os.path import abspath, join
import os
from subprocess import run
import urllib
import requests
import socket

class Background:
    def __init__(self, width, height):
        self.seed = random.seed()
        self.w = width
        self.h = height
        with open('fall11_urls.txt', errors='ignore') as links:
            self.raw_links = links.read().split()[0::2]
        socket.setdefaulttimeout(3)

    def load_img(self):
        try:
            data = urllib.request.urlopen(self.get_link()).read()
            data = np.fromstring(data,np.uint8)
            img = cv2.imdecode(data,cv2.IMREAD_COLOR)
            if(img.shape == (374,500,3)):
                print("Failed Flickr")
                return self.load_img()
            return cv2.resize(img, (self.w,self.h), interpolation=cv2.INTER_CUBIC)
        except:
            print('Download Fail')
            return self.load_img()

    def get_link(self):
        n = random.randint(0, len(self.raw_links) - 1)
        if '.gif' in self.raw_links[n]:
            return self.get_link()
        return self.raw_links[n]


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
    num_overlays = 10
    im_files = os.listdir(abspath(im_folder))
    #Make 5 overlays for each image of the object
    count = 0
    for i, f in enumerate(im_files):
        name = abspath(join(im_folder,f))
        im = cv2.imread(name, cv2.IMREAD_UNCHANGED) # To get alpha values
        for j in range(num_overlays - 1):
            print("Image {}".format(count))
            new_name = abspath(join(im_folder,str(count)+f))
            overlay_img(im, bkgd.load_img(), new_name)
            count += 1
        print("Image {}{}".format(j,i))
        overlay_img(im, bkgd.load_img(), name)

#python overlay.py {blender exe} {models folder}
# saves your images to data/objects
def main(argv):
    w = 256
    h = 256
    blender_exe = argv[1]
    obj_folder = argv[2]

    for obj in os.listdir(obj_folder):
        proc = run([blender_exe, '-b', join(obj_folder, obj), '--python', 'blenderscript.py'])
        proc.check_returncode()

    im_folder = 'data/models/'
    bkgd = Background(int(w), int(h))
    for fold in os.listdir(im_folder):
        print("Processing {}".format(fold)) 
        overlay_folder(w, h, join(im_folder, fold), bkgd)

main(sys.argv)
