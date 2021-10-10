

import cv2

from interface.Loader import Loader
from interface.Writer import Writer

from colorDetector.ColorDetector import ColorDetector
from sneakerExtractor.ShoeExtractor import ShoeExtractor
from typeDetector.TypeDetector import TypeDetector

from Data.Tag import Tag
from Data.Color import Color
from Data.Type import Type


class BlackBox:
    '''The BlackBox coordinates all the image dealings and the extraction of the values.'''
    
    #in prep for multithreading, we make some ids for each instance of the blackbox class
    nextBBIndexAvailable = 0
    
    def __init__(self, testMode:bool=False):
        self.id = BlackBox.nextBBIndexAvailable
        BlackBox.nextBBIndexAvailable += 1
        self.testMode = testMode
    
    def startComputation(self):
        '''Start a new Blackbox to deal with images.
        
        The method will take images of shoes from the Loader and from there:\n 
            -extract them\n
            -detect their colors (main and secondary)\n
            -detect their type (high or low)\n
            -write the results in the output file.'''
        
        
        images = Loader.getImages(True);
        for img in images:
            
            if img is None: continue
            
            shoeImg = ShoeExtractor.extractShoeFromImage(img)
            
            (mainColor, secondaryColor) = ColorDetector.detectColorsOf(shoeImg)
            typeOfShoe = TypeDetector.detectTypeOfShoe(shoeImg)
            
            tag = Tag(0) # yeah temporary id for now we don't care too much about that
            
            tag.setType(typeOfShoe)
            tag.setMainColor(mainColor)
            tag.setSecondaryColor(secondaryColor)
            
            if self.testMode:
                print('New data written in the test output file.')
                Writer.outputTagAsJson(tag, '../out/testData.json')
            else:
                Writer.outputTagAsJson(tag)
            
            self.showImage(img)
        
        
    def showImage(self, img):
        cv2.imshow("From blackbox "+str(self.id), img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()