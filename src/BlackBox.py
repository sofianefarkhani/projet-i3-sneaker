

import cv2

from interface.Loader import Loader
from interface.Writer import Writer
from interface.ConfigLoader import ConfigLoader

from colorDetector.ColorDetector import ColorDetector
from sneakerExtractor.ShoeExtractor import ShoeExtractor
from typeDetector.TypeDetector import TypeDetector
from preprocess.ImagePreprocessor import ImagePreprocessor

from Data.Tag import Tag

import multiprocessing
from processes.Enums import *
from processes.Task import Answer
from processes.Utilities import Utilities


class BlackBox(multiprocessing.Process):
    '''The BlackBox coordinates all the image dealings and the extraction of the values.
    
    It is its own process taking on images from the task queue when it needs to.'''
    
    #in prep for multithreading, we make some ids for each instance of the blackbox class
    nextBBIndexAvailable = 0
    
    def __init__(self, task_queue, answerQueue, testMode:bool=False):
        '''Creates a blackbox and readies it to complete Tasks.'''
        self.id = BlackBox.assignId()
        
        self.testMode = testMode
        self.taskQueue = task_queue
        self.answerQueue = answerQueue
        multiprocessing.Process.__init__(self)

    
    def run(self):
        '''Runs this Blackbox to deal with images in the task queue.
        
        The method takes images of shoes from the Loader and from there:\n 
            -extract them\n
            -detect their colors (main and secondary)\n
            -detect their type (high or low)\n
            -write the results in the output file.
            
        It has to communicate with the main and the loader: 
            - to get new tasks and to terminate its service, through taskQueue
            - to send its status, through resultQueue'''
        
        
        
        (numProcesses, procTalkative, bbTalkative) = Utilities.getRunningConfig()    
            
        proc_name = self.name
        print(self.name+' runnin')
        
        while True:
            next_task = self.taskQueue.get()
            
            if next_task is None:
                print ('NONE') 
                if Utilities.shouldAutoRegulate():
                    if procTalkative: print ('%s: Requesting for main to close a blackbox' % proc_name)
                    self.result_queue.put(Answer(AnswerType.ENDREQ))
                    # the loader is overwhelmed; ask to kill a blackbox
                else: continue                           # the loader may have a bit of lag; we wait a bit and try again
            if next_task.type == TaskType.END:
                break
            else: 
                if next_task.img is None: # this should not happen, but i still left it as a precaution
                    continue
                
                if bbTalkative: print ('%s: %s' % (proc_name, next_task))
                self.compute(next_task.img)
                
                #answer = next_task()
                
                self.taskQueue.task_done()    # helps when we want to join threads at the end of the programm
                #self.result_queue.put(answer)
                
                if Utilities.shouldReloadConfig():
                    ConfigLoader.loadVars()
            
        self.taskQueue.task_done()
        if procTalkative: print ('%s: End of service' % proc_name)
        return
    
    def compute(self, img):
        if img is None and not Loader.endOfService: 
            return 
        elif Loader.endOfService:
            return 'exit'
        
        shoeImg = ShoeExtractor.extractShoeFromImage(ImagePreprocessor.preprocessForShoeExtraction(img, self.name), self.name)
        
        (mainColor, secondaryColor) = ColorDetector.detectColorsOf(ImagePreprocessor.preprocessForColorsIdentification(shoeImg, self.name), self.name)
        typeOfShoe = TypeDetector.detectTypeOfShoe(ImagePreprocessor.preprocessForTypeIdentification(shoeImg, self.name), self.name)
        
        tag = Tag(0) # yeah temporary id for now we don't care too much about that
        
        tag.setType(typeOfShoe)
        tag.setMainColor(mainColor)
        tag.setSecondaryColor(secondaryColor)
        
        if self.testMode:
            if Utilities.iaShouldTalk(): print('%s: New data written in the test output file.' % (self.name))
            Writer.outputTagAsJson(tag, ConfigLoader.getVariable('output', 'testData'))
        else:
            Writer.outputTagAsJson(tag)
        
        self.showImage(img)
    
    def showImage(self, img):
        '''Shows an image if the config allows it. 
        
        Stops this BlackBox from executing anything new while the image is on display.'''
        if ConfigLoader.getVariable('runConfig', 'gui', 'showImages'):
            cv2.imshow("From blackbox "+str(self.id), img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    
    def assignId():
        '''Assigns an id to this instance of Blackbox.'''
        BlackBox.nextBBIndexAvailable += 1
        return BlackBox.nextBBIndexAvailable-1