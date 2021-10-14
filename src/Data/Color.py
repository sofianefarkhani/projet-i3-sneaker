
from typing import List
from Data.BasicColors import ColorEnum
import json


class Color():
    '''A color stores attributes of RGB format, and if given, the name of the color.
    
    An instance of color should have the following variables:
        - "name", the color's name (this is mandatory);
        - "rgb", a RGB code, in the form [int, int, int]  (not mandatory).
        
    Author: Esteban'''
    
    
    
    def __init__(self, name:str=None, rgb:List[int]=None):
        '''Creates a color.
        
            -If only given the color's name, will create the RGB code from the corresponding color in BasicColors(Enum).
                ->If no predefined color has this name, raises an exception.
        
            -If only given the rgb values, searches for the closest Color in BasicColors(Enum).
        
            -If given both, creates an entirely new color. 
        '''
        
        if ((name is None) and (rgb is None)):
            raise ValueError('Cannot create a color without either a name or an rgb code.')
        
        elif (rgb is not None and len(rgb) != 3):
            raise ValueError('Please give me an rgb List of length 3, and not '+str(len(rgb))+", like you just did.")
        
        elif (rgb is None):
            for color in ColorEnum:
                if color.name == name:
                    self.name = name
                    self.rgb = color.value
                    return
                
            if not hasattr(self, 'name'):
                raise ValueError('The default color '+name+' does not exist. How very sad.')
        
        elif (name is None):
            maxDivergence = 1
            decidedC = None
            for color in ColorEnum: #search for the basic color closest to the given rgb code. 
                rc = color.value[0]
                gc = color.value[1]
                bc = color.value[2]
                
                difRc = abs(rc-rgb[0])/255.0
                difGc = abs(gc-rgb[1])/255.0
                difBc = abs(bc-rgb[2])/255.0
                generalDif = (difRc+difGc+difBc)/3 #the divergence measured between the two colors, measured in [0,1]
                if generalDif<maxDivergence:
                    maxDivergence = generalDif
                    decidedC = color;
            
            if decidedC is None:
                raise ValueError("Hey you just got an exception you should've never had :D call Esteban")
            else:
                self.name = decidedC.name
                self.rgb = rgb
        else:
            self.rgb = rgb
            self.name = name
   
    def testColorCreation():
        c = Color("almost magenta", [255,25,255])
        print("\n\nHere are the end results: this you asked for the color:")
        print (c.name)
        print (c.rgb)
        
        c = Color(rgb = [255,25,255])
        print("\n\nHere are the end results: this you asked for the color:")
        print (c.name)
        print (c.rgb)
        
        c = Color("AQUA")
        print("\n\nHere are the end results: this you asked for the color:")
        print (c.name)
        print (c.rgb)
        
        c = Color()
        print("\n\nHere are the end results: this you asked for the color:")
        print (c.name)
        print (c.rgb)
        
    def toString(self):
        return self.__dict__