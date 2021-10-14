import jsonpickle
from Data.Tag import Tag


class JsonReader:
    def readOutputFile(inputFilePath:str='../out/data.json', verbalOutput=False):
        
        '''Reads the json data in the output file.
        
        To change the file read, you can input the desired file path.
        Returns the list of tags stored in the output file.'''
        
        file_object = open(inputFilePath, 'r')
        lines = file_object.readlines()
        
        tagList = [] 
        
        #print(lines)
        
        if verbalOutput: print('decoding '+str(len(lines))+" objects:")
        
        for line in lines:
            object = jsonpickle.decode(line) #OBJECT IS ALREADY A TAG
            if verbalOutput: print('    '+str(object.toString()))
            tagList.append(object)
            
        if verbalOutput: print('End of decoding.')
        return tagList
            
        
            
            