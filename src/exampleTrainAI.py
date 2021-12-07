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
import tensorflow as tf

# https://towardsdatascience.com/10-minutes-to-building-a-cnn-binary-image-classifier-in-tensorflow-4e216b2034aa

import os 
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import os
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="0"

gpu_devices = tf.config.experimental.list_physical_devices('GPU')
for device in gpu_devices:
    tf.config.experimental.set_memory_growth(device, True)



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
    model.compile(loss='binary_crossentropy',optimizer=RMSprop(learning_rate=0.001),metrics='accuracy')

    model.summary()

    (trainingSet, testSet) = getDataseTrainingIA(
        target_size=(200, 200), ratio=0.8)

    # set steps_per_epoch=3000 and validation_steps=1000 with real data
    model.fit(trainingSet, validation_data=testSet, batch_size=32, epochs=4)
    model.save("../in/AI/DetectShoes/model.h5", overwrite=True)
    model.save_weights('../in/AI/DetectShoes/weights.h5', overwrite=True)

    # test_datagen = ImageDataGenerator(rescale=1./255)
    # test_generator = test_datagen.flow_from_directory(
    #     "/home/vedoc/Images/Sneaker-data/test_temp",
    #     target_size=(200, 200),
    #     batch_size=32,
    #     color_mode="grayscale",
    #     class_mode=None,
    #     shuffle=False)

    # # make the prediction
    # prediction = model.predict(
    #     test_generator, verbose=1, steps=len(test_generator.filenames))
    # # print(model.get_config())
    # # print(model.get_weights())
    # # model.predict_on_batch();
    # print(prediction)

# with tf.device('/cpu:0'):
with tf.device("/gpu:0"):
    trainAIV1()
exit()


#predict after train
model = load_model('../in/AI/DetectShoes/model.h5')
model.load_weights('../in/AI/DetectShoes/weights.h5')


test_datagen = ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_directory(
    "/mnt/424cf323-70f0-406a-ae71-29e3da370aec/Sneaker-data/test_temp/",
    target_size=(200, 200),
    batch_size=1,
    color_mode="grayscale",
    class_mode=None,
    shuffle=False)

# make the prediction
predictions = model.predict(
    test_generator, verbose=1)

# print(model.get_config())
# print(model.get_weights())
# model.predict_on_batch();
print(predictions)

# with open("output.txt", "w") as txt_file:
#     for line in predictions:
#         txt_file.write(" ".join(line) + "\n")