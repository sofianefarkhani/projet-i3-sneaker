

from utilities.configUtilities.ConfigLoader import ConfigLoader


class LoadConfig:
    """Gets values from the config file to the Loader."""
    
    def getIfLocalSource():
        return ConfigLoader.getVariable('loader', 'takeFromLocalSource')
    
    def getLocalImageSource():
        return ConfigLoader.getVariable('loader', 'localImgSrc')
    
    def getRemoteImgSrc():
        return ConfigLoader.getVariable('loader', 'remoteImgSrc')
    
    def getBatchSize():
        return ConfigLoader.getVariable('loader', 'batchSize')

    def getReloadNumber():
        return ConfigLoader.getVariable('loader', 'reloadNumber')
       

    