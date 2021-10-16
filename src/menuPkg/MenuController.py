from Data.BasicColors import ColorEnum
from Data.Color import Color
from Data.Tag import Tag
from Data.Type import Type
from interface.Writer import Writer

class MenuController:
    
    
    def upIndex(vars):
        if 'tagIndex' in vars:
            vars['tagIndex'] += 1
        else: 
            vars['tagIndex'] = 0
 
    def setLowType(vars):
        vars['type'] = 'low'
        
    def setHighType(vars):
        vars['type'] = 'high'
        
    def chooseMainShoeColor(vars):
        boucleColorPrincipal = True
        while(boucleColorPrincipal):
            choiceColorPrincipal = str(input("Enter your color : "))
            if choiceColorPrincipal == "":
                print("You didn't enter any color...")
                continue
            else:
                choiceColorPrincipal = choiceColorPrincipal.upper()
                if choiceColorPrincipal == "NONE" : 
                    colorsFirst = None
                    boucleColorPrincipal = False
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
                        boucleColorPrincipal = False
                    else:
                        print("This choice doesn't exist...")
                        continue
                else:
                    print("Your color is already in our database")
                    colorsFirst = Color(str(choiceColorPrincipal))
                    boucleColorPrincipal = False
        vars['mainColor'] = colorsFirst

    def chooseSecondaryShoeColor(vars):
        boucleColorSecondaire = True
        while(boucleColorSecondaire):
            choiceColorsecond = str(input("Enter your color : "))
            if choiceColorsecond == "":
                print("You didn't enter any color...")
                continue
            else:
                choiceColorsecond = choiceColorsecond.upper()
                if choiceColorsecond == "NONE" : 
                    colorsSecond = None
                    boucleColorSecondaire = False
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
                        boucleColorSecondaire = False
                    else:
                        print("This choice doesn't exist...")
                        continue
                else:
                    print("Your color is already in our database")
                    colorsSecond = Color(str(choiceColorsecond))
                    boucleColorSecondaire = False
        vars['secondaryColor'] = colorsSecond            

    
    def registerTag(vars):
        newTag = Tag(vars['tagIndex'], Type.getType(vars['type']), vars['mainColor'], vars['secondaryColor'])
        print(newTag.toString())
        Writer.outputTagAsJson(newTag, "../out/testData.json")