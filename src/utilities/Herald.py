from colorama import Fore, Back, Style
'''Quick note on colorama: 
Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
Style: DIM, NORMAL, BRIGHT, RESET_ALL
'''

from utilities.Beaver                           import Beaver
from utilities.configUtilities.ConfigLoader     import ConfigLoader
from utilities.configUtilities.ProcConfig       import ProcConfig
from processes.Task             import *
from processes.LoaderMessage    import *
from processes.Enums            import *
import queue
from pprint import pprint



class Herald:
    '''A utility class that processes use to transmit/print/log messages.
    
    This class is basically a fancy way to send signals between processes, and log them.
    Its nothing complicated, just used to hide stuff where the rest of the code is more important. 
    It will all by itself queue the messages, and print the infos / log them.'''
    
   
    
    
    # PRINTING / LOGGING
    def printError(message):
        '''Prints a string in the terminal, in bright red.'''
        print (Style.BRIGHT + Fore.RED + message)
        print(Style.RESET_ALL)
        Beaver.log(message)
    
    def printStart(procName):
        '''Announces the start of a process in the terminal.'''
        if ConfigLoader.getVariable('runConfig', 'talkative', 'processes'): 
            print (Fore.CYAN+'%s: Start of service' % procName+Style.RESET_ALL)
        if ConfigLoader.getVariable('runConfig', 'logs', 'processes'): 
            Beaver.log('%s: Start of service' % procName)
            
    def printTermination(procName):
        '''Announces the end of a process in the terminal.'''
        if ConfigLoader.getVariable('runConfig', 'talkative', 'processes'): 
            print (Fore.CYAN+'%s: End of service' % procName+Style.RESET_ALL)
        if ConfigLoader.getVariable('runConfig', 'logs', 'processes'): 
            Beaver.log('%s: End of service' % procName)
    
    # LOADER SPECIFIC MESSAGES
    def printLoading(number):
        '''Announces in the terminal that the Loader will load more images.'''
        if ProcConfig.loaderShouldTalk() : 
            print(Fore.BLUE+'Loading '+str(number)+' more images'+Style.RESET_ALL)
        if ConfigLoader.getVariable('runConfig', 'logs', 'loader')==True:
            Beaver.log('Loading '+str(number)+' more images')
    
    def signalLoad(imgName):
        '''Announces in the terminal that an image was loaded successfully.'''
        if ProcConfig.loaderShouldTalk() : 
            print(Fore.BLUE+'    - Loaded '+ imgName+Style.RESET_ALL)
        if ConfigLoader.getVariable('runConfig', 'logs', 'loader')==True:
            Beaver.log('    - Loaded '+ imgName)    
            
            
    def printNoMoreImages():
        '''Announces in the terminal that the Loader reached the end of the database.'''
        if ProcConfig.loaderShouldTalk() : 
            print(Fore.BLUE+'No more images in database to load'+Style.RESET_ALL)
        if ConfigLoader.getVariable('runConfig', 'logs', 'loader')==True:
            Beaver.log('No more images in database to load') 
    
    def printForLoader(msg):
        if ProcConfig.loaderShouldTalk() : 
            print(msg)
        if ConfigLoader.getVariable('runConfig', 'logs', 'loader')==True:
            Beaver.log(msg) 

    # BLACKBOX SPECIFIC MESSAGES
    def printWrittenData(procName):
        if ProcConfig.iaShouldTalk(): 
            print('%s: New data written in the test output file.' % (procName))
        if ConfigLoader.getVariable('runConfig', 'logs', 'ias')==True:
            Beaver.log('%s: New data written in the test output file.' % (procName)) 
            
    def printResults(results:dict, indent:int=1, returned = False):
        msg = "{\n"
        for key in results:
            msg += Herald.getPrintElement(key, results[key], indent)+',\n'
        
        msg = "".join(msg.rsplit(',', 1))
        
        if returned == False:
            print(Fore.YELLOW+Style.BRIGHT+msg+"}"+Style.RESET_ALL)
        else:
            indentStr = ''
            for i in range(indent-1): indentStr += '    '
            return msg+indentStr+"}"
        
    
    def getPrintElement(key:str, element, indent:int):
        indentStr = ''
        for i in range(indent): indentStr += '    '
        msg = indentStr+key+": "
        
        if type(element)==dict: 
            msg += Herald.printResults(element, indent+1, True)
        elif type(element)==list:
            msg+= '[\n'
            for e in element:
                msg += indentStr+'    '+str(e)+',\n'
            msg+= indentStr+']'
            msg = "".join(msg.rsplit(',', 1))
        else: msg+=element
        return msg
        
        
    # RECIEVING MESSAGES
    def getMessageFrom(procName, queue):
        '''Returns the next available message in the given queue, and prints/logs it if necessary.'''
        message = queue.get()
        if ProcConfig.messagesShouldBeSpoken(): 
            print(Style.BRIGHT+Fore.MAGENTA+procName+Style.NORMAL+': Recieved message: %s' % str(message.type))
        if ConfigLoader.getVariable('runConfig', 'logs', 'messages'):
            Beaver.log('%s: Recieved message: %s' % (procName, str(message.type))) 
        return message
    
    # QUEUING MESSAGES  
    def queueMessageIn(procName, queue, msg):
        '''Places the given message in the given queue, and prints/logs the action if necessary.'''
        queue.put(msg)
        if ProcConfig.messagesShouldBeSpoken(): 
            print(Style.BRIGHT+Fore.MAGENTA+procName+Style.NORMAL+': Sent message: %s' % str(msg.type))
        if ConfigLoader.getVariable('runConfig', 'logs', 'messages'):
            Beaver.log('%s: Sent message: %s' % (procName, str(msg.type))) 
        
    # IA DETAILS
    def printShoeExtractor(procName):
        if ProcConfig.iaShouldTalkInDetail(): print("%s: Extracting shoe from the given image" % procName)
        if ConfigLoader.getVariable('runConfig', 'logs', 'ias-detailed'):
            Beaver.log("%s: Extracting shoe from the given image" % procName) 
        
    def printPreprocessForShoeExtraction(procName):
        if ProcConfig.iaShouldTalkInDetail(): print("%s: Preprocessing the image before detection and extraction of the shoe"% procName)
        if ConfigLoader.getVariable('runConfig', 'logs', 'ias-detailed'):
            Beaver.log("%s: Preprocessing the image before detection and extraction of the shoe"% procName)
   
    def printPreprocessForColorIdentification(procName):
        if ProcConfig.iaShouldTalkInDetail(): print("%s: Preprocessing the image before detecting the main colors of the shoe"% procName)
        if ConfigLoader.getVariable('runConfig', 'logs', 'ias-detailed'):
            Beaver.log("%s: Preprocessing the image before detecting the main colors of the shoe"% procName)
    
    def printPreprocessForTypeIdentification(procName):
        if ProcConfig.iaShouldTalkInDetail(): print("%s: Preprocessing the image before detecting the type of the shoe"% procName)
        if ConfigLoader.getVariable('runConfig', 'logs', 'ias-detailed'):
            Beaver.log("%s: Preprocessing the image before detecting the type of the shoe"% procName)
    
    def printColorDetection(procName):
        if ProcConfig.iaShouldTalkInDetail(): print('%s: Color detector attributed a color to the given image.'% procName)
        if ConfigLoader.getVariable('runConfig', 'logs', 'ias-detailed'):
            Beaver.log('%s: Color detector attributed a color to the given image.'% procName)
            
    def printTypeDetection(procName):
        if ProcConfig.iaShouldTalkInDetail(): print("%s: Detecting the type of the shoe"%procName)
        if ConfigLoader.getVariable('runConfig', 'logs', 'ias-detailed'):
            Beaver.log("%s: Detecting the type of the shoe"%procName)
    