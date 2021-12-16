
from utilities.configUtilities.ConfigLoader import ConfigLoader


class ShoeDetectionConfig:
    
    def getModelFile():
        return ConfigLoader.getVariable('neuronNetworks', 'shoeDetectModelFilePath')
    
    def getWeightsFile():
        return ConfigLoader.getVariable('neuronNetworks', 'shoeDetectWeightsFilePath')
       