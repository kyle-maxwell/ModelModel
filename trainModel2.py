from keras import models, layers, regularizers, optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint

def make_model(input_shape, output_shape):
    nn = models.Sequential()

    # first, second, third layer

    nn.add(layers.Conv2D(32,
        (3, 3),
        activation="linear",
        kernel_regularizer=regularizers.l2(.01),
        input_shape=input_shape,
        kernel_initializer="he_normal"
    ))

    nn.add(layers.LeakyReLU(0.001))

    nn.add(layers.Conv2D(32,
        (3, 3),
        activation="linear",
        kernel_regularizer=regularizers.l2(.01),
        kernel_initializer="he_normal"
    ))
    nn.add(layers.LeakyReLU(0.001))

    nn.add(layers.Conv2D(32,
        (3, 3),
        activation="linear",
        #kernel_regularizer=regularizers.l2(.01),
        kernel_initializer="he_normal"
    ))
    nn.add(layers.LeakyReLU(0.001))

    nn.add(layers.BatchNormalization())
    nn.add(layers.Dropout(.4))
    nn.add(layers.MaxPooling2D())

    # four, five, sixth layer
    nn.add(layers.Conv2D(64,
        (3, 3),
        activation="linear",
        kernel_regularizer=regularizers.l2(.01),
        kernel_initializer="he_normal"
    )) 

    nn.add(layers.LeakyReLU(0.001))

    nn.add(layers.Conv2D(64,
        (3, 3),
        activation="linear",
        kernel_regularizer=regularizers.l2(.01),
        kernel_initializer="he_normal"
    ))
    nn.add(layers.LeakyReLU(0.001))

    nn.add(layers.Conv2D(64,
        (3, 3),
        activation="linear",
        #kernel_regularizer=regularizers.l2(.01),
        kernel_initializer="he_normal"
    ))
    nn.add(layers.LeakyReLU(0.001))

    nn.add(layers.BatchNormalization()) 
    nn.add(layers.Dropout(.4))
    nn.add(layers.MaxPooling2D())

    # seven, eight, nine, ten layer
    nn.add(layers.Conv2D(64,
        (1, 1),
        activation="linear",
        kernel_regularizer=regularizers.l2(.01),
        kernel_initializer="he_normal"
    ))  

    nn.add(layers.LeakyReLU(0.001))

    nn.add(layers.Conv2D(32,
        (1,1),
        activation="linear",
        kernel_regularizer=regularizers.l2(.01),
        kernel_initializer="he_normal"
    ))
    nn.add(layers.LeakyReLU(0.001))

    nn.add(layers.Conv2D(16,
        (1,1),
        activation="linear",
        #kernel_regularizer=regularizers.l2(.01),
        kernel_initializer="he_normal"
    ))
    nn.add(layers.LeakyReLU(0.001))

    nn.add(layers.Conv2D(16,
        (3,3),
        activation="linear",
        #kernel_regularizer=regularizers.l2(.01),
        kernel_initializer="he_normal"
    ))
    nn.add(layers.LeakyReLU(0.001))
    nn.add(layers.BatchNormalization())
    nn.add(layers.MaxPooling2D())
    nn.add(layers.Flatten())

    # eleventh layer

    nn.add(layers.Dense(64,
        activation="relu",
        kernel_regularizer=regularizers.l2(.01),
        kernel_initializer="he_normal"
    ))
    nn.add(layers.Dropout(.3))
    nn.add(layers.Dense(output_shape, activation='softmax'))

    nn.summary()

    nn.compile(
        optimizer=optimizers.Adam(lr=0.0001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return nn


def main():
    IMAGE_SIZE = 128
    BATCH_SIZE = 64
    BATCH_PER_EPOCH = 30
    EPOCHS = 200
    CATEGORIES = 4
    
    # Generator getting pictures from data/train, and augmenting them
    train_datagen = ImageDataGenerator(
        rotation_range=10,
        zoom_range=.1,
        horizontal_flip=True,
        rescale=1/255,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2
    )
    train_generator = train_datagen.flow_from_directory(
        'data/train',
        target_size = (IMAGE_SIZE, IMAGE_SIZE),
        batch_size = BATCH_SIZE,
        class_mode = 'categorical'
    )

    validation_datagen = ImageDataGenerator(   
        rescale=1/255
    )
    validation_generator = validation_datagen.flow_from_directory(
        'data/val',
        target_size = (IMAGE_SIZE, IMAGE_SIZE),
        batch_size = BATCH_SIZE,
        class_mode = 'categorical'
    )
    
    # Checkpoint: save models that are improvements
    filepath = "weights/weights-{epoch:02d}-{val_acc:.4f}.h5"
    checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=0, save_best_only=True, mode='max')

    # Train Model
    input_shape = (IMAGE_SIZE, IMAGE_SIZE, 3) # 3 channels? or 4? alpha levels?
    # it is three for R G B ?
    model = make_model(input_shape, CATEGORIES)
    
    hst = model.fit_generator(
        train_generator,
        steps_per_epoch= BATCH_PER_EPOCH,
        callbacks=[checkpoint],
        validation_data=validation_generator,
        epochs=EPOCHS
    ).history

if __name__ == '__main__':
    main()
