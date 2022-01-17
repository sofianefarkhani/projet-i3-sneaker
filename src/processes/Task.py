
from processes.Enums import *
import time

class Task(object):
    '''A task contains a tasktype and an image. It is destined to be passed to BlackBoxes, who will deal with it.'''
    def __init__(self, taskType:TaskType, imgPath=None, imgPathInCache=None, img=None, tfImg=None, tf2Img=None):
        self.type = taskType
        self.imgPath=imgPath
        self.imgPathInCache=imgPathInCache
        self.img = img
        self.tfImg = tfImg
        self.tf2Img= tf2Img
        
    def __str__(self):
        return '%s' % (self.type)
    
    # def __call__(self):
    #     time.sleep(0.1) # pretend to take some time to do the work
    #     return '%s' % (self.type)
    
class Answer(object):
    """An Answer is sent to the Main by a BlackBox. 
    
    It contains an AnswerType that caracterizes it."""
    def __init__(self, taskType:AnswerType):
        self.type = taskType
    def __call__(self):
        time.sleep(0.1) # pretend to take some time to do the work
        return '%s' % (self.type)
    def __str__(self):
        return '%s' % (self.type)
