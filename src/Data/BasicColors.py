from enum import Enum
import matplotlib.colors as mcolors
import numpy as np

class ColorEnum(Enum):
    '''Each ColorEnum is represented by the name of the color in uppercase, and has for value the rgb representation of the color.'''
    BLACK = [0, 0, 0]
    CARBONE = [19, 14, 10]
    WHITE = [255, 255, 255]
    GRAY  = [128, 128, 128]
    SILVER = [206, 206, 206]
    ANTHRACITE = [48, 48, 48]
    LICORICE = [27, 18, 18]
    RED   = [255, 0, 0]
    REAL_RED   = [250, 0, 0]
    BORDEAUX = [109, 7, 26]
    GRENADINE = [233, 56, 63]
    BLUE  = [0, 0, 255]
    REAL_BLUE = [0, 0, 250]
    CYAN = [43, 250, 250]
    NAVY = [3, 34, 76]
    ROYAL_BLUE = [49, 140, 231]
    GREEN = [0, 255, 0]
    REAL_GREEN = [0, 250, 0]
    EPINARD = [47, 79, 79]
    GRASS = [58, 137, 35]
    MINT = [22, 184, 78]
    ORANGE = [237, 127, 16]
    CAROT = [244, 102, 27]
    ORANGEE = [250, 164, 1]
    YELLOW = [255, 255, 0]
    MIMOSA = [254, 248, 108]
    GOLD = [255, 215, 0]
    PINK = [253, 108, 158]
    MAGENTA = [255, 0, 255]
    CHERRY = [222, 49, 99]
    PURPLE = [102, 0, 153]
    MAUVE = [212, 115, 212]
    HELIOTROPE = [223, 115, 255]
    LILA = [182, 102, 210]
    BROWN = [88, 41, 0]
    HAZEL = [149, 86, 40]
    BEIGE = [200, 173, 127]
    CHESTNUT = [167, 103, 38]
    
    def colorExist(ColorName:str):
        """
        Verify existance of the color

        :param ColorName : name of the color

        :return : true (color exists) or false (color not exists)
        """
        for C in ColorEnum:
            if C.name == ColorName.upper():
                return True
        return False
    
    def getColor(name:str):
        """
        Get color by name

        :param name : name of the color

        :return : object color
        """
        for C in ColorEnum:
            if C.name == name.upper():
                return C
        return None

    def getClosestColorByRGB(r, g, b):
        """
        Generate color by rgb

        :param r : red value
        :param g : green value
        :param b : blue value

        : return : object color
        """
        maxDivergence = 1
        for color in ColorEnum: #search for the basic color closest to the given rgb code. 
            rc = color.value[0]
            gc = color.value[1]
            bc = color.value[2]
            
            difRc = abs(rc-r)/255.0
            difGc = abs(gc-g)/255.0
            difBc = abs(bc-b)/255.0
            generalDif = (difRc+difGc+difBc)/3 #the divergence measured between the two colors, measured in [0,1]
            if generalDif<maxDivergence:
                maxDivergence = generalDif
                decidedC = color.name;
        return decidedC

    def getColorByName(name:str):
        """
        Generate color by name

        :param name : name of the color

        :return : object color
        """
        for color in ColorEnum:
            if color.name in name.upper():
                return (name, color.value)
            
        raise ValueError('The default color '+name+' does not exist. How very sad.')



