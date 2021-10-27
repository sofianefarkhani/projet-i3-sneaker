#A file to test anything you need in the moment.

from numpy.lib.type_check import imag
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
from preprocess.BackgroundSuppression import BackgroundSuppression
from menuPkg.Menu import Menu

from colorDetector.ColorDetector import ColorDetector

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

# images = Loader.getImages(talking=True);
#for img in images:
#     showImage(img)



#### TEST CONFIG CLASS
#from interface.ConfigLoader import ConfigLoader
# ConfigLoader.getVariable('mysql', 'other', 'tbeau')

#BackgroundSuppression.testMaskColor()
images = Loader.getImages(talking=True)
ColorDetector.getDominantColors(images)


#menu = Menu()