

import os


class DataFormatter:
    
    
    
    def buildColorWay(mainColor, secondaryColor):
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
    
    
    def getFullData(refProd:str, imgName:str, typeOfShoe, colorway:dict):
        return {
            "IDProduct": refProd,
            "img": imgName,
            "style": typeOfShoe,
            "Colorway": colorway
        }