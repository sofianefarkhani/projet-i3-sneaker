from os import path

from predictAI.getPredictionAI import getPredictionShoesOrNot


def getStringToAddToTrainData(nameOfFile, isAShoes, needBreakLine=True):
    return '{"py/object": "Data.TrainDataElement.TrainDataElement", "imageName": "'+nameOfFile+'", "isThereAShoe": true, "shoeType": {"py/reduce": [{"py/type": "Data.Type.Type"}, {"py/tuple": ['+str(isAShoes)+']}]}}' + ("\n" if needBreakLine else "")


def getNameImageFromTrainData(pathTrainData="../in/trainData.json"):
    f = open(pathTrainData, "r")
    lst_name_shoes = []
    lst_name_other = []
    for line in f:
        name = line.split("imageName\"")[1].split("\"")[1].split("\"")[0]
        if line.split('}, {"py/tuple": [')[1].split(']')[0] == "0":
            lst_name_shoes.append(name)
        else:
            lst_name_other.append(name)
    return (lst_name_shoes, lst_name_other)


def getIsShoes(nameImage, pathTrainData="../in/trainData.json"):
    f = open(pathTrainData, "r")
    for line in f:
        name = line.split("imageName\"")[1].split("\"")[1].split("\"")[0]
        if name == nameImage:
            return line.split('}, {"py/tuple": [')[1].split(']')[0]
    return "Error"


def writeNewTrainData(pathTrainData, lst_name_shoes, lst_name_other):
    newFileString = ""
    for nameImage in lst_name_shoes:
        newFileString+= getStringToAddToTrainData(nameImage, "0")
    for nameImage in lst_name_other:
        newFileString+= getStringToAddToTrainData(nameImage, "1")
    f = open(pathTrainData, "w")
    f.write(newFileString)
    f.close()

def copyImageToFolder(pathSource, pathDestination, nameImage):
    from shutil import copyfile
    copyfile(pathSource + nameImage, pathDestination + nameImage)

def copyImageListToFolder(pathSource, pathDestination, lstNameImage):
    from shutil import copyfile
    for nameImage in lstNameImage:
        copyfile(pathSource + nameImage, pathDestination + nameImage)

def listerFilesInFolder(folderPath):
    from os import listdir
    from os.path import isfile, join
    fichiers = [f for f in listdir(folderPath) if isfile(join(folderPath, f))]
    return fichiers

def showImage(imagePath):
    import cv2
    im = cv2.imread(imagePath)
    im=cv2.resize(im, (200, 200))
    cv2.imshow("test", im)
    cv2.waitKey()

def getRandomImageNotInTrainData(numberOfImage, pathTrainData, pathAllImage = None, pathFileAllImage = None):
    import random
    import hashlib

    lstAllImage = []
    if pathAllImage is not None:
        f = open(pathFileAllImage, "r")
        for line in f:
            lstAllImage.append(line.replace("\n", ""))
    else:
        lstAllImage.extend(listerFilesInFolder(pathAllImage))
    (lst_name_shoes, lst_name_other) = getNameImageFromTrainData(pathTrainData)
    lstAllImageUseInTrainData = []
    lstAllImageUseInTrainData.extend(lst_name_shoes)
    lstAllImageUseInTrainData.extend(lst_name_other)

    lstChoice = []
    lstHashOfChoice = []
    for img in lstAllImageUseInTrainData:
        with open(pathAllImage+img, "rb") as f:
            bytes = f.read()
            hash = hashlib.sha256(bytes).hexdigest()
            lstHashOfChoice.append(hash)
    for i in range(numberOfImage):
        isOk = False
        while not isOk:
            choice = random.choice(lstAllImage)
            if choice not in lstChoice:
                with open(pathAllImage+choice, "rb") as f:
                    bytes = f.read()
                    hash = hashlib.sha256(bytes).hexdigest()
                    if hash not in lstHashOfChoice:
                        lstHashOfChoice.append(hash)
                        lstChoice.append(choice)
                        isOk = True

                    f.close()
    
    return lstChoice

def getPrediction(imagePath):
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

    img = loadImage(imagePath)
    return getPredictionShoesOrNot(img, model)[0][0]




# (lst_name_shoes, lst_name_other) = getNameImageFromTrainData()
# print(len(lst_name_shoes))
# print(len(lst_name_other))

# print(getStringToAddToTrainData("test.jpg", 0))
# print(getStringToAddToTrainData("test123.jpg", 1))

# print(getIsShoes(getNameImageFromTrainData()[0][0]))
# print(getIsShoes(getNameImageFromTrainData()[2][0]))

# (lst_name_shoes, lst_name_other) = getNameImageFromTrainData()
# writeNewTrainData("../in/trainDataV56132.json", lst_name_shoes, lst_name_other)

# pathSource = "/mnt/424cf323-70f0-406a-ae71-29e3da370aec/Sneaker-data/test_temp/Nouveau dossier/test/test1/"
# pathDest = "/mnt/424cf323-70f0-406a-ae71-29e3da370aec/Sneaker-data/test_temp/Nouveau dossier/test/test2/"
# copyImageToFolder(pathSource, pathDest, listerFilesInFolder(pathSource)[0])
# print(listerFilesInFolder(pathDest))

# pathSource = "/mnt/424cf323-70f0-406a-ae71-29e3da370aec/Sneaker-data/test_temp/Nouveau dossier/test/test1/"
# showImage(pathSource + listerFilesInFolder(pathSource)[0])

lstImage = getRandomImageNotInTrainData(30, "../in/trainDataV3.json", "D:/Images/resources/", "C:/Users/moonc/Desktop/lst_nom.txt")
path = "D:/Images/resources/"
for x in lstImage:
    print(x + " -> ", end="")
    predict = getPrediction(path + x)
    print(("shoe" if predict> 0.5 else "other"), end="")
    proba = predict-0.5 if predict > 0.5 else 0.5-predict
    proba*=2
    print("  proba=" + str(proba))
    showImage(path + x)
