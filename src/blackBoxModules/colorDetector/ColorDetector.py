from typing import List
from Data.Color import Color

import cv2
import numpy as np
from skimage import io
from preprocess.BackgroundSuppression import BackgroundSuppression
from interface.ConfigLoader import ConfigLoader
import ast


from utilities.Herald import Herald
class ColorDetector:

    #Get the number of background used
    nbrBackground = len(ConfigLoader.getVariable("background"))
    
    def detectColorsOf(shoeImage):
        """
        Function which allowed to get the dominants colors and the counts of pixels for each colors

        :param shoeImage: image load

        :return : list of dominant color and the list of the counts of pixel for each colors
        """
        average = shoeImage.mean(axis=0).mean(axis=0)
        pixels = np.float32(shoeImage.reshape(-1, 3))

        n_colors = ColorDetector.nbrBackground + 4
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS

        #cv2 give in palette all the colors that we have in an image
        _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, ConfigLoader.getVariable('color_detection','attempts'), flags)
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

            #Get the new palette without the dominant and put the dominant in another variable
            palette, colorDominant = ColorDetector.getNewList(palette, dominant)
            listColorDominants.append(colorDominant)
            listCounts.append(count)
            
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
            for imgPreproc in imagesNoBg:
                colors,counts = ColorDetector.detectColorsOf(imgPreproc)
                listColorDominants.append(colors)
                listCounts.append(counts)
        return listColorDominants

    def deleteBackground(listColorDominants):
        """
        Delete background colors of list of dominant colors

        :param listColorDominants: list of dominant colors

        :return : list of dominant colors without background color of images
        """
        # load list of background color
        listColorBg = ColorDetector.getBackgroundColors('color')

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

    def getRatio(list, images):
        """
        Function estimate ratio of primary and secondary color for each image of the image list

        :param list: list of primary and secondary color for each images
        :param images: list of images

        :return : list of ratio for primary and secondary color for each image of the list
        """
        margiRgbCode = ConfigLoader.getVariable('color_detection','margin')

        # load background colors
        listRatioImages = []
        listColorBg = ColorDetector.getBackgroundColors('np')

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
                    moinsRGB, plusRGB = ColorDetector.rangeRatioRGB(rgbColorFound)

                    dstColorFound = cv2.inRange(img,moinsRGB, plusRGB)
                    #print("\n###################################################")
                    #print("\n moins :",moinsRGB)
                    #print("\n plus :",plusRGB)
                    ratioColorFound = cv2.countNonZero(dstColorFound)/(height*width)
                    ratioColorFound /= denominatorRatioColorFound
                    #print("\n Ratio : ",ratioColorFound)
                    #print("\n COULEUR : ",rgbColorFound)
                    #print("\n###################################################")
                    listRatio.append(ratioColorFound)
                listRatioImage.append(listRatio)
            listRatioImages.append(listRatioImage)
            
        listSumItem = []
        for item in listRatioImages:
            sumItem = []
            ratioColor1 = 0
            ratioColor2 = 0
            #print(item)
            for i in range(len(item)):
                ratioColor1 = ratioColor1 + item[i][0]
                ratioColor2 = ratioColor2 + item[i][1]
            ratioColor1 = ratioColor1/len(item)
            ratioColor2 = ratioColor2/len(item)
            sumItem.append(ratioColor1)
            sumItem.append(ratioColor2)
            listSumItem.append(sumItem)
        #print("\n LISTE SOMME",listSumItem)
        return listSumItem

    def associateRatioColor(listColor, listRatio):
        list = []
        for i in range(len(listColor)):
            dictRatio = {}
            for j in range(len(listColor[i])):
                dictRatio[listColor[i][j].name] = listRatio[i][j]
            list.append(dictRatio)
        return list

    def persistanceColor(list):
        """
        :param list : list of primary and secondary color
        """
        seuil = ConfigLoader.getVariable('color_detection','seuil')
        for dict in list:
            listKeySuppr = []
            if dict[max(dict, key=dict.get)] >= seuil:
                for key in dict:
                    if dict[key] < seuil:
                        listKeySuppr.append(key)
            else:
                keys = dict.keys()
                premierElem = str([*keys][0])
                deuxiemeElem = str([*keys][1])
                if (dict[premierElem] != dict[deuxiemeElem]):
                    dict.pop(min(dict, key=dict.get))

            if(len(listKeySuppr) != 0):
                dict.pop(key)

    def rangeRatioRGB(colorFound):
        """
        :param colorFound : color use for the range

        :return : minimal value, maximal value
        """
        moinsRGB = [0, 0, 0]
        plusRGB = [0, 0, 0]
        margiRgbCode = ConfigLoader.getVariable('color_detection','margin')

        for i in range(len(colorFound)):
            if colorFound[i]-margiRgbCode < 0:
                moinsRGB[i] = 0
            else:
                moinsRGB[i] = colorFound[i] - margiRgbCode
            
            if(colorFound[i] + margiRgbCode > 255):
                plusRGB[i] = 255
            else:
                plusRGB[i] = colorFound[i] + margiRgbCode
        
        return np.array(moinsRGB, np.uint8), np.array(plusRGB, np.uint8)

    def getBackgroundColors(mode):
        """
        Load background colors in a list

        :param mode: type of object in color list
            - color : color object
            - np : nparray with uint8 for rgb code
        
        :return : list of background colors
        """
        listColor = ConfigLoader.getVariable('background')
        listColorBg = []
        print()
        for color in listColor:
            if mode == 'color':
                newColor = Color(rgb=[(elem * 255) for elem in ast.literal_eval(listColor[color])])
                listColorBg.append(newColor.name)
            elif mode == 'np':
                bgColor = np.array([(elem * 255) for elem in ast.literal_eval(listColor[color])], np.uint8)
                listColorBg.append(bgColor)
        return listColorBg
    
    def printListColor(list):
        """
        Print informations of dominant color list

        :param list : dominant colors list
        """
        for i in range(len(list)):
            print('--------------------- IMAGE ',i+1 ,'---------------------')
            for color in list[i]:
                print('Color (name, rgb): (',color.name,',',color.rgb,')')
            print('----------------------------------------------------\n')

    def detection(images):
        """
        Function grouping together all the treatments

        :param images: list of images

        :return :
            - list of primary and secondary color for each image
            - list of ratio for primary and secondary color
        """
        print('Color detection started ...')
        if len(images) > 0:
            list = ColorDetector.getDominantColors(images)
            list = ColorDetector.deleteBackground(list)
            listFinal = ColorDetector.extractColor(list)
            listRatio = ColorDetector.getRatio(listFinal,images)
            res = ColorDetector.associateRatioColor(listFinal, listRatio)
            ColorDetector.persistanceColor(res)
        else:
            print("Error : no images loaded")
            res = -1
        print('Color detection DONE !')
        return res
