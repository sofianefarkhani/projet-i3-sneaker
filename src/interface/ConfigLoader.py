import yaml

class ConfigLoader:
    configFile = '../config/config.yaml'
     
    def getVariable(*varPath):
        with open(ConfigLoader.configFile) as f:
            configData = yaml.load(f, Loader=yaml.FullLoader)
            
            validPath = 'In the file: '+ConfigLoader.configFile
            
            for i in range(len(varPath)):
                if dTemp := configData[varPath[i]]:
                    configData = configData[varPath[i]]
                else:
                    return None
            return configData