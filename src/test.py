#A file to test anything you need in the moment.

from Data.Color import Color
from Data.Tag import Tag
from Data.Type import Type
import json
from json import JSONEncoder
import jsonpickle
from interface.Writer import Writer

#### Testing the creation of colors
#Color.testColorCreation()




##### AND HERE WE MAKE JSON 
c = Color(rgb = [13, 0, 255])
c2 = Color(rgb = [0, 2, 0])
t = Tag(0)
t.setType(Type.HIGH)
t.setMainColor(c)
t.setSecondaryColor(c2)

# data = jsonpickle.encode(t)
# print(data)

# t2 = jsonpickle.decode(data)
# print(t2.__class__)
# print(t2.mainColor.name)
# print(t2.mainColor.rgb)

# print(t2.type)


# file_object = open('../out/data.json', 'a')
# file_object.write("\n"+data)

Writer.outputTagAsJson(t)