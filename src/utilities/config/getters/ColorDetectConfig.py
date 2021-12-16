from utilities.config.AbstractGetter import AbstractGetter as AG
from utilities.config.ConfigChecker import ConfigChecker
from utilities.config.ConfigRequirementException import ConfigRequirementException

class ColorDetectConfig(AG):
    
    def getAttempts():
        return AG.get('color_detection', 'attempts')
    
    def getMargin():
        return AG.get('color_detection', 'margin')
    
    def getSeuil():
        return AG.get('color_detection', 'seuil')