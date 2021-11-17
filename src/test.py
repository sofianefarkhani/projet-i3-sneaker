#A file to test anything you need in the moment.

from numpy.lib.type_check import imag
from Data.Color import Color
from Data.Tag import Tag
from Data.Type import Type
import json
from json import JSONEncoder
import jsonpickle
from interface.ConfigLoader import ConfigLoader
from interface.Writer import Writer
from interface.JsonReader import JsonReader 
from interface.Loader import Loader
import cv2
from preprocess.BackgroundSuppression import BackgroundSuppression
from menuPkg.Menu import Menu
import numpy as np

from colorDetector.ColorDetector import ColorDetector
from preprocess.ContrastAndBrightness import ContrastAndBrightness

import ast

from preprocess.ImagePreprocessor import ImagePreprocessor
#### Testing the creation of colors
#Color.testColorCreation()




##### AND HERE WE MAKE JSON 
#c = Color(rgb = [13, 0, 255])
#c = Color(rgb = [0, 2, 0])
#print(c.toString())
# tag = Tag(0)
# tag.setType(Type.HIGH)
# tag.setMainColor(c)
# tag.setSecondaryColor(c2)
#c = Color('black')
#c2 = Color('mediumblue')
#print(c2.toString())
# data = jsonpickle.encode(t)
# print(data)

# t2 = jsonpickle.decode(data)
# print(t2.__class__)
# print(t2.mainColor.name)
# print(t2.mainColor.rgb)

# print(t2.type)


# file_object = open('../out/data.json', 'a')
# file_object.write("\n"+data)

# Writer.outputTagAsJson(tag)



##### READING THE OUTPUT FILE
#JsonReader.readOutputFile(verbalOutput=True)



##### Test loading of images
## images are loaded as we need them. 

def showImage(img):
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()  

def cloneImages(images):
    imagesList = []
    for img in images:
        if isinstance(img,np.ndarray):
            imagesList.append(img)
    return imagesList

# images = Loader.getImages(talking=True);
#for img in images:
#     showImage(img)



#### TEST CONFIG CLASS
#from interface.ConfigLoader import ConfigLoader
# ConfigLoader.getVariable('mysql', 'other', 'tbeau')

#BackgroundSuppression.testMaskColor()
#Test for ColorDetector
images = Loader.getImages(talking=True)
imagesClone = cloneImages(images)
for img in imagesClone:
    newImg = ImagePreprocessor.contrastAndBrightnessAdjustment(img)
    newImgNoBg = BackgroundSuppression.replaceBackground(newImg)
    for test in newImgNoBg:
        showImage(test) 
#listColorsDetect = ColorDetector.detection(imagesClone)
#print('Colors detect : ',listColorsDetect)

#menu = Menu()