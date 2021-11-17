import cv2
from skimage.exposure import is_low_contrast
from preprocess.ContrastAndBrightness import ContrastAndBrightness
class ImagePreprocessor:

    def contrastAndBrightnessAdjustment(image):
        """
        Adjust contrast and brightness of an image if image has a low contrast
        
        :param image : 
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if is_low_contrast(gray, fraction_threshold=0.35):
            print('Start contrast and brightness adjustment')
            ContrastAndBrightness.printInfoContrast(image, "LOW CONTRAST", (0, 0, 255))
            imageAdjust = ContrastAndBrightness.adjustment(image)
            ContrastAndBrightness.showImage(imageAdjust)
            print('Contrast and brightness adjustment : DONE')