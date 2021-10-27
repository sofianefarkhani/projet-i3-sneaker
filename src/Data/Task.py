
from Data.TaskType import TaskType
import time

class Task(object):
    '''A task contains a tasktype and an image.
    
    It is destined to be passed to BlackBoxes, who will deal with it.'''
    def __init__(self, taskType:TaskType, img = None):
        self.type = taskType
        self.img = img
    def __call__(self):
        time.sleep(0.1) # pretend to take some time to do the work
        return '%s' % (self.type)
    def __str__(self):
        return '%s' % (self.type)
