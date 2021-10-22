import pandas
from keras.preprocessing.image import ImageDataGenerator
from interface.JsonReader import JsonReader
from interface.ConfigLoader import ConfigLoader

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
    dataFrameTraining = {'id': dataset['id'][:int(len(
        dataset['id'])*ratio)], 'label': dataset['label'][:int(len(dataset['label'])*ratio)]}
    dataFrameTest = {'id': dataset['id'][int(len(
        dataset['id'])*ratio):], 'label': dataset['label'][int(len(dataset['label'])*ratio):]}

    dataFrameTraining = pandas.DataFrame(data=dataFrameTraining)
    dataFrameTest = pandas.DataFrame(data=dataFrameTest)

    # import os
    # print("##############################  "+str(os.getcwd())) 
    
    
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
