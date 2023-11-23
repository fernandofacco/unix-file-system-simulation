from Inode import Inode
from User import User
from colorama import Fore, Style
from datetime import datetime
import re

class FileSystem:
    def __init__(self, maxBlocks):
        self.maxBlocks = maxBlocks
        self.blocks = [b'\0' * 512] * maxBlocks
        self.inodes = {} # Dictionary that stores path and inode. Example: {('/', <Inode.Inode object at ...) ('/teste', <Inode.Inode object at ...>)}
        self.rootDirectory = "/"
        self.currentDirectory = self.rootDirectory
        self.users = []
        self.currentUserId = None
        self.currentUsername = None
        self.adduser("root", "1234", "0")
        self.mkdir(self.rootDirectory) # Create directory and Inode for root

    def formata(self):
        self.__init__(self.maxBlocks)

    def touch(self, fileName):
        filePath = self.getFileOrDirectoryPath(fileName)
        if filePath in self.inodes:
            # Update dates
            self.inodes[filePath].lastAccessedDate = datetime.now()
            self.inodes[filePath].lastModifiedDate = datetime.now()
        else:
            # Create new Inode for a new File
            newInode = Inode(self.currentUserId, False)
            self.inodes[filePath] = newInode

    def gravar_conteudo(self, name, position, nbytes, buffer):
        # Grava conteúdo em um arquivo
        pass

    def cat(self, name):
        # Exibe o conteúdo de um arquivo
        pass

    def rm(self, fileName):
        filePath = self.getFileOrDirectoryPath(fileName)
        if (filePath in self.inodes):
            if (not self.inodes[filePath].isDirectory):
                self.inodes.pop(filePath)
            else:
                print("Failed to remove '"+ fileName +"': Not a file.")
        else:
            print("No such file or directory.")

    def chown(self, newOwnerName, fileDirectoryName):
        newOwner = self.getUser(newOwnerName)
        if (newOwner == None):
            print("User with specified username not found.")
            return
        
        fileDirectoryPath = self.getFileOrDirectoryPath(fileDirectoryName)
        if (fileDirectoryPath in self.inodes):
                # Change inode owner
                inode = self.inodes.get(fileDirectoryPath)
                inode.ownerId = newOwner.userId
        else:
            print("No such file or directory.")

    def getUser(self, username):
        for user in self.users:
            if (user.username == username):
                return user
        return None

    def chmod(self, fileDirectoryName, flags):
        fileDirectoryPath = self.getFileOrDirectoryPath(fileDirectoryName)

        if (fileDirectoryPath in self.inodes):
            scopes = ['u', 'g', 'o']
            actions = ['+', '-', '=']
            permissions = ['r', 'w', 'x']
                
            if (isinstance(flags, str)):
                flagsParts = flags.split(",")

                for part in flagsParts:
                    scope = flags[0]
                    action = flags[1]
                    permissionParts = re.split('=|\+|-', part)
                    permission = permissionParts[2]
        else:
            print("No such file or directory.")

    def mkdir(self, directoryName):
        newInode = self.createInode()
        directoryPath = self.getFileOrDirectoryPath(directoryName)
        self.inodes[directoryPath] = newInode

    # Return created inode with current user id or root id
    def createInode(self):
        if (self.currentUserId != None):
            return Inode(self.currentUserId, True)
        else:
            # Root directory owned by root user Uid: 0
            return Inode(0, True)

    def rmdir(self, directoryName):
        directoryPath = self.getFileOrDirectoryPath(directoryName)
        if (directoryPath in self.inodes):
            if (self.inodes[directoryPath].isDirectory):
                if (self.isEmpty(directoryPath)):
                    self.inodes.pop(directoryPath)
                else:
                    print("Failed to remove '"+ directoryName +"': Directory not empty.")
            else:
                print("Failed to remove '"+ directoryName +"': Not a directory.")
        else:
            print("No such file or directory.")
    
    def isEmpty(self, directoryPath):
        for path, inode in self.inodes.items():
            if path.startswith(directoryPath + "/"):
                return False
        return True

    def cd(self, changeToDirectoryName):
        directoryPath = self.getFileOrDirectoryPath(changeToDirectoryName)
            
        if (changeToDirectoryName == ".."):
            if (self.currentDirectory != "/"):
                directory = self.currentDirectory.split("/")
                if (len(directory) > 2): # If cd .. next directory is not root
                    self.currentDirectory = "/".join(directory[:-1])
                else: # cd .. next directory is root
                    self.currentDirectory = "/"
            else:
                self.currentDirectory = "/"
        elif (directoryPath in self.inodes):
            if (self.inodes[directoryPath].isDirectory):
                # If chosen directory is not root add "/" before dir/file name
                self.currentDirectory += "/" + changeToDirectoryName if self.currentDirectory != "/" else changeToDirectoryName
            else:
                print(changeToDirectoryName + "is not a directory.")
        else:
            print("No such file or directory.")

    def ls(self):
        for directoryFilePath, inode in self.inodes.items():
            currentDirectoryPath = self.currentDirectory + ("/" if self.currentDirectory != "/" else "")  # Prevent getting/printing current directory if not root

            # Depths used to only print files and directories from the current directory and not from all directories
            depthCurrentDir = len(currentDirectoryPath.split("/"))
            depthDirItem = len(directoryFilePath.split("/"))

            if (depthDirItem == depthCurrentDir and directoryFilePath.startswith(currentDirectoryPath)):
                if (self.inodes[directoryFilePath].isDirectory):
                    # If is a directory, text will be blue
                    print(Fore.BLUE + directoryFilePath.split("/")[-1], end = " ")
                    print(Style.RESET_ALL, end = "")
                else:
                    print(directoryFilePath.split("/")[-1], end = " ")
        print()

    def adduser(self, username, password, userId):
        for user in self.users:
            if (user.username == username):
                print("User with this username already exists.")
                return
            if (user.userId == userId):
                print("User with this id already exists.")
                return
        newUser = User(username, userId, password)
        self.users.append(newUser)

        # Success message only printed when user is not root
        if (userId != "0"):
            print("User created with success.")

    def rmuser(self, username):
        for user in self.users:
            if (user.username == username):
                self.users.remove(user)
                print("User removed with success.")
                return
        print("User with specified username not found.")

    def lsuser(self):
        for user in self.users:
            print(user.username + " Uid: " + user.userId)
    
    def login(self, username, password):
        for user in self.users:
            if (user.username == username):
                if (user.password == password):
                    self.currentUserId = user.userId
                    self.currentUsername = user.username
                    return
                else:
                    print("Wrong password.")
                    return
        print("User with specified username does not exist.")

    def logout(self):
        self.currentUserId = None
        self.currentUsername = None

    # Display file or directory status
    def stat(self, fileName):
        filePath = self.getFileOrDirectoryPath(fileName)
        if filePath in self.inodes:
            print("  File: " + fileName)
            print(self.inodes[filePath].inodeInfo())

    # Used to get file or directory full path by passing its name
    # Example: if directoryFileName = "documents" and currentDirectory = "/home/usertest/", the file or directory full path will be /home/usertest/documents 
    def getFileOrDirectoryPath(self, directoryFileName):
        if (directoryFileName == "/"):
            return directoryFileName
        
        if (self.currentDirectory == "/"):
            directoryPath = self.currentDirectory + directoryFileName
        else:
            directoryPath = self.currentDirectory + "/" + directoryFileName
        return directoryPath