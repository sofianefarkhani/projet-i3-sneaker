from typing import List
from Data.Color import Color

import cv2
import numpy as np
from skimage import io
from preprocess.BackgroundSuppression import BackgroundSuppression
from interface.ConfigLoader import ConfigLoader
import ast
class ColorDetector:

    #Get the number of background used
    nbrBackground = len(ConfigLoader.getVariable("background"))
    
    #function which allowed to get the dominants colors and the counts of pixels for each colors
    def detectColorsOf(shoeImage):

        #print('Color detector attributed a color to the given image.')
        #img = io.imread(shoeImage)[:, :, :-1]

        average = shoeImage.mean(axis=0).mean(axis=0)
        pixels = np.float32(shoeImage.reshape(-1, 3))

        n_colors = ColorDetector.nbrBackground + 4
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS

        #cv2 give in palette all the colors that we have in an image
        _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
        #counts has the number of pixels for each colors in palette
        _, counts = np.unique(labels, return_counts=True)
        
        listColorDominants = []
        listCounts = []

        #for each background, we take the dominants colors and the numbers of pixels for each dominants colors
        for i in range(ColorDetector.nbrBackground):
            #print("\n I : ",i)
            count = 0

            #Get the dominants color
            dominant = palette[np.argmax(counts)]
            #Delete the counts for the dominant color and put it in another variable
            counts,count = ColorDetector.getCounts(counts)

            #print("\n Palette initiale ", palette)
            #print("\n Dominant ", dominant)

            #Get the new palette without the dominant and put the dominant in another variable
            palette, colorDominant = ColorDetector.getNewList(palette, dominant)
            listColorDominants.append(colorDominant)
            listCounts.append(count)
            #print("\n ListeCouleur : ",listColorDominants)
                        
            #print("\n Palette maintenant ", palette)
            #print("\n Counts : ", counts)
        #return of the list of dominant color and the list of the counts of pixel for each colors
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
        return listColorDominants

    def deleteBackground(listColorDominants):
        listColor = ConfigLoader.getVariable('background')
        listColorBg = []
        for color in listColor:
            newColor = Color(rgb=[(elem * 255) for elem in ast.literal_eval(listColor[color])])
            listColorBg.append(newColor)
        #redColorBackground = [0,0,254]
        #greenColorBackground = [0,254,0]
        #blueColorBackground = [254,0,0]
        listeTest = listColorDominants.copy()
        listFinal = []
        for elem in listeTest:
            listInterm = []
            for subelement in elem :
                temp = 0
                for color in subelement:
                    newColor = color.tolist()
                    newColor = Color(rgb=[newColor[2],newColor[1],newColor[0]])
                    if [ (color.name) for color in listColorBg] != newColor.name:
                    #if(str(greenColorBackground) in str(newColor) or str(redColorBackground) in str(newColor) or str(blueColorBackground) in str(newColor) ):
                    #    print("")
                    #else:
                        if(temp < ColorDetector.nbrBackground):
                            listInterm.append(newColor)
            listFinal.append(listInterm)
        return listFinal

    #Inverse R and B to have a RGB color
    def reverseChannel(listIntermediaire):
        for elem in listIntermediaire :
            for subelement in elem :
                subelement.reverse()
        return listIntermediaire

    #Convert RGB into color
    def convertRBGtoColor(list):
        listFinal = []
        for elem in list :
            newList=[]
            for subelement in elem : 
                newList.append(Color(rgb = subelement))
            listFinal.append(newList)
        return listFinal

    #Get the primary color and the secondary color
    def getPrimaryAndSecondaryColor(listFinal):
        listColor = []
        for i in range(0,len(listFinal), ColorDetector.nbrBackground):
            listColorIntermediaire = []
            for j in range(1,ColorDetector.nbrBackground):
                for k in range(0,2,1):
                    if(listFinal[i][k].name in listFinal[j][0].name or listFinal[i][k].name in listFinal[j][1].name):
                        #listColorIntermediaire.append(color.name)
                        if(listFinal[i][k].name in listColorIntermediaire):
                            listColorIntermediaire.append(listFinal[i][k].name)
                            #print("\n LISTE INTERMEDIAIRE : ",listColorIntermediaire)
            listColor.append(listColorIntermediaire)
        return listColor

    def extractColor(list):
        colors = []
        for item in list:
            listInter = []
            for i in range(0,len(item),ColorDetector.nbrBackground):
                for j in range(len(item),i,-1):
                    for k in range(0,2,1):
                        if(list[i][k].name in list[j][0].name or list[i][k].name in list[j][1].name):
                            listInter.append(list[i][k].name)
            colors.append(listInter)
        return colors

    def showImage(img):
        cv2.imshow("img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
