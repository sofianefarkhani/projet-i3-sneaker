import os
import re
import time
import cv2
import matplotlib.pyplot as plt

# file = open("/home/vedoc/Bureau/lst_nom.txt", "r")
# lst_all_files = file.readlines()
# file.close()

# file = open("/home/vedoc/Bureau/lst_nom_chaussure_from_discord.txt", "r")
# lst_all_chaussure = file.readlines()
# file.close()

# lst_nom_chaussure = [] 
# for i in range(len(lst_all_chaussure)):
#     lst_all_chaussure[i] = lst_all_chaussure[i].replace("\n", "")
# for i in range(len(lst_all_files)):
#     lst_all_files[i] = lst_all_files[i].replace("\n", "")


# percent = 0.00
# for productReference in lst_all_chaussure:
#     if "-" in productReference and productReference.startswith(productReference.replace("-", "_")):
#         r = re.compile(r"("+productReference+"|"+productReference.replace("-", "_")+").*")
#     else:
#         r = re.compile(r"("+productReference+").*")
#     newlist = list(filter(r.match, lst_all_files))
#     # if len(newlist) != 0:
#     #     print(productReference)
#     lst_nom_chaussure.append(newlist)
#     percentUpdate = lst_all_chaussure.index(productReference)/len(lst_all_chaussure)
#     if percentUpdate > percent:
#         time.sleep(1.0)
#         percent += 0.03
#         print (percent)

# with open("output.txt", "w") as txt_file:
#     for line in lst_nom_chaussure:
#         txt_file.write(" ".join(line) + "\n")


file = open("../output.txt", "r")
lst = file.readlines()
file.close()

print()

for img_path in lst:
    path = '/run/user/1000/gvfs/sftp:host=access886997315.webspace-data.io,user=u106097170-projetia/resources/' + img_path
    print(path)
    img = cv2.imread(path)    
    print(path)
    if (img is None):
        print("None")
        exit()
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()