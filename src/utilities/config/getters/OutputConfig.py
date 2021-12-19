from utilities.config.AbstractGetter import AbstractGetter as AG
from utilities.config.ConfigChecker import ConfigChecker
from utilities.config.ConfigRequirementException import ConfigRequirementException

class OutputConfig(AG):
    
    def getData():
        return AG.get('output', 'data')
    
    def getTestData():
        return AG.get('output', 'testData')
        
    def getTempData():
        '''Gets and checks the existence of the dir for the temp output. Create the dir if non existent.'''
        dir = AG.get('output', 'tempData')
        AG.makeSureDirExists(dir, ['output', 'tempData']) 
        if dir[-1]=='/' or dir[-1]=='\\':
            dir = dir[:-1]     
        return dir
        
    def getKeepTempFiles():
        return AG.get('output', 'keepTempFiles')