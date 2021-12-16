from keras.preprocessing.image import ImageDataGenerator
from keras.saving.hdf5_format import load_weights_from_hdf5_group
from numpy.lib.type_check import mintypecode

def getPredictionShoesOrNot(img, model):
    
    # make the prediction
    prediction = model.predict(
        img, verbose=0)

    return prediction



