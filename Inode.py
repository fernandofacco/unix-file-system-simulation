from datetime import datetime

class Inode:
    def __init__(self, ownerId, isDirectory):
        self.ownerId = ownerId
        self.createdDate = datetime.now()
        self.lastAccessedDate = self.createdDate
        self.lastModifiedDate = self.createdDate
        self.permissions = {
            "user": {"read": True, "write": True, "execute": False},
            "group": {"read": True, "write": False, "execute": False},
            "other": {"read": True, "write": False, "execute": False},
        }   
        self.isDirectory = isDirectory
        self.size = 0
        self.blocks = [None] * 10
        self.blockCount = 0
        self.singleIndirectBlock = None

    def inodeInfo(self):
        if (self.isDirectory):
            return f"  Size: {self.size}               Blocks: {self.blockCount}               directory\nAccess: ({self.buildPermissionStringFormat()})    Uid: {self.ownerId}\nAccess: {self.lastAccessedDate} \nModify: {self.lastModifiedDate} \n Birth: {self.createdDate}"
        else:
            return f"  Size: {self.size}               Blocks: {self.blockCount}               {'regular file' if self.size != 0 else 'regular empty file'}\nAccess: ({self.buildPermissionStringFormat()})    Uid: {self.ownerId}\nAccess: {self.lastAccessedDate} \nModify: {self.lastModifiedDate} \n Birth: {self.createdDate}"
        
    def buildPermissionStringFormat(self):
        permissionString = "-"
        for scope, permission in self.permissions.items():
            permissionString += "r" if permission["read"] else "-"
            permissionString += "w" if permission["write"] else "-"
            permissionString += "x" if permission["execute"] else "-"
        return permissionString
