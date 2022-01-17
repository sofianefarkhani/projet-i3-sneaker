
import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '4'

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
from trainAI.getDatasetTrainingIA import getDataseTrainingIAFromJson
import tensorflow as tf
from keras.callbacks import ModelCheckpoint
import os 
import datetime

# https://towardsdatascience.com/10-minutes-to-building-a-cnn-binary-image-classifier-in-tensorflow-4e216b2034aa

# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
# os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_DEVICE_ORDER"]="FASTEST_FIRST"
# os.environ["CUDA_VISIBLE_DEVICES"]="2,1,0"
# os.environ["TF_GPU_THREAD_MODE"]="gpu_private"

gpu_devices = tf.config.experimental.list_physical_devices('GPU')
for device in gpu_devices:
    tf.config.experimental.set_memory_growth(device, True)

# import os
# os.add_dll_directory("C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v11.2\\bin")


# @tf.function(jit_compile=True)
def trainAIV1():
    tf.config.list_physical_devices('GPU') 
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
    model.add(Dense(units=2048, activation='relu', kernel_initializer='random_normal',
                    bias_initializer='zeros'
                    ))
    model.add(Dropout(0.8))
    model.add(Dense(units=4, activation='softmax'))
    # model.add(Dense(units=4))


    # 0.0001 
    model.compile(loss='categorical_crossentropy',optimizer=RMSprop(learning_rate=0.0004),metrics='accuracy')
    # model.compile(optimizer='adam',
    #           loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    #           metrics=['accuracy'])


    checkpoint = ModelCheckpoint("../in/AI/DetectType/best_weights.h5", monitor='val_accuracy', verbose=1,save_best_only=True, mode='max')
    (trainingSet, testSet) = getDataseTrainingIAFromJson(
        target_size=(200, 200), ratio=0.8, pathJson="D:\projet_IA\projet-i3-sneaker\data4class.json")
    model.summary()

    # log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    # tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
    # callbacks_list = [checkpoint, tensorboard_callback]
    callbacks_list = [checkpoint]


    # set steps_per_epoch=3000 and validation_steps=1000 with real data
    model.save("../in/AI/DetectType/model.h5", overwrite=True)
    model.fit(trainingSet, validation_data=testSet, batch_size=16, epochs=500, callbacks=callbacks_list)
    model.save_weights('../in/AI/DetectType/weights.h5', overwrite=True)
    

# with tf.device('/cpu:0'):
with tf.device("/gpu:1"):
    trainAIV1()
# trainAIV1()
exit()


#predict after train
model = load_model('../in/AI/DetectType/model.h5')
model.load_weights('../in/AI/DetectType/weights.h5')

