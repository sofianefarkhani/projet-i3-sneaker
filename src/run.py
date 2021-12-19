#!/usr/bin/python3
# -*- coding: utf-8 -*-
import multiprocessing
from processes.Task             import *
from processes.LoaderMessage    import *
from processes.Enums            import *

from interface.Loader           import Loader
from interface.Writer           import Writer
from interface.Loader           import Connexion

from BlackBox                   import BlackBox

from utilities.Herald           import Herald
from utilities.Beaver           import Beaver 
from utilities.DataFusion       import DataFusion
from utilities.DataFusion       import Util as DFU

from utilities.config.getters.RunConfigGeneral import RunConfigGeneral as RCG 
from utilities.config.getters.LoaderConfig import LoaderConfig as LC 

if __name__ == '__main__':
    
    Herald.printStart(__name__)
    
    # Prepare environment
    Beaver.reinitLogsIfNeeded()
    Writer.prepareTempFiles()
    
    
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    loaderTasks = multiprocessing.JoinableQueue()
    loaderResults = multiprocessing.Queue()

    DFU.cleanTempFiles(True)
    
    try:
        # start the loader    
        c = Connexion() 
        loader = Loader(loaderTasks, loaderResults, tasks, c)
        loader.start()
        
        
        
        # Start BlackBoxes
        consumers = [ BlackBox(tasks, results, testMode = True) for i in range(RCG.getNbProcess()) ]
        
        for bb in consumers:
            bb.start()
                
        # create the variables that will keep track of the state of stuff
        mainRunning = True
        currentlyRunningNb = len(consumers)
        loaderIsLoading = False
        loaderRunning = True
        
        # Main loop: checks for answers
        while mainRunning:
            
            # check if everyone is still fine
            if currentlyRunningNb<=0 and loaderRunning==False: #  nobody running... Can only be a mistake. Destroy all tasks, exit the program.
                for i in range(tasks.qsize()):
                    t = Herald.getMessageFrom(__name__, tasks)
                    tasks.task_done()
                mainRunning = False
            
            # Check if we need to load more and the loader is not already trying to load more  
            # If the loader is stopped and there aer no more tasks, stop the whole machine.
            elif tasks.qsize()<=LC.getReloadNumber() and not loaderIsLoading:
                if loaderRunning: 
                    Herald.queueMessageIn(__name__, loaderTasks, LoaderTask(LoaderTaskType.LOAD))
                    loaderIsLoading = True
                
                elif tasks.qsize()==0: # NO MORE TASKS TO ACCOMLISH EVER! STOP EVERYTHING! 
                    mainRunning = False
            
            # Process answers from the BlackBoxes.
            currentAnswerNb = results.qsize()
            for i in range(currentAnswerNb):    # for each answer
                answer = Herald.getMessageFrom(__name__, results)
                if answer.type == AnswerType.BOXENDSERVICE:
                    currentlyRunningNb -= 1
                    if currentlyRunningNb <= 0: # this is an issue, politely stop the program.
                        Herald.queueMessageIn(__name__, loaderTasks, LoaderTask(LoaderTaskType.TERMINATE))
                        Herald.printError('No blackboxes are running. Politely stopping the program.')
            

            # Process answers from the Loader
            currentAnswerNb = loaderResults.qsize()
            for i in range(currentAnswerNb):                                # for each answer
                answer = Herald.getMessageFrom(__name__, loaderResults)
                
                if answer.type == LoaderAnswerType.NOMORE:                      # if he says there are no more images to load
                    Herald.queueMessageIn(__name__, loaderTasks, LoaderTask(LoaderTaskType.TERMINATE))
                    loaderRunning = False                                         # break main loop
                elif answer.type == LoaderAnswerType.LOADDONE:                  # if he says he finished loading images: 
                    loaderIsLoading = False                                         # unlock the possibility of loading more images
                elif answer.type == LoaderAnswerType.END:
                    loaderRunning = False   
                
        
        
        # BRUTALLY MURDER each blackbox when Loader ends its service 
        for i in range(currentlyRunningNb):
            Herald.queueMessageIn(__name__, tasks, Task(TaskType.END, None))
            
        # Wait for all of the tasks to finish
        tasks.join()
        loaderTasks.join()
        
        DataFusion.fusionJson()

        Herald.printTermination(__name__)


    except KeyboardInterrupt:
        # destroy all current tasks
        for i in range(tasks.qsize()):
            t = Herald.getMessageFrom(__name__, tasks)
            tasks.task_done()
        for i in range(loaderTasks.qsize()):
            t = Herald.getMessageFrom(__name__, loaderTasks)
            loaderTasks.task_done()
        
        # kill all blackboxes
        for i in range(currentlyRunningNb):
            Herald.queueMessageIn(__name__, tasks, Task(TaskType.END, None))
        # kill the loader
        Herald.queueMessageIn(__name__, loaderTasks, LoaderTask(LoaderTaskType.TERMINATE))
        
        # wait for the end of it all
        tasks.join()
        loaderTasks.join()