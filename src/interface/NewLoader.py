
import os
import cv2
import multiprocessing
from interface.ConfigLoader import ConfigLoader
from processes.Utilities import Utilities
from processes.Task import *
from processes.Enums import *
from processes.LoaderMessage import *


class Loader(multiprocessing.Process):
    '''A class that runs in a separate process, and spends its time loading images.
    
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
        imagesGenerator = self.getImagesGenerator()
        
        while True:
            task = self.taskQueue.get() # gets the new task. If there is None, blocks the Loader until there is.
            if Utilities.loaderShouldTalk() : print('Loader recieved task: '+str(task.type))
            
            if task is not None:
                if task.type == LoaderTaskType.LOAD:
                    batchSize = imgBatchSize = ConfigLoader.getVariable('loader', 'batchSize')
                    if Utilities.loaderShouldTalk() : print('Loading '+str(batchSize)+' more images')
                    for i in range(batchSize):
                        img = next(imagesGenerator)
                        if img is None:                 # if image generator yields None, this is the end of the db
                            self.answerQueue.put(LoaderAnswer(LoaderAnswerType.NOMORE))
                        else: # else append the image to the tasks
                            self.bbTaskQueue.put(Task(TaskType.PROCESS, img))
                    self.answerQueue.put(LoaderAnswer(LoaderAnswerType.LOADDONE))
                
                elif task.type == LoaderTaskType.TERMINATE:
                    self.taskQueue.task_done()
                    break        
            self.taskQueue.task_done()
                  
        self.answerQueue.put(LoaderAnswer(LoaderAnswerType.END))
    
     # while not self.endOfService:
        #     print ('loader running '+__name__)
        #     # look if we have recieved any instructions
            
        #     # do we need to load more images? 
        #     if self.bbTaskQueue.qsize() <= ConfigLoader.getVariable('loader', 'reloadNumber'):
        #         batchSize = imgBatchSize = ConfigLoader.getVariable('loader', 'batchSize')
        #         if Utilities.loaderShouldTalk() : print('Loading '+str(batchSize)+' more images')
        #         for i in range(batchSize):
        #             img = next(imagesGenerator)
        #             if img is None: # if image generator yields None, this is the end.
        #                 self.endOfService = True
        #                 break
        #             else: # else append the image to the tasks
        #                 self.bbTaskQueue.put(Task(TaskType.PROCESS, img))
        # at the end of service, send an answer so that the main process knows
        
        
        
        
    def getImagesGenerator(self):
        localLoading = ConfigLoader.getVariable('loader','takeFromLocalSource')
        localFile = ConfigLoader.getVariable('loader','localImgSrc')
        
        if localLoading: 
            files = os.listdir(localFile)
            for file in files:
                if Utilities.loaderShouldTalk() : print('    - Loaded '+ localFile+file)
                yield cv2.imread(localFile+file)
        
        yield None
                