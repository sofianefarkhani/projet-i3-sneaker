from enum import Enum
import matplotlib.colors as mcolors
import numpy as np

class ColorEnum(Enum):
    '''Each ColorEnum is represented by the name of the color in uppercase, and has for value the rgb representation of the color.'''
    BLACK = [0, 0, 0]
    WHITE = [255, 255, 255]
    GRAY  = [128, 128, 128]
    SILVER = [206, 206, 206]
    RED   = [255, 0, 0]
    BORDEAUX = [109, 7, 26]
    BLUE  = [0, 0, 255]
    CYAN = [43, 250, 250]
    GREEN = [0, 255, 0]
    EPINARD = [47, 79, 79]
    ORANGE = [237, 127, 16]
    YELLOW = [255, 255, 0]
    PINK = [253, 108, 158]
    MAGENTA = [255, 0, 255]
    VIOLET = [102, 0, 153]
    MAUVE = [212, 115, 212]
    MARRON = [88, 41, 0]
    BEIGE = [200, 173, 127]
    
    
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



