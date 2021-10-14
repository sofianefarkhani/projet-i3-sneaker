



import jsonpickle
from Data.Tag import Tag
from menuPkg.MenuImageLoader import MenuImageLoader
from Data.BasicColors import ColorEnum
from enum import Enum
from interface.Writer import Writer
from Data.Color import Color
import yaml


class Menu: 
    
    ##### Constructor
    
    def __init__(self, file='menuPkg/mainMenuChoices.yaml', controllerPath='menuPkg/MenuController.py'):
        self.file = file
        self.closeMenu = False
        self.choices = []
        self.controller = controllerPath
    
    
    
    ###### PATH UTILITIES
    
    def goBack(self, position):
        self.closeMenu = True
        if (position == []):
            self.closeMenu = True
        else:
            position = position[:len(position)-1] # remove the last index
        self.load(position)
        
        
    def goInChoice(self, choiceName, position, instructions):
        if (choiceName) in instructions:
            position.append(choiceName)
            self.load(position)
            self.executeInstructions(position)
        else:
            self.consolePrint('There is no such choice: '+choiceName)
        
            
    
    def load(self, position):
        
        
        '''Load the instructions in: position'''
        with open(self.file) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            
            for instruct in position:
                config = config[instruct]
            return config

    
    #### Running the menu
    def executeInstructions(self, position=[]):
        if position is None: position = self.position
        
        setOfInstructions = self.load(position)
        
        indexOfFirstChoice=1
        choices = []
        canExit = True
        
        for i in setOfInstructions:
            
            if self.closeMenu:
                self.closeMenu = False
                break
                        
            if i == 'disp': continue
            
            elif i[0] == 'p': # this is asking for a prompt
                self.consolePrint (str(setOfInstructions[i]), position)

            elif i[0] == 'c': # this is a new choice
                if choices==[]: indexOfFirstChoice = int(i[1:])
                choices.append(setOfInstructions[i])

            elif i[0] == 'a': # this is an action
                # First, check if it is a default action
                if setOfInstructions[i] == "_ASK_":
                    self.ask(choices, indexOfFirstChoice, position, setOfInstructions, canExit)
                    choices = []
                    position = position[:len(position)-1]
                    
                if setOfInstructions[i] == "_LOOP_":
                    print ('LOOOOOOP')
                    if not self.closeMenu:
                        self.load(position)
                        self.executeInstructions(position)
                    else:
                        self.closeMenu=False
            elif i=='set' and setOfInstructions[i]=="_NOEXIT_":
                canExit=False
                
                
   
   
   
   
   
   
   
    # User interaction
    
    def ask(self, choices, id1, position, instructions, canExit=True):
        if choices==[]:
            self.consolePrint('The menu asks me to ask you between no choice, on path: '+str(position), position)
            self.goInChoice('c1', position, instructions)
            return 
        
        m = "" 
        i = 0
        for choice in choices:
            m += "\n"+str(i+id1) + ": "+str(choice['disp'])
            i+=1
        exitId = i+id1
        if canExit: m+="\n"+str(exitId) + ": Exit"
        
        self.consolePrint(m, position)
        answer = input(self.indent(position)+'Your choice >> ')
        
        if int(answer)==exitId and canExit: # he asked to go back
            self.goBack(position)
        elif ('c'+answer) in instructions: # if the choice 'c'+answer exists, then execute this part.
            self.goInChoice('c'+answer, position, instructions)
        else: # ask again, since he has not understood
            self.consolePrint('This choice: "'+answer+'" does not exist', position)
            self.ask(choices, id1, position, instructions, canExit)
        
        
        
    
    def consolePrint(self, message:str, position):
        indent = self.indent(position)
        print (indent+message.replace('\n', indent))
           
    def indent(self, position):
        m = "\n"
        for i in range(len(position)):
            m+='|    '
        return m
    