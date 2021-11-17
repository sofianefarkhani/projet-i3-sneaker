
import os
import cv2

import itertools
import threading
import time
import sys

import multiprocessing
from processes.Task             import *
from processes.Enums            import *
from processes.LoaderMessage    import *

from utilities.Herald                           import Herald
from utilities.Beaver                           import Beaver
from utilities.configUtilities.ProcConfig       import ProcConfig
from utilities.configUtilities.LoadConfig       import LoadConfig

class Connexion:
    def __init__(self) -> None:
        self.local=LoadConfig.getIfLocalSource()
        if self.local == False: 
            self.hostname=input('Host > ')
            self.username=input('User > ')
            self.password=input('Pswd > ')

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
    
    
    def __init__(self, taskQueue, answerQueue, bbTaskQueue, connexion:Connexion):
        """Initializes the loader, ready to place things in the task queue"""
        multiprocessing.Process.__init__(self)
        self.bbTaskQueue = bbTaskQueue
        self.taskQueue = taskQueue
        self.answerQueue = answerQueue
        self.connexion = connexion
        
    def run(self):
        (numProcesses, procTalkative, bbTalkative) = ProcConfig.getRunningConfig()
        Herald.printStart('Loader')
        
        imagesGenerator = self.getImagesGenerator()
        
        while True:
            task = Herald.getMessageFrom('Loader', self.taskQueue)
            
            if task is not None:
                if task.type == LoaderTaskType.LOAD:
                    batchSize = LoadConfig.getBatchSize()
                    
                    Herald.printLoading(batchSize)
                    
                    for i in range(batchSize):
                        img = next(imagesGenerator)
                        if img is None:        # if image generator yields None, this is the end of the db
                            self.answerQueue.put(LoaderAnswer(LoaderAnswerType.NOMORE))
                        else:                  # else append the image to the tasks
                            self.bbTaskQueue.put(Task(TaskType.PROCESS, img))
                    self.answerQueue.put(LoaderAnswer(LoaderAnswerType.LOADDONE))
                
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
        
        else: 
            # print ('Not implemented yet you dumbdumb')
            os.chmod('../img/temp', 777)
            
            import pysftp
            
            cnopts = pysftp.CnOpts(knownhosts='known_hosts')
            cnopts.hostkeys = None
            with pysftp.Connection(host=self.connexion.hostname, username=self.connexion.username, password=self.connexion.password, cnopts=cnopts) as sftp:
                Herald.printForLoader("Connection to FTP server succesfully established !")
                Herald.printForLoader("Loading the list of images name... Please wait. This could take up to a few minutes, depending on the number of images in the distant folder.")
                Herald.printForLoader("Please don't ctrl c during this time")
                
                
                sftp.cwd(LoadConfig.getRemoteImgSrc())
                
                # load names with a waiting animation
                done = False
                def animate():
                    for c in itertools.cycle(['|', '/', '-', '\\']):
                        if done :
                            break
                        sys.stdout.write('\rloading ' + c )
                        sys.stdout.flush()
                        time.sleep(0.1)
                    sys.stdout.write('\rDone!     ')
                t = threading.Thread(target=animate)
                t.start()
                
                listNames = sftp.listdir()          
                
                done = True
                
                Herald.printForLoader(str(len(listNames))+" image names loaded! Starting task distribution")
                
                while len(listNames)>0:
                    temp = listNames.pop(0)
                    Herald.signalLoad(temp)
                    
                    # download from remote in cache folder
                    sftp.get(temp, '../img/temp/'+temp)  
                    
                    # yield image from folder
                    yield cv2.imread('../img/temp/'+temp)
                    
                    # remove image from cache
                    os.remove('../img/temp/'+temp)
                
        yield None
                