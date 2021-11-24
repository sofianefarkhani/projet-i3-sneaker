import cv2
import numpy as np
from skimage.exposure import histogram

class ContrastAndBrightness:

    def adjustment(image, nbAlpha = 1, nbBeta = 1):
        """
        Adjust contrast and brightness of an image

        :param image : original image

        :return : image with new contrast and new brightness
        """
        max, min = ContrastAndBrightness.histogramme(image, 0.8)

        alpha = 255 / (max - min)     
        beta = -min * alpha           

        imageAdjust = cv2.convertScaleAbs(image, alpha=alpha * nbAlpha, beta=beta * nbBeta)

        ContrastAndBrightness.showImage(imageAdjust)

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

    def histogramme(image,clip_hist_percent=25):
        #Image in gray shade
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Calculate grayscale histogram
        hist = cv2.calcHist([gray],[0],None,[256],[0,256])
        hist_size = len(hist)

        # Calculate cumulative distribution from the histogram
        accumulator = []
        accumulator.append(float(hist[0]))
        for index in range(1, hist_size):
            accumulator.append(accumulator[index -1] + float(hist[index]))

        # Locate points to clip
        maximum = accumulator[-1]
        clip_hist_percent *= (maximum/100.0)
        clip_hist_percent /= 2.0

        # Locate left cut
        minimum_gray = 0
        while accumulator[minimum_gray] < clip_hist_percent:
            minimum_gray += 1

        # Locate right cut
        maximum_gray = hist_size -1
        while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
            maximum_gray -= 1
        
        return maximum_gray, minimum_gray