#!/usr/bin/python3
# -*- coding: utf-8 -*-
from typing import Generator
import cv2
from threading import Lock
from interface.ConfigLoader import ConfigLoader


class Loader :
    '''The loader loads images and keeps them ready to use for any class that would request them.
    
    Images are stored in a dedicated list of images, and are accessible by all threads through the getImages() generator.
    
    To access the images, run the getImages() method and store its return value;
    you can now iterate on them, and they will be loaded as you need them.
    '''
    
    __images = []
    '''The list of images loaded and available to the threads dealing with them.'''
    
    endOfService = False
    '''Set to true to end the Loader's services immediately.'''
    endOfServiceOnNextNoImage = False
    '''Set to true to signify there are no more images to load in the database.'''
    
    idOfNextImageToLoad = 1
    
    imgBatchSize = ConfigLoader.getVariable('loader', 'batchSize')
    reloadNumber = ConfigLoader.getVariable('loader', 'reloadNumber')
    
    localImgSrc = ConfigLoader.getVariable('loader', 'localImgSrc')
    
    critical_function_lock = Lock()
    '''A thread.Lock to stop multiple threads from accessing the same part of the code at once.'''
    
    
    talking = False
    
    
    def getImages(talking = False):
        '''Returns an iterator that lets you get unlimited images.'''
        
        Loader.talking = talking
        
        #while the application still runs, be ready to give images. (to one thread at a time though.)
        while not Loader.endOfService:
            with Loader.critical_function_lock:          #this part here should only be accessible to one thread at a time
                if not Loader.endOfServiceOnNextNoImage and len(Loader.__images)<Loader.reloadNumber: #if we have not loaded all existing images and there are not many loaded images left
                    Loader.loadImages()
                
                if len(Loader.__images)!=0:
                    if talking : print('There are '+str(len(Loader.__images))+' loaded images in store: i\'ll give you one')
                    yield Loader.getFirstImg();
                else:
                    print("No more images in store for now, returning None instead")
                    if Loader.endOfServiceOnNextNoImage:
                        Loader.endService()
                    yield None
        
            
    
    
    def loadImages(number:int=None):
        '''A method that is here to load some test images.
        
        Load a number of images in the list of available images.
        
        The loaded images names range from 1.png to 9.png.'''
        
        if number is None:
            number = Loader.imgBatchSize
            
        if Loader.talking : print('Loading '+str(number)+' more images')
        
        imgSuffix = '.png'
        if number<=0: return;
        while (image := cv2.imread(Loader.localImgSrc+str(Loader.idOfNextImageToLoad)+imgSuffix)) is not None:
            Loader.__images.append(image)
            number -= 1
            Loader.idOfNextImageToLoad += 1
            
            if Loader.talking : print('    - Loaded '+ Loader.localImgSrc+str(Loader.idOfNextImageToLoad)+imgSuffix)
            
            if number==0: return
            
        # if we reach this point, there are no more images to load in the database.
        if Loader.talking : print('No more images in database to load')
        Loader.endServiceWhenNoMoreImages()
        
            
            
            
            
    
    def getFirstImg():
        '''Returns the first available image in the list of loaded images.'''
        if len(Loader.__images)>0: return Loader.__images.pop(0)
        elif(Loader.endOfServiceOnNextNoImage):
            Loader.endService()
        else: return None
    
    
    # def showImage(self):
    #     cv2.imshow("Img",self.__img)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()

    def endService():
        '''Terminates the Loader.getImages() method for all threads using it.'''
        Loader.endOfService = True
        
    def endServiceWhenNoMoreImages():
        Loader.endOfServiceOnNextNoImage = True