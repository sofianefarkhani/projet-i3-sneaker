
import os
import cv2

import multiprocessing
from processes.Task             import *
from processes.Enums            import *
from processes.LoaderMessage    import *

from utilities.configUtilities.ConfigLoader     import ConfigLoader
from utilities.Herald                           import Herald
from utilities.configUtilities.ProcConfig       import ProcConfig
from utilities.configUtilities.LoadConfig       import LoadConfig

class Loader(multiprocessing.Process):
    '''A class that runs in a separate process, and spends its time loading images when requested.
    
    It communicates with the main through:
        -self.taskQueue: a queue of things the loader has to do.
            these tasks can be of three types: 
                -> No task: wait
                -> Load: load more images.
                -> End: stop the service.
        -self.answerQueue: a queue of messages for the main process.
            This queue will hold the messages:
                -> No message: nothing happened 
                -> NoMore: there is nothing left in the database
                -> LoadDone: Finished loading
        -self.bbTaskQueue: a queue of tasks that the BlackBoxes will have to accomplish.'''
    
    
    def __init__(self, taskQueue, answerQueue, bbTaskQueue):
        """Initializes the loader, ready to place things in the task queue"""
        multiprocessing.Process.__init__(self)
        self.bbTaskQueue = bbTaskQueue
        self.taskQueue = taskQueue
        self.answerQueue = answerQueue
        
    def run(self):
        (numProcesses, procTalkative, bbTalkative) = ProcConfig.getRunningConfig()
        Herald.printStart('Loader')
        
        imagesGenerator = self.getImagesGenerator()
        
        while True:
            task = Herald.getMessageFrom('Loader', self.taskQueue)
            
            if task is not None:
                if task.type == LoaderTaskType.LOAD:
                    if LoadConfig.getIfLocalSource() == True:
                        batchSize = LoadConfig.getBatchSize()
                        
                        Herald.printLoading(batchSize)
                        
                        for i in range(batchSize):
                            img = next(imagesGenerator)
                            if img is None:                                     # if image generator yields None, this is the end of the db
                                self.answerQueue.put(LoaderAnswer(LoaderAnswerType.NOMORE))
                            else:                                               # else append the image to the tasks
                                self.bbTaskQueue.put(Task(TaskType.PROCESS, img))
                        self.answerQueue.put(LoaderAnswer(LoaderAnswerType.LOADDONE))
                    else: 
                        Herald.printError('Oh no, getting images from FTP is not yet implemented :\'(')
                
                elif task.type == LoaderTaskType.TERMINATE:
                    self.taskQueue.task_done()
                    break        
                
                self.taskQueue.task_done()
                  
        Herald.queueMessageIn('Loader', self.answerQueue, LoaderAnswer(LoaderAnswerType.END))
        Herald.printTermination('Loader')
        
        
        
        
    def getImagesGenerator(self):
        localFile = LoadConfig.getLocalImageSource()
        
        if LoadConfig.getIfLocalSource(): 
            files = os.listdir(localFile)
            for file in files:
                Herald.signalLoad(localFile+file)
                
                yield cv2.imread(localFile+file)
        
        yield None
                