import numpy
import cv2
import os
from os.path import abspath,join

#Resizes all images in each subdirectory of root, to given size
def resize(root,size):
    for folder in os.listdir(root):
        for im in os.listdir(join(root,folder)):
            try:
                img = cv2.imread(abspath(join(root, join(folder, im))))
                img = cv2.resize(img, size)
                cv2.imwrite(abspath(join(root, join(folder, im))), img)
            except:
                print('Resize failed (Probably too small)')


resize('data/val',(128,128))
resize('data/train',(128,128))
