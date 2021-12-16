from utilities.config.AbstractGetter import AbstractGetter as AG


class LogsConfig(AG):
    
    def getLogFile():
        return AG.get('runConfig', 'logs', 'file')
        
    def getRmPrevious():
        return AG.get('runConfig', 'logs', 'removePrevious')
    
    def getProc():
        return AG.get('runConfig', 'logs', 'processes')
    
    def getMsgs():
        return AG.get('runConfig', 'logs', 'messages')
    
    def getIAs():
        return AG.get('runConfig', 'logs', 'ias')
    
    def getIADetails():
        return AG.get('runConfig', 'logs', 'ias-detailed')
    
    def getLoader():
        return AG.get('runConfig', 'logs', 'loader')