from Inode import Inode
from User import User
from Block import Block
from colorama import Fore, Style
from datetime import datetime

class FileSystem:
    def __init__(self, maxBlocks):
        self.maxBlocks = maxBlocks
        self.blocks = 0  
        self.blockSize = 512
        self.inodes = {} # Dictionary that stores path and inode. Example: {('/', <Inode.Inode object at ...) ('/teste', <Inode.Inode object at ...>)}
        self.rootDirectoryPath = "/"
        self.currentDirectory = self.rootDirectoryPath
        self.users = []
        self.currentUserId = None
        self.currentUsername = None
        self.adduser("root", "1234", "0", True)
        self.mkdir(self.rootDirectoryPath) # Create directory and Inode for root

    def format(self):
        self.__init__(self.maxBlocks)

    def touch(self, fileName):
        filePath = self.getFileOrDirectoryPath(fileName)
        if (filePath in self.inodes):
            # Update dates
            self.inodes[filePath].lastAccessedDate = datetime.now()
            self.inodes[filePath].lastModifiedDate = datetime.now()
        else:
            # Create new Inode for a new File
            newInode = Inode(self.currentUserId, False)
            self.inodes[filePath] = newInode

    def writeContent(self, fileName, data):
        filePath = self.getFileOrDirectoryPath(fileName)
        if (filePath in self.inodes):
            inode = self.inodes.get(filePath)
            if (inode.isDirectory):
                print(fileName +" Is a directory.")
                return
            
            if (not self.hasWritePermission(inode)):
                print("User does not have permission to write file: " + fileName)
                return
            
            # Transform content into bytes
            bytesData = bytearray(data, 'utf-8')
            bytesCount = len(bytesData)

            # Overwrite file blocks
            inode.blocks = [None] * 10 
            inode.size = bytesCount
            self.blocks -= inode.blockCount
            inode.blockCount = 0

            # Write content in new blocks
            for byte in range(0, bytesCount, self.blockSize):
                inode.blockCount += 1
                if (inode.blockCount > 10):
                    print ("Content exceeds 10 blocks of " + str(self.blockSize) + " bytes each.")
                    inode.blockCount = 0
                    inode.blocks = [None] * 10 
                    break

                newBlock = Block(self.blockSize)
                newBlock.write(bytesData[byte:byte + self.blockSize])
                inode.blocks.append(newBlock)
            
            self.blocks += inode.blockCount
            inode.lastModifiedDate = datetime.now()
        else:
            print("File not found.")

    def hasWritePermission(self, inode):
        currentUser = self.getUser(self.currentUsername)
        if (currentUser.isAdmin):
            return True
        
        inodePermissions = inode.permissions
        if (self.currentUserId == inode.ownerId):
            if (inodePermissions["user"]["write"]):
                return True
        elif (inodePermissions["other"]["write"]):
            return True
        return False
            
    def cat(self, fileName):
        filePath = self.getFileOrDirectoryPath(fileName)
        if (filePath in self.inodes):
            inode = self.inodes.get(filePath)
            if (inode.isDirectory):
                print(fileName +" Is a directory.")
                return
            
            if (not self.hasReadPermission(inode)):
                print("User does not have permission to read file: " + fileName)
                return

            fileContent = ""
            for block in inode.blocks:
                if (block != None):
                    fileContent += block.read().decode('utf-8')
            print(fileContent)
        else:
            print("File not found.")

    def hasReadPermission(self, inode):
        currentUser = self.getUser(self.currentUsername)
        if (currentUser.isAdmin):
            return True
        
        inodePermissions = inode.permissions
        if (self.currentUserId == inode.ownerId):
            if (inodePermissions["user"]["read"]):
                return True
        elif (inodePermissions["other"]["read"]):
            return True
        return False

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

    def chmod(self, permissions, fileDirectoryName):
        fileDirectoryPath = self.getFileOrDirectoryPath(fileDirectoryName)

        if (fileDirectoryPath in self.inodes):
            permissionsDictionary = {
                "0": [False, False, False], # ---
                "1": [False, False, True],  # --x
                "2": [False, True, False],  # -w-
                "3": [False, True, True],   # -wx
                "4": [True, False, False],  # r--
                "5": [True, False, True],   # r-x
                "6": [True, True, False],   # rw-
                "7": [True, True, True]     # rwx
            }
            # Transforms permissions string into a list with chars. Example: "754" -> ['7','5','4']
            permissionsChars = list(permissions) 

            # Guarantee that chmod has permission to user, group and others (000 - three chars)
            for i in range (len(permissionsChars), 3, 1):
                permissionsChars.append('0')
        
            # Get corresponding permissions from dictionary
            permissionUser = permissionsDictionary.get(permissionsChars[0])
            permissionGroup = permissionsDictionary.get(permissionsChars[1])
            permissionOther = permissionsDictionary.get(permissionsChars[2])

            self.inodes[fileDirectoryPath].permissions["user"] = {
                "read": permissionUser[0],
                "write": permissionUser[1],
                "execute": permissionUser[2]
            }

            self.inodes[fileDirectoryPath].permissions["group"] = {
                "read": permissionGroup[0],
                "write": permissionGroup[1],
                "execute": permissionGroup[2]
            }

            self.inodes[fileDirectoryPath].permissions["other"] = {
                "read": permissionOther[0],
                "write": permissionOther[1],
                "execute": permissionOther[2]
            }
        else:
            print("No such file or directory.")

    def mkdir(self, directoryName):
        directoryPath = self.getFileOrDirectoryPath(directoryName)
        if (directoryPath in self.inodes):
            if (self.inodes[directoryPath].isDirectory):
                print ("Failed to create directory '" + directoryName + "': Directory already exists.")
                return
            
        newInode = self.createInode()
        newInode.blocks.append(Block(self.blockSize))
        newInode.blockCount += 1
        self.blocks += 1
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
            inode = self.inodes[directoryPath]
            if (inode.isDirectory):
                if (self.isEmpty(directoryPath)):
                    self.blocks -= inode.blockCount
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

    def adduser(self, username, password, userId, isAdmin):
        currentUser = self.getUser(self.currentUsername)
        if (currentUser != None and not currentUser.isAdmin):
            print("Only administrator can add a new user")
            return
        
        for user in self.users:
            if (user.username == username):
                print("User with this username already exists.")
                return
            if (user.userId == userId):
                print("User with this id already exists.")
                return
        newUser = User(username, userId, password, isAdmin)
        self.users.append(newUser)

        # Success message only printed when user is not root
        if (userId != "0"):
            print("User created with success.")

    def rmuser(self, username):
        currentUser = self.getUser(self.currentUsername)
        if (currentUser != None and not currentUser.isAdmin):
            print("Only administrator can remove a user")
            return
        
        if (username == "root"):
            print("Root user can not be removed.")
            return

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
        if (filePath in self.inodes):
            print("  File: " + fileName)
            print(self.inodes[filePath].inodeInfo())
        else:
            print("No such file or directory.")

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
    
    def help(self):
        stringHelp = "Commands:\n"
        stringHelp += "\nformat:\n    Formats the file system, clearing all files, directories and users.\n"
        stringHelp += "\ntouch 'fileName':\n    Creates a empty file or update the acceess and modification times to the current time.\n"
        stringHelp += "\nwrite 'fileName' 'content':\n    Writes content into specified file.\n"
        stringHelp += "\ncat 'fileName':\n    Displays the content of the specified file.\n"
        stringHelp += "\nrm 'fileName':\n    Removes the specified file.\n"
        stringHelp += "\nchown 'newOwnerName' 'fileOrDirectoryName':\n    Changes the owner of the file or directory to the specified user name.\n"
        stringHelp += "\nchmod 'permissions' 'fileOrDirectoryName':\n    Changes the permissions of the file or directory using digits 4 (read), 2 (write), and 1 (execute) for owner, group, and others.\n"
        stringHelp += "\n    Example: 'chmod 754 fileName123' sets read, write, and execute permissions for the owner (7), read and execute for the group (5), and read for the others (4).\n"
        stringHelp += "\nmkdir 'directoryName':\n    Creates a new directory with specified name.\n"
        stringHelp += "\nrmdir 'directoryName':\n    Removes the specified directory.\n"
        stringHelp += "\ncd 'directoryName':\n    Changes the current directory to the specified one.\n"
        stringHelp += "\nls:\n    Lists files and directories in the current directory.\n"
        stringHelp += "\nadduser 'username' 'password' 'userId':\n    Adds a new user with the specified username, password and user ID.\n"
        stringHelp += "\nrmuser 'username':\n    Removes a user with the specified username.\n"
        stringHelp += "\nlsuser:\n    Lists all users.\n"
        stringHelp += "\nlogin 'username' 'password':\n    Logs into the system with the specified username and password.\n"
        stringHelp += "\nlogout:\n    Logs out current user from the system.\n"
        stringHelp += "\nstat 'fileOrDirectoryName':\n    Display information about the specified file or directory, such as owner ID, permissions, size and dates\n"

        print(stringHelp)
