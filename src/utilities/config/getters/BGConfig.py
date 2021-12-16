from utilities.config.AbstractGetter import AbstractGetter as AG
from utilities.config.ConfigChecker import ConfigChecker
from utilities.config.ConfigRequirementException import ConfigRequirementException

class BGConfig(AG):
    
    def getBG():
        return AG.get('background')

    def getNbBg():
        return len(BGConfig.getBG().keys())