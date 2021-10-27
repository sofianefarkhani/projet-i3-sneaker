

from Data.Type import Type

from processes.Utilities import Utilities

class TypeDetector:
    
    
    def detectTypeOfShoe(image, procName):
        if Utilities.iaShouldTalkInDetail(): print("%s: Detecting the type of the shoe"%procName)
        return Type.HIGH