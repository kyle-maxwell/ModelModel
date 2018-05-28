import cv2
import numpy as np
import os
import sys

# Creates directory for water bottle pics and not water bottle
def process_video(files):
    emptyFrame = 0
    objectFrame = 0
    for filename in files:
        if "empty" in filename:
            dir_name = 'empty_pics'
            try:
                if not os.path.exists(dir_name):
                    os.mkdir(dir_name)
                emptyFrame = cap_vid(filename, emptyFrame, dir_name)

            except OSError:
                print('Error Creating: ' + dir_name)                
        else:
            dir_name = filename.split('_')[0]
            try:
                if not os.path.exists(dir_name):
                    os.mkdir(dir_name)
                objectFrame = cap_vid(filename, objectFrame, dir_name)
            except OSError:
                print('Error Creating: ' + dir_name)

def cap_vid(filename, currentFrame, dir_name):
    video = cv2.VideoCapture(filename)
    while(True):
        ret, frame = video.read()
        if(ret):
            name = dir_name + '/frame' + str(currentFrame) + '.jpg'
            print('Creating ', name)
            if(currentFrame%3==0):
                cv2.imwrite(name, frame)
            currentFrame += 1
        else:
            print("Done processing " + filename + "\n\n\n")
            break
    video.release()
    cv2.destroyAllWindows()
    return currentFrame

# Run this with the command line arguments of the filenames to be processed
# Name files either empty_(...) or (object)_n, where n is a real number
def main(argv):
    process_video(sys.argv[1:])

if __name__ == "__main__":
    main(sys.argv)
