
from utilities.config.AbstractGetter import AbstractGetter as AG

class LoaderConfig(AG):
    
    def sourceIsLocal():
        return AG.get('loader', 'takeFromLocalSource')
    
    def getLocalSource():
        return AG.get('loader', 'localImgSrc')
    
    def getRemoteSource():
        return AG.get('loader', 'remoteImgSrc')
    
    def getRemoteHost():
        return AG.get('loader', 'remoteCoIds', 'host')
    
    def getRemoteUser():
        return AG.get('loader', 'remoteCoIds', 'user')
    
    def getRemotePswd():
        return AG.get('loader', 'remoteCoIds', 'pswd')
    
    def getBatchsize():
        return AG.get('loader', 'batchSize')
    
    def getReloadNumber():
        return AG.get('loader', 'reloadNumber')
    
    def getDoneFile():
        return AG.get('loader', 'doneFile')
    
    def redoOldProducts():
        return AG.get('loader', 'redoOldProducts')