#!/usr/bin/python3
# -*- coding: utf-8 -*-
from BlackBox import BlackBox
from processes.TaskType import TaskType
from interface.Loader import Loader
import multiprocessing
from processes.Task import Task
from processes.Utilities import Utilities


if __name__ == '__main__':
    # Get basic parameters
    (numProcesses, procTalkative, bbTalkative) = Utilities.getRunningConfig()
    
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    
    # Start consumers
    
    if procTalkative: print ('Creating %d consumers' % numProcesses)
    consumers = [ BlackBox(tasks, testMode = True) for i in range(numProcesses) ]
    for bb in consumers:
        bb.start()
    
    # Enqueue jobs 
    images = Loader.getImages();
    for img in images:                              # Main loop
        if Loader.endOfService: break
        tasks.put(Task(TaskType.PROCESS, img))
        
    # BRUTALLY MURDER each blackbox when Loader ends its service 
    for i in range(numProcesses):
        tasks.put(Task(TaskType.END, img))

    # Wait for all of the tasks to finish
    tasks.join()
    
    if procTalkative: print("t'was fun working with you :D")
    















########## NOT GOOD! DOES NOT CHECK IF THE INDEXES ARE GOOD 

# if __name__ == '__main__':
#     p1 = Process(target=bb1.startComputation)
#     p1.start()
#     p2 = Process(target=bb2.startComputation)
#     p2.start()
#     p1.join()
#     p2.join()