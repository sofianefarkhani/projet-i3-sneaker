#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import json
from utilities.configUtilities.BBConfig import BBConfig
class Writer(json.JSONEncoder):
    '''The Writer writes JSON. 
    
    The Writer takes a Tag and image upon request from the BlackBox. It writes the tag into the appropriate json file.'''


    def prepareTempFiles():
        dir = BBConfig.getTempOutput()
        filesToRemove = os.listdir(dir)
        for f in filesToRemove:
            os.remove(dir+'/'+f)


    def convertToJson(data: dict):
        return json.dumps(data)
    
    def writeDataToTempFile(procName, data:dict):
        tempDir = BBConfig.getTempOutput()
        print(tempDir)
        outputFilePath = tempDir+"/"+ procName+'.json'
        
        with open(outputFilePath, 'a') as f:
            f.write("\n"+Writer.convertToJson(data))