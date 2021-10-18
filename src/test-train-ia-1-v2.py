from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten, Activation, Dropout
from keras.layers import Dense
from keras import callbacks
import os.path
import jsonpickle
import pandas
import json

from keras.preprocessing.image import ImageDataGenerator

model = Sequential()

# Step 1 - Convolution
model.add(Conv2D(32, (3, 3), input_shape=(64, 64, 1)))
model.add(Activation("relu"))
# Step 2 - Pooling
model.add(MaxPooling2D(pool_size=(2, 2)))
# Adding a second convolutional layer
model.add(Conv2D(32, (3, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))
# Step 3 - Flattening
model.add(Flatten())

# Step 4 - Full connection
model.add(Dense(units=128, activation='relu'))
model.add(Dense(units=1, activation='softmax'))
model.add(Activation("relu"))
model.add(Dropout(0.5))
# Compiling the CNN
model.compile(optimizer='adam', loss='binary_crossentropy',
              metrics=['accuracy'])
model.summary()

# Part 2 - Fitting the CNN to the images
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(
    rescale=1. / 255)

with open('../img/datasetLabelType.json') as json_file:
    dataframeTraining = json.load(json_file)

dataframeTraining = pandas.DataFrame(data=dataframeTraining)


trainingSet = train_datagen.flow_from_dataframe(
    dataframe=dataframeTraining,
    directory="../img/test/",
    x_col="id",
    y_col="label",
    target_size=(64, 64),
    batch_size=32,
    color_mode="grayscale",
    class_mode='binary')


testSet = test_datagen.flow_from_dataframe(
    dataframe=dataframeTraining,
    directory="../img/test/",
    x_col="id",
    y_col="label",
    target_size=(64, 64),
    batch_size=32,
    color_mode="grayscale",
    class_mode='binary')


model.fit(trainingSet, validation_data=testSet, epochs=5,
          validation_steps=1000, steps_per_epoch=100)  # set steps_per_epoch = 3000 with real data

# """
# Tensorboard log
# """
# log_dir = 'tf_log'
# tb_cb = callbacks.TensorBoard(log_dir=log_dir, histogram_freq=0)
# cbks = [tb_cb]

# # If the CNN weight model already exists make predictions
# if os.path.isfile("weights.h5") & os.path.isfile("model.h5"):
#     print("CNN Weight and models already exists, make the predictions")
# # Else Load the data and store the CNN weight model
# else:
#     model.fit(trainingSet, validation_data=testSet, epochs=5,
#               callbacks=cbks, validation_steps=1000, steps_per_epoch=3)

#     model.save("model.h5")
#     model.save_weights('weights.h5', overwrite=True)
