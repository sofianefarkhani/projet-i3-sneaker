import os
from utilities.configUtilities.BBConfig import BBConfig
import json
import shutil

class DataFusion :

    def fusionJson():
        jsonObjectList = []
        pathFile = BBConfig.getTempOutput()
        outPutFile = ("../out/data.json")
        for fileName in os.listdir(pathFile):
            DataFusion.getObjectFromFile(pathFile+"/"+fileName,jsonObjectList)
        DataFusion.getSortedListe(jsonObjectList)
        tempList = []
        tempProduct = None
        while(len(jsonObjectList)>0):
            tempObject = jsonObjectList.pop(0)
            if(tempObject["IDProduct"] != tempProduct):
                dataToAdd = DataFusion.fusionProduct(tempList.copy())
                tempList = []
                tempProduct = tempObject["IDProduct"]
                if(dataToAdd != None):
                    fileData = open(outPutFile, "a")
                    newLineToWrite = json.dumps(dataToAdd) + "\n"
                    fileData.write(newLineToWrite)
                    fileData.close()
            else:
                tempList.append(tempObject)

        shutil.rmtree(pathFile,ignore_errors=True)
        os.mkdir("../out/temp")

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
            dictColorsSecondary = {}
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

                    if(len(dict["Colorway"]) > 1):
                        if(len(dictColorsSecondary) == 0):
                            dictColorsSecondary[dict["Colorway"]["secondaryColor"]["color"]] = 1
                        else:
                            if(dict["Colorway"]["secondaryColor"]["color"] in dictColorsSecondary):
                                dictColorsSecondary[dict["Colorway"]["secondaryColor"]["color"]] += 1
                            else:
                                dictColorsSecondary[dict["Colorway"]["secondaryColor"]["color"]] = 1

            shoeProb = sumProbProb/len(list)
            mainColor = max(dictColorsMain, key=dictColorsMain.get)
            if(len(dictColorsSecondary) != 0):
                secondaryColor = max(dictColorsSecondary, key=dictColorsSecondary.get)
            else:
                secondaryColor = None

            interDict["lstImg"]=listImg
            interDict["style"]=style
            interDict["mainColor"]=mainColor
            if(secondaryColor != None):
                if(secondaryColor != mainColor):
                    interDict["secondaryColor"]=secondaryColor
            interDict["probaShoes"]=shoeProb
            
            finalDict[IDProduct] = interDict
            return finalDict