from Data.Color import Color



from utilities.Herald import Herald
class ColorDetector:
    
    
    
    def detectColorsOf(shoeImage, procName):
        '''Detects the two main colors of the given shoe, and returns them as a tuple.
        
        So far it only returns a dummy values.'''
        Herald.printColorDetection(procName)
        return (Color(rgb = [13, 0, 255]), Color(rgb = [255, 71, 50]))