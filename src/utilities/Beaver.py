from utilities.config.getters.LogsConfig import LogsConfig as LC

class Beaver:
    """The Beaver likes logs. 
    
    Logs the activity of the application in the files defined in the config.yaml.
    """
    
    def reinitLogsIfNeeded():
        logFile = LC.getLogFile()
        if LC.getRmPrevious()==True:
            file_object = open(logFile, 'w')
            file_object.write("The wise Beaver's big dam of logs: ")
    
    def log(msg):
        logFile = LC.getLogFile()
        with open(logFile, 'a') as f:
            f.write("\n---------------------------------------\n"+msg)
            f.close()