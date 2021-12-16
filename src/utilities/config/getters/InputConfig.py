from utilities.config.AbstractGetter import AbstractGetter as AG
from utilities.config.ConfigChecker import ConfigChecker
from utilities.config.ConfigRequirementException import ConfigRequirementException

class InputConfig(AG):
    
    def getTIF():
        return AG.get('input', 'trainingImagesFolder')
    
    def getSDETD():
        return AG.get('input', 'shoeDetectAndExtractTrainData')
    
    def getSTTD():
        return AG.get('input', 'shoeTypeTrainData')