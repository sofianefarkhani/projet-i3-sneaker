

from utilities.configUtilities.ConfigLoader import ConfigLoader

class BBConfig:
    
    
    def getIfShowImages():
        return ConfigLoader.getVariable('runConfig', 'gui', 'showImages')

    def getTestOutputFile():
        return ConfigLoader.getVariable('output', 'testData')
        
    def getOutputFile():
        return ConfigLoader.getVariable('output', 'data')
    
    def getBackground():
        return ConfigLoader.getVariable('background')
    
    def getResultsShow():
        return ConfigLoader.getVariable('runConfig', 'talkative', 'ias')
    
    def getTempOutput():
        return ConfigLoader.getVariable('output', 'tempData')
    
    def getTFVerboseLvl():
        return str(ConfigLoader.getVariable('runConfig', 'talkative', 'tensorflow'))
    