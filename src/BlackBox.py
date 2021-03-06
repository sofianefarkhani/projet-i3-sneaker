import os
import cv2
import traceback

import multiprocessing
from processes.Enums                                import *
from processes.Task                                 import Answer

from keras.models                                   import load_model

from interface.Writer                               import Writer
from utilities.DataFormatter import DataFormatter

from utilities.Herald                               import Herald
from utilities.DataFormatter                        import DataFormatter

from blackBoxModules.typeDetector.TypeDetector      import TypeDetector
from blackBoxModules.colorDetector.ColorDetector    import ColorDetector
from blackBoxModules.sneakerExtractor.ShoeExtractor import ShoeExtractor
from blackBoxModules.preprocess.ImagePreprocessor   import ImagePreprocessor

from utilities.config.getters.RunConfigGeneral import RunConfigGeneral as RCG 
from utilities.config.getters.IANetworkConfig import IANConfig as IAC
from utilities.config.getters.TalkConfig import TalkConfig as TC

os.environ['TF_CPP_MIN_LOG_LEVEL'] = str(TC.getTF())

class BlackBox(multiprocessing.Process):
    '''The BlackBox coordinates all the image dealings and the extraction of the values.

    It is its own process taking on images from the task queue when it needs to.'''

    # in prep for multithreading, we make some ids for each instance of the blackbox class
    nextBBIndexAvailable = 0

    def __init__(self, task_queue, answerQueue, testMode: bool = False):
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
        proc_name = self.name

        try:    
            Herald.printStart(proc_name)
            
            # load IA models and shut TF up
            modelShoeDetector = load_model(IAC.getSDModel())
            modelShoeDetector.load_weights(IAC.getSDWeights())
            modelTypeDetector = load_model(IAC.getTDModel())
            modelTypeDetector.load_weights(IAC.getTDWeights())
            
            # This is the main loop
            while True:
                nextTask = Herald.getMessageFrom(proc_name, self.taskQueue)
                
                if nextTask.type == TaskType.END: break
                
                elif nextTask.type == TaskType.PROCESS: 
                    if nextTask.img is None: continue # this should not happen, but i still left it as a precaution
                    
                    self.compute(
                        nextTask.img, 
                        nextTask.imgPath, 
                        nextTask.imgPathInCache, 
                        nextTask.tfImg, 
                        nextTask.tf2Img, 
                        modelShoeDetector, 
                        modelTypeDetector)
                    
                    self.taskQueue.task_done()    # helps when we want to join threads at the end of the programm
                    
            self.taskQueue.task_done()
        
        
        except Exception as e:
            try:
                self.taskQueue.task_done()
            except:
                Herald.printError( 'A dev broke the basic skeletton of the BlackBox.' )

            Herald.printError(
                proc_name+' encountered an error, and stopped its execution. See the error below: \n')
            Herald.printError(traceback.format_exc())

        Herald.queueMessageIn(proc_name, self.answerQueue,
                              Answer(AnswerType.BOXENDSERVICE))
        Herald.printTermination(proc_name)
    
    
    
    
    def compute(self, img, imgPath:str, imgPathInCache:str=None, tfDetectImg=None, tfTypeImg=None, modelShoeDetector=None, modelTypeDetector=None):
        '''Computes if there is a shoe, its type and color.
        If there is a path in cache, use this one.
        tfImg is the image loaded for the needs of tensorflow. Don't use it unless you're called Vivien.'''
        imgName  = DataFormatter.getLastFromPath(imgPath)
        refProd  = DataFormatter.extractProdRef(imgName)

        img = ImagePreprocessor.resize(img)
        
        shoeProb = ShoeExtractor.isThereShoe(
            tfDetectImg,
            modelShoeDetector
        )
        
        try:
            if shoeProb>0.7:
                    (mainColor, secondaryColor) = ColorDetector.detection(
                        img,
                        self.name,
                        imgName
                    )
                    
                    # type of shoe takes the form : [high, low, mid], each float in [0, 1]
                    typeOfShoe = TypeDetector.detectTypeOfShoe(
                        tfTypeImg,
                        modelTypeDetector
                    )

                    colorway = DataFormatter.buildColorWay(mainColor, secondaryColor)
                    dataShoes= DataFormatter.getFullData(refProd, imgName, "NOT IMPLEMENTED YET", colorway, shoeProb, typeOfShoe)
                    Herald.printResults(dataShoes)
                
            else: # there was no shoe
                dataShoes = DataFormatter.getNoneData(refProd, imgName, shoeProb)
                Herald.printResults(dataShoes)

        except Exception as e:
            Herald.printError("A blackbox encountered an error when dealing with image: '"+imgPath+"'. Image will be ignored. Full error is: "+e)
            dataShoes = DataFormatter.getNoneData(refProd, imgName, shoeProb)
            Herald.printResults(dataShoes)
        
        # prepare for all the data display / saving
        Writer.writeDataToTempFile(self.name, dataShoes)
        Herald.printWrittenData(self.name)
        self.showImage(img)
        
        
        

    def showImage(self, img):
        '''Shows an image if the config allows it. 

        Stops this BlackBox from executing anything new while the image is on display.'''
        if RCG.getShowImages():
            cv2.imshow("From blackbox "+str(self.id), img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def assignId():
        '''Assigns an id to this instance of Blackbox.'''
        BlackBox.nextBBIndexAvailable += 1
        return BlackBox.nextBBIndexAvailable-1
