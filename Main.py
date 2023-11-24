from FileSystem import FileSystem
import atexit, pickle
import re
from Block import Block

def saveFileSystemState(fileSystem):
    with open('FileSystem_State.pkl', 'wb') as file:
        pickle.dump(fileSystem, file)
    print("File system state saved.")

def loadFileSystemState():
    try:
        with open('FileSystem_State.pkl', 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return None

if __name__ == "__main__":
    fileSystem = loadFileSystemState()
    
    if fileSystem is None:
        fileSystem = FileSystem(1000)
    
    def exitHandler():
        fileSystem.logout()
        saveFileSystemState(fileSystem)


    #atexit.register(exitHandler)

    commandsDictionary = {
        "format": lambda fileSystem, _: fileSystem.format(),
        "touch": lambda fileSystem, args: fileSystem.touch(args[0]),
        "write": lambda fileSystem, args: fileSystem.writeContent(args[0], ' '.join(args[1:])), # Join inputParts except the command
        "cat": lambda fileSystem, args: fileSystem.cat(args[0]),
        "rm": lambda fileSystem, args: fileSystem.rm(args[0]),
        "chown": lambda fileSystem, args: fileSystem.chown(args[0], args[1]),
        "chmod": lambda fileSystem, args: fileSystem.chmod(args[0], args[1]),
        "mkdir": lambda fileSystem, args: fileSystem.mkdir(args[0]),
        "rmdir": lambda fileSystem, args: fileSystem.rmdir(args[0]),
        "cd": lambda fileSystem, args: fileSystem.cd(args[0]),
        "ls": lambda fileSystem, _: fileSystem.ls(),
        "adduser": lambda fileSystem, args: fileSystem.adduser(args[0], args[1], args[2], False),
        "rmuser": lambda fileSystem, args: fileSystem.rmuser(args[0]),
        "lsuser": lambda fileSystem, _: fileSystem.lsuser(),
        "login": lambda fileSystem, args: fileSystem.login(args[0], args[1]),
        "logout": lambda fileSystem, _: fileSystem.logout(),
        "stat": lambda fileSystem, args: fileSystem.stat(args[0]),
        "help": lambda fileSystem, args: fileSystem.help(),
    }

    while True:
        if (fileSystem.currentUserId is None):
            # Root user(username: root  password:)
            userInput = input("Enter your credentials to log in ('login username password') or 'exit' to quit\n: ")
        else:
            userInput = input(fileSystem.currentUsername + ":" + fileSystem.currentDirectory + "$ ")

        inputParts = userInput.split()
        inputCommand = inputParts[0] if len(inputParts) > 0 else None
        commandArgs = inputParts[1:] # Get all elements of the list except the one in the first index

        if (inputCommand == "exit"):
            break

        if (fileSystem.currentUserId is None):
            if (inputCommand == "login"):
                fileSystem.login(commandArgs[0], commandArgs[1])
        else:
            if (inputCommand in commandsDictionary):
                commandsDictionary[inputCommand](fileSystem, commandArgs)
            else:
                print("Command not recognized")