from keras.layers.normalization.batch_normalization import BatchNormalization
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten, Activation, Dropout
from keras.layers import Dense
from keras.preprocessing.image import ImageDataGenerator
from keras import callbacks
from keras.models import load_model
from tensorflow.keras import initializers
from tensorflow.keras.optimizers import RMSprop
from trainAI.getDatasetTrainingIA import getDataseTrainingIA
from keras.applications.vgg16 import VGG16


def trainAIV1():
    model = Sequential()

    # Convolution
    model.add(Conv2D(16, (3, 3), input_shape=(200, 200, 1)))
    model.add(Activation("relu"))
    # Pooling
    model.add(MaxPooling2D(2, 2))

    model.add(Conv2D(32, (3, 3)))
    model.add(Activation("relu"))
    # Pooling
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation("relu"))
    # Pooling
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation("relu"))
    # Pooling
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation("relu"))
    # Pooling
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # Flattening
    model.add(Flatten())

    # Full connection
    model.add(Dense(units=512, activation='relu', kernel_initializer='random_normal',
                    bias_initializer='zeros'
                    ))
    # model.add(Dense(units=256, activation='relu'))
    model.add(Dropout(0.25))
    # softmax # hard_sigmoid # sigmoid
    model.add(Dense(units=1, activation='sigmoid'))
    # model.add(Activation("sigmoid"))
    # model.add(Dropout(0.2))
    # Compiling the CNN

    # model.compile(optimizer='adam', loss='categorical_crossentropy',
    #               metrics=['accuracy'])
    model.compile(loss='binary_crossentropy',optimizer=RMSprop(lr=0.001),metrics='accuracy')
    model.summary()

    (trainingSet, testSet) = getDataseTrainingIA(
        target_size=(200, 200), ratio=0.8)

    # set steps_per_epoch=3000 and validation_steps=1000 with real data
    model.fit(trainingSet, validation_data=testSet, batch_size=32, epochs=25)
    model.save("model.h5", overwrite=True)
    model.save_weights('weights.h5', overwrite=True)

    test_datagen = ImageDataGenerator(rescale=1./255)
    test_generator = test_datagen.flow_from_directory(
        "/home/vedoc/Images/Sneaker-data/test_temp",
        target_size=(200, 200),
        batch_size=32,
        color_mode="grayscale",
        class_mode=None,
        shuffle=False)

    # make the prediction
    prediction = model.predict(
        test_generator, verbose=1, steps=len(test_generator.filenames))
    # print(model.get_config())
    # print(model.get_weights())
    # model.predict_on_batch();
    print(prediction)


trainAIV1()

model = load_model('model.h5')
model.load_weights('weights.h5')


test_datagen = ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_directory(
    "/home/vedoc/Images/Sneaker-data/test_temp",
    target_size=(200, 200),
    batch_size=1,
    color_mode="grayscale",
    class_mode=None,
    shuffle=False)

# make the prediction
prediction = model.predict(
    test_generator, verbose=1)
# print(model.get_config())
# print(model.get_weights())
# model.predict_on_batch();
print(prediction)
