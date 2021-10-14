#!/usr/bin/python3
# -*- coding: utf-8 -*-
import jsonpickle
from Data.Tag import Tag


continued = True
while(continued):

    print("\nOption 1 - Taper 1") 

    """
    Créer du data - il donne une image et on doit mettre les données (remplir à la main les données d'une image
    quand il demande la couleur et le type -> puisse mettre ? -> rappel des données dispo
    confirmation des données à la fin (demande)
    dans un fichier json -> vérifie que l'image n'est pas déjà enregistré si enregistré demande quelles données gardées
    """

    print("Option 2 - Taper 2") #Modifier les data d'une image
    print("Avoir les informations d'une image - Taper 3") #Montrer des informations des images -> lis le json, cherche les data de cette image
    print("Quitter le menu - Taper 4")

    choice = int(input("Que voulez-vous faire ? \n"))
        
    if(choice == 1):
        print("vous avez choisi l'option 1")
    elif(choice == 2):
        print("vous avez choisi l'option 2")

    elif(choice == 3):
        #Pour le moment il n'y a pas de nom

        boucleId = True
        boucleName = False
        hasId = False
        hasName = False

        while(boucleId):
            print("Si vous avez l'id de l'image - Taper 1")
            print("Sinon taper 2")
            choixId = int(input("choix : "))
            if(choixId == 1):
                print("Vous connaissez l'id de l'image")
                idImage = int(input("Entrez l'id de l'image : "))
                hasId = True
                boucleId = False
            elif(choixId == 2):
                print("Vous ne connaissez pas l'id de l'image\n")
                boucleName = True
                boucleId = False
            else:
                print("Ce choix n'existe pas\n")

        while(boucleName):
            print("Si vous avez le nom de l'image - Taper 1")
            print("Sinon taper 2")
            choixName = int(input("choix : "))
            if(choixName == 1):
                print("Vous connaissez le nom de l'image")
                nameImage = str(input("Entrez le nom de l'image : "))
                hasName = True
                boucleName = False
            elif(choixName == 2):
                print("Vous ne connaissez pas le nom de l'image\n")
                boucleName = False
            else:
                print("Ce choix n'existe pas\n")
        
        if(hasId):
            file_object = open("../out/testData.json", 'r')
            lines = file_object.readlines()
            tagList = []
            for line in lines:
                print(line)
                object = jsonpickle.decode(line)
                if object.databaseID == idImage:
                    print("Test valide")
                else:
                    print("L'id que vous avez donné n'existe pas...")
            
        elif(hasName):
            print("on a le nom\n")
            continue
        else:
            print("Vous n'avez aucun informations pour avoir accès aux données...\n")
            continue

    elif(choice == 4):
        continued = False
    else:
        print("Votre choix n'existe pas, veuillez rechoisir votre choix")
    