
import os
import cv2

import itertools
import threading
import time
import sys

import numpy                    as np
import tensorflow               as tf

import multiprocessing
from processes.Task             import *
from processes.Enums            import *
from processes.LoaderMessage    import *

from utilities.Herald                           import Herald
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
        Herald.printStart('Loader')
        
        imagesGenerator = self.getImagesGenerator()
        
        while True:
            
            task = Herald.getMessageFrom('Loader', self.taskQueue)
            
            if task is not None:
                if task.type == LoaderTaskType.LOAD:
                    batchSize = LoadConfig.getBatchSize()
                    
                    Herald.printLoading(batchSize)
                    
                    self.loadImages(batchSize, imagesGenerator)
                    
                    Herald.queueMessageIn('Loader', self.answerQueue, LoaderAnswer(LoaderAnswerType.LOADDONE))
                
                elif task.type == LoaderTaskType.TERMINATE:
                    self.taskQueue.task_done()
                    break        
                
                self.taskQueue.task_done()
                  
        Herald.queueMessageIn('Loader', self.answerQueue, LoaderAnswer(LoaderAnswerType.END))
        Herald.printTermination('Loader')
        
        
    def loadImages(self, batchSize, imagesGenerator):
        for i in range(batchSize):
            imgInfo = next(imagesGenerator)
            
            if imgInfo is not None:
                imgPath = imgInfo['imgPath']
                
                try: imgPathInCache = imgInfo['imgPathInCache']
                except: imgPathInCache = None
                
                img = imgInfo['img']
                
                tfImg = imgInfo['tfImg']
                
            else: 
                imgPath = None
                imgPathInCache = None
                img = None
                        
            if imgInfo is None:  # if image generator yields None, this is the end of the db
                Herald.queueMessageIn('Loader', self.answerQueue, LoaderAnswer(LoaderAnswerType.NOMORE))
                break
            else:                  # else append the image to the tasks
                Herald.queueMessageIn('Loader', self.bbTaskQueue, Task(TaskType.PROCESS, imgPath=imgPath, imgPathInCache=imgPathInCache, img=img, tfImg=tfImg))
                    
        
    def getImagesGenerator(self):
        
        # from local directory
        if LoadConfig.getIfLocalSource(): 
            localFile = LoadConfig.getLocalImageSource()
            files = os.listdir(localFile)
            
            files.sort()
            
            for file in files:
                Herald.signalLoad(localFile+file)
                yield { 
                       'imgPath': file,
                       'img':cv2.imread(os.path.join(localFile,file), cv2.IMREAD_COLOR),
                       'tfImg': self.loadTensorFlowImage(os.path.join(localFile,file))
                    }
        
        # from distant directory
        else: 
            os.chmod('../img/temp', 777)
            
            import pysftp
            
            cnopts = pysftp.CnOpts(knownhosts='known_hosts')
            cnopts.hostkeys = None
            with pysftp.Connection(host=self.connexion.hostname, username=self.connexion.username, password=self.connexion.password, cnopts=cnopts) as sftp:
                Herald.printForLoader("Connection to FTP server succesfully established !")
                Herald.printForLoader("Loading the list of image names... Please wait. This could take up to a few minutes, depending on the number of images in the distant folder.")
                Herald.printForLoader("Please don't ctrl c during this time")
                
                sftp.cwd(LoadConfig.getRemoteImgSrc())
                
                # load names with a waiting animation
                done = False
                def animate():
                    for c in itertools.cycle(['|', '/', '-', '\\']):
                        if done :
                            break
                        sys.stdout.write('\rLoading ' + c )
                        sys.stdout.flush()
                        time.sleep(0.1)
                t = threading.Thread(target=animate)
                t.start()
                
                listNames = sftp.listdir()  
                done = True
                
                listNames.sort()
                
                
                Herald.printForLoader("\n"+str(len(listNames))+" image names loaded! Starting task distribution")
                
                while len(listNames)>0:
                    temp = listNames.pop(0)
                    Herald.signalLoad(temp)
                    
                    # download from remote in cache folder
                    sftp.get(temp, '../img/temp/'+temp)  
                    
                    # yield image from folder
                    yield { 
                            'imgPath': os.path.join(LoadConfig.getRemoteImgSrc(),temp),
                            'imgPathInCache': os.path.join('../img/temp/',temp),
                            'img': cv2.imread(os.path.join('../img/temp/',temp), cv2.IMREAD_COLOR),
                            'tfImg': self.loadTensorFlowImage(os.path.join('../img/temp/',temp))
                        }
                    
                    # remove image from cache
                    os.remove('../img/temp/'+temp)
        
        yield None

    def loadTensorFlowImage(self, path):
        img = tf.keras.preprocessing.image.load_img(
        path, color_mode="grayscale", target_size=(200, 200))
        img = tf.keras.preprocessing.image.img_to_array(img)
        img = img.astype('float32')/255.
        img = np.array([img])  # Convert single image to a batch.
        return img
