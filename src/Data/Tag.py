from Data.Color import Color
#from Type import Type
import json
from Data.Type import Type

class Tag():
    '''
     A tag represents the data concerning one shoe.
     
     All the following values: 
        - int: databaseID
        - Type: type
        - mainColor: Color
     Have to be defined for the Tag to be complete.
      
     The secondary color: "secondaryColor", is not mandatory for the tag to be complete. 
    '''
    
    def __init__(self, databaseID:int, type:Type=None, mainColor:Color=None, secondaryColor:Color=None):
        '''Instantiates a new Tag.
        
        The expected values in the constructor are, in order:
            -databaseID, the integer representing the id of the picture in the database (must be given in constructor)
            -type, the detected Type of the shoe (can be added later)
            -mainColor, the detected main Color of the shoe
            -secondaryColor, the secondary color of the shoe (if detected)
        '''
        self.databaseID = databaseID
        if type is not None: self.type = type
        if mainColor is not None: self.mainColor = mainColor
        if secondaryColor is not None: self.secondaryColor = secondaryColor
    
    
    
    ####### GETTERS, SETTERS
    
    def isComplete(self):
        return hasattr(self, 'databaseID', 'type', 'mainColor')
    
    def hasSecondaryColor(self):
        return hasattr(self, 'secondaryColor')
    
    def setType(self, type:Type):
        self.type = type
    
    def setMainColor(self, color:Color):
        self.mainColor = color
    
    def setSecondaryColor(self, color:Color):
        self.secondaryColor = color
        
    def toString(self):
        return self.__dict__
    
    