
from utilities.configUtilities.ConfigLoader import ConfigLoader

class Beaver:
    
    """The Beaver likes logs. 
    
    Logs the activity of the application in the files defined in the config.yaml.
    """
    
    def reinitLogsIfNeeded():
        logFile = ConfigLoader.getVariable('runConfig', 'logs', 'file')
        if ConfigLoader.getVariable('runConfig', 'logs', 'removePrevious')==True:
            file_object = open(logFile, 'w')
            file_object.write("The wise Beaver's big dam of logs: ")
    
    def log(msg):
        logFile = ConfigLoader.getVariable('runConfig', 'logs', 'file')
        file_object = open(logFile, 'a')
        file_object.write("\n---------------------------------------\n"+msg)