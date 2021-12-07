from keras.preprocessing.image import ImageDataGenerator

def getPredictionShoesOrNot(img, model):
    
    # make the prediction
    prediction = model.predict(
        img, verbose=0)

    return prediction
