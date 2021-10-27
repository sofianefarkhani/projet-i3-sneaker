





from processes.Utilities import Utilities
class ImagePreprocessor:
    
    
    def preprocessForShoeExtraction(image, procName):
        if Utilities.iaShouldTalkInDetail(): print("%s: Preprocessing the image before detection and extraction of the shoe"% procName)
        return image
    
    def preprocessForColorsIdentification(image, procName):
        if Utilities.iaShouldTalkInDetail(): print("%s: Preprocessing the image before detecting the main colors of the shoe"% procName)
        return image
    
    def preprocessForTypeIdentification(image, procName):
        if Utilities.iaShouldTalkInDetail(): print("%s: Preprocessing the image before detecting the type of the shoe"% procName)
        return image