from Data.Color import Color

import cv2
import numpy as np

from utilities.Herald import Herald
from utilities.config.getters.BGConfig import BGConfig as BGC 
from utilities.config.getters.ColorDetectConfig import ColorDetectConfig as CDC 

from blackBoxModules.preprocess.BackgroundSuppression import BackgroundSuppression
from utilities.Herald import Herald
from utilities.config.ConfigLoader import ConfigLoader

from blackBoxModules.preprocess.BackgroundSuppression import BackgroundSuppression
from blackBoxModules.preprocess.ContrastAndBrightness import ContrastAndBrightness

import cv2
import ast
import numpy as np

class ColorDetector:
    #Get the number of background used
    nbrBackground = BGC.getNbBg()
    
    def detectColorsOf(shoeImage):
        """
        Function which allowed to get the dominants colors and the counts of pixels for each colors

        :param shoeImage: image load

        :return : list of dominant color and the list of the counts of pixel for each colors
        """
        average = shoeImage.mean(axis=0).mean(axis=0)
        pixels = np.float32(shoeImage.reshape(-1, 3))

        n_colors = ColorDetector.nbrBackground + 4
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.1)
        flags = cv2.KMEANS_RANDOM_CENTERS

        # cv2 give in palette all the colors that we have in an image
        _, labels, palette = cv2.kmeans(
            pixels,
            n_colors,
            None,
            criteria,
            ConfigLoader.getVariable("color_detection", "attempts"),
            flags,
        )
        # counts has the number of pixels for each colors in palette
        _, counts = np.unique(labels, return_counts=True)

        listColorDominants = []
        listCounts = []

        # for each background, we take the dominants colors and the numbers of pixels for each dominants colors
        for i in range(ColorDetector.nbrBackground):
            while len(listColorDominants) != 3:

                count = 0

                # Get the dominants color
                dominant = palette[np.argmax(counts)]
                # Delete the counts for the dominant color and put it in another variable
                counts, count = ColorDetector.getCounts(counts)

                # Get the new palette without the dominant and put the dominant in another variable
                palette, colorDominant = ColorDetector.getNewList(palette, dominant)

                arr = np.array(listColorDominants)

                if Color(rgb=np.uint8(colorDominant)[0]).name not in [
                    Color(rgb=np.uint8(color)[0]).name for color in arr
                ]:
                    listColorDominants.append(colorDominant)
                    listCounts.append(count)

        # return of the list of dominant color and the list of the counts of pixel for each colors
        return np.uint8(listColorDominants), np.uint8(listCounts)

    def getNewList(list, dominant):
        """
        Get the new palette without the dominant and put the dominant in another variable

        :param list: list of the main colors
        :param dominant: dominant color

        :return : list without dominant color, list exclusively compose of dominant color
        """
        paletteColors = []
        listColorDominants = []
        indice = 0
        for i in range(len(list)):
            if (
                list[i][0] == dominant[0]
                and list[i][1] == dominant[1]
                and list[i][2] == dominant[2]
            ):
                indice = i
        for i in range(len(list)):
            if i != indice:
                paletteColors.append(list[i])
            else:
                listColorDominants.append(list[i])
        return paletteColors, listColorDominants

    def getCounts(list):
        """
        :param list
        :return : two list
        """
        counts = []
        maxCounts = 0
        for i in range(len(list)):
            if list[i] > maxCounts:
                # get the max pixel in one colors
                maxCounts = list[i]
        for i in range(len(list)):
            if list[i] != maxCounts:
                # delete the max count on the new list
                counts.append(list[i])
        return counts, maxCounts

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

            colors, counts = ColorDetector.detectColorsOf(imgPreproc)
            listColorDominants.append(colors)
            listCounts.append(counts)

        return listColorDominants

    def deleteBackground(listColorDominants):
        """
        Delete background colors of list of dominant colors

        :param listColorDominants: list of dominant colors

        :return : list of dominant colors without background color of images
        """
        listColorBg = ColorDetector.getBackgroundColors("color")

        listColorDominantsCopy = listColorDominants.copy()
        listColorsWithoutBg = []
        for elem in listColorDominantsCopy:
            listColors = []
            listNameColors = []
            for subelement in elem:

                for color in subelement:

                    colorList = color.tolist()
                    colorList = Color(rgb=[colorList[2], colorList[1], colorList[0]])

                    if colorList.name not in listColorBg:

                        listColors.append(colorList)
                        listNameColors.append(colorList.name)

            if len(listColors) > 2:

                listColors.pop(-1)
                listNameColors.pop(-1)

            listColorsWithoutBg.append(listColors)

        return listColorsWithoutBg

    def extractColor(list):
        """
        Function extract primary and secondary color for each image

        :param list: list of dominant colors without background colors

        :return : list contains primary and secondary color for each image
        """

        colors = []

        while list != []:
            temp = []
            for i in range(ColorDetector.nbrBackground):
                temp.append(list.pop(0))
            dictionnary = {}
            for i in range(len(temp)):
                for j in range(len(temp[i])):
                    if j in dictionnary:
                        dictionnary[j] = dictionnary[j] + 1
                    else:
                        dictionnary[j] = 1
                listColor = []

                if len(temp) != 0 and len(dictionnary) != 0:
                    for k in range(2):
                        maxValue = max(dictionnary, key=dictionnary.get)

                        listColor.append(temp[i][maxValue])
                        dictionnary.pop(maxValue)
                else:
                    listColor.append([])
            colors.append(listColor)
        return colors

    def getRatio(list, image):
        """
        Function estimate ratio of primary and secondary color for each image of the image list

        :param list: list of primary and secondary color for each images
        :param image: image

        :return : list of ratio for primary and secondary color for each image of the list
        """
        # load background colors
        listColorBg = ColorDetector.getBackgroundColors("np")
        listRatioImage = ColorDetector.calculateRatio(list, image, listColorBg)

        listRatios = []

        ratios = []
        ratioColor1 = 0
        ratioColor2 = 0

        for i in range(len(listRatioImage)):
            ratioColor1 = ratioColor1 + listRatioImage[i][0]
            ratioColor2 = ratioColor2 + listRatioImage[i][1]
        ratioColor1 = ratioColor1 / len(listRatioImage)
        ratioColor2 = ratioColor2 / len(listRatioImage)
        ratios.append(ratioColor1)
        ratios.append(ratioColor2)
        listRatios.append(ratios)

        return listRatios

    def calculateRatio(list, image, listColorBg):
        # calculate ratio with OpenCV
        imagesNoBg = BackgroundSuppression.replaceBackground(image)
        listRatioImage = []
        for j in range(len(imagesNoBg)):
            img = imagesNoBg[j]
            height, width, _ = img.shape
            listRatio = []
            dstBg = cv2.inRange(img, listColorBg[j], listColorBg[j])
            ratioBg = cv2.countNonZero(dstBg) / (height * width)
            denominatorRatioColorFound = 1 - ratioBg
            for k in range(len(list[0])):
                rgbColorFound = np.array(list[0][k].rgb, np.uint8)
                subRGB, addRGB = ColorDetector.rangeRatioRGB(rgbColorFound)

                dstColorFound = cv2.inRange(img, subRGB, addRGB)

                ratioColorFound = cv2.countNonZero(dstColorFound) / (height * width)
                ratioColorFound /= denominatorRatioColorFound

                listRatio.append(ratioColorFound)
            listRatioImage.append(listRatio)
        return listRatioImage

    def associateRatioColor(listColor, listRatio):
        listRatioColor = []
        for i in range(len(listColor)):
            dictRatio = {}
            for j in range(len(listColor[i])):
                dictRatio[listColor[i][j].name] = listRatio[i][j]
            listRatioColor.append(dictRatio)
        return listRatioColor

    def persistanceColor(list):
        """
        :param list : list of primary and secondary color
        """
        seuil = CDC.getSeuil()
        for dict in list:
            listKeySuppr = []
            if dict[max(dict, key=dict.get)] >= seuil:
                for key in dict:
                    if dict[key] < seuil:
                        listKeySuppr.append(key)
            else:
                keys = dict.keys()

                if len(keys) == 2:
                    firstItem = str([*keys][0])
                    secondItem = str([*keys][1])

                    if dict[firstItem] != dict[secondItem]:
                        dict.pop(min(dict, key=dict.get))

            if len(listKeySuppr) != 0:
                dict.pop(key)

    def rangeRatioRGB(colorFound):
        """
        :param colorFound : color use for the range

        :return : minimal value, maximal value
        """
        margiRgbCode = CDC.getMargin()
        subRGB = [0, 0, 0]
        addRGB = [0, 0, 0]

        for i in range(len(colorFound)):
            if colorFound[i] - margiRgbCode < 0:
                subRGB[i] = 0
            else:
                subRGB[i] = colorFound[i] - margiRgbCode

            if colorFound[i] + margiRgbCode > 255:
                addRGB[i] = 255
            else:
                addRGB[i] = colorFound[i] + margiRgbCode

        return np.array(subRGB, np.uint8), np.array(addRGB, np.uint8)

    def getBackgroundColors(mode):
        """
        Load background colors in a list

        :param mode: type of object in color list
            - color : color object
            - np : nparray with uint8 for rgb code
        
        :return : list of background colors
        """
        listColor = BGC.getBG()
        listColorBg = []
        for color in listColor:
            if mode == "color":
                newColor = Color(
                    rgb=[(elem * 255) for elem in ast.literal_eval(listColor[color])]
                )
                listColorBg.append(newColor.name)
            elif mode == "np":
                bgColor = np.array(
                    [(elem * 255) for elem in ast.literal_eval(listColor[color])],
                    np.uint8,
                )
                listColorBg.append(bgColor)
        return listColorBg

    def estimateDominantColor(image):
        pixels = np.float32(image.reshape(-1, 3))
        n_colors = 1
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.1)
        flags = cv2.KMEANS_RANDOM_CENTERS
        _, _, palette = cv2.kmeans(
            pixels,
            n_colors,
            None,
            criteria,
            ConfigLoader.getVariable("color_detection", "attempts"),
            flags,
        )
        palette = palette[0]
        return Color(rgb=[int(palette[2]),int(palette[1]),int(palette[0])])

    def detection(image, procname, imgName):
        """
        Function grouping together all the treatments

        :param images: list of images

        :return :
            - list of primary and secondary color for each image
            - list of ratio for primary and secondary color
        """
        Herald.printColorDetection(procname)

        mainColor = None
        secondaryColor = None

        contrast = ContrastAndBrightness.getContrastValue(image)
        if contrast >= 0.95:
            color = ColorDetector.estimateDominantColor(image)
            mainColor = color
        else :
            list = ColorDetector.getDominantColors(image)
            list = ColorDetector.deleteBackground(list)
            listColors = ColorDetector.extractColor(list)

            if len(listColors) >= 1 and len(listColors[0]) != 0:
                listRatio = ColorDetector.getRatio(listColors, image)
                colorWithRatio = ColorDetector.associateRatioColor(listColors, listRatio)

                ColorDetector.persistanceColor(colorWithRatio)

                keyList = colorWithRatio[0].keys()
                mainColor = Color(str([*keyList][0]))
                if len(keyList) > 1:
                    secondaryColor = Color(str([*keyList][1]))

        return (mainColor, secondaryColor)