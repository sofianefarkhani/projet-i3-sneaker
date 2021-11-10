

from utilities.configUtilities.ConfigLoader import ConfigLoader

class BBConfig:
    
    
    def getIfShowImages():
        return ConfigLoader.getVariable('runConfig', 'gui', 'showImages')

    def getTestOutputFile():
        return ConfigLoader.getVariable('output', 'testData')
        
    def getOutputFile():
        return ConfigLoader.getVariable('output', 'data')