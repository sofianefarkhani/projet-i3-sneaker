#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import json
from utilities.configUtilities.BBConfig import BBConfig
from Data.TrainDataElement import TrainDataElement
class Writer(json.JSONEncoder):
    '''The Writer writes JSON. 
    
    The Writer takes a Tag and image upon request from the BlackBox. It writes the tag into the appropriate json file.'''


    def prepareTempFiles():
        dir = BBConfig.getTempOutput()
        if dir[-1]=='/' or dir[-1]=='\\':
            dir = dir[:-1]

        if not os.path.exists(dir):
            os.mkdir(dir,mode=0o777)
        
            
        filesToRemove = os.listdir(dir)
        for f in filesToRemove:
            os.remove(dir+'/'+f)


    def convertToJson(data: dict):
        return json.dumps(data)
    
    def writeDataToTempFile(procName, data:dict):
        tempDir = BBConfig.getTempOutput()
        if tempDir[-1]=='/' or tempDir[-1]=='\\':
            tempDir = tempDir[:-1]
        outputFilePath = tempDir+"/"+ procName+'.json'
        
        with open(outputFilePath, 'a') as f:
            f.write("\n"+Writer.convertToJson(data))
