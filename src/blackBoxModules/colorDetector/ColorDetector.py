from typing import List
from Data.Color import Color

import cv2
import numpy as np
from blackBoxModules.preprocess.BackgroundSuppression import BackgroundSuppression
from utilities.configUtilities.ConfigLoader import ConfigLoader
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
            while(len(listColorDominants) != 3):
            
                count = 0

                #Get the dominants color
                dominant = palette[np.argmax(counts)]
                #Delete the counts for the dominant color and put it in another variable
                counts,count = ColorDetector.getCounts(counts)

                #Get the new palette without the dominant and put the dominant in another variable
                palette, colorDominant = ColorDetector.getNewList(palette, dominant)

                arr = np.array(listColorDominants)
                #print(np.uint8(colorDominant))
                if(Color(rgb=np.uint8(colorDominant)[0]).name not in [Color(rgb=np.uint8(color)[0]).name for color in arr]):
                    listColorDominants.append(colorDominant)
                    listCounts.append(count)
            
        #return of the list of dominant color and the list of the counts of pixel for each colors
        return np.uint8(listColorDominants), np.uint8(listCounts)

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

    def getDominantColors(image):
        """
        :param image: loaded image

        :return : list of dominant color
        """
        listColorDominants = []
        listCounts = []
        colors = []
        counts = []
        
        imagesNoBg = BackgroundSuppression.replaceBackground(image)
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

        #for i in range(len(listColorDominants)):
        #    for j in range(len(listColorDominants)):
                #print("COULEURS DE LA LISTE AVANT LA SUPPR DU FOND : ",listColorDominants[i][j])
        
        listColorBg = ColorDetector.getBackgroundColors('color')

        listeTest = listColorDominants.copy()
        listFinal = []
        for elem in listeTest:
            listInterm = []
            listInterm2 = []
            for subelement in elem :
                
                for color in subelement:
                    
                    newColor = color.tolist()
                    newColor = Color(rgb=[newColor[2],newColor[1],newColor[0]])
                    #print("La couleur est créee : ", newColor.name)
                    if (newColor.name not in listColorBg):

                        listInterm.append(newColor)
                        listInterm2.append(newColor.name)
                            
            if(len(listInterm)>2):
                #print("IL PASSE DANS LA BOUCLE SUP 2 SUPPR")
                listInterm.pop(-1)
                listInterm2.pop(-1)

            listFinal.append(listInterm)
            #print("taille de la liste apres la suppression du fond ! normalement 2 : ", len(listInterm))
            #print("liste des couleurs dans la liste : ", listInterm2)
        return listFinal

    def extractColor(list, imgName):
        """
        Function extract primary and secondary color for each image

        :param list: list of dominant colors without background colors

        :return : list contains primary and secondary color for each image
        """
        
        #print("###################################  Taille de la liste: ", len(list))
        #print("################################### LIST : ",list)
        #print("------- Extract color: Nom de l'image:", imgName)

        colors = []
        #for item in list:
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
                
                #print("------- Extract color: listInter ", listInter)
                #print("------- Extract color: taille listInter ", listInter)
                #print("------- Extract color: dictionnary ", dictionnary)
                #print("------- Extract color: taille dictionnary ", len(dictionnary))

                if(len(listInter) != 0 and len(dictionnary) != 0):
                    for k in range(2):
                        maxValue = max(dictionnary, key=dictionnary.get)

                        #print("-------> Extract color: maxvalue ", maxValue)
                        #print("-------> Extract color: liste des couleurs ", listInter[i][maxValue].name)

                        listColor.append(listInter[i][maxValue])
                        dictionnary.pop(maxValue)
                else:
                    listColor.append([])
            colors.append(listColor)

            #print("-------> Extract color: liste couleurs finales ", colors)

        return colors

    def getRatio(list, image):
        """
        Function estimate ratio of primary and secondary color for each image of the image list

        :param list: list of primary and secondary color for each images
        :param image: image

        :return : list of ratio for primary and secondary color for each image of the list
        """
        margiRgbCode = ConfigLoader.getVariable('color_detection','margin')

        # load background colors
        listColorBg = ColorDetector.getBackgroundColors('np')

        # calculate ratio with OpenCV
        imagesNoBg = BackgroundSuppression.replaceBackground(image)
        listRatioImage = []
        for j in range(len(imagesNoBg)):
            img = imagesNoBg[j]
            height, width, _ = img.shape
            listRatio = []
            dstBg = cv2.inRange(img, listColorBg[j], listColorBg[j])
            ratioBg = cv2.countNonZero(dstBg)/(height*width)
            denominatorRatioColorFound = 1 - ratioBg
            for k in range(len(list[0])):
                rgbColorFound = np.array(list[0][k].rgb, np.uint8)
                moinsRGB, plusRGB = ColorDetector.rangeRatioRGB(rgbColorFound)

                dstColorFound = cv2.inRange(img,moinsRGB, plusRGB)
                
                ratioColorFound = cv2.countNonZero(dstColorFound)/(height*width)
                ratioColorFound /= denominatorRatioColorFound
                
                listRatio.append(ratioColorFound)
            listRatioImage.append(listRatio)
            
        listSumItem = []
        
        sumItem = []
        ratioColor1 = 0
        ratioColor2 = 0
        
        for i in range(len(listRatioImage)):
            ratioColor1 = ratioColor1 + listRatioImage[i][0]
            ratioColor2 = ratioColor2 + listRatioImage[i][1]
        ratioColor1 = ratioColor1/len(listRatioImage)
        ratioColor2 = ratioColor2/len(listRatioImage)
        sumItem.append(ratioColor1)
        sumItem.append(ratioColor2)
        listSumItem.append(sumItem)
        
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

                if(len(keys) == 2):
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
        for color in listColor:
            if mode == 'color':
                newColor = Color(rgb=[(elem * 255) for elem in ast.literal_eval(listColor[color])])
                listColorBg.append(newColor.name)
            elif mode == 'np':
                bgColor = np.array([(elem * 255) for elem in ast.literal_eval(listColor[color])], np.uint8)
                listColorBg.append(bgColor)
        return listColorBg
    
    

    def detection(image, procname, imgName):
        """
        Function grouping together all the treatments

        :param images: list of images

        :return :
            - list of primary and secondary color for each image
            - list of ratio for primary and secondary color
        """
        Herald.printColorDetection(procname)
        
        list = ColorDetector.getDominantColors(image)
        #print("****************************** sortie getDominantColors ", list)
        #print("****************************** taille ", len(list))

        list = ColorDetector.deleteBackground(list)
        #print("****************************** sortie deleteBackground ", list)
        #print("****************************** taille ", len(list))


        listFinal = ColorDetector.extractColor(list, imgName)
        #print("****************************** sortie extractColor ", listFinal)
        #print("****************************** taille ", len(listFinal))

        #print("########################################## Taille de la liste ", len(listFinal))
        #print("****************************************** contenu de la listeFinal ", listFinal)
        #print("****************************************** taille de la listeFinal ", len(listFinal[0]))

        if(len(listFinal) >= 1 and len(listFinal[0]) != 0):
            listRatio = ColorDetector.getRatio(listFinal,image)
            res = ColorDetector.associateRatioColor(listFinal, listRatio)
        
            ColorDetector.persistanceColor(res)
            
            keyList = res[0].keys()
            mainColor = Color(str([*keyList][0]))
            secondaryColor = None
            if len(keyList)>1:
                secondaryColor = Color(str([*keyList][1]))
        else:
            mainColor = None
            secondaryColor = None  

        #print(" ============ main color: ", mainColor.name)
        #print(" ============ second color: ", secondaryColor.name)

        return (mainColor, secondaryColor)

    def showImage(img):
        cv2.imshow("img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()