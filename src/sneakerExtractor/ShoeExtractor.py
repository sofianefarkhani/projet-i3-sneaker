
from processes.Utilities import Utilities



class ShoeExtractor:
    
    def extractShoeFromImage(image):
        if Utilities.iaShouldTalk(): print("Extracting shoe from the given image")
        return image