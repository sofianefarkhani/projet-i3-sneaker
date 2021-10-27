from enum import Enum
import matplotlib.colors as mcolors
import numpy as np

class ColorEnum(Enum):
    '''Each ColorEnum is represented by the name of the color in uppercase, and has for value the rgb representation of the color.'''
    RED   = [255, 0, 0]
    GREEN = [0, 255, 0]
    BLUE  = [0, 0, 255]
    WHITE = [255, 255, 255]
    BLACK = [0, 0, 0]
    GRAY  = [128, 128, 128]
    AQUA  = [0, 255, 255]
    FUSCHIA = [255, 0, 255]
    YELLOW = [255, 255, 0]    
    
    
    def colorExist(ColorName:str):
        for C in ColorEnum:
            if C.name == ColorName.upper():
                return True
        return False
    
    def getColor(name:str):
        for C in ColorEnum:
            if C.name == name.upper():
                return C
        return None

    def getClosestColorByRGB(r, g, b):
        maxDivergence = 1
        for color in mcolors.CSS4_COLORS: #search for the basic color closest to the given rgb code. 
            rc = mcolors.to_rgb(color)[0]*255.0
            gc = mcolors.to_rgb(color)[1]*255.0
            bc = mcolors.to_rgb(color)[2]*255.0
            
            difRc = abs(rc-r)/255.0
            difGc = abs(gc-g)/255.0
            difBc = abs(bc-b)/255.0
            generalDif = (difRc+difGc+difBc)/3 #the divergence measured between the two colors, measured in [0,1]
            if generalDif<maxDivergence:
                maxDivergence = generalDif
                decidedC = color;
        return decidedC

    def getColorByName(name:str):
        for color in mcolors.CSS4_COLORS:
            if color.upper() == name.upper():
                return (name, np.multiply(mcolors.to_rgb(color),255))
            
        raise ValueError('The default color '+name+' does not exist. How very sad.')



