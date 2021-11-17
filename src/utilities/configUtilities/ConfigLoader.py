import yaml

class ConfigLoader:
    configFile = '../config/config.yaml'
    
    lastLoadedVars = None
    
    
    def loadVars():
        with open(ConfigLoader.configFile) as f:
            ConfigLoader.lastLoadedVars = yaml.load(f, Loader=yaml.FullLoader)
    
    def getVariable(*varPath):
        if ConfigLoader.lastLoadedVars is None:
            ConfigLoader.loadVars()
        
        configData = ConfigLoader.lastLoadedVars
        for i in range(len(varPath)):
            if varPath[i] in configData:
                configData = configData[varPath[i]]
            else:
                raise ValueError('No such value in the config file: '+str(varPath)+"\n(failed at: "+str(varPath[i]))
        return configData
    
    
        
    