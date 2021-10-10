from Data.Color import Color




class ColorDetector:
    
    
    
    def detectColorsOf(shoeImage):
        '''Detects the two main colors of the given shoe, and returns them as a tuple.
        
        So far it only returns a dummy values.'''
        print('Color detector attributed a color to the given image.')
        return (Color(rgb = [13, 0, 255]), Color(rgb = [255, 71, 50]))