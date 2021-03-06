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
    IMAGE_SIZE = 128
    BATCH_SIZE = 1
    print(dir_name)
    
    val_datagen = ImageDataGenerator(
        rescale=1/255
    )   
    val_generator = val_datagen.flow_from_directory(
        dir_name,
        shuffle = False,
        target_size = (IMAGE_SIZE,IMAGE_SIZE),
        batch_size = BATCH_SIZE,
        class_mode = 'categorical'
    )
    return val_generator

def get_totals(data_labels,data_predictions):
    predictions = np.array([0,0,0,0])
    for prediction in data_predictions:
        predictions[np.argmax(prediction)] += 1 
    print(predictions)

#python modelPredict.py model.h5 picture_dir
def main():
    val_gen = get_generator(sys.argv[2])
    model = load_model(sys.argv[1])
    model.summary()
    res = model.predict_generator(val_gen, verbose=1)
    print(val_gen.class_indices)
    get_totals(val_gen.classes,res)
    for (filename, label, prediction) in zip(val_gen.filenames,val_gen.classes, res):
        image = cv2.imread(sys.argv[2] + filename, cv2.IMREAD_COLOR)
        rs = cv2.resize(image, (128,128), interpolation=cv2.INTER_CUBIC)
        cv2.imshow('Image',rs)
        print('label: {}'.format(list(val_gen.class_indices)[label]))
        print('prediction: {}'.format(list(val_gen.class_indices)[np.argmax(prediction)]))
        print(np.around(prediction, decimals=3))
        cv2.waitKey(3000) # Image will show for 3s, or when you press a key
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

