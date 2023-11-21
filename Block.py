class Block:
    def __init__(self):  
        self.data = ""
        self.size = 512

    def write(self, newData):
        self.data = newData

    def read(self):
        return self.data