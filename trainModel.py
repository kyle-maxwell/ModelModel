from keras import models, layers, regularizers
from keras.utils import to_categorical
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint


def load_data():
    pass
    # return (train_data, train_labels), (test_data, test_labels)


def make_model(input_shape, output_shape):
    nn = models.Sequential()
    nn.add(layers.Conv2D(64, (3, 3), activation='relu', input_shape=input_shape))
    nn.add(layers.MaxPooling2D((2, 2)))

    nn.add(layers.Dropout(0.5))
    nn.add(layers.Conv2D(128, (3, 3), activation='relu'))
    nn.add(layers.MaxPooling2D((2, 2)))

    nn.add(layers.Conv2D(128, (3, 3), activation='relu'))

    nn.add(layers.Flatten())
    nn.add(layers.Dense(64, activation='relu'))
    nn.add(layers.Dense(output_shape, activation='softmax'))

    nn.compile(
        optimizer="rmsprop",
        loss='categorical_crossentropy',
        metrics=['accuracy'])

    return nn


def main():

    (train_data, train_labels), (test_data, test_labels) = load_data()

    model = make_model((train_data.shape[1:]), train_labels.shape[1])

    # Turn into flat vectors
    # train_data = train_data.reshape( (???) )
    # test_data = test_data.reshape( (???) )

    train_data = train_data.astype('float32') / 255
    test_data = test_data.astype('float32') / 255
    train_labels = to_categorical(train_labels)
    test_labels = to_categorical(test_labels)

    datagen = ImageDataGenerator(rotation_range=10, zoom_range=.1)

    # Checkpoint: save models that are improvements
    filepath = "weights-{epoch:02d}-{val_acc:.4f}.h5"
    checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=0, save_best_only=True, mode='max')

    # Train Model
    BATCH_SIZE = 128
    EPOCHS = 64

    hst = model.fit_generator(
        datagen.flow(train_data, train_labels, batch_size=BATCH_SIZE),
        steps_per_epoch= len(train_data) / BATCH_SIZE,
        callbacks=[checkpoint],
        validation_data=(test_data, test_labels),
        epochs=EPOCHS).history


    # for acc, loss, val_acc, val_loss in zip(hst['acc'], hst['loss'],
    #                                         hst['val_acc'], hst['val_loss']):
    #     print("%.5f / %.5f  %.5f / %.5f" % (acc, loss, val_acc, val_loss))


if __name__ == '__main__':
    main()
