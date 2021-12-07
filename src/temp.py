
lst_name = []
f = open("../in/trainData.json", "r")
for line in f:
    name = line.split("imageName\"")[1].split("\"")[1].split("\"")[0]
    lst_name.append(name)

lst_shoes = []
f = open("C:/Users/moonc/Desktop/shoesNoDuplicate.txt", "r")
for line in f:
    lst_shoes.append(line.replace("\n", ""))

newFileString = ""
f = open("../in/trainData.json", "r")
for line in f:
    name = line.split("imageName\"")[1].split("\"")[1].split("\"")[0]
    if(not name in lst_shoes):
        newFileString+=line
    else:
        newFileString+='{"py/object": "Data.TrainDataElement.TrainDataElement", "imageName": "'+name+'", "isThereAShoe": true, "shoeType": {"py/reduce": [{"py/type": "Data.Type.Type"}, {"py/tuple": [0]}]}}\n'
        del lst_shoes[lst_shoes.index(name)]
for name in lst_shoes:
    newFileString = '{"py/object": "Data.TrainDataElement.TrainDataElement", "imageName": "'+name+'", "isThereAShoe": true, "shoeType": {"py/reduce": [{"py/type": "Data.Type.Type"}, {"py/tuple": [0]}]}}\n' + newFileString
    
f.close()
# print(newFileString)

f = open("../in/trainDataV3.json", "w")
f.write(newFileString)
f.close()

