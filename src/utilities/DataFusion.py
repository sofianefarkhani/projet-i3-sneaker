import os
import json
import shutil
import numpy                                as np
from statistics                             import median

from utilities.config.getters.OutputConfig import OutputConfig as OC
from utilities.config.getters.LoaderConfig import LoaderConfig as LC

class Util:
    '''A simple utility class that does simple, menial tasks.'''
    def removeOldData():
        '''Destroys the data file from the previous session.'''
        path = OC.getData()
        if(os.path.exists(path)): 
            os.remove(path)
    
    def writeToFile(dataToAdd):
        if dataToAdd is None: return
        outPutFile = OC.getData()
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
        pathFile =  OC.getTempData()
        shutil.rmtree(pathFile,ignore_errors=True)
        os.mkdir(pathFile)
    
    def registerProductAsDone(product:str):
        '''Registers the product in a file. Products found in this file will not be dealt with again.'''
        if product is None: return
        with open(LC.getDoneFile(), 'a') as f:
            f.write(','+product)


class DataFusion :

    def fusionJson():
        '''Searches through the temp json files created by each blackbox, and gathers product by product the results for each related image.
        Then adds the fusion of these results to the final json.'''
        
        jsonObjectList = []                 # the list of objects (one by img) in all blackbox-temp-jsons
        pathTempDir = OC.getTempData()
        
        # prepare file for final data
        Util.removeOldData()
        
        # prepare data from the temp json files (one per blackbox ran)
        for fileName in os.listdir(pathTempDir):
            Util.getObjectsFromFile(pathTempDir+"/"+fileName,jsonObjectList)   
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
            
            # we build the final dictionnary with everything we want
            finalProductData = { 
                    'idProduct'     : imgDataList[0]["IDProduct"],
                    'lstImg'        : DFU.buildImgNamesList(imgDataList),
                    'probaShoe'     : DFU.calculateProbaShoe(imgDataList)
            }
            
            # if a shoe was detected, add the missing data.
            if finalProductData['probaShoe'] > 0.5:
                finalProductData['style'] = DFU.determineStyle(imgDataList)
                finalProductData['colors'] = DFU.determineColors(imgDataList)
                    
            return finalProductData

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
            'mainColor': DFU.determineOneColor('the main one', imgDataList),
            'secondaryColor': DFU.determineOneColor('the secondary one', imgDataList)
        }
        if colors['secondaryColor'] is None:
            colors.pop('secondaryColor')
        return colors
        
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
                if choosen in imgData['Colorway']:
                    # extract the color from the data
                    dataColor     = imgData["Colorway"][choosen]
                    colorName = dataColor["color"]
                    rgb       = dataColor["rgb"]
                    
                    # we count how many times each color appears in the imgs data
                    DFU.incrementInDict(colorName, colorCounters)
                    
                    # we store the rgb values
                    rgbCodes['r'].append(rgb[0])
                    rgbCodes['g'].append(rgb[1])
                    rgbCodes['b'].append(rgb[2])
        
        # if ColorCounters is empty, then we have found nothing. We can return none.
        if len(colorCounters.keys())==0:
            return None
        
        # take the most represented color
        finalColor = max(colorCounters, key=colorCounters.get)
        
        # get the medians for rgb values
        rgbCodes['r'].sort()
        rgbCodes['g'].sort()
        rgbCodes['b'].sort()
        finalRGB = [
            median(rgbCodes['r']),
            median(rgbCodes['g']),
            median(rgbCodes['b'])
        ]
        
        # return the product color data
        return {
            'name' : finalColor,
            'rgb'  : finalRGB
        }
                
    def incrementInDict(key, dict):
        '''Adds +1 to the given key in the given dict. Initializes at 1 if the key doesn't exist.'''
        if key in dict:
            dict[key] += 1
        else:
            dict[key] = 1