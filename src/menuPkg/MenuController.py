from Data.BasicColors import ColorEnum
from Data.Color import Color
from Data.Tag import Tag
from Data.Type import Type
from interface.Writer import Writer
import jsonpickle
import cv2
from interface.JsonReader import JsonReader
from Data.Image import Image
from os.path import isfile, join

class MenuController:
    
    def upIndex(vars):
        file_object = open("../out/testData.json", 'r')
        lines = file_object.readlines()
        size = len(lines)
        if(size > 0):
            lastLine = jsonpickle.decode(lines[-1])
            value = (lastLine.databaseID+1)
            vars['tagIndex'] = value
            file_object.close()
        else:
            vars['tagIndex'] = 0
            file_object.close()
        
 
    def setLowType(vars):
        vars['type'] = Type.LOW
        
    def setHighType(vars):
        vars['type'] = Type.HIGH
        
    def chooseMainShoeColor(vars):
        #boucleColorPrincipal = True
        while(True):
            choiceColorPrincipal = str(input("Enter your color : "))
            if choiceColorPrincipal == "":
                print("You didn't enter any color...")
                continue
            else:
                choiceColorPrincipal = choiceColorPrincipal.upper()
                if choiceColorPrincipal == "NONE" : 
                    colorsFirst = None
                    #boucleColorPrincipal = False
                    return
                elif not ColorEnum.colorExist(choiceColorPrincipal):
                    print("Your color isn't in our database")
                    print("If you change to change the color - Press 1")
                    print("If you want to add the color - Press 2")
                    choiceAddDatabase = int(input("Enter your choice : "))
                    if choiceAddDatabase == 1 :
                        continue
                    elif choiceAddDatabase == 2:
                        colorR = int(input("Enter your value between 0 and 255 for Red : "))
                        colorG = int(input("Enter your value between 0 and 255 for Green : "))
                        colorB = int(input("Enter your value between 0 and 255 for Blue : "))

                        if colorR > 255 : colorR=255
                        elif colorR < 0 : colorR=0
                        if colorG > 255 : colorG=255
                        elif colorG < 0 : colorG=0
                        if colorB > 255 : colorB=255
                        elif colorB < 0 : colorB=0

                        colorsFirst = [colorR, colorG, colorB]
                        #boucleColorPrincipal = False
                        vars['mainColor'] = colorsFirst
                        return colorsFirst
                    else:
                        print("This choice doesn't exist...")
                        continue
                else:
                    print("Your color is already in our database")
                    colorsFirst = Color(str(choiceColorPrincipal))
                    vars['mainColor'] = colorsFirst
                    #boucleColorPrincipal = False
                    return colorsFirst

    def chooseSecondaryShoeColor(vars):
        #boucleColorSecondaire = True
        while(True):
            choiceColorsecond = str(input("Enter your color : "))
            if choiceColorsecond == "":
                print("You didn't enter any color...")
                continue
            else:
                choiceColorsecond = choiceColorsecond.upper()
                if choiceColorsecond == "NONE" : 
                    colorsSecond = None
                    #boucleColorSecondaire = False
                    return
                elif not ColorEnum.colorExist(choiceColorsecond):
                    print("Your color isn't in our database")
                    print("If you change to change the color - Press 1")
                    print("If you want to add the color - Press 2")
                    choiceAddDatabase = int(input("Enter your choice : "))
                    if choiceAddDatabase == 1 :
                        continue
                    elif choiceAddDatabase == 2:
                        colorR = int(input("Enter your value between 0 and 255 for Red : "))
                        colorG = int(input("Enter your value between 0 and 255 for Green : "))
                        colorB = int(input("Enter your value between 0 and 255 for Blue : "))

                        if colorR > 255 : colorR=255
                        elif colorR < 0 : colorR=0
                        if colorG > 255 : colorG=255
                        elif colorG < 0 : colorG=0
                        if colorB > 255 : colorB=255
                        elif colorB < 0 : colorB=0

                        colorsSecond = [colorR, colorG, colorB]
                        #boucleColorSecondaire = False
                        vars['secondaryColor'] = colorsSecond
                        return colorsSecond
                    else:
                        print("This choice doesn't exist...")
                        continue
                else:
                    print("Your color is already in our database")
                    colorsSecond = Color(str(choiceColorsecond))
                    #boucleColorSecondaire = False
                    vars['secondaryColor'] = colorsSecond  
                    return colorsSecond          

    
    def registerTag(vars):
        newTag = Tag(vars['tagIndex'], vars['type'], vars['mainColor'], vars['secondaryColor'])
        print(newTag.toString())
        Writer.outputTagAsJson(newTag, "../out/testData.json")
    
    def enterIdOfImage(vars):
        idImage = int(input("Enter the ID : "))
        tagList = JsonReader.readOutputFile("../out/testData.json")
        for tag in tagList:
            if(tag.databaseID == idImage):
                image = Image(cv2.imread(join("../img/train/trainingTestImages/" + str(idImage) +".png")), ("../img/train/trainingTestImages/" + str(idImage) +".png"), idImage, str(idImage))
                cv2.imshow("Image",image.img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                print(tag.type, " " ,tag.mainColor.toString(), " " ,tag.secondaryColor.toString())
                return image    
        print("Your id isn't in the database")

    def enterIdOfImageModify(vars) :
        idImageModify = int(input("Enter the ID : "))
        everything = ""
        file_object = open("../out/testData.json", 'r')
        lines = file_object.readlines()
        size = len(lines)
        modify = True
        if(idImageModify > size):
            print("Your id isn't in our databse")
            modify = False
        if(modify):
            for line in lines :
                thisLine = jsonpickle.decode(line)
                if(thisLine.databaseID == idImageModify):
                    print("Please enter the news data of this shoes \n")
                    print("What is the type of your shoes ?\n")
                    print("1 - Low Type\n 2 - High Type\n 3 - You don't know")
                    type = int(input("Enter your type : "))
                    if type == 1:
                        theType = Type.LOW
                    elif type == 2:
                        theType = Type.HIGH
                    else:
                        theType = None
                    
                    print("\nWhat is the principal color of your shoes ?\n")
                    firstColor = MenuController.chooseMainShoeColor(vars)

                    print("\nWhat is the secondary color of your shoes ?\n")
                    secondColor = MenuController.chooseSecondaryShoeColor(vars)

                    newTag = Tag(idImageModify,theType, firstColor, secondColor)
                    newTagEncode = jsonpickle.encode(newTag)
                    everything += newTagEncode + "\n"

                else:
                    thisLineEncode = jsonpickle.encode(thisLine)
                    everything += thisLineEncode + "\n"
            file_object.close

            file_object = open("../out/testData.json", 'w')
            file_object.truncate()
            for line in everything:
                file_object.write(line)