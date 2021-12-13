from utilities.configUtilities.ConfigLoader import ConfigLoader

class ColorDetectorConfig:
    
    def getNbAttempts():
        return ConfigLoader.getVariable('color_detection','attempts')
    
    def getMargin():
        return ConfigLoader.getVariable('color_detection','margin')
    
    def getSeuil():
        return ConfigLoader.getVariable('color_detection','seuil')
    
    def getBackground():
        return ConfigLoader.getVariable('background')
    
    def getNbBg():
        return len(ColorDetectorConfig.getBackground())