import os
from utilities.configUtilities.BBConfig import BBConfig
import json
import shutil
from statistics import median
import numpy as np

class DataFusion :

    def fusionJson():
        jsonObjectList = []
        pathFile = BBConfig.getTempOutput()
        outPutFile = ("../out/data.json")
        if(os.path.exists(outPutFile)):
            os.remove(outPutFile)
        for fileName in os.listdir(pathFile):
            DataFusion.getObjectFromFile(pathFile+"/"+fileName,jsonObjectList)
        DataFusion.getSortedListe(jsonObjectList)
        tempList = []
        tempProduct = None
        while(len(jsonObjectList) != 0):
            tempObject = jsonObjectList.pop(0)

            # if this is a new product
            if(tempObject["IDProduct"] != tempProduct):
                dataToAdd = DataFusion.fusionProduct(tempList.copy())
                tempList = []
                tempProduct = tempObject["IDProduct"]
                if(dataToAdd != None):
                    DataFusion.writeToFile(outPutFile, dataToAdd)
                    
            tempList.append(tempObject)

        dataToAdd = DataFusion.fusionProduct(tempList.copy())
        if(dataToAdd != None):
            DataFusion.writeToFile(outPutFile, dataToAdd)

        shutil.rmtree(pathFile,ignore_errors=True)
        os.mkdir("../out/temp")

    def writeToFile(outPutFile, dataToAdd):
        fileData = open(outPutFile, "a")
        newLineToWrite = json.dumps(dataToAdd) + "\n"
        fileData.write(newLineToWrite)
        fileData.close()

    def decodeJson(string:str):
        return json.loads(string)

    def getObjectFromFile(file,jsonList):
        with open(file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if not line.strip()=="":
                    jsonList.append(DataFusion.decodeJson(line))
    
    def getSortedListe(list):
        list.sort(key=lambda x : x["IDProduct"])
    
    def fusionProduct(list):
        if(len(list) != 0):
            IDProduct = list[0]["IDProduct"]
            style = "NOT IMPLEMENTED YET"
            listImg = []
            sumProbProb = 0
            dictColorsMain = {}
            listColorRedMain = []
            listColorGreenMain = []
            listColorBlueMain = []
            dictColorsSecondary = {}
            listColorRedSecondary = []
            listColorGreenSecondary = []
            listColorBlueSecondary = []
            finalList = []
            finalDict = {}
            interDict = {}
            for dict in list:
                #concaténer les img
                listImg.append(dict["img"])

                #ShoeProb -> moyenne
                sumProbProb = sumProbProb + float(dict["shoeProb"])

                #COLORWAY MOYENNE -> à la majorité -> dico avec détection couleur et nombre
                if("Colorway" in dict):
                    if(len(dictColorsMain) == 0):
                        dictColorsMain[dict["Colorway"]["mainColor"]["color"]] = 1
                    else:
                        if(dict["Colorway"]["mainColor"]["color"] in dictColorsMain):
                            dictColorsMain[dict["Colorway"]["mainColor"]["color"]] += 1
                        else:
                            dictColorsMain[dict["Colorway"]["mainColor"]["color"]] = 1

                    listColorRedMain.append(dict["Colorway"]["mainColor"]["rgb"][0])
                    listColorGreenMain.append(dict["Colorway"]["mainColor"]["rgb"][1])
                    listColorBlueMain.append(dict["Colorway"]["mainColor"]["rgb"][2])

                    if(len(dict["Colorway"]) > 1):
                        if(len(dictColorsSecondary) == 0):
                            dictColorsSecondary[dict["Colorway"]["secondaryColor"]["color"]] = 1
                        else:
                            if(dict["Colorway"]["secondaryColor"]["color"] in dictColorsSecondary):
                                dictColorsSecondary[dict["Colorway"]["secondaryColor"]["color"]] += 1
                            else:
                                dictColorsSecondary[dict["Colorway"]["secondaryColor"]["color"]] = 1

                        listColorRedSecondary.append(dict["Colorway"]["secondaryColor"]["rgb"][0])
                        listColorGreenSecondary.append(dict["Colorway"]["secondaryColor"]["rgb"][1])
                        listColorBlueSecondary.append(dict["Colorway"]["secondaryColor"]["rgb"][2])

            shoeProb = sumProbProb/len(list)

            if(len(dictColorsMain) != 0):
                mainColor = max(dictColorsMain, key=dictColorsMain.get)
                listColorRedMain.sort()
                RGBRedMain = median(listColorRedMain)
                listColorGreenMain.sort()
                RGBGreenMain = median(listColorGreenMain)
                listColorBlueMain.sort()
                RGBBlueMain = median(listColorBlueMain)
                RGBMain = [RGBRedMain,RGBGreenMain,RGBBlueMain]
            else:
                mainColor = None

            if(len(dictColorsSecondary) != 0):
                secondaryColor = max(dictColorsSecondary, key=dictColorsSecondary.get)
                listColorRedMain.sort()
                RGBRedSecondary = median(listColorRedSecondary)
                listColorGreenSecondary.sort()
                RGBGreenSecondary = median(listColorGreenSecondary)
                listColorBlueSecondary.sort()
                RGBBlueSecondary = median(listColorBlueSecondary)
                RGBSecondary = [RGBRedSecondary,RGBGreenSecondary,RGBBlueSecondary]
            else:
                secondaryColor = None

            colorDict = {}
            interDict["idProduct"]=IDProduct
            interDict["lstImg"]=listImg
            interDict["style"]=style
            if(mainColor != None):
                interDict["Colorway"]=[]
                interDict["Colorway"].append({"mainColor":{"name":mainColor,"rgb":RGBMain}})
            if(secondaryColor != None):
                if(secondaryColor != mainColor):
                    interDict["Colorway"].append({"secondaryColor":{"name":secondaryColor,"rgb":RGBSecondary}})
            interDict["probaShoes"]=np.round(shoeProb, 3)
            
            return interDict