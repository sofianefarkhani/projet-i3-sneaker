#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
from Data.Tag import Tag
import jsonpickle
from interface.ConfigLoader import ConfigLoader
class Writer(json.JSONEncoder):
    '''The Writer writes JSON. 
    
    The Writer takes a Tag and image upon request from the BlackBox. It writes the tag into the appropriate json file.'''

    # def json_convert(self, obj): 
    #     if isinstance(obj, Tags):
    #         return [obj.id, obj.mainColor, obj.secondColor, obj.type]
    #     raise ValueError("Writer take only Tags object, your object is not Tags")
    #     return json.JSONEncoder.json_convert(self, obj)
        
    def outputTagAsJson(tag:Tag, outputFilePath:str=ConfigLoader.getVariable('output', 'data')):
        '''Writes the given tag under the Json format in the output file: ../out/data.json .
        
        Checks if the tag is complete first. 
        If it is, the json string of the given tag is appended to the file in a new line.
        
        This function may seem simple, but it was very painful to make. I had lots of research to do before getting smthg that actually works.
        
        With love, 
        
        Esteban'''
        if not tag.isComplete(): return
        data = jsonpickle.encode(tag)
        file_object = open(outputFilePath, 'a')
        file_object.write("\n"+data)