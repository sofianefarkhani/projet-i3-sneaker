
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '4'

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
from trainAI.getDatasetTrainingIA import getDataseTrainingIA, getDataseTrainingIAFromJson
import tensorflow as tf
from keras.callbacks import ModelCheckpoint
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
    model.add(Dropout(0.25))
    model.add(Dense(units=3, activation='sigmoid'))# softmax??

    
    model.compile(loss='categorical_crossentropy',optimizer=RMSprop(learning_rate=0.001),metrics='accuracy')

    model.summary()

    checkpoint = ModelCheckpoint("../in/AI/DetectType/best_weights.h5", monitor='val_accuracy', verbose=1,save_best_only=True, mode='max')
    callbacks_list = [checkpoint]
    (trainingSet, testSet) = getDataseTrainingIAFromJson(
        target_size=(200, 200), ratio=0.8, pathJson="/mnt/424cf323-70f0-406a-ae71-29e3da370aec/data.json")

    # set steps_per_epoch=3000 and validation_steps=1000 with real data
    model.fit(trainingSet, validation_data=testSet, batch_size=32, epochs=100, callbacks=callbacks_list)
    model.save("../in/AI/DetectType/model.h5", overwrite=True)
    model.save_weights('../in/AI/DetectType/weights.h5', overwrite=True)

# with tf.device('/cpu:0'):
with tf.device("/gpu:0"):
    trainAIV1()
exit()


#predict after train
model = load_model('../in/AI/DetectType/model.h5')
model.load_weights('../in/AI/DetectType/weights.h5')

