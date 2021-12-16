import multiprocessing

from utilities.config.AbstractGetter import AbstractGetter

class RunConfigGeneral(AbstractGetter):
    
    def getNbProcess():
        '''Returns the number of processus asked in config.yaml'''
        request = RunConfigGeneral.get('runConfig', 'nbProcess')
        
        if request == 'default':
            return multiprocessing.cpu_count() - 2
        elif type(request) == int:
            if request > 0: return request
            else: raise ValueError('Please enter a strictly positive integer for the number of processes in config.yaml') 
        else:
            raise ValueError('Invalid value for a number of processes; you entered: "'+request+'". \nPlease modify this value in config.yaml.') 

    def getShowImages():
        return RunConfigGeneral.get('runConfig', 'gui', 'showImages')
    
    