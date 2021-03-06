
from utilities.config.getters.TalkConfig import TalkConfig as TC 

class ShoeExtractor:
    
    def isThereShoe(img, model):
        """Makes the prediction:
        
        If prediction near 1: There is a shoe
        
        If prediction near 0: There is NO shoe."""
        
        prediction = model.predict( img, verbose=(1 if TC.getIADetails() else 0) )
        return prediction[0][0]