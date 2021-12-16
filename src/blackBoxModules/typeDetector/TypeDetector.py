
from utilities.config.getters.TalkConfig import TalkConfig as TC

class TypeDetector:
    
    
    def detectTypeOfShoe(image, model):
        prediction = model.predict( image, verbose=(1 if TC.getIADetails() else 0) )
        return prediction.tolist()[0] # a table of [high, low, mid] prediction: each of them floats between 0 and 1.