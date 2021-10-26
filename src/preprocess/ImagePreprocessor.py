





from processes.Utilities import Utilities
class ImagePreprocessor:
    
    
    def preprocessForShoeExtraction(image):
        if Utilities.iaShouldTalk(): print("Preprocessing the image before detection and extraction of the shoe")
        return image
    
    def preprocessForColorsIdentification(image):
        if Utilities.iaShouldTalk(): print("Preprocessing the image before detecting the main colors of the shoe")
        return image
    
    def preprocessForTypeIdentification(image):
        if Utilities.iaShouldTalk(): print("Preprocessing the image before detecting the type of the shoe")
        return image