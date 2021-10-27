
from processes.Utilities import Utilities



class ShoeExtractor:
    
    def extractShoeFromImage(image, procName):
        if Utilities.iaShouldTalkInDetail(): print("%s: Extracting shoe from the given image" % procName)
        return image