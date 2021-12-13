
from utilities.configUtilities.ConfigLoader import ConfigLoader


class TypeDetectionConfig:
    
    def getModelFile():
        return ConfigLoader.getVariable('neuronNetworks', 'typeDetectModelFilePath')
    
    def getWeightsFile():
        return ConfigLoader.getVariable('neuronNetworks', 'typeDetectWeightsFilePath')
       