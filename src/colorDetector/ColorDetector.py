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
    
    def detectColorsOf(shoeImage):
        """
        Function which allowed to get the dominants colors and the counts of pixels for each colors

        :param shoeImage: image load

        :return : list of dominant color and the list of the counts of pixel for each colors
        """

        #print('Color detector attributed a color to the given image.')
        #img = io.imread(shoeImage)[:, :, :-1]

        average = shoeImage.mean(axis=0).mean(axis=0)
        pixels = np.float32(shoeImage.reshape(-1, 3))

        n_colors = ColorDetector.nbrBackground + 4
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, .1)
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
        """
        Get the new palette without the dominant and put the dominant in another variable

        :param list: list of the main colors
        :param dominant: dominant color

        :return : list without dominant color, list exclusively compose of dominant color
        """
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
        """
        :param list
        :return : two list
        """
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
        """
        :param images: list of images load

        :return : list of dominant color
        """
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
        """
        Delete background colors of list of dominant colors

        :param listColorDominants: list of dominant colors

        :return : list of dominant colors without background color of images
        """

        # load list of background color
        listColor = ConfigLoader.getVariable('background')
        listColorBg = []
        for color in listColor:
            newColor = Color(rgb=[(elem * 255) for elem in ast.literal_eval(listColor[color])])
            listColorBg.append(newColor.name)

        listeTest = listColorDominants.copy()
        listFinal = []
        for elem in listeTest:
            listInterm = []
            for subelement in elem :
                temp = 0
                for color in subelement:
                    newColor = color.tolist()
                    newColor = Color(rgb=[newColor[2],newColor[1],newColor[0]])
                    if (newColor.name not in listColorBg):
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

    def extractColor(list):
        """
        Function extract primary and secondary color for each image

        :param list: list of dominant colors without background colors

        :return : list contains primary and secondary color for each image
        """
        colors = []
        for item in list:
            while(list != []):
                listInter = []
                for i in range(ColorDetector.nbrBackground):
                    listInter.append(list.pop(0))
                dictionnary = {}
                for i in range(len(listInter)):
                    for j in range(len(listInter[i])):
                        if(j in dictionnary):
                            dictionnary[j] = dictionnary[j] + 1
                        else:
                            dictionnary[j] = 1
                    listColor = []        
                    for k in range(2):
                        maxValue = max(dictionnary, key=dictionnary.get)
                        #print('\n Max value : ',maxValue)
                        #print('\n Name color : ',listInter[i][maxValue].name)
                        listColor.append(listInter[i][maxValue])
                        dictionnary.pop(maxValue)
                colors.append(listColor)
        return colors

        """
            for i in range(0,len(item),ColorDetector.nbrBackground):
                for j in range(len(item),i,-1):
                    for k in range(0,2,1):
                        if(list[i][k].name in list[j][0].name or list[i][k].name in list[j][1].name):
                            listInter.append(list[i][k].name)
            colors.append(listInter)
        return listInter
        """

    def getRatio(list, images):
        """
        Function estimate ratio of primary and secondary color for each image of the image list

        :param list: list of primary and secondary color for each images
        :param images: list of images

        :return : list of ratio for primary and secondary color for each image of the list
        """
        margiRgbCode = ConfigLoader.getVariable('color_detection','margin')

        # load background colors
        listColor = ConfigLoader.getVariable('background')
        listColorBg = []
        listRatioImages = []
        for color in listColor:
            bgColor = np.array([(elem * 255) for elem in ast.literal_eval(listColor[color])], np.uint8)
            listColorBg.append(bgColor)

        # calculate ratio with OpenCV
        for i in range(len(images)):
            imagesNoBg = BackgroundSuppression.replaceBackground(images[i])
            listRatioImage = []
            for j in range(len(imagesNoBg)):
                img = imagesNoBg[j]
                height, width, _ = img.shape
                listRatio = []
                dstBg = cv2.inRange(img, listColorBg[j], listColorBg[j])
                ratioBg = cv2.countNonZero(dstBg)/(height*width)
                denominatorRatioColorFound = 1 - ratioBg
                for k in range(len(list[i])):
                    rgbColorFound = np.array(list[i][k].rgb, np.uint8)
                    dstColorFound = cv2.inRange(img,rgbColorFound-margiRgbCode, rgbColorFound+margiRgbCode)
                    ratioColorFound = cv2.countNonZero(dstColorFound)/(height*width)
                    ratioColorFound /= denominatorRatioColorFound
                    listRatio.append(ratioColorFound)
            listRatioImage.append(listRatio)
            listRatioImages.append(listRatioImage)
        return listRatioImages

    def showImage(img):
        cv2.imshow("img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
