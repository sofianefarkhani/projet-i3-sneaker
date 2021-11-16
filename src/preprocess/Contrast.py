import cv2
from skimage.exposure import is_low_contrast

class Contrast:


    def run(image):
        # convert image in gray image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # blur the image slightly and perform edge detection
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 30, 150)
    
        msg = "Low contrast : NO"
        color = (0, 255, 0)
        if is_low_contrast(gray, fraction_threshold=0.35):
            msg = "Low contrast : YES"
            color = (0, 0, 255)

        # draw the text on the output image
        cv2.putText(image, msg, (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
            color, 2)
        # show the output image and edge map
        cv2.imshow("Image", image)
        cv2.imshow("Edge", edged)
        cv2.waitKey(0)
