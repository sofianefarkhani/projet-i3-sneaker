#!/usr/bin/python3
# -*- coding: utf-8 -*-
from BlackBox import BlackBox
from TaskType import TaskType
from interface.Loader import Loader
import multiprocessing
from multiprocessing import Process
from Task import Task
import time
from interface.ConfigLoader import ConfigLoader


def calcNbProcessus():
    request = ConfigLoader.getVariable('runConfig', 'nbProcess')
    if request == 'default':
        return multiprocessing.cpu_count() -1
    else:
        return request

if __name__ == '__main__':
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    
    # Start consumers
    num_processes = calcNbProcessus()
    print ('Creating %d consumers' % num_processes)
    consumers = [ BlackBox(tasks, testMode = True) for i in range(num_processes) ]
    for bb in consumers:
        bb.start()
    
    # Enqueue jobs
    images = Loader.getImages(True);
    for img in images:
        if Loader.endOfService: 
            break
        tasks.put(Task(TaskType.PROCESS, img))
        #time.sleep(2)
        
    # job is finished: kill each blackbox
    for i in range(num_processes):
        tasks.put(Task(TaskType.END, img))

    # Wait for all of the tasks to finish
    tasks.join()
    















########## NOT GOOD! DOES NOT CHECK IF THE INDEXES ARE GOOD 

# if __name__ == '__main__':
#     p1 = Process(target=bb1.startComputation)
#     p1.start()
#     p2 = Process(target=bb2.startComputation)
#     p2.start()
#     p1.join()
#     p2.join()