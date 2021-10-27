from Data.Color import Color

import cv2
import numpy as np
from skimage import io
from preprocess.BackgroundSuppression import BackgroundSuppression




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
        _, counts = np.unique(labels, return_counts=True)
        
        listColorDominants = []
        listCounts = []
        for i in range(3):
            #print("\n I : ",i)
            count = 0

            dominant = palette[np.argmax(counts)]
            counts,count = ColorDetector.getCounts(counts)

            #print("\n Palette initiale ", palette)
            #print("\n Dominant ", dominant)

            palette, colorDominant = ColorDetector.getNewList(palette, dominant)
            listColorDominants.append(colorDominant)
            listCounts.append(count)
            #print("\n ListeCouleur : ",listColorDominants)
                        
            #print("\n Palette maintenant ", palette)
            #print("\n Counts : ", counts)

        return np.uint8(listColorDominants),np.uint8(listCounts)

    def getNewList(list, dominant):
        newList = []
        newListDominant = []
        xInNewList = 0
        for i in range(len(list)):
            if (list[i][0] == dominant[0] and list[i][1] == dominant[1] and list[i][2] == dominant[2]):
                xInNewList = i
        for i in range(len(list)):
            if(i != xInNewList):
                newList.append(list[i])
            else:
                newListDominant.append(list[i])
        return newList, newListDominant

    def getCounts(list):
        newList = []
        maxCounts = 0
        for i in range(len(list)):
            if(list[i] > maxCounts):
                maxCounts = list[i]
        for i in range(len(list)):
            if(list[i]!=maxCounts):
                newList.append(list[i])
        return newList, maxCounts

    def getDominantColors(images):
        listColorDominants = []
        listCounts = []
        colors = []
        counts = []
        for img in images:
            imagesNoBg = BackgroundSuppression.replaceBackground(img)
            #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            for imgPreproc in imagesNoBg:
                colors,counts = ColorDetector.detectColorsOf(imgPreproc)
                listColorDominants.append(colors)
                listCounts.append(counts)
                #ColorDetector.showImage(imgPreproc)

        #print("\nLISTE COULEURS ",np.uint8(listColorDominants))
        #print("\nLISTE COUNT ",np.uint8(listCounts))

        redColorBackground = [0,0,254]
        greenColorBackground = [0,254,0]
        blueColorBackground = [254,0,0]
        newListBlue = []
        newListRed = []
        indexGreen = 0
        indexBlue = 0
        indexRed = 0
        listCountGreen = []
        listCountBlue = []
        listCountRed = []

        nbrImage = (int)(len(listColorDominants)/3)
        listeTest = listColorDominants.copy()
        for elem in listeTest:
            for subelement in elem :
                for color in subelement:
                    newColor = color.tolist()
                    print("\n",str(newColor))
                    print("\n",str(greenColorBackground))
                    print("\n",type(color))
                    if(str(greenColorBackground) in str(newColor)):
                        print("OUIIIIIIIIIIIIIIIIIIIII")
                    else:
                        print("NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOON")
        
        """
        for i in range(nbrImage):
            newListGreen = []
            for j in range(3):
                if(listColorDominants[0 + 3*i][j][0] != greenColorBackground[0] and listColorDominants[0 + 3*i][j][1] != greenColorBackground[1] and listColorDominants[0 + 3*i][i][2] != greenColorBackground[2]):
                    newListGreen.append(listColorDominants[0][j])
                    indexGreen = j
            #ICI COUNTS
            listColorDominants[0+3*i] = newListGreen
        """

        """
        for i in range(3):
            if(i != indexGreen):
                listCountGreen.append(listCounts[i])
        listCounts
        """
        

        """
    for colors in range(len(listColorDominants)):
        for color in range(len(colors)):
            print("Voici une couleur : ", color)
            if(color == )
            """

    def showImage(img):
        cv2.imshow("img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
