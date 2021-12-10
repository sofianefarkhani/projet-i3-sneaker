



class ConfigRequirementException(Exception):
    
    def __init__(self, msg):
        message = '\n\n###############################\n\nThe configuration file contains an invalid parameter : \n'
        super().__init__(message+msg)