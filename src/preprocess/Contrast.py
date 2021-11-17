import cv2
from skimage.exposure import is_low_contrast
import numpy as np

class Contrast:


    def getContrast(image):
        # convert image in gray image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
        #msg = "Low contrast : NO"
        #color = (0, 255, 0)
        if is_low_contrast(gray, fraction_threshold=0.35):
            msg = "Low contrast : YES"
            color = (0, 0, 255)
            Contrast.printInfoContrast(image, msg, color)
            imageAdjust = Contrast.adjustment(image)
            Contrast.showImage(imageAdjust)

        #Contrast.printInfoContrast(image, msg, color)

    def adjustment(image):

        alpha = 2.0     # alpha is between 1.0 and 3.0
        beta = 50        # beta is between 0 and 100

        imageAdjust = np.zeros(image.shape, image.dtype)

        for y in range(image.shape[0]):
            for x in range(image.shape[1]):
                for c in range(image.shape[2]):
                    imageAdjust[y,x,c] = np.clip(alpha*image[y,x,c]+beta, 0, 255)

        return imageAdjust

    def printInfoContrast(image, msg, color):
        # draw the text on the output image
        cv2.putText(image, msg, (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
            color, 2)
        # show the output image
        cv2.imshow("Image", image)
        cv2.waitKey(0)

    def showImage(img):
        cv2.imshow("img adjust", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()  
