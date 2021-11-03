

from Data.Type import Type
from interface.Herald import Herald

from processes.Utilities import Utilities

class TypeDetector:
    
    
    def detectTypeOfShoe(image, procName):
        Herald.printTypeDetection(procName)
        return Type.HIGH