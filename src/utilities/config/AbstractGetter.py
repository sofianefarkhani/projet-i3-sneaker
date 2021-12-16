


from utilities.config.ConfigChecker import ConfigChecker
from utilities.config.ConfigLoader import ConfigLoader
import os.path as map

from utilities.config.ConfigRequirementException import ConfigRequirementException

class AbstractGetter:
    '''Returns the values asked for, after checking them and modifying stuff if necessary. 
    Trusts that ConfigChecker has done its work.'''
    
    def get(*varPath):
        return ConfigLoader.getVarFromList(varPath)
       
       
    ###### DIRECTORY CHECKS
    def checkedDirPath(dir, var):
        '''Raises an exception if what we are looking at is not a dir or does not exist.'''
        if map.exists(dir)==False or map.isdir(dir)==False: 
            configPath = ConfigChecker.getPathAsException(var)
            raise ConfigRequirementException('Invalid directory for '+configPath)
    
    def makeSureDirExists(dir, var):
        if map.isdir(dir) == False: 
            configPath = ConfigChecker.getPathAsException(var)
            raise ConfigRequirementException('Invalid directory for '+configPath)
        if map.exists(dir)==False:
            map.mkdir(dir, mode=0o777)
                
    
    
    ###### FILE CHECKS
    def checkExistanceOfFile(file:str):
        return map.isfile(file)