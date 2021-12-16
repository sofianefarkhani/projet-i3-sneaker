
from utilities.config.AbstractGetter import AbstractGetter as AG

class TalkConfig(AG):
    
    def getProc():
        return AG.get('runConfig', 'talkative', 'processes')
    
    def getMsgs():
        return AG.get('runConfig', 'talkative', 'messages')
    
    def getIAs():
        return AG.get('runConfig', 'talkative', 'ias')
    
    def getIADetails():
        return AG.get('runConfig', 'talkative', 'ias-detailed')
    
    def getLoader():
        return AG.get('runConfig', 'talkative', 'loader')
    
    def getTF():
        return AG.get('runConfig', 'talkative', 'tensorflow')
    