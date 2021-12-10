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
print(dataset)
lstImg = dataset['id']

# lstImg = lstImg[:5]

lstPrediction = []
nbImg = 0
# for img in lstImg:
#     nbImg+=1
#     img = loadImage(path + img)
#     lstPrediction.append(getPredictionShoesOrNot(img, model)[0][0])
#     if nbImg%500 == 0:
#         print(nbImg)

lstImgData = []
for img in lstImg:
    nbImg+=1
    lstImgData.append(loadImage(path + img))

nbImg = 0
for img in lstImgData:
    nbImg+=1
    prediction = getPredictionShoesOrNot(img, model)
    # lstPrediction.append([0][0])
    # if nbImg%500 == 0:
    print("predict img: " + lstImg[nbImg-1] + "   ->   ", end="")
    print(prediction)

# print(lstPrediction)
# print("Moyenne v2: " + str(np.mean(lstPrediction)))

# nb = 0
# for x in lstPrediction:
#     if x > 0.5:
#         nb+=1

# print("nb = " + str(nb) + "  / " + str(len(lstPrediction)))

# # semble être plus pertinant, à tester sur un groupe d'image dont les probas sont vraiment différentes (genre 0.3; 0.7; 0.9)
# # print("Médiane: " + str(np.median(lstPrediction)))
# # https://support.minitab.com/fr-fr/minitab/18/help-and-how-to/statistics/basic-statistics/how-to/store-descriptive-statistics/interpret-the-statistics/interpret-the-statistics/
