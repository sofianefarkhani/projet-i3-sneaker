#A file to test anything you need in the moment.

from Data.Color import Color
from Data.Tag import Tag
from Data.Type import Type
import json
from json import JSONEncoder
import jsonpickle
from interface.Writer import Writer
from interface.JsonReader import JsonReader 
from interface.Loader import Loader
import cv2

SIZE_IMAGE = 100 # Todo: set and load this in config and not here

def showImage(img):
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
Loader.loadImages(number=10)

# 
# Note: Maybe use another loader (or manage the existing) to load the images and the data linked (example: the type of the image (LOW/HIGH))
#

for i in range(9):
    img = cv2.resize(Loader.getImgAtIndex(i), (100, 100))
    showImage(img)

