
import os
from keras import layers
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
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import RMSprop
from trainAI.getDatasetTrainingIA import getDataseTrainingIAFromJsonV2Color
import tensorflow as tf
from keras.callbacks import ModelCheckpoint
import os 
from tensorflow.keras import layers, models, optimizers

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
    (trainingSet, testSet) = getDataseTrainingIAFromJsonV2Color(
        target_size=(224, 224), ratio=0.8, pathJson="D:\projet_IA\projet-i3-sneaker\data4class.json") 

    NCLASSES = 4
    HEIGHT = 224
    WIDTH = 224
    NUM_CHANNELS = 3
    BATCH_SIZE = 32
    base_model = tf.keras.applications.vgg19.VGG19(input_shape=(HEIGHT, WIDTH, NUM_CHANNELS), include_top=False, weights='imagenet')
    base_model.trainable = False
    x = base_model.output
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dense(4, activation='softmax')(x)
    model = models.Model(inputs=base_model.input, outputs=x)
    print(model.summary())


    checkpoint = ModelCheckpoint("../in/AI/DetectType/best_weights.h5", monitor='val_accuracy', verbose=1,save_best_only=True, mode='max')
   
    model.summary()

    base_learning_rate = 0.00004
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=base_learning_rate),
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


    # log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    # tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
    # callbacks_list = [checkpoint, tensorboard_callback]

    callbacks_list = [checkpoint]

    # set steps_per_epoch=3000 and validation_steps=1000 with real data
    model.save("../in/AI/DetectType/model.h5", overwrite=True)
    # model.fit(trainingSet, validation_data=testSet, batch_size=16, epochs=100, callbacks=callbacks_list)
    model.fit(trainingSet, validation_data=testSet, epochs=500, batch_size=16, steps_per_epoch=50, callbacks=callbacks_list)
    model.save_weights('../in/AI/DetectType/weights.h5', overwrite=True)
    

# with tf.device('/cpu:0'):
with tf.device("/gpu:1"):
    trainAIV1()
# trainAIV1()
exit()


#predict after train
model = load_model('../in/AI/DetectType/model.h5')
model.load_weights('../in/AI/DetectType/weights.h5')

