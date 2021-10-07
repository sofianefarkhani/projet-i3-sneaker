from enum import Enum

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