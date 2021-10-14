#!/usr/bin/python3
# -*- coding: utf-8 -*-
import jsonpickle
from Data.Tag import Tag
from menuPkg.MenuImageLoader import MenuImageLoader
from Data.BasicColors import ColorEnum
from enum import Enum


continued = True
while(continued):

    print("\nAdd some datas - Press 1") 
    print("Modify some datas - Press 2")
    print("Get some informations about an image - Press 3")
    print("Exit the menu - Press 4")

    choice = int(input("What do you want to do ? \n"))
        
    if(choice == 1):
        #Get the new ID
        file_object = open("../out/testData.json", 'r')
        lines = file_object.readlines()
        size = len(lines)
        lastLine = jsonpickle.decode(lines[-1])
        indexLastLine = lastLine.databaseID

        #Get the type
        boucleType = True
        while(boucleType):
            print("If your shoes are low - Press 0")
            print("If your shoes are high - Press 1")
            print("If you don't know - Press 2")
            choiceType = int(input("Enter the type of your shoes : "))
            if(choiceType == 0 or choiceType == 1):
                boucleType = False
            elif(choiceType == 2):
                choiceType = None
                boucleType = False
            else:
                print("This option doesn't exist... Choose something else...\n")

        #Récup la couleur principal -> ? donne les couleurs existantes -> si nom pas dans base proposée de changer de couleur, et de créer le rgb
        boucleColorPrincipal = True
        while(boucleColorPrincipal):
            print("What is the principal color in your shoes ?")
            print("If you don't want to write it, write none")
            choiceColorPrincipal = str(input("Enter your color : "))
            if choiceColorPrincipal == "":
                print("You didn't enter any color...")
                continue
            else:
                choiceColorPrincipal.upper
                if choiceColorPrincipal == "NONE" : 
                    colorsFirst = None
                    boucleColorPrincipal = False
                elif choiceColorPrincipal not in ColorEnum:
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

        #Récup la couleur secondaire
        boucleColorSecondaire = True
        while(boucleColorSecondaire):
            print("What is the secondary color in your shoes ?")
            print("If you don't want to write it, write none")
            choiceColorsecond = str(input("Enter your color : "))
            if choiceColorsecond == "":
                print("You didn't enter any color...")
                continue
            else:
                choiceColorsecond.upper
                if choiceColorsecond == "NONE" : 
                    colorsSecond = None
                    boucleColorSecondaire = False
                elif choiceColorsecond not in ColorEnum:
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

    elif(choice == 2):
        print("You chose option 2")

    elif(choice == 3):
        boucleId = True
        boucleName = False
        hasId = False
        hasName = False

        while(boucleId):
            print("If you have the ID of the image - Press 1")
            print("Else press 2")
            choixId = int(input("choice : "))
            if(choixId == 1):
                print("Vous know the ID of the image")
                idImage = int(input("Enter the ID : "))
                hasId = True
                boucleId = False
            elif(choixId == 2):
                print("You don't know the ID\n")
                boucleName = True
                boucleId = False
            else:
                print("This choice doesn't exist... Choose something else\n")

        while(boucleName):
            print("If you have the name of the image - Press 1")
            print("Else press 2")
            choixName = int(input("choice : "))
            if(choixName == 1):
                print("You know the name of the image")
                nameImage = str(input("Enter the name : "))
                hasName = True
                boucleName = False
            elif(choixName == 2):
                print("You don't know the name\n")
                boucleName = False
            else:
                print("This choice doesn't exist... Choose something else\n")
        
        if(hasId):
            theTag = MenuImageLoader.loadImageById(idImage)
            print(theTag.toString())
            continue    
        elif(hasName):
            print("We have the name\n")
            continue
        else:
            print("You don't have any information to access some datas...\n")
            continue

    elif(choice == 4):
        continued = False
    else:
        print("Your choice doesn't exist... Choose something else...\n")
    