

from Data.Type import Type

from processes.Utilities import Utilities

class TypeDetector:
    
    
    def detectTypeOfShoe(image):
        if Utilities.iaShouldTalk(): print("Detecting the type of the shoe")
        return Type.HIGH