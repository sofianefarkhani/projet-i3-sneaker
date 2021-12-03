from keras.datasets.fashion_mnist import load_data
from keras.layers.normalization.batch_normalization import BatchNormalization
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten, Activation, Dropout
from keras.layers import Dense
from keras import callbacks
from tensorflow.keras.utils import to_categorical

model = Sequential()

# first CONV => RELU => CONV => RELU => POOL layer set
model.add(Conv2D(32, (3, 3), input_shape=(28, 28, 1), padding="same"))
model.add(Conv2D(32, (3, 3), padding="same",
                 input_shape=(28, 28, 1)))
model.add(Activation("relu"))
model.add(BatchNormalization(axis=1))
model.add(Conv2D(32, (3, 3), padding="same"))
model.add(Activation("relu"))
model.add(BatchNormalization(axis=1))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
# second CONV => RELU => CONV => RELU => POOL layer set
model.add(Conv2D(64, (3, 3), padding="same"))
model.add(Activation("relu"))
model.add(BatchNormalization(axis=1))
model.add(Conv2D(64, (3, 3), padding="same"))
model.add(Activation("relu"))
model.add(BatchNormalization(axis=1))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
# First (and only) set of FC => RELU layers
model.add(Flatten())
model.add(Dense(512))
model.add(Activation("relu"))
model.add(BatchNormalization())
model.add(Dropout(0.5))
# Softmax classifier
model.add(Dense(10))
model.add(Activation("softmax"))
# Compiling the CNN
model.compile(optimizer='adam', loss='categorical_crossentropy',
              metrics=['accuracy'])
model.summary()

(xTrain, yTrain), (xTest, yTest) = load_data()

xTrain = xTrain.reshape((xTrain.shape[0], 28, 28, 1))
xTest = xTest.reshape((xTest.shape[0], 28, 28, 1))

xTrain = xTrain.astype("float32") / 255.0
xTest = xTest.astype("float32") / 255.0
yTrain = to_categorical(yTrain, 10)
yTest = to_categorical(yTest, 10)

model.fit(x=xTrain, y=yTrain,
          validation_data=(xTest, yTest),
          batch_size=32, epochs=25)


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
