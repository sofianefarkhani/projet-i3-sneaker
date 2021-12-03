import hashlib

lst_name = []
lst_hash = []
lst_name_to_delete = []
lst_temp_index_to_delete = []

f = open("../in/trainData.json", "r")
for line in f:
    name = line.split("imageName\"")[1].split("\"")[1].split("\"")[0]
    lst_name.append(name)
    
f.close()
path = "D:/Images/resources/"

# lst_name = lst_name[:40]


for name in lst_name:
    with open(path+name, "rb") as f:
        bytes = f.read()
        lst_hash.append(hashlib.sha256(bytes).hexdigest())
        f.close()


print(len(lst_name))
print(len(lst_hash))

# for i in range(len(lst_name)):
#     print(str(i)+ "  "+ lst_name[i] + "  ->  " + lst_hash[i])

indexDone = -1
while indexDone < len(lst_name)-1:
    indexDone+=1
    hashToCheck = lst_hash[indexDone]
    for i in range(indexDone+1, len(lst_hash)):
        if lst_hash[i] == hashToCheck:
            lst_temp_index_to_delete.append(i)

    lst_temp_index_to_delete.reverse()
    for i in lst_temp_index_to_delete:
        lst_name_to_delete.append(lst_name[i])
        del lst_name[i]
        del lst_hash[i]
    lst_temp_index_to_delete.clear()

lst_name_to_delete.sort()

print("Après:")
# for name in lst_name_to_delete:
#     print("del: " + name)
print(len(lst_name))
print(len(lst_hash))

# for i in range(len(lst_name)):
#     print(str(i)+ "  "+ lst_name[i] + "  ->  " + lst_hash[i])


newFileString = ""

f = open("../in/trainData.json", "r")
for line in f:
    name = line.split("imageName\"")[1].split("\"")[1].split("\"")[0]
    if(not name in lst_name_to_delete):
        newFileString+=line
    
f.close()
# print(newFileString)

f = open("../in/trainDataV2.json", "w")
f.write(newFileString)
f.close()