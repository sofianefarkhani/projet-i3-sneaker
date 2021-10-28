from typing import List
from Data.Color import Color

import cv2
import numpy as np
from skimage import io
from preprocess.BackgroundSuppression import BackgroundSuppression
from interface.ConfigLoader import ConfigLoader
class ColorDetector:

    nbrBackground = len(ConfigLoader.getVariable("background"))
    
    def detectColorsOf(shoeImage):
        '''Detects the two main colors of the given shoe, and returns them as a tuple.
        
        So far it only returns a dummy values.'''
        #print('Color detector attributed a color to the given image.')
        #img = io.imread(shoeImage)[:, :, :-1]
        average = shoeImage.mean(axis=0).mean(axis=0)
        pixels = np.float32(shoeImage.reshape(-1, 3))

        n_colors = 7 #modif this parameter in funtion of nbrBackground
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS

        _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
        _, counts = np.unique(labels, return_counts=True)
        
        listColorDominants = []
        listCounts = []

        for i in range(ColorDetector.nbrBackground):
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
                #get the max pixel in one colors
                maxCounts = list[i]
        for i in range(len(list)):
            if(list[i]!=maxCounts):
                #delete the max count on the new list
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

        listeTest = listColorDominants.copy()

        #Delete background of the list
        listIntermediaire = []
        for elem in listeTest:
            listInterm = []
            for subelement in elem :
                temp = 0
                for color in subelement:
                    newColor = color.tolist()
                    if(str(greenColorBackground) in str(newColor) or str(redColorBackground) in str(newColor) or str(blueColorBackground) in str(newColor) ):
                        print("")
                    else:
                        if(temp < ColorDetector.nbrBackground):
                            listInterm.append(newColor)
            listIntermediaire.append(listInterm)

        #Inverse R and B to have a RGB color
        for elem in listIntermediaire :
            for subelement in elem :
                subelement.reverse()
        #print('\n',listIntermediaire)
        
        #Convert the RGB code in Color
        listFinal = []
        for elem in listIntermediaire :
            newList=[]
            for subelement in elem : 
                newList.append(Color(rgb = subelement))
            listFinal.append(newList)

        #print('\n',listFinal)

        #Get primary color and secondary color
        listColor = []
        for i in range(0,len(listFinal), ColorDetector.nbrBackground):
            listColorIntermediaire = []
            for j in range(1,ColorDetector.nbrBackground+1):
                for color in listFinal[i]:
                    if(color.name in listFinal[j][0].name or color.name in listFinal[j][1].name):
                        #listColorIntermediaire.append(color.name)
                        if(not(color.name in listColorIntermediaire)):
                            listColorIntermediaire.append(color.name)
                            #print("\n LISTE INTERMEDIAIRE : ",listColorIntermediaire)
            listColor.append(listColorIntermediaire)
        print("\n LISTE FINAL : ",listColor)
        print("\n taille ",len(listColor))


    def showImage(img):
        cv2.imshow("img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
