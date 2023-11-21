from Inode import Inode
from colorama import Fore, Style
from datetime import datetime
import re

class FileSystem:
    def __init__(self, maxBlocks):
        self.maxBlocks = maxBlocks
        self.blocks = [b'\0' * 512] * maxBlocks
        self.inodes = {}
        self.rootDirectory = "/"
        self.mkdir(self.rootDirectory) # Create directory and Inode for root
        self.currentDirectory = self.rootDirectory
        self.users = {"admin": 0}

    def formata(self):
        self.blocks = [b'\0' * 512] * self.maxBlocks
        self.inodes = {}
        self.rootDirectory = "/"
        self.currentDirectory = self.rootDirectory
        self.users = {"admin": 0}

    def touch(self, fileName):
        filePath = self.getFileOrDirectoryPath(fileName)
        if filePath in self.inodes:
            # Update dates
            self.inodes[filePath].lastAccessedDate = datetime.now()
            self.inodes[filePath].lastModifiedDate = datetime.now()
        else:
            # Create new Inode for a new File
            newInode = Inode(123, False)
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

    def chown(self, user1, user2, arquivo):
        # Altera o proprietário de um arquivo ou diretório
        pass

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
        newInode = Inode(0, True)
        directoryPath = self.getFileOrDirectoryPath(directoryName)
        self.inodes[directoryPath] = newInode

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
                    print(Fore.BLUE + directoryFilePath.split("/")[-1], end = " ")
                    print(Style.RESET_ALL, end = "")
                else:
                    print(directoryFilePath.split("/")[-1], end = " ")
        print()

    def adduser(self, name, user_id):
        # Adiciona um novo usuário
        pass

    def rmuser(self, name):
        # Remove um usuário e todos os seus arquivos
        pass

    def lsuser(self):
        # Lista todos os usuários
        pass

    def stat(self, fileName):
        filePath = self.getFileOrDirectoryPath(fileName)
        if filePath in self.inodes:
            print("  File: " + fileName)
            print(self.inodes[filePath].inodeInfo())


    def isEmpty(self, directoryPath):
        for path, inode in self.inodes.items():
            if path.startswith(directoryPath + "/"):
                return False
        return True

    def getFileOrDirectoryPath(self, directoryFileName):
        if (directoryFileName == "/"):
            return directoryFileName
        
        if (self.currentDirectory == "/"):
            directoryPath = self.currentDirectory + directoryFileName
        else:
            directoryPath = self.currentDirectory + "/" + directoryFileName
        return directoryPath
