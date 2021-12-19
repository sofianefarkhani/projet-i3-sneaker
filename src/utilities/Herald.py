from colorama import Fore, Back, Style
'''Quick note on colorama: 
Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
Style: DIM, NORMAL, BRIGHT, RESET_ALL
'''

from utilities.Beaver                           import Beaver
from utilities.config.getters.TalkConfig        import TalkConfig as TC
from utilities.config.getters.LogsConfig        import LogsConfig as LC
from processes.Task             import *
from processes.LoaderMessage    import *
from processes.Enums            import *



class Herald:
    '''A utility class that processes use to transmit/print/log messages.
    
    This class is basically a fancy way to send signals between processes, and log them.
    Its nothing complicated, just used to hide stuff where the rest of the code is more important. 
    It will all by itself queue the messages, and print the infos / log them.'''
    
    def applyStyle(msg, style:Style=None, fore:Fore=None):
        if style is not None:
            msg = style + msg
        if fore is not None:
            msg = fore + msg
        if style is not None or fore is not None:
            msg += Style.RESET_ALL
        return msg
    
    def bringTheNews(msg:str, consolePrint:bool, logPrint:bool, style:Style=None, fore:Fore=None):
        if consolePrint==True:
            fullMsg = msg
            fullMsg = Herald.applyStyle(fullMsg, style, fore)
            print (fullMsg)
        
        if logPrint==True:
            Beaver.log(msg)    
    
    # PRINTING / LOGGING
    def printError(message):
        '''Prints a string in the terminal, in bright red.'''
        Herald.bringTheNews(message, True, True, Style.BRIGHT, Fore.RED)
    
    def printStart(procName):
        '''Announces the start of a process in the terminal.'''
        msg = '%s: Start of service' % procName
        Herald.bringTheNews(msg, TC.getProc(), LC.getProc(), Style.BRIGHT, Fore.CYAN)
            
    def printTermination(procName):
        '''Announces the end of a process in the terminal.'''
        msg = '%s: End of service' % procName
        Herald.bringTheNews(msg, TC.getProc(), LC.getProc(), fore=Fore.CYAN)
    
    # LOADER SPECIFIC MESSAGES
    def printLoading(number):
        '''Announces in the terminal that the Loader will load more images.'''
        msg = 'Loading %s more images' % str(number)
        Herald.bringTheNews(msg, TC.getLoader(), LC.getLoader(), fore=Fore.BLUE)
    
    
    def signalLoad(imgName):
        '''Announces in the terminal that an image was loaded successfully.'''
        msg = '    - Loaded '+ imgName
        Herald.bringTheNews(msg, TC.getLoader(), LC.getLoader(), fore=Fore.BLUE)  
    
    def printNbImgRemoved(imgRemovedCounter:int):
        '''Announces in the terminal how many images were removed from the initial file list.
        
        Images are removed when they are from products that were previously dealt with already.'''
        if imgRemovedCounter<=0:
            msg = 'All images are new.'
        else:
            msg = 'Loader detected '+str(imgRemovedCounter)+' images that were already dealt with. These will not be sent to the blacboxes.'
        Herald.bringTheNews(msg, TC.getLoader(), LC.getLoader(), fore=Fore.BLUE)  
            
    def printNoMoreImages():
        '''Announces in the terminal that the Loader reached the end of the database.'''
        msg = 'No more images in database to load'
        Herald.bringTheNews(msg, TC.getLoader(), LC.getLoader(), fore=Fore.BLUE)
    
    def printForLoader(msg):
        Herald.bringTheNews(msg, TC.getLoader(), LC.getLoader(), fore=Fore.BLUE)

    # BLACKBOX SPECIFIC MESSAGES
    def printWrittenData(procName):
        msg = '%s: New data written in the test output file.' % procName
        Herald.bringTheNews(msg, TC.getIAs(), LC.getIAs())
        
    def printResults(results:dict, indent:int=1, returned = False):
        msg = "{\n"
        for key in results:
            msg += Herald.getPrintElement(key, results[key], indent)+',\n'
        
        msg = "".join(msg.rsplit(',', 1))
        
        if returned == False: # we want to print it directly
            Herald.bringTheNews(msg+"}", True, False, Style.BRIGHT, Fore.YELLOW)
        else:
            # we just want the string, not printed
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
        else: msg+=str(element)
        return msg
        
        
    # RECIEVING MESSAGES
    def getMessageFrom(procName, queue):
        '''Returns the next available message in the given queue, and prints/logs it if necessary.'''
        message = queue.get()
        
        sstring = Herald.applyStyle(procName, Style.BRIGHT)
        sstring += ': Recieved message: %s' % str(message.type)
        
        Herald.bringTheNews(sstring, TC.getMsgs(), False, fore=Fore.MAGENTA)
        if LC.getMsgs():
            Beaver.log(procName + ': Recieved message: %s' % str(message.type)) 
        return message
    
    # QUEUING MESSAGES  
    def queueMessageIn(procName, queue, msg):
        '''Places the given message in the given queue, and prints/logs the action if necessary.'''
        queue.put(msg)
        
        sstring = Herald.applyStyle(procName, Style.BRIGHT)
        sstring += ': Sent message: %s' % str(msg.type)
        
        Herald.bringTheNews(sstring, TC.getMsgs(), False, fore=Fore.MAGENTA) 
        if LC.getMsgs():
            Beaver.log(procName + ': Sent message: %s' % str(msg.type))
        
    # IA DETAILS
    def printShoeExtractor(procName):
        msg = "%s: Extracting shoe from the given image" % procName
        Herald.bringTheNews(msg, TC.getIADetails(), LC.getIADetails()) 
        
    def printPreprocessForShoeExtraction(procName):
        msg = "%s: Preprocessing the image before detection and extraction of the shoe" % procName
        Herald.bringTheNews(msg, TC.getIADetails(), LC.getIADetails()) 
        
    def printPreprocessForColorIdentification(procName):
        msg = "%s: Preprocessing the image before detecting the main colors of the shoe"% procName
        Herald.bringTheNews(msg, TC.getIADetails(), LC.getIADetails()) 
    
    def printPreprocessForTypeIdentification(procName):
        msg = "%s: Preprocessing the image before detecting the type of the shoe"% procName
        Herald.bringTheNews(msg, TC.getIADetails(), LC.getIADetails()) 
    
    def printColorDetection(procName):
        msg = '%s: Color detector attributed a color to the given image.' % procName
        Herald.bringTheNews(msg, TC.getIADetails(), LC.getIADetails()) 
            
    def printTypeDetection(procName):
        msg = "%s: Detecting the type of the shoe" % procName
        Herald.bringTheNews(msg, TC.getIADetails(), LC.getIADetails()) 
    