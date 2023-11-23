from datetime import datetime

class Inode:
    def __init__(self, ownerId, isDirectory):
        self.ownerId = ownerId
        self.createdDate = datetime.now()
        self.lastAccessedDate = self.createdDate
        self.lastModifiedDate = self.createdDate
        self.permissions = {
            "user": {"read": True, "write": True, "execute": True},
            "group": {"read": True, "write": True, "execute": True},
            "public": {"read": True, "write": False, "execute": False},
        }   
        self.isDirectory = isDirectory
        self.size = 0
        self.blocks = [None] * 10
        self.indirect_block = None

    def inodeInfo(self):
        if (self.isDirectory):
            return f"  Size: {self.size} Blocks: {self.blocks}        directory\n   Uid: {self.ownerId}\nAccess: {self.lastAccessedDate} \nModify: {self.lastModifiedDate} \n Birth: {self.createdDate}"
        else:
            return f"  Size: {self.size} Blocks: {self.blocks}        file\n   Uid: {self.ownerId}\nAccess: {self.lastAccessedDate} \nModify: {self.lastModifiedDate} \n Birth: {self.createdDate}"
