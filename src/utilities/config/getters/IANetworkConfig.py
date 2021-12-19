from utilities.config.AbstractGetter import AbstractGetter as AG
from utilities.config.ConfigChecker import ConfigChecker
from utilities.config.ConfigRequirementException import ConfigRequirementException

class IANConfig(AG):
    
    def getSDModel():
        return AG.get('neuronNetworks', 'shoeDetectModelFilePath')
    
    def getSDWeights():
        return AG.get('neuronNetworks', 'shoeDetectWeightsFilePath')

    def getTDModel():
        return AG.get('neuronNetworks', 'typeDetectModelFilePath')
    
    def getTDWeights():
        return AG.get('neuronNetworks', 'typeDetectWeightsFilePath')
