import numpy as np
import tensorflow as tf
from predictAI.getPredictionAI import getPredictionShoesOrNot
from keras.models import load_model


def loadImage(path):
    img = tf.keras.preprocessing.image.load_img(
        path, color_mode="grayscale", target_size=(200, 200))
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = img.astype('float32')/255.
    img = np.array([img])  # Convert single image to a batch.
    return img


model = load_model('model.h5')
model.load_weights('weights.h5')

img = loadImage('/mnt/424cf323-70f0-406a-ae71-29e3da370aec/Sneaker-data/test_temp/Nouveau dossier/6836-2--55e3d05d-e4c8-4105-acbf-df9d25f0a61a.jpg')
getPredictionShoesOrNot(img, model)

