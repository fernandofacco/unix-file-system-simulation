from FileSystem import FileSystem
import atexit, pickle
import re
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

    '''
    bloco = bytearray(512)
    stringa = bytearray("abc",'utf-8')
    x = 0
    for i in stringa:
        bloco[x] = i
        x += 1

    for i in bloco:
        if i != 0:
            print(i)

    print(stringa.decode('utf-8'))
    '''
    commands = {
        "formata": lambda fileSystem, _: fileSystem.formata(),
        "touch": lambda fileSystem, args: fileSystem.touch(args[0]),
        "gravar_conteudo": lambda _, __: print("Not implemented"),
        "cat": lambda _, __: print("Not implemented"),
        "rm": lambda fileSystem, args: fileSystem.rm(args[0]),
        "chown": lambda fileSystem, args: fileSystem.chown(args[0], args[1]),
        "chmod": lambda _, __: print("Not implemented"),
        "mkdir": lambda fileSystem, args: fileSystem.mkdir(args[0]),
        "rmdir": lambda fileSystem, args: fileSystem.rmdir(args[0]),
        "cd": lambda fileSystem, args: fileSystem.cd(args[0]),
        "ls": lambda fileSystem, _: fileSystem.ls(),
        "adduser": lambda fileSystem, args: fileSystem.adduser(args[0], args[1], args[2]),
        "rmuser": lambda fileSystem, args: fileSystem.rmuser(args[0]),
        "lsuser": lambda fileSystem, _: fileSystem.lsuser(),
        "login": lambda fileSystem, args: fileSystem.login(args[0], args[1]),
        "logout": lambda fileSystem, _: fileSystem.logout(),
        "stat": lambda fileSystem, args: fileSystem.stat(args[0]),
    }

    while True:
        if fileSystem.currentUserId is None:
            userInput = input("'adduser username password userId' to create a user or 'login username password' to log into a user\n: ")
        else:
            userInput = input(fileSystem.currentUsername + ":" + fileSystem.currentDirectory + "$ ")

        inputParts = userInput.split()
        inputCommand = inputParts[0] if len(inputParts) > 0 else None
        commandArgs = inputParts[1:] # Get all elements of the list except the one in the first index

        if inputCommand == "exit":
            break

        if inputCommand in commands:
            commands[inputCommand](fileSystem, commandArgs)
        else:
            print("Command not recognized")

    '''
    while True:
        userInput = ""
        inputParts = ""
        if (fileSystem.currentUserId == None):
            userInput = input("'adduser username password userId' to create a user or 'login username password' to log into a user\n: ")
            inputParts = userInput.split()
            if (inputParts[0] == "exit"):
                    break
            elif (inputParts[0] == "adduser"):
                fileSystem.adduser(inputParts[1], inputParts[2], inputParts[3])  
            elif (inputParts[0] == "login"):
                fileSystem.login(inputParts[1], inputParts[2])
        else:
            userInput = input(fileSystem.currentDirectory + ": ")
            inputParts = userInput.split()
            if(len(inputParts) > 0):
                if (inputParts[0] == "exit"):
                    break
                elif (inputParts[0] == "formata"):
                    fileSystem.formata() 
                elif (inputParts[0] == "touch"):
                    fileSystem.touch(inputParts[1]) 
                elif (inputParts[0] == "gravar_conteudo"):
                    print("Not implemented")
                elif (inputParts[0] == "cat"):
                    print("Not implemented")
                elif (inputParts[0] == "rm"):
                    fileSystem.rm(inputParts[1])
                elif (inputParts[0] == "chown"):
                    fileSystem.chown(inputParts[1], inputParts[2])
                elif (inputParts[0] == "chmod"):
                    print("Not implemented")
                elif (inputParts[0] == "mkdir"):
                    fileSystem.mkdir(inputParts[1])
                elif (inputParts[0] == "rmdir"):
                    fileSystem.rmdir(inputParts[1]) 
                elif (inputParts[0] == "cd"):
                    fileSystem.cd(inputParts[1])
                elif (inputParts[0] == "ls"):
                    fileSystem.ls()  
                elif (inputParts[0] == "adduser"):
                    fileSystem.adduser(inputParts[1], inputParts[2], inputParts[3])  
                elif (inputParts[0] == "rmuser"):
                    fileSystem.rmuser(inputParts[1]) 
                elif (inputParts[0] == "lsuser"):
                    fileSystem.lsuser() 
                elif (inputParts[0] == "login"):
                    fileSystem.login(inputParts[1], inputParts[2])
                elif (inputParts[0] == "logout"):
                    fileSystem.logout()
                elif (inputParts[0] == "stat"):
                    fileSystem.stat(inputParts[1])
    '''
