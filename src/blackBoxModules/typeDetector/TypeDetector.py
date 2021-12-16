

from Data.Type import Type
from utilities.Herald import Herald
from utilities.configUtilities.ProcConfig import ProcConfig

class TypeDetector:
    
    
    def detectTypeOfShoe(image, model):
        prediction = model.predict( image, verbose=(1 if ProcConfig.iaShouldTalkInDetail() else 0) )
        return prediction.tolist()[0] # a table of [high, low, mid] prediction: each of them floats between 0 and 1.