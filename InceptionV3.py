from keras import models, layers, regularizers
from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras import backend as K
from keras.callbacks import ModelCheckpoint



def main():
    # create the base pre-trained model
    base_model = InceptionV3(weights='imagenet', include_top=False)

    # add a global spatial average pooling layer
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(32, activation='relu')(x) # Was 1024 when had 200 classes, 512 also


    CATEGORIES = 2
    predictions = Dense(CATEGORIES, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)
    # i.e. freeze *all* convolutional InceptionV3 layers
    for layer in base_model.layers:
        layer.trainable = False

    # compile the model *after* setting layers to non-trainable
    model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=["accuracy"])

    # train the model on the new data for a few epochs
    # model.fit_generator(...)
    # train_model(model, epochs, batch_per_epoch, batch_size)
    train_model(model, 2, 30, 64)

    # freeze the bottom N layers and train the remaining top layers.
    # we chose to train the top 2 inception blocks, i.e. we will freeze
    # the first 249 layers and unfreeze the rest:
    for layer in model.layers[:249]:
       layer.trainable = False
    for layer in model.layers[249:]:
       layer.trainable = True

    # we need to recompile the model for these modifications to take effect
    # we use SGD with a low learning rate
    from keras.optimizers import SGD, Adam, RMSprop
    #model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy', metrics=["accuracy"])
    model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss = "categorical_crossentropy", metrics=["accuracy"])
    # we train our model again (this time fine-tuning the top 2 inception blocks
    # alongside the top Dense layers
    # model.fit_generator(...)
    # train_model(model, epochs, batch_per_epoch, batch_size)
    train_model(model, 20, 30, 64)



def train_model(model, EPOCHS, BATCH_PER_EPOCH, BATCH_SIZE):
    IMAGE_SIZE = 128
    CATEGORIES = 2
    
    # Generator getting pictures from data/train, and augmenting them
    train_datagen = ImageDataGenerator(
        rotation_range=10,
        zoom_range=.1,
        horizontal_flip=True,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        rescale=1/255
    )
    train_generator = train_datagen.flow_from_directory(
        'data/train',
        target_size = (IMAGE_SIZE,IMAGE_SIZE),
        batch_size = BATCH_SIZE,
        class_mode = 'categorical'
    )

    validation_datagen = ImageDataGenerator(   
        rescale=1/255
    )
    validation_generator = validation_datagen.flow_from_directory(
        'data/val',
        target_size = (IMAGE_SIZE,IMAGE_SIZE),
        batch_size = BATCH_SIZE,
        class_mode = 'categorical'
    )
    
    # Checkpoint: save models that are improvements
    filepath = "weights/weights-{epoch:02d}-{val_acc:.4f}.h5"
    checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=0, save_best_only=True, mode='max')

    hst = model.fit_generator(
        train_generator,
        steps_per_epoch= BATCH_PER_EPOCH,
        callbacks=[checkpoint],
        validation_data=validation_generator,
        epochs=EPOCHS
    ).history




if __name__ == '__main__':
    main()
