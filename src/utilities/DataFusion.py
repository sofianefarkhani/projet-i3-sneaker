import os
import json
import shutil
import numpy                                as np
from statistics                             import median
from utilities.configUtilities.BBConfig     import BBConfig
from utilities.configUtilities.LoadConfig   import LoadConfig




class Util:
    '''A simple utility class that does simple, menial tasks.'''
    def removeOldData():
        '''Destroys the data file from the previous session.'''
        path = BBConfig.getOutputFile()
        if(os.path.exists(path)): 
            os.remove(BBConfig.getOutputFile(path))
    
    def writeToFile(dataToAdd):
        if dataToAdd is None: return
        outPutFile = BBConfig.getOutputFile()
        with open(outPutFile, "a") as f:
            newLineToWrite = json.dumps(dataToAdd) + "\n"
            f.write(newLineToWrite)
            f.close()

    def getObjectsFromFile(file,jsonList):
        '''Adds the objects (one by image) with the data found by one blackbox, to the given list.'''
        with open(file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if not line.strip()=="":
                    jsonList.append(json.loads(line))
            f.close()
    
    def sortByIdOfProduct(list):
        list.sort(key=lambda x : x["IDProduct"])
        
    def cleanTempFiles():
        '''Removes the temporary files created by the blackboxes.'''
        pathFile = BBConfig.getTempOutput()
        shutil.rmtree(pathFile,ignore_errors=True)
        os.mkdir(pathFile)
    
    def registerProductAsDone(product:str):
        '''Registers the product in a file. Products found in this file will not be dealt with again.'''
        if product is None: return
        with open(LoadConfig.getProdDoneFile(), 'a') as f:
            f.write(','+product)


class DataFusion :

    def fusionJson():
        '''Searches through the temp json files created by each blackbox, and gathers product by product the results for each related image.
        Then adds the fusion of these results to the final json.'''
        
        jsonObjectList = []                 # the list of objects (one by img) in all blackbox-temp-jsons
        pathFile = BBConfig.getTempOutput()
        
        # prepare file for final data
        Util.removeOldData()
        
        # prepare data from the temp json files (one per blackbox ran)
        for fileName in os.listdir(pathFile):
            Util.getObjectsFromFile(pathFile+"/"+fileName,jsonObjectList)   
        Util.sortByIdOfProduct(jsonObjectList)
        
        tempList = []       # will contain the images for one product.
        tempProduct = None  # tells the ID of the product we wanna place in tempList.
        
        while(len(jsonObjectList) != 0):        # while there's still image's data to sort
            tempObject = jsonObjectList.pop(0)

            # if this is a new product
            if(tempObject["IDProduct"] != tempProduct):
                dataToAdd = DataFusion.fusionOfOneProduct(tempList.copy())  # Fuse its data into the final json
                
                # write the product as done (on next use of the Launcher, product will not be reused.)
                Util.registerProductAsDone(tempProduct)
                
                # prepare for next product
                tempList = []
                tempProduct = tempObject["IDProduct"]
                
                # register the final data
                Util.writeToFile(dataToAdd)
               
            tempList.append(tempObject) # add the new image to the list for the current product.  

        # all images are sorted, except the last one: sort it.
        Util.registerProductAsDone(tempProduct)
        Util.writeToFile(DataFusion.fusionOfOneProduct(tempList.copy()))

        Util.cleanTempFiles()


    ### FROM ONE LIST FOR ONE PRODUCT, FIND THE FINAL RESULT
    def fusionOfOneProduct(imgDataList):
        '''Gets the data for ONE product, according to the informations from the images recorded in the parameter list.'''
        if(len(imgDataList) != 0):
            
            IDProduct = imgDataList[0]["IDProduct"]

            sumProbProb = 0     # DO NOT RENAME. THIS IS FINE.
            
            dictColorsMain = {}             # contient les couleurs de tous les produits
            listColorRedMain = []           # liste des valeurs rouge dans les produits (main color)
            listColorGreenMain = []         # liste des valeurs verte dans les produits
            listColorBlueMain = []          # pareil
            
            dictColorsSecondary = {}        # 
            listColorRedSecondary = []      # 
            listColorGreenSecondary = []    # 
            listColorBlueSecondary = []     # 
            
            # we build the final dictionnary with everything we want
            finalProductData = { 
                    'idProduct'     : IDProduct,
                    'lstImg'        : DFU.buildImgNamesList(imgDataList),
                    'probaShoe'     : DFU.calculateProbaShoe(imgDataList)
            }
            
            shoeProbProb = finalProductData['probaShoe']
            
            # if there is a shoe
            if shoeProbProb>0.5:
                finalProductData['style'] = DFU.determineStyle(imgDataList)
                finalProductData['colors'] = DFU.determineColors(imgDataList)
                    
            return finalProductData
            
            
            
           ###### OBSOLETE, TO REWRITE 
            for imgData in imgDataList:
                #COLORWAY MOYENNE -> à la majorité -> dico avec détection couleur et nombre
                if("Colorway" in imgData):
                    #increment DONE

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

            
            ## CONSTRUCTION OF THE FINAL DICT
            colorDict = {}
            if(mainColor != None):
                finalProductData["Colorway"]=[]
                finalProductData["Colorway"].append({"mainColor":{"name":mainColor,"rgb":RGBMain}})
            if(secondaryColor != None):
                if(secondaryColor != mainColor):
                    finalProductData["Colorway"].append({"secondaryColor":{"name":secondaryColor,"rgb":RGBSecondary}})
            
            
            


class DFU: 
    '''DataFusionUtility class.
    
    Assembles the final dictionnary that describes one standalone product.'''
    
    def buildImgNamesList(imgDataList):
        '''Returns the list of image names from the given data list.'''
        imgNamesList = []
        for imgData in imgDataList:
            imgNamesList.append( imgData["img"] )
        return imgNamesList
    
    def calculateProbaShoe(imgDataList):
        '''Calculates the average probability of there being a shoe, according to the given data list.'''
        sumProbProb = 0
        
        for imgData in imgDataList:
            sumProbProb += float(imgData["shoeProb"])
        
        probProb = sumProbProb/len(imgDataList)
        return np.round(probProb, 3)
        
    def determineStyle(imgDataList):
        return "NOT IMPLEMENTED YET - See utilities.DataFusion.DFU"
    
    def determineColors(imgDataList):
        colors = {
            'mainColor': DFU.determineOneColor('the main one', imgDataList)
        }
        
    
    def determineOneColor(which:str, imgDataList):
        '''The parameter can be "the main one" or "the secondary one".'''
        
        # defines if we are searching for the main or secondary color
        choosen = 'mainColor' if (which=='the main one') else 'secondaryColor'
        
        # this dict stores the names of the colors encountered, and the number of times we encountered them.
        colorCounters = {}
        
        rgbCodes = { # this stores the rgb codes for averaging later
            'r': [],
            'g': [],
            'b': []
        }
        
        # we count how many times each color appears in the imgs data
        for imgData in imgDataList:
            if("Colorway" in imgData):
                if choosen in imgData['ColorWay']:
                    # extract the color from the data
                    color     = imgData["Colorway"][choosen]
                    colorName = color["color"]
                    rgb       = color["rgb"]
                    
                    # we count how many times each color appears in the imgs data
                    DFU.incrementInDict(colorName, colorCounters)
                    
                    # we store the rgb values
                    rgbCodes['r'].append(rgb[0])
                    rgbCodes['g'].append(rgb[1])
                    rgbCodes['b'].append(rgb[2])
        
        
        
                
                
                
    def incrementInDict(key, dict):
        '''Adds +1 to the given key in the given dict. Initializes at 1 if the key doesn't exist.'''
        if key in dict:
            dict[key] += 1
        else:
            dict[key] = 1