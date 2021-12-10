
from utilities.configUtilities.ConfigRequirementException import ConfigRequirementException

class ConfigChecker:

    # To modify the configuration settings, modify the getVarData() function. And READ the paragraph below.
    # Do NOT, I REPEAT, DO NOT modify anything else in this class.
    
    # varData: How does it work? 
    # Basically it contains everything we need to check for the vars
    # there is the struct of the config file, then each var has attributes:
    
    # type: the list of types it can take;
    # min:  the min value (included) (if int)
    # max:  the max value (included) (if int)
    # str:  needs to be one of those (if str)
    # size: the length of the provided list (if list or tuple)
    
    # If we do not find the value in the place where it should be, search for an 'any' value, and use that instead.
    # Once the value is found, we check its type, and if there are any other parameters (min, max...) we check thoses.
    # In case there is a problem, we throw an exception. We did good. 
    
    def getVarData():
        runConfig = {
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
            'any': {
                'type': [str]
            }
        }
    
        input = {
            'any': {
                'type': [str]
            }
        }
    
        loader = {
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
            }
        }
    
        background = {
            'any': {
                'type': [str],
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
                'type': [str]
            }
        }
    
        return  {
            'runConfig' : runConfig,
            'output' : output, 
            'input' : input, 
            'loader' : loader,
            'background' : background,
            'color_detection' : color_detection,
            'shoeDetection' : shoeDetection
        }
    
    def checkAllVars(allVars:dict, allVarsData:dict = None, varPath:list = None):
        """Checks all vars in allVars, by type and given value, recursively."""
        
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
                print('There is no clause for '+str(var)+', ConfigChecker cannot verify its validity')
        
    def checkVar(varValue, specifications: dict, varPath):
        """Checks if a single variable respects the given specifications. Throws an exception in case the variable does not."""
        
        varType = type(varValue)
        
        # we check the specifications: 
        if 'type' in specifications: # Checking the variable type
            ConfigChecker.checkType(varType, varValue, varPath, specifications)
        
        if varType == int:
            if 'min' in specifications:
                ConfigChecker.checkMin(varType, varValue, varPath, specifications)
            if 'max' in specifications:
                ConfigChecker.checkMax(varType, varValue, varPath, specifications)

        if varType == str:
            if 'str' in specifications:
                ConfigChecker.checkStrValue(varType, varValue, varPath, specifications)
                
        if varType == list or varType == tuple:
            if 'size' in specifications:
                ConfigChecker.checkSize(varType, varValue, varPath, specifications)
        
    def getPathAsException(varPath) :
        msg=''
        for i in range(len(varPath)):
            msg += (((i+1)*'    '))[:-1] + '-> ' + varPath[i]+'\n'
        return msg
        
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
        isGud = False
        for t in specifications['type']:
            if varType == t: 
                isGud = True
                break
        if isGud == False:
            msg = 'Invalid type given to the parameter: \n'+ConfigChecker.getPathAsException(varPath)
            msg += '    Expected type: '+ ConfigChecker.possibleValuesSentence(str(specifications['type']))
            msg += '\n    Given type   : '+str(varType)
            msg += '\n    With value   : '+str(varValue)
            raise ConfigRequirementException(msg)
    
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
            msg += '    Expected: '+str(size)
            msg += '\n    Given   : '+str(len(varValue))
            raise ConfigRequirementException(msg)
    
    def possibleValuesSentence(tabAsStr:str):
        return tabAsStr.replace('[', '').replace(']', '').replace(', ', ' or ')