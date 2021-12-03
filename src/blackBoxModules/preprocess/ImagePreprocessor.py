import cv2
from skimage.exposure import is_low_contrast
from blackBoxModules.preprocess.ContrastAndBrightness import ContrastAndBrightness
import numpy as np
class ImagePreprocessor:

    def contrastAndBrightnessAdjustment(image):
        """
        Adjust contrast and brightness of an image if image has a low contrast
        
        :param image : 
        """

        image = ContrastAndBrightness.adjustment(image)

        return image

    def resize(img):
        return cv2.resize(img, (600,600))