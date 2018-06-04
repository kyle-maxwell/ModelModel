from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing import image
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras import backend as K

# create the base pre-trained model
base_model = InceptionV3(weights='imagenet', include_top=False)

# add a global spatial average pooling layer
x = base_model.output
x = GlobalAveragePooling2D()(x)
# let's add a fully-connected layer
x = Dense(1024, activation='relu')(x)
# and a logistic layer -- let's say we have 200 classes
CATEGORIES = 2
predictions = Dense(CATEGORIES, activation='softmax')(x)

# this is the model we will train
model = Model(inputs=base_model.input, outputs=predictions)

# first: train only the top layers (which were randomly initialized)
# i.e. freeze all convolutional InceptionV3 layers
for layer in base_model.layers:
    layer.trainable = False

# compile the model (should be done *after* setting layers to non-trainable)
model.compile(optimizer='rmsprop', loss='categorical_crossentropy')

# train the model on the new data for a few epochs
# model.fit_generator(...)

# train_model(model, epochs, batch_per_epoch, batch_size)
train_model(model, 20, 30, 32)


# at this point, the top layers are well trained and we can start fine-tuning
# convolutional layers from inception V3. We will freeze the bottom N layers
# and train the remaining top layers.
# let's visualize layer names and layer indices to see how many layers
# we should freeze:
for i, layer in enumerate(base_model.layers):
   print(i, layer.name)

# we chose to train the top 2 inception blocks, i.e. we will freeze
# the first 249 layers and unfreeze the rest:
for layer in model.layers[:249]:
   layer.trainable = False
for layer in model.layers[249:]:
   layer.trainable = True

# we need to recompile the model for these modifications to take effect
# we use SGD with a low learning rate
from keras.optimizers import SGD
model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy')

# we train our model again (this time fine-tuning the top 2 inception blocks
# alongside the top Dense layers
#model.fit_generator(...)

# train_model(model, epochs, batch_per_epoch, batch_size)
train_model(model, 20, 30, 32)








def train_model(model, epochs, batch_per_epoch, batch_size):
    IMAGE_SIZE = 128
    BATCH_SIZE = batch_size
    BATCH_PER_EPOCH = batch_per_epoch
    EPOCHS = epochs
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
    filepath = "weights/weights-{epoch:02d}-{val_acc:.4f}.h5"
    checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=0, save_best_only=True, mode='max')

    hst = model.fit_generator(
        train_generator,
        steps_per_epoch= BATCH_PER_EPOCH,
        callbacks=[checkpoint],
        validation_data=validation_generator,
        epochs=EPOCHS
    ).history
