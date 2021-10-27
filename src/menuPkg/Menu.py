



import jsonpickle
from Data.Tag import Tag
from menuPkg.MenuImageLoader import MenuImageLoader
from Data.BasicColors import ColorEnum
from enum import Enum
from interface.Writer import Writer
from Data.Color import Color
import yaml




class MenuContext:
    def __init__(self, path, setOfInstructions):
        self.path = path
        self.instructions = setOfInstructions
        self.closeMenu = False

class Choice:
    def __init__(self, choiceName, choiceIndex, linkedInstructions):
        self.choiceName = choiceName
        self.index = choiceIndex
        self.linkedInstructions = linkedInstructions
        
    def toString(self):
        return str(self.index)+': '+str(self.linkedInstructions['disp'])

class AnswerType:
    EXIT_REQUEST = 0
    CHOOSE = 1
    KEEP_GOING = 2

class Menu:
    ##### Constructor
    
    lastReturnedVars = None;
    
    def __init__(self, file='menuPkg/mainMenuChoices.yaml'):
        self.file = file
        self.vars = {
            'yamlFile' : self.file
        }
        with open(self.file) as f:
            allInstructions = yaml.load(f, Loader=yaml.FullLoader)
            self.executeInstructions(MenuContext([], allInstructions)) # launches the menu at its root
            print ('Exiting the menu app, its vars can be found in Menu.lastReturnedVars')
            Menu.lastReturnedVars = self.vars.copy()
    
    def choiceExists(choices, answer):
        for choice in choices:
            if answer == str(choice.index):
                return choice
        return None
    
    def nameOfChoice(choices, answer):
        for choice in choices:
            if choice.index == answer: return choice.name
            
    
    def consolePrint(self, message:str, position):
        indent = self.indent(position)
        print (indent+str(message).replace('\n', indent))
           
    def indent(self, position):
        m = "\n"
        for i in range(len(position)):
            m+='|    '
        return m
    
    
    # User interaction
    def ask(self, choices, context, canExit=True):
        # if choices is [], there is still the possibility to ask for the guy to exit
        while len(choices)!=0 or canExit:
            m = "" 
            for choice in choices:
                m += "\n"+choice.toString()
            
            exitIndex = len(choices)+1
            if canExit: m+="\n"+str(exitIndex) + ": Exit"
            
            self.consolePrint(m, context.path)
            answer = input(self.indent(context.path)+'Your choice >> ')
            
            if canExit and int(answer)==exitIndex: # he asked to go back
                    return (AnswerType.EXIT_REQUEST, None)
            
            elif choice := Menu.choiceExists(choices, answer): # if the choice 'c'+answer exists, then execute this part.
                return (AnswerType.CHOOSE, choice.choiceName)
            else: # ask again, since he has not understood
                self.consolePrint('This choice: "'+answer+'" does not exist', context.path)
                self.consolePrint('Please try giving your choice again:', context.path)
        
        
    
    #### Running the menu
    def executeInstructions(self, context:MenuContext):
        choices = []
        canExit = True
        
        for i in context.instructions:
            
            if context.closeMenu: break
                        
            if i == 'disp': continue # we don't care about disp, it is not an instruction to execute
            
            elif i == 'controllerModule':
                self.vars['controllerModule'] = context.instructions[i]
                
            elif i == 'controllerClass':
                self.vars['controllerClass'] = context.instructions[i]
            
            elif i[0] == 'p': # this is asking for a prompt
                self.consolePrint (str(context.instructions[i]), context.path)

            elif i[0] == 'c': # this is a new choice
                choices.append(Choice(i, len(choices)+1, context.instructions[i]))

            elif i[0] == 'a': # this is an action
                # First, check if it is a default action
                if context.instructions[i] == "_ASK_":
                    (answerType, answerData) = self.ask(choices, context, canExit)
                    
                    if answerType == AnswerType.EXIT_REQUEST:
                        break
                    elif answerType == AnswerType.CHOOSE:
                        newPath = context.path.copy()
                        newPath.append(answerData)
                        newContext = MenuContext(newPath, context.instructions[answerData])
                        self.executeInstructions(newContext)
                    
                    elif answerType != AnswerType.KEEP_GOING: 
                        print('this line should never appear. Ask esteban for help after he stops crying.')
                    
                    choices = []
                    canExit = True
                    
                elif context.instructions[i] == "_LOOP_":
                    if not context.closeMenu: # if we have not asked to exit the menu yet, we loop it
                        self.executeInstructions(context)
                
                elif context.instructions[i] == "_VARS_":
                    self.consolePrint(self.vars, context.path)
                
                else: # we want to launch a method from the controller 
                    mod = __import__(self.vars['controllerModule'], fromlist=[self.vars['controllerClass']])
                    klass = getattr(mod, self.vars['controllerClass'])
                    methodName = context.instructions[i]
                    method = getattr(klass, methodName)
                    method(self.vars)
                        
                        
            elif i=='set' and context.instructions[i] =="_NOEXIT_":
                canExit=False
            
                
                
   
   
   
   
   
   
   
    
        
    
    
    

    