
from utilities.Herald import Herald
from utilities.configUtilities.ProcConfig import ProcConfig

class ShoeExtractor:
    
    def isThereShoe(img, model):
        """Makes the prediction:
        
        If prediction near 1: There is a shoe
        
        If prediction near 0: There is NO shoe.
        """
        prediction = model.predict( img, verbose=(1 if ProcConfig.iaShouldTalkInDetail() else 0) )
        return prediction[0][0]