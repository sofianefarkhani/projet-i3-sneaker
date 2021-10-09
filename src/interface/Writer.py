#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
from Tag import Tag


class Writer(json.JSONEncoder):
    '''The Writer writes JSON. 
    
    The Writer takes a Tag and image upon request from the BlackBox. It writes the tag into the appropriate json file.'''

    def json_convert(self, obj): 
        if isinstance(obj, Tags):
            return [obj.id, obj.mainColor, obj.secondColor, obj.type]
        raise ValueError("Writer take only Tags object, your object is not Tags")
        return json.JSONEncoder.json_convert(self, obj)
        

