from Data.Color import Color

import cv2
import numpy as np
from skimage import io




class ColorDetector:
    
    
    
    def detectColorsOf(shoeImage):
        '''Detects the two main colors of the given shoe, and returns them as a tuple.
        
        So far it only returns a dummy values.'''
        #print('Color detector attributed a color to the given image.')
        #img = io.imread(shoeImage)[:, :, :-1]
        average = shoeImage.mean(axis=0).mean(axis=0)
        pixels = np.float32(shoeImage.reshape(-1, 3))

        n_colors = 7
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS

        _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
        
        listColorDominants = []
        for i in range(3):
            #print("\n I : ",i)
            _, counts = np.unique(labels, return_counts=True)
            dominant = palette[np.argmax(counts)]

            #print("\n Palette initiale ", palette)
            #print("\n Dominant ", dominant)

            palette, colorDominant = ColorDetector.getNewList(palette, dominant)
            listColorDominants.append(colorDominant)
            #print("\n ListeCouleur : ",listColorDominants)
                        
            #print("\n Palette maintenant ", palette)
            #print("\n Counts : ", counts)



        return np.uint8(listColorDominants)

    def getNewList(list, dominant):
        newList = []
        newListDominant = []
        xInNewList = 0
        yInNewList = 0
        for i in range(len(list)):
            for j in range(len(list[i])):
                if list[i][j] == dominant[j]:
                    xInNewList = i
                    yInNewList = j
        for i in range(len(list)):
            if(i != xInNewList):
                newList.append(list[i])
            else:
                newListDominant.append(list[i])
        return newList, newListDominant