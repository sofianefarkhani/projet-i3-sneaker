




class Image:
    '''An image wrapper for the cv2.image class. 
    
    Contains an image: img, 
            an id, 
            a name.'''


    def __init__(self, img, id, name):
        self.img = img
        self.id = id
        self.name = name
        