#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
from interface.ConfigLoader import ConfigLoader
import ast

class BackgroundSuppression:

    __BLUR = 21
    __CANNY_THRESH_1 = 20
    __CANNY_THRESH_2 = 20
    __MASK_DILATE_ITER = 10
    __MASK_ERODE_ITER = 10

    def replaceBackground(image):
        """
        Replace the background of an image by three color define in config.yaml.
        
        :param image: image load by OpenCV
        :return: list of images
        """
        __MASK_COLOR = ConfigLoader.getVariable('background')
        imagesNoBg = []
        if image is not None:
            gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, BackgroundSuppression.__CANNY_THRESH_1, BackgroundSuppression.__CANNY_THRESH_2)
            edges = cv2.dilate(edges, None)
            edges = cv2.erode(edges, None)
            contour_info = []
            contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            for c in contours:
                contour_info.append((
                    c,
                    cv2.isContourConvex(c),
                    cv2.contourArea(c),
                ))
            contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
            max_contour = contour_info[0]

            #-- Create empty mask, draw filled polygon on it corresponding to largest contour ----
            # Mask is black, polygon is white
            mask = np.zeros(edges.shape)
            cv2.fillConvexPoly(mask, max_contour[0], (255))

            #-- Smooth mask, then blur it --------------------------------------------------------
            mask = cv2.dilate(mask, None, iterations=BackgroundSuppression.__MASK_DILATE_ITER)
            mask = cv2.erode(mask, None, iterations=BackgroundSuppression.__MASK_ERODE_ITER)
            mask = cv2.GaussianBlur(mask, (BackgroundSuppression.__BLUR, BackgroundSuppression.__BLUR), 0)
            mask_stack = np.dstack([mask]*3)    # Create 3-channel alpha mask

            #-- Blend masked image into MASK_COLOR background --------------------------------------
            mask_stack  = mask_stack.astype('float32') / 255.0          # Use float matrices, 
            image         = image.astype('float32') / 255.0                 #  for easy blending

            for key in __MASK_COLOR:
                masked = (mask_stack * image) + ((1-mask_stack) * ast.literal_eval(__MASK_COLOR[key]))
                imagesNoBg.append((masked * 255).astype('uint8'))
         # Blend
        return imagesNoBg