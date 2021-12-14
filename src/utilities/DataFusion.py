import os
from utilities.configUtilities.BBConfig import BBConfig
import json
import shutil
from statistics import median
import numpy as np
from interface.Writer import Writer 

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
                
                if tempProduct is not None:
                    Writer.registerProductAsDone(tempProduct)
                
                tempList = []
                tempProduct = tempObject["IDProduct"]
                if(dataToAdd != None): 
                    DataFusion.writeToFile(outPutFile, dataToAdd)
                    
            tempList.append(tempObject)

        
        if tempProduct is not None: Writer.registerProductAsDone(tempProduct)
        if((dataToAdd:=DataFusion.fusionProduct(tempList.copy())) is not None):
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
    
    def fusionProduct(imgDataList):
        '''Gets the data for ONE product, according to the informations from the images recorded in the parameter list.'''
        if(len(imgDataList) != 0):
            IDProduct = imgDataList[0]["IDProduct"]
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
            interDict = {}
            for imgData in imgDataList:
                #concaténer les img
                listImg.append(imgData["img"])

                #ShoeProb -> moyenne
                sumProbProb = sumProbProb + float(imgData["shoeProb"])

                #COLORWAY MOYENNE -> à la majorité -> dico avec détection couleur et nombre
                if("Colorway" in imgData):
                    if(len(dictColorsMain) == 0):
                        dictColorsMain[imgData["Colorway"]["mainColor"]["color"]] = 1
                    else:
                        if(imgData["Colorway"]["mainColor"]["color"] in dictColorsMain):
                            dictColorsMain[imgData["Colorway"]["mainColor"]["color"]] += 1
                        else:
                            dictColorsMain[imgData["Colorway"]["mainColor"]["color"]] = 1

                    listColorRedMain.append(imgData["Colorway"]["mainColor"]["rgb"][0])
                    listColorGreenMain.append(imgData["Colorway"]["mainColor"]["rgb"][1])
                    listColorBlueMain.append(imgData["Colorway"]["mainColor"]["rgb"][2])

                    if(len(imgData["Colorway"]) > 1):
                        if(len(dictColorsSecondary) == 0):
                            dictColorsSecondary[imgData["Colorway"]["secondaryColor"]["color"]] = 1
                        else:
                            if(imgData["Colorway"]["secondaryColor"]["color"] in dictColorsSecondary):
                                dictColorsSecondary[imgData["Colorway"]["secondaryColor"]["color"]] += 1
                            else:
                                dictColorsSecondary[imgData["Colorway"]["secondaryColor"]["color"]] = 1

                        listColorRedSecondary.append(imgData["Colorway"]["secondaryColor"]["rgb"][0])
                        listColorGreenSecondary.append(imgData["Colorway"]["secondaryColor"]["rgb"][1])
                        listColorBlueSecondary.append(imgData["Colorway"]["secondaryColor"]["rgb"][2])

            shoeProb = sumProbProb/len(imgDataList)

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