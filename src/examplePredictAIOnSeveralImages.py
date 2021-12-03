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


model = load_model('../in/AI/DetectShoes/model.h5')
model.load_weights('../in/AI/DetectShoes/weights.h5')

path = '/home/vedoc/Bureau/projet-i3-sneaker/img/train/trainingTestImages_hdd/'
lstImg = ['CZ8281_005-2--26d0a1ca-591c-4f50-8459-388c868e8266.png',
          'CZ8281_005-3--dbf6e79d-30d0-4941-9231-8bf28aa125c0.png',
          'CZ8281_005-4--445592a0-ca45-4cac-a8c5-4350db2470a0.png',
          'CZ8281_010-3--db011cde-4f18-4cb2-b1a6-0fecce0efc51.png',
          'CZ8281_011-2--5628292c-9566-4e77-8efa-e04759dd4eac.png',
          'CZ8281_011-3--fb54830a-11f8-4c87-8222-bd70c8fe141f.png',
          'CZ8281_100-1--16067ee3-3bf9-4b75-b740-60a77c222961.png',
          'CZ8281_100-4--a63fdb82-c237-44c7-b7cd-b226081b90ae.png',
          'CZ8281_606-1--47c521fe-f0ad-4cb2-a15d-e3246361a1ed.png',
          'CZ8281_606-3--d1352aed-df91-4c7c-a8b8-f62f7bc29c53.png',
          'CZ8281_606-4--9f6d4318-c776-4609-8ecc-2576d293b374.png']

lstPrediction = []

for img in lstImg:
    img = loadImage(path + img)
    lstPrediction.append(getPredictionShoesOrNot(img, model)[0][0])

print(lstPrediction)
# print("Moyenne v2: " + str(np.mean(lstPrediction)))

# semble être plus pertinant, à tester sur un groupe d'image dont les probas sont vraiment différentes (genre 0.3; 0.7; 0.9)
print("Médiane: " + str(np.median(lstPrediction)))
# https://support.minitab.com/fr-fr/minitab/18/help-and-how-to/statistics/basic-statistics/how-to/store-descriptive-statistics/interpret-the-statistics/interpret-the-statistics/
