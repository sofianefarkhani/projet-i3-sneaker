#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
class Writer(json.JSONEncoder):

    def json_convert(self, obj): 
        if isinstance(obj, Tags):
            return [obj.id, obj.mainColor, obj.secondColor, obj.type]
        raise ValueError("Writer take only Tags object, your object is not Tags")
        return json.JSONEncoder.json_convert(self, obj)
        
