




class Image:
    '''An image wrapper for the cv2.image class. 
    
    Contains an image: img, 
            an id, 
            the path of the image
            a name.'''


    def __init__(self, img, path, id, name):
        self.img = img
        self.path = path
        self.id = id
        self.name = name
        
    def toString(self, indent = 0):
        
        indentmsg = ""
        for i in range(indent):
            indentmsg+="    "
        
        msg=indentmsg+"{"
        
        msg+="\n"+indentmsg+"    name      : "+self.name
        msg+="\n"+indentmsg+"    id        : "+str(self.id)
        msg+="\n"+indentmsg+"    location  : "+self.path
        
        msg+="\n"+indentmsg+"}"
        return msg