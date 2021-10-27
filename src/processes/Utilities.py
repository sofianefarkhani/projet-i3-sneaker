
from interface.ConfigLoader import ConfigLoader
import multiprocessing

class Utilities:
    
    
    def getRunningConfig():
        '''Returns (numProcesses, procTalkative, bbTalkative) from config.yaml'''
        numProcesses = Utilities.calcNbProcessus()
        procTalkative = ConfigLoader.getVariable('runConfig', 'talkative', 'processes')
        bbTalkative = ConfigLoader.getVariable('runConfig', 'talkative', 'ias')
        return (numProcesses, procTalkative, bbTalkative)
    
    def calcNbProcessus():
        '''Returns the number of processus asked in config.yaml'''
        request = ConfigLoader.getVariable('runConfig', 'nbProcess')
        if request == 'default':
            return multiprocessing.cpu_count() -1
        elif request == 'auto': 
            return multiprocessing.cpu_count() -1
        elif type(request) == int:
            if request > 0: return request
            else: raise ValueError('Please enter a strictly positive integer for the number of processes in config.yaml') 
        else:
            raise ValueError('Invalid value for a number of processes; you entered: "'+request+'". \nPlease modify this value in config.yaml.') 

    def isNbProcessAuto():
        return ConfigLoader.getVariable('runConfig', 'nbProcess') == 'auto'

    def shouldAutoRegulate():
        return ConfigLoader.getVariable('runConfig', 'nbProcess') == 'auto'

    def iaShouldTalk():
        return ConfigLoader.getVariable('runConfig', 'talkative', 'ias')
    
    def loaderShouldTalk():
        return ConfigLoader.getVariable('runConfig', 'talkative', 'loader')
    
    def iaShouldTalkInDetail():
        return ConfigLoader.getVariable('runConfig', 'talkative', 'ias-detailed')
    
    def shouldReloadConfig():
        return ConfigLoader.getVariable('runConfig', 'dynamicConfig')