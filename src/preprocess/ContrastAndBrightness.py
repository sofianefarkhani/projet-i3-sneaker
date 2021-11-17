import cv2
import numpy as np

class ContrastAndBrightness:

    def adjustment(image):
        """
        Adjust contrast and brightness of an image

        :param image : original image

        :return : image with new contrast and new brightness
        """
        alpha = 2.0     # alpha is between 1.0 and 3.0
        beta = 50        # beta is between 0 and 100

        imageAdjust = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

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
