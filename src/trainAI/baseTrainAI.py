from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten, Activation, Dropout
from keras.layers import Dense
from keras import callbacks
from trainAI.getDatasetTrainingIA import getDataseTrainingIA

def trainAIV1():
    model = Sequential()

    # Convolution
    model.add(Conv2D(32, (3, 3), input_shape=(64, 64, 1)))
    model.add(Activation("relu"))
    # Pooling
    model.add(MaxPooling2D(pool_size=(2, 2)))
    # Adding a second convolutional layer
    model.add(Conv2D(32, (3, 3)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    # Flattening
    model.add(Flatten())

    # Full connection
    model.add(Dense(units=128, activation='relu'))
    model.add(Dense(units=1, activation='softmax'))
    model.add(Activation("relu"))
    model.add(Dropout(0.5))
    # Compiling the CNN
    model.compile(optimizer='adam', loss='binary_crossentropy',
                metrics=['accuracy'])
    model.summary()

    (trainingSet, testSet) = getDataseTrainingIA(target_size=(64, 64), ratio=0.8)


    model.fit(trainingSet, validation_data=testSet, epochs=5,
            validation_steps=30, steps_per_epoch=30)  # set steps_per_epoch=3000 and validation_steps=1000 with real data

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
