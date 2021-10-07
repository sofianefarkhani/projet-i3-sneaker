#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cv2
class Loader :
    def __init__(self, readMode):
        if readMode == 'l':
            self.__img = cv2.imread('img/test/sneaker1.jpeg')

    def getImg(self):
        return self.__img
    
    def showImage(self):
        cv2.imshow("Img",self.__img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()