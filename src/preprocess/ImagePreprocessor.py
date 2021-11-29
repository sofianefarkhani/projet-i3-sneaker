import cv2
from preprocess.ContrastAndBrightness import ContrastAndBrightness
import numpy as np
class ImagePreprocessor:

    def contrastAndBrightnessAdjustment(image):
        """
        Adjust contrast and brightness of an image if image has a low contrast
        
        :param image : 
        """

        image = ContrastAndBrightness.adjustment(image)

        return image