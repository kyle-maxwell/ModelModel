from keras import models, layers, regularizers
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint

def make_model(input_shape, output_shape):
    nn = models.Sequential()

    # first layer

    nn.add(layers.Conv2D(32,
        (3, 3),
        activation='relu',
        kernel_regularizer=regularizers.l2(.01),
        input_shape=input_shape
    ))
    nn.add(layers.BatchNormalization())
    nn.add(layers.MaxPooling2D())

    # second layer

    nn.add(layers.Conv2D(64,
        (3, 3),
        activation='relu',
        kernel_regularizer=regularizers.l2(.01)
    ))
    nn.add(layers.BatchNormalization())
    nn.add(layers.MaxPooling2D())

    # third layer

    nn.add(layers.Conv2D(128,
        (3, 3),
        activation='relu',
        kernel_regularizer=regularizers.l2(.01)
    ))
    nn.add(layers.BatchNormalization()) 
    nn.add(layers.MaxPooling2D())

# 

    nn.add(layers.Conv2D(64,
        (1, 1),
        activation='relu',
        kernel_regularizer=regularizers.l2(.01)
    ))
    nn.add(layers.Conv2D(32,
        (1,1),
        activation='relu',
        kernel_regularizer=regularizers.l2(.01)
    ))
    nn.add(layers.BatchNormalization())
 
    nn.add(layers.Flatten())
    nn.add(layers.Dense(32,
        activation='relu',
        kernel_regularizer=regularizers.l2(.01)
    ))

    nn.add(layers.LeakyReLU(alpha=0.01))
    nn.add(layers.Dense(output_shape, activation='softmax'))

    nn.summary()
    
    nn.compile(
        optimizer="rmsprop",
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return nn


def main():
    IMAGE_SIZE = 128
    BATCH_SIZE = 32
    BATCH_PER_EPOCH = 30
    EPOCHS = 40
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
