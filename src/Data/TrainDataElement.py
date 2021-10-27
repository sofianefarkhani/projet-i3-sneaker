


from Data.Type import Type


class TrainDataElement():
    
    
    def __init__(self, imageName, isThereAShoe:bool, shoeType:Type=None):
        self.imageName = imageName
        self.isThereAShoe = isThereAShoe
        self.shoeType = shoeType
        
    