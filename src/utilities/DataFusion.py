import os
from utilities.configUtilities.BBConfig import BBConfig
import json 

class DataFusion :

    def fusionJson():
        jsonObjectList = []
        pathFile = BBConfig.getTempOutput()
        for fileName in os.listdir(pathFile):
            DataFusion.getObjectFromFile(pathFile+"/"+fileName,jsonObjectList)
        DataFusion.getSortedListe(jsonObjectList)
        tempList = []
        tempProduct = None
        while(len(jsonObjectList)>0):
            tempObject = jsonObjectList.pop(0)
            if(tempObject["IDProduct"] != tempProduct):
                DataFusion.fusionProduct(tempList.copy())
                tempList = []
                tempProduct = tempObject["IDProduct"]
            else:
                tempList.append(tempObject)

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
            for dict in list:
                #concaténer les img
                listImg.append(dict["img"])

                #ShoeProb -> moyenne
                sumProbProb = sumProbProb + float(dict["shoeProb"])

                #COLORWAY MOYENNE -> à la majorité -> dico avec détection couleur et nombre

                if(len(dictColorsMain) == 0):
                    dictColorsMain[dict["Colorway"]["mainColor"]["color"]] = 1
                else:
                    if(dict["Colorway"]["mainColor"]["color"] in dictColorsMain):
                        dictColorsMain[dict["Colorway"]["mainColor"]["color"]] += 1
                    else:
                        dictColorsMain[dict["Colorway"]["mainColor"]["color"]] = 1

            shoeProb = sumProbProb/len(list)
            mainColor = max(dictColorsMain, key=dictColorsMain.get)

            print("IDProduct : ",IDProduct," style : ",style," Liste Images : ",listImg," proba shoe : ", shoeProb, " couleur principal : ",mainColor)