import pandas
from keras.preprocessing.image import ImageDataGenerator
from interface.JsonReader import JsonReader
from interface.ConfigLoader import ConfigLoader
import random

def getDataseTrainingIA(target_size=(64, 64), ratio=0.8):
    # Fitting the CNN to the images
    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True
    )

    test_datagen = ImageDataGenerator(
        rescale=1. / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

    (imagesNames, imagesLabels) = JsonReader.getDataForIATypeTraining(typeAsString=True)
    dataset = {
        'id': imagesNames,
        'label': imagesLabels
    }

    # Need randomize the dataset order before separate it in two part
    (dataFrameTraining, dataFrameTest) = shuffleDataSet(dataset, ratio)

    dataFrameTraining = pandas.DataFrame(data=dataFrameTraining)
    dataFrameTest = pandas.DataFrame(data=dataFrameTest)

    
    trainingSet = train_datagen.flow_from_dataframe(
        dataframe=dataFrameTraining,
        directory=ConfigLoader.getVariable('input', 'trainingImagesFolder'),
        x_col="id",
        y_col="label",
        target_size=target_size,
        batch_size=32,
        color_mode="grayscale",
        class_mode='binary')

    testSet = test_datagen.flow_from_dataframe(
        dataframe=dataFrameTest,
        directory=ConfigLoader.getVariable('input', 'trainingImagesFolder'),
        x_col="id",
        y_col="label",
        target_size=target_size,
        batch_size=32,
        color_mode="grayscale",
        class_mode='binary')

    return (trainingSet, testSet)


def shuffleDataSet(dataset, ratio):
    lstLabel = []
    for label in dataset['label']:
        isNewLabel = True
        for l in lstLabel:
            if l == label:
                isNewLabel = False
                break
        if isNewLabel:
            lstLabel.append(label)
    
    idTraining = []
    labelTraining = []
    idTest = []
    labelTest = []

    for label in lstLabel:
        lstIndex = []
        for i in range(len(dataset['label'])):
            if dataset['label'][i] == label:
                lstIndex.append(i)
        random.shuffle(lstIndex)
        for idIndex in lstIndex[:int(len(lstIndex)*ratio)]:
            idTraining.append(dataset['id'][idIndex])
            labelTraining.append(label)
        for idIndex in lstIndex[int(len(lstIndex)*ratio):]:
            idTest.append(dataset['id'][idIndex])
            labelTest.append(label)

    dataFrameTraining = {'id': idTraining, 'label': labelTraining}
    dataFrameTest = {'id': idTest, 'label': labelTest}

    return (dataFrameTraining, dataFrameTest)

def getDataseTrainingIAFromJson(target_size=(64, 64), ratio=0.8, pathJson=None):
    # Fitting the CNN to the images
    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True
    )

    test_datagen = ImageDataGenerator(
        rescale=1. / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

    import json
    f = open(pathJson)
    dataset = json.load(f)
    f.close()

    print(dataset)

    # Need randomize the dataset order before separate it in two part
    (dataFrameTraining, dataFrameTest) = shuffleDataSet(dataset, ratio)

    dataFrameTraining = pandas.DataFrame(data=dataFrameTraining)
    dataFrameTest = pandas.DataFrame(data=dataFrameTest)

    
    trainingSet = train_datagen.flow_from_dataframe(
        dataframe=dataFrameTraining,
        x_col="id",
        y_col="label",
        target_size=target_size,
        batch_size=32,
        color_mode="grayscale",
        class_mode='categorical')

    testSet = test_datagen.flow_from_dataframe(
        dataframe=dataFrameTest,
        x_col="id",
        y_col="label",
        target_size=target_size,
        batch_size=32,
        color_mode="grayscale",
        class_mode='categorical')

    return (trainingSet, testSet)