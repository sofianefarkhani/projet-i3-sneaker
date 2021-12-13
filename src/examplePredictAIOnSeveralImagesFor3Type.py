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


model = load_model('../in/AI/DetectType/model.h5')
model.load_weights('../in/AI/DetectType/weights.h5')

path = '/mnt/424cf323-70f0-406a-ae71-29e3da370aec/allDataWithoutDoublon/'

import json
f = open("/home/vedoc/Bureau/projet-i3-sneaker/data3class.json")
dataset = json.load(f)
f.close()
lstImg = dataset['id']

lstPrediction = []
nbImg = 0

lstImgData = []
for img in lstImg:
    nbImg+=1
    lstImgData.append(loadImage(path + img))

nbImg = 0
for img in lstImgData:
    nbImg+=1
    prediction = getPredictionShoesOrNot(img, model)
    print("predict img: " + lstImg[nbImg-1] + "   ->   ", end="")
    print(prediction)

