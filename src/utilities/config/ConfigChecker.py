
from utilities.config.ConfigRequirementException import ConfigRequirementException
from colorama import Style, Fore

class ConfigChecker:

    # To modify the configuration settings, modify the getVarData() function. And READ the paragraph below.
    # Do NOT, I REPEAT, DO NOT modify anything else in this class.
    
    # varData: How does it work? 
    # Basically it contains everything we need to check for the vars
    # there is the struct of the config file, then each var has attributes:
    
        # type: the list of types it can take;
        # min : the min value (included) (if int or float)
        # max : the max value (included) (if int or float)
        # str : needs to be one of those (if str)
        # ext : needs to end with this extension (if str)
        # size: the length of the provided list (if list or tuple)
        # contentType: the expected type of content (if list or tuple)
        # contentMin : The minimum value of the content (included) (if list or tuple, and content is an int or float)
        # contentMax : The maximum value of the content (included) (if list or tuple, and content is an int or float)
    
    # If we do not find the value in the place where it should be, search for an 'any' value, and use that instead.
    # Once the value is found, we check its type, and if there are any other parameters (min, max...) we check thoses.
    # In case there is a problem, we throw an exception. We did good. 
    
    #### BUILDING THE REQUIREMENTS FOR THE CONFIG
    
    def getVarData():
        """Builds and returns the dictionnary of requirements for the variables in config.yaml."""
        runConfig = {
            'noTwoAppsFile': {
                'type': [str]
            },
            
            'nbProcess': {
                'type': [int, str],
                'min' : 1,
                'str' : ['default']
            },
            'talkative': {
                'any' : {
                    'type': [bool] 
                },     
                'tensorflow': {
                    'type': [int],
                    'min' : 0,
                    'max' : 4
                }   
            },
            'logs': {
                'any' : {
                    'type': [bool]
                },
                'file': {
                    'type': [str]
                }
            },
            'gui' : {
                'any': {
                    'type': [bool]
                }
            }
        }
        
        output = {
            'tempData':{
                'type': [str]
            },
            'keepTempFiles':{
                'type':[bool]    
            },
            'any': {
                'type': [str],
                'ext' : '.json'
            }
        }
    
        input = {
            'any': {
                'type': [str],
                'ext' : '.json'
            }
        }
    
        loader = {
            'doneFile' : {
                'type' : [str]
            },
            'redoOldProducts': {
                'type' : [bool]
            },
            'takeFromLocalSource' : {
                'type' : [bool]
            },
            'localImgSrc' : {
                'type' : [str]
            },
            'remoteImgSrc': {
                'type' : [str]
            },
            'batchSize'   : {
                'type': [int],
                'min' : 1
            },
            'reloadNumber': {
                'type': [int],
                'min' : 0
            },
            'remoteCoIds': {
                'any': {
                    'type':[str, None]
                }
            }
        }
    
        background = {
            'any': {
                'type': [list],
                'size': 3,
                'contentType': [float],
                'contentMin' : 0,
                'contentMax' : 1
            }
        }
    
        color_detection = {
            'attempts' : {
                'type': [int],
                'min' : 1
            },
            'margin'   : {
                'type': [int],
                'min' : 1
            },
            'seuil'    : {
                'type': [float],
                'min' : 0,
                'max' : 1
            }
        }
    
        shoeDetection = {
            'any': {
                'type': [str],
                'ext' : '.h5' 
            }
        }
    
        return  {
            'runConfig' : runConfig,
            'output' : output, 
            'input' : input, 
            'loader' : loader,
            'background' : background,
            'color_detection' : color_detection,
            'neuronNetworks' : shoeDetection
        }
    
    
    
    #### THE FUNCTION TO CALL
    
    def checkAllVars(allVars:dict, allVarsData:dict = None, varPath:list = None):
        """Checks all vars in allVars, by type and given value, recursively.
        
        Do not give any other parameter, these are used for the recursivity in the function."""
        
        if allVarsData is None: allVarsData = ConfigChecker.getVarData()
        if varPath is None    : varPath = []

        for var in allVars:
            varValue = allVars[var]
            
            varPathCopy = varPath.copy()
            varPathCopy.append(var)
            
            if var in allVarsData: # there is a pecific clause: 
                if type(varValue) == dict: # is it a dictionnary? 
                    ConfigChecker.checkAllVars(varValue, allVarsData[var], varPathCopy)
                    
                else:  # else: we found an endpoint, check the things we found
                    ConfigChecker.checkVar(varValue, allVarsData[var], varPathCopy)
            
            elif 'any' in allVarsData: # there is an 'any' clause: 
                ConfigChecker.checkVar(varValue, allVarsData['any'], varPathCopy)
            
            else: # there is no clause: show warning
                print(Style.BRIGHT + Fore.RED+'WARNING: There is no requirement clause for :\n'+ConfigChecker.getPathAsException(varPathCopy)+'ConfigChecker cannot verify its validity!'+Style.RESET_ALL)

        
    
    
    #### THE FUNCTION THAT DECIDES WHICH TESTS TO EXECUTE ON A VARIABLE
     
    def checkVar(varValue, specifications: dict, varPath):
        """Checks if a single variable respects the given specifications. Throws an exception in case the variable does not."""
        
        varType = type(varValue)
        
        # we check the specifications: 
        if 'type' in specifications: # Checking the variable type
            ConfigChecker.checkType(varType, varValue, varPath, specifications)
        
        if varType==int or varType==float:
            if 'min' in specifications:
                ConfigChecker.checkMin(varType, varValue, varPath, specifications)
            if 'max' in specifications:
                ConfigChecker.checkMax(varType, varValue, varPath, specifications)

        if varType == str:
            if 'str' in specifications:
                ConfigChecker.checkStrValue(varType, varValue, varPath, specifications)
            if 'ext' in specifications:
                ConfigChecker.checkExtension(varType, varValue, varPath, specifications)
                
        if varType == list or varType == tuple:
            if 'size' in specifications:
                ConfigChecker.checkSize(varType, varValue, varPath, specifications)
            if 'contentType' in specifications:
                ConfigChecker.checkContentType(varType, varValue, varPath, specifications)
            if 'contentMin' in specifications:
                ConfigChecker.checkContentMin(varType, varValue, varPath, specifications)
            if 'contentMax' in specifications:
                ConfigChecker.checkContentMax(varType, varValue, varPath, specifications)
       
    
        
    #### TESTING ONE VARIABLE FROM THE REQUIREMENTS
        
    def checkMin(varType, varValue, varPath, specifications):
        min = specifications['min']
        if varValue < min:
            msg = 'Invalid value given to the int parameter: \n'+ConfigChecker.getPathAsException(varPath)
            msg += '    Minimum possible: '+str(specifications['min'])
            msg += '\n    Given value   : '+str(varValue)
            raise ConfigRequirementException(msg)
    
    def checkMax(varType, varValue, varPath, specifications):
        max = specifications['max']
        if varValue > max:
            msg = 'Invalid value given to the int parameter: \n'+ConfigChecker.getPathAsException(varPath)
            msg += '    Maximum possible: '+str(specifications['max'])
            msg += '\n    Given value   : '+str(varValue)
            raise ConfigRequirementException(msg)
        
    def checkType(varType, varValue, varPath, specifications):
        for t in specifications['type']:
            if varType == t: 
                return
            if t is None and varValue is None:
                return 
        msg = 'Invalid type given to the parameter: \n'+ConfigChecker.getPathAsException(varPath)
        msg += '    Expected type: '+ ConfigChecker.possibleValuesSentence(str(specifications['type']))
        msg += '\n    Given type   : '+str(varType)
        msg += '\n    With value   : '+str(varValue)
        raise ConfigRequirementException(msg)
    
    def checkContentType(varType, varValue, varPath, specifications):
        i=0
        for var in varValue:
            isGud = False
            for t in specifications['contentType']:
                if type(var) == t: 
                    isGud = True
                    break
            if isGud == False:
                msg = 'Invalid value given to the '+('list' if varType==list else 'tuple')+': \n'+ConfigChecker.getPathAsException(varPath)
                msg += '    '+('List' if varType==list else 'Tuple')+' given: '+str(varValue)
                msg += '\n    Expected content type:'+ ConfigChecker.possibleValuesSentence(str(specifications['contentType']))
                msg += '\n    Given type    : '+str(type(var))
                msg += '\n    At index      : '+str(i)
                msg += '\n    With value    : '+str(var)
                raise ConfigRequirementException(msg)
            
            i+=1
    
    def checkContentMin(varType, varValue, varPath, specifications):
        i=0
        min = specifications['contentMin']
        for var in varValue:
            if type(var)==int or type(var)==float:  
                if var<min:
                    msg = 'Invalid value given to the '+('list' if varType==list else 'tuple')+': \n'+ConfigChecker.getPathAsException(varPath)
                    msg += '    '+('List' if varType==list else 'Tuple')+' given: '+str(varValue)
                    msg += '\n    Expected content minimum value: '+ ConfigChecker.possibleValuesSentence(str(specifications['contentMin']))
                    msg += '\n    Given value    : '+str(var)
                    msg += '\n    At index      : '+str(i)
                    raise ConfigRequirementException(msg)
            i+=1
    
    def checkContentMax(varType, varValue, varPath, specifications):
        i=0
        max = specifications['contentMax']
        for var in varValue:
            if type(var)==int or type(var)==float:  
                if var>max:
                    msg = 'Invalid value given to the '+('list' if varType==list else 'tuple')+': \n'+ConfigChecker.getPathAsException(varPath)
                    msg += '    '+('List' if varType==list else 'Tuple')+' given: '+str(varValue)
                    msg += '\n    Expected content maximum value: '+ ConfigChecker.possibleValuesSentence(str(specifications['contentMax']))
                    msg += '\n    Given value    : '+str(var)
                    msg += '\n    At index      : '+str(i)
                    raise ConfigRequirementException(msg)
            i+=1
    
    def checkStrValue(varType, varValue, varPath, specifications):
        '''Checks if the given value is one of the str in the specifications.'''
        isGud = False
        for t in specifications['str']:
            if varValue == t: 
                isGud = True
                break
        if isGud == False:
            msg = 'Invalid str value given to the parameter: \n'+ConfigChecker.getPathAsException(varPath)
            msg += '    Possible strings are: '+ ConfigChecker.possibleValuesSentence(str(specifications['str']))
            msg += '\n    Given string   : '+varValue
            raise ConfigRequirementException(msg)
    
    def checkSize(varType, varValue, varPath, specifications):
        size = specifications['size']
        if len(varValue)!=size:
            msg = 'Invalid size given to the '+str(varType)+' parameter: \n'+ConfigChecker.getPathAsException(varPath)
            msg += '    Expected     : '+str(size)
            msg += '\n    Given        : '+str(len(varValue))
            msg += '\n    With Value   : '+str(varValue)
            raise ConfigRequirementException(msg)
    
    def checkExtension(varType, varValue:str, varPath, specifications):
        ext = specifications['ext']
        if varValue.endswith(ext)==False:
            msg =  'Invalid file given to the file parameter: \n'+ConfigChecker.getPathAsException(varPath)
            msg += '    Expected extension: '+ ext
            msg += '\n    Given value       : '+varValue
            raise ConfigRequirementException(msg)

    #### BUILDING STRINGS FOR EXCEPTION MESSAGES
    
    def getPathAsException(varPath) :
        msg=''
        for i in range(len(varPath)):
            msg += (((i+1)*'    '))[:-1] + '-> ' + varPath[i]+'\n'
        return msg
    
    def possibleValuesSentence(tabAsStr:str):
        return tabAsStr.replace('[', '').replace(']', '').replace(', ', ' or ')