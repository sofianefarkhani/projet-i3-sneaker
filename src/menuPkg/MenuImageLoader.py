

from os import listdir
from os.path import isfile, join
from Data.Image import Image
import cv2

class MenuImageLoader:
    '''A class that loads a table of images for the menu. Simple enough.'''
    
    
    
    def loadImages(nbImg=-1, pathOfFolder='../img/train/trainingTestImages', debugMode=False):
        '''A function that returns a table of images for training. The table is of fixed length, by default 100.
        
        The images are loaded all at once! consider loading them dynamically if there are hundreds of them.
        By default, nbImg=-1 means you will take all images. 
        If there are not enough images according to the number you gave, then we load this number.'''
        
        files = [f for f in listdir(pathOfFolder) if isfile(join(pathOfFolder, f))]
        
        images = []
        id = 0
        
        for f in files:
            if (nbImg!=-1 and nbImg==0): break
            images.append(Image(cv2.imread(join(pathOfFolder, f)), join(pathOfFolder, f), id, "no name: "+str(id)))
            id += 1
            if nbImg!=-1:
                nbImg -= 1
            if debugMode:
                print('Loaded image: ')
                print(images[-1].toString(1))
        return images
    
    def loadImagesButDynamically(nbImg=-1, pathOfFolder='../img/train/trainingTestImages', debugMode=False):
        '''If there are too many images, load them as a generator.
        
        By default, nbImg=-1 means you will take all images. 
        I love generators, if you could not tell. '''
        
        files = [f for f in listdir(pathOfFolder) if isfile(join(pathOfFolder, f))]
        id = 0
        
        for f in files:
            if (nbImg!=-1 and nbImg==0): break
            image = Image(cv2.imread(join(pathOfFolder, f)), join(pathOfFolder, f), id, "no name: "+str(id))
            id += 1
            if nbImg!=-1:
                    nbImg -= 1
            if debugMode:
                print('Loaded image: ')
                print(image.toString(1))
            yield image
    
    