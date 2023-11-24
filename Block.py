class Block:
    def __init__(self, blockSize):  
        self.data = ""
        self.size = blockSize

    def write(self, newData):
        self.data = newData

    def read(self):
        return self.data