import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.datasets import mnist
from keras import models,layers, regularizers
from keras.utils import to_categorical
from keras.models import load_model
from PIL import Image
import glob
import cv2
import sys
# Displays Validation Data with Title of Window as Prediction Value

def get_generator(dir_name):
    IMAGE_SIZE = 256 
    BATCH_SIZE = 1
    BATCH_PER_EPOCH = 30
    EPOCHS = 40
    CATEGORIES = 2 
    print(dir_name)
    # Generator getting pictures from data/train, and augmenting them
    train_datagen = ImageDataGenerator(
        rescale=1/255
    )   
    train_generator = train_datagen.flow_from_directory(
        dir_name,
        shuffle = False,
        target_size = (IMAGE_SIZE,IMAGE_SIZE),
        batch_size = BATCH_SIZE,
        class_mode = 'categorical'
    )
    return train_generator

def main():
    val_gen = get_generator(sys.argv[2])
    
    model = load_model(sys.argv[1])
    res = model.predict_generator(val_gen, verbose=1)
    
    for (filename, prediction) in zip(val_gen.filenames, res):
        image = cv2.imread(sys.argv[2] + filename, cv2.IMREAD_COLOR)
        rs = cv2.resize(image, None, fx=.5, fy=.5, interpolation=cv2.INTER_CUBIC)
        if(np.around(prediction[0]) == 1):
            cv2.imshow('BOTTLE',rs)
            print('Image ' + sys.argv[2] + filename + " is A BOTTLE.")
        else:
            cv2.imshow('NOT BOTTLE', rs)
            print('Image ' + sys.argv[2] + filename + " is NOT A BOTTLE.")
        cv2.waitKey(3000) # Image will show for 3s, or when you press a key

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

