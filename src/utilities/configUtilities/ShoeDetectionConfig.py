
from utilities.configUtilities.ConfigLoader import ConfigLoader


class ShoeDetectionConfig:
    
    def getModelFile():
        return ConfigLoader.getVariable('shoeDetection', 'modelFilePath')
    
    def getWeightsFile():
        return ConfigLoader.getVariable('shoeDetection', 'weightsFilePath')
       