from keras import models, layers, regularizers
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint

def make_model(input_shape, output_shape):
    nn = models.Sequential()
    nn.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    nn.add(layers.MaxPooling2D((2, 2)))

    nn.add(layers.Conv2D(64, (3, 3), activation='relu'))
    nn.add(layers.MaxPooling2D((2, 2)))

    nn.add(layers.Conv2D(64, (3, 3), activation='relu'))
    nn.add(layers.MaxPooling2D((2, 2)))

    nn.add(layers.Conv2D(128,
        (3, 3),
        activation='relu',
        kernel_regularizer=regularizers.l2(.01)
    ))

    nn.add(layers.Flatten())
    nn.add(layers.Dense(16,
        activation='relu',
        kernel_regularizer=regularizers.l2(.01)
    ))
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
    CATEGORIES = 2
    
    # Generator getting pictures from data/train, and augmenting them
    train_datagen = ImageDataGenerator(
        rotation_range=10,
        zoom_range=.1,
        horizontal_flip=True,
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
    filepath = "weights-{epoch:02d}-{val_acc:.4f}.h5"
    checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=0, save_best_only=True, mode='max')

    # Train Model
    model = make_model((IMAGE_SIZE,IMAGE_SIZE,3), CATEGORIES)
    
    hst = model.fit_generator(
        train_generator,
        steps_per_epoch= BATCH_PER_EPOCH,
        callbacks=[checkpoint],
        validation_data=validation_generator,
        epochs=EPOCHS
    ).history

if __name__ == '__main__':
    main()
