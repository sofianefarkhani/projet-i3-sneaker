#!/usr/bin/python3
# -*- coding: utf-8 -*-
from BlackBox import BlackBox

from interface.ConfigLoader import ConfigLoader
from interface.NewLoader    import Loader

import multiprocessing
from interface.Herald           import Herald
from processes.Utilities        import Utilities
from processes.Task             import *
from processes.LoaderMessage    import *
from processes.Enums            import *
import queue


def processAnswer(tasks, results, currentlyRunningNb):
    if Utilities.shouldAutoRegulate():
        try: 
            next_answer = results.get(False)
            if next_answer.type == AnswerType.ENDREQ and currentlyRunningNb>1:
                tasks.put(Task(TaskType.END, None))
                currentlyRunningNb-=1
        except: queue.Empty


if __name__ == '__main__':
    
    Herald.printStart(__name__)
    
    # Get basic parameters
    (numProcesses, procTalkative, bbTalkative) = Utilities.getRunningConfig()
    
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    loaderTasks = multiprocessing.JoinableQueue()
    loaderResults = multiprocessing.Queue()
    
    
    
    # start the loader
    loader = Loader(loaderTasks, loaderResults, tasks)
    loader.start()
    
    # Start BlackBoxes
    consumers = [ BlackBox(tasks, results, testMode = True) for i in range(numProcesses) ]
    for bb in consumers:
        bb.start()
        
    # create the variables that will keep track of the state of stuff
    mainRunning = True
    currentlyRunningNb = len(consumers)
    loaderIsLoading = False
    loaderRunning = True
    
    # Main loop: checks for answers
    while mainRunning:
        # Check if we need to load more and the loader is not already trying to load more  
        
        if tasks.qsize()==0 and not loaderIsLoading:
            if loaderRunning: 
                Herald.queueMessageIn(__name__, loaderTasks, LoaderTask(LoaderTaskType.LOAD))
                loaderIsLoading = True
            else: mainRunning = False
            
        # Process answers from the BlackBoxes.
        processAnswer(tasks, results, currentlyRunningNb)

        # Process answers from the Loader
        currentAnswerNb = loaderResults.qsize()
        for i in range(currentAnswerNb):                                # for each answer
            
            answer = Herald.getMessageFrom(__name__, loaderResults)
               
            if answer.type == LoaderAnswerType.NOMORE:                      # if he says there are no more images to load
                if Utilities.stopsWhenNoMoreImages():                       # if the run config is set to stop
                    Herald.queueMessageIn(__name__, loaderTasks, LoaderTask(LoaderTaskType.TERMINATE))
                    loaderRunning = False                                         # break main loop
            elif answer.type == LoaderAnswerType.LOADDONE:                  # if he says he finished loading images: 
                loaderIsLoading = False                                         # unlock the possibility of loading more images
        
        if Utilities.shouldReloadConfig():
            ConfigLoader.loadVars()
    
    
    # BRUTALLY MURDER each blackbox when Loader ends its service 
    for i in range(numProcesses):
        Herald.queueMessageIn(__name__, tasks, Task(TaskType.END, None))
        
    # Wait for all of the tasks to finish
    tasks.join()
    loaderTasks.join()
    
    Herald.printTermination(__name__)















########## NOT GOOD! DOES NOT CHECK IF THE INDEXES ARE GOOD 

# if __name__ == '__main__':
#     p1 = Process(target=bb1.startComputation)
#     p1.start()
#     p2 = Process(target=bb2.startComputation)
#     p2.start()
#     p1.join()
#     p2.join()