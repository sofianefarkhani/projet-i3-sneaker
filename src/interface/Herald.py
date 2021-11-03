from colorama import Fore, Back, Style
'''Quick note on colorama: 
Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
Style: DIM, NORMAL, BRIGHT, RESET_ALL
'''
from interface.ConfigLoader     import ConfigLoader
from processes.Utilities        import Utilities
from processes.Task             import *
from processes.LoaderMessage    import *
from processes.Enums            import *
import queue

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
    
    def printStart(procName):
        '''Announces the start of a process in the terminal.'''
        if ConfigLoader.getVariable('runConfig', 'talkative', 'processes'): 
            print ('%s: Start of service' % procName)
            
    def printTermination(procName):
        '''Announces the end of a process in the terminal.'''
        if ConfigLoader.getVariable('runConfig', 'talkative', 'processes'): 
            print ('%s: End of service' % procName)
    
    
    # LOADER SPECIFIC MESSAGES
    def printLoading(number):
        '''Announces in the terminal that the Loader will load more images.'''
        if Utilities.loaderShouldTalk() : 
            print('Loading '+str(number)+' more images')
    
    def signalLoad(imgName):
        '''Announces in the terminal that an image was loaded successfully.'''
        if Utilities.loaderShouldTalk() : 
            print('    - Loaded '+ imgName)
            
    def printNoMoreImages():
        '''Announces in the terminal that the Loader reached the end of the database.'''
        if Utilities.loaderShouldTalk() : 
            print('No more images in database to load')
    
    
    # BLACKBOX SPECIFIC MESSAGES
    def printWrittenData(procName):
        if Utilities.iaShouldTalk(): 
            print('%s: New data written in the test output file.' % (procName))
    
    
    # RECIEVING MESSAGES
    def getMessageFrom(procName, queue):
        '''Returns the next available message in the given queue, and prints/logs it if necessary.'''
        message = queue.get()
        if Utilities.messagesShouldBeSpoken(): 
            print('%s: Recieved message: %s' % (procName, str(message.type)))
        return message
    
    
    # QUEUING MESSAGES  
    def queueMessageIn(procName, queue, msg):
        '''Places the given message in the given queue, and prints/logs the action if necessary.'''
        queue.put(msg)
        if Utilities.messagesShouldBeSpoken(): 
            print('%s: Sent message: %s' % (procName, str(msg.type)))
    
    
    # IA DETAILS
    def printShoeExtractor(procName):
        if Utilities.iaShouldTalkInDetail(): print("%s: Extracting shoe from the given image" % procName)
        
    def printPreprocessForShoeExtraction(procName):
        if Utilities.iaShouldTalkInDetail(): print("%s: Preprocessing the image before detection and extraction of the shoe"% procName)
        
    def printPreprocessForColorIdentification(procName):
        if Utilities.iaShouldTalkInDetail(): print("%s: Preprocessing the image before detecting the main colors of the shoe"% procName)
        
    def printPreprocessForTypeIdentification(procName):
        if Utilities.iaShouldTalkInDetail(): print("%s: Preprocessing the image before detecting the type of the shoe"% procName)
        
    def printColorDetection(procName):
        if Utilities.iaShouldTalkInDetail(): print('%s: Color detector attributed a color to the given image.'% procName)
    
    def printTypeDetection(procName):
        if Utilities.iaShouldTalkInDetail(): print("%s: Detecting the type of the shoe"%procName)