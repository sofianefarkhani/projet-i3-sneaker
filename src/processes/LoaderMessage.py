from processes.Enums import *
import time

class LoaderTask(object):
    '''A task contains a TaskType.
    
    It is destined to be passed to the Loader, who will deal with it.'''
    def __init__(self, taskType:LoaderTaskType):
        self.type = taskType
    def __call__(self):
        time.sleep(0.1) # pretend to take some time to do the work
        return '%s' % (self.type)
    def __str__(self):
        return '%s' % (self.type)

class LoaderAnswer(object):
    """An Answer is sent to the Main by the Loader. 
    
    It contains an AnswerType that caracterizes it."""
    def __init__(self, taskType:LoaderAnswerType):
        self.type = taskType
    def __call__(self):
        time.sleep(0.1) # pretend to take some time to do the work
        return '%s' % (self.type)
    def __str__(self):
        return '%s' % (self.type)
