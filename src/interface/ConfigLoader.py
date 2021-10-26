import yaml

class ConfigLoader:
    configFile = '../config/config.yaml'
    
    lastLoadedVars = dict()
     
    def getVariable(*varPath):
        varPathAsString = ""
        for var in varPath: varPathAsString+="/"+var
        
        if varPathAsString in ConfigLoader.lastLoadedVars:
            return ConfigLoader.lastLoadedVars[varPathAsString]
        else: 
            return ConfigLoader.getVarFromFile(varPath)
    
    def getVarFromFile(varPath):
        '''Gets the asked for variable from the config file.'''        
        
        with open(ConfigLoader.configFile) as f:
            configData = yaml.load(f, Loader=yaml.FullLoader)
            for i in range(len(varPath)):
                if varPath[i] in configData:
                    configData = configData[varPath[i]]
                else:
                    raise ValueError('No such value in the config file: '+str(varPath)+"\n(failed at: "+str(varPath[i]))
            return configData
        
    def refreshValues():
        ConfigLoader.lastLoadedVars = dict()