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
            if not (line == '' or line == '\n'):
                object = jsonpickle.decode(line)
                if verbalOutput: print('    '+str(object.toString()))
                tagList.append(object)
            
        if verbalOutput: print('End of decoding.')
        return tagList
            
        
    def getDataForIATypeTraining(fileForTags = '../out/testData.json', typeAsString=False):
        '''Gets you the data for training the AI that recognizes shoe types.
        
        Returns the data under the form: 
            >>    (imgs=[list of image paths],   types=[list of shoe type]).
        The image paths are strings that only tell you the name of the image file, not the path.
        Those names are built as: imageId+"png".
        The shoe types are stored as Data.Type, unless typeAsString is set to True; in which case, types are returned as 'LOW', and 'HIGH'.
        
        These arrays are "sorted" so that for any integer k, 
            imgs[k] has the a shoe of the type: types[k].
        '''
        
        storedTags = JsonReader.readOutputFile(fileForTags)
        imgs = []
        types = []
        
        for tag in storedTags:
            if not typeAsString:
                types.append(tag.type)
            else: 
                types.append(tag.type.name)
            imgs.append(str(tag.databaseID)+'.png')
        
        return (imgs, types)
            
        
        
        
        