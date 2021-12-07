# import hashlib

# lst_name = []
# lst_hash = []
# lst_name_to_delete = []
# lst_temp_index_to_delete = []


# path = "D:/Images/resources/"

# f = open("C:/Users/moonc/Desktop/shoes.txt", "r")
# for line in f:
#     lst_name.append(line.split("\n")[0])

# for name in lst_name:
#     with open(path+name, "rb") as f:
#         bytes = f.read()
#         lst_hash.append(hashlib.sha256(bytes).hexdigest())
#         f.close()

# indexDone = -1
# while indexDone < len(lst_name)-1:
#     indexDone+=1
#     hashToCheck = lst_hash[indexDone]
#     for i in range(indexDone+1, len(lst_hash)):
#         if lst_hash[i] == hashToCheck:
#             lst_temp_index_to_delete.append(i)

#     lst_temp_index_to_delete.reverse()
#     for i in lst_temp_index_to_delete:
#         lst_name_to_delete.append(lst_name[i])
#         del lst_name[i]
#         del lst_hash[i]
#     lst_temp_index_to_delete.clear()


# newFileString = ""
# f = open("C:/Users/moonc/Desktop/shoes.txt", "r")
# for line in f:
#     if(not line.split("\n")[0] in lst_name_to_delete):
#         newFileString+=line.split("\n")[0] + '\n'
    
# f.close()
# # print(newFileString)

# f = open("C:/Users/moonc/Desktop/shoesNoDuplicate.txt", "w")
# f.write(newFileString)
# f.close()


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

path = 'D:/Images/resources/'

f = open("C:/Users/moonc/Desktop/shoesNoDuplicate.txt", "r")
lstImg = []
for line in f:
    lstImg.append(line.split("\n")[0])

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
    if nbImg%500 == 0:
        print("load img: " + str(nbImg))

nbImg = 0
for img in lstImgData:
    nbImg+=1
    lstPrediction.append(getPredictionShoesOrNot(img, model)[0][0])
    if nbImg%500 == 0:
        print("predict img: " + str(nbImg))

print(lstPrediction)
print("Moyenne v2: " + str(np.mean(lstPrediction)))

nb = 0
for x in lstPrediction:
    if x > 0.5:
        nb+=1

print("nb = " + str(nb) + "  / " + str(len(lstPrediction)))

# semble être plus pertinant, à tester sur un groupe d'image dont les probas sont vraiment différentes (genre 0.3; 0.7; 0.9)
# print("Médiane: " + str(np.median(lstPrediction)))
# https://support.minitab.com/fr-fr/minitab/18/help-and-how-to/statistics/basic-statistics/how-to/store-descriptive-statistics/interpret-the-statistics/interpret-the-statistics/
