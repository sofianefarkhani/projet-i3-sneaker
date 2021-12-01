from keras.backend import mean
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
lstImg = ['DC3432_001-1--830a7406-9152-41e1-9e4a-d3a96b13edb8.png',
          'DC3432_001-2--90db9fb0-1771-4b1f-af1a-2c0cfad260fc.png',
          'DC3432_001-3--c239e5f3-3865-4fad-b6f6-cf7948dcb34b.png',
          'DC3432_001-4--84d49666-cf3a-4b44-a0bd-e8bbe6cfda45.png',
          'DC3432_007-2--7faec874-c3ee-4c15-88fe-dc83b5b04ec4.png',
          'DC3432_007-3--af14b088-8cd9-472e-be8d-cd544ae56aef.png',
          'DC3432_008-1--fa62240b-9ff8-4ed5-bb97-cbc6cad303c3.png',
          'DC3432_008-3--716c4f02-57d0-43ef-a704-a639e834c89d.png',
          'DC3432_008-4--de9ed675-9170-429e-aca1-10b63df7849d.png',
          'DC3432_125-1--7dca0653-d22b-4a62-bc24-1c4dbec690ae.png',
          'DC3432_125-3--7455f321-7da7-422f-afec-ed1b89ebe58c.png',
          'DC3432_188-1--45db97fc-7488-4307-9f05-c90cbe54d1fd.png',
          'DC3432_188-2--6b9bc6e5-3e17-4914-b80a-2e4ae244d922.png']

lstPrediction = []

for img in lstImg:
    img = loadImage(path + img)
    lstPrediction.append(getPredictionShoesOrNot(img, model)[0][0])

print(lstPrediction)
# print("Moyenne: " + str(mean(lstPrediction)))
print("Moyenne v2: " + str(np.mean(lstPrediction)))

# semble être plus pertinant, à tester sur un groupe d'image dont les probas sont vraiment différentes (genre 0.3; 0.7; 0.9)
print("Médiane: " + str(np.median(lstPrediction)))
