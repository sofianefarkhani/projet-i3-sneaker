from enum import Enum

class Type(Enum):
    LOW = 0
    HIGH = 1
    
    
    def getType(name):
        for t in Type:
            if t.name == name.upper():
                return t
        return None