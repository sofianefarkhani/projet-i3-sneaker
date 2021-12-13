

import os


class DataFormatter:
    
    
    
    def buildColorWay(mainColor, secondaryColor):

        if(mainColor != None):
            colorway = {
                "mainColor": {
                    "color": mainColor.name,
                    "rgb": mainColor.rgb
                }
            }

            if secondaryColor != None:
                colorway["secondaryColor"] = {
                    "color": secondaryColor.name,
                    "rgb": secondaryColor.rgb
                }
            return colorway
        return {}
    
    def extractProdRef(imgName:str):
        tempRef = None
        if '-' in imgName:
            tempRef = imgName.split('-')[0]
        if tempRef is None:
            tempRef = imgName
        if '_' in tempRef:
            tempRef = tempRef.split('_')[0]
        return tempRef
    
    def getLastFromPath(path:str):
        return os.path.normpath(path)
    
    
    def getFullData(refProd:str, imgName:str, typeOfShoe, colorway:dict, shoeProb):
        return {
            "IDProduct": refProd,
            "img": imgName,
            "style": typeOfShoe,
            "Colorway": colorway,
            "shoeProb":str(shoeProb)
        }
    
    def getNoneData(refProd:str, imgName:str, shoeProb):
        return {
            "IDProduct": refProd,
            "img": imgName,
            "shoeProb":str(shoeProb)
        }