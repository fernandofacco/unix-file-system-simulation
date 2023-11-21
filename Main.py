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
        saveFileSystemState(fileSystem)

    atexit.register(exitHandler)

    while True:
        userInput = input(fileSystem.currentDirectory + ": ")
        inputParts = userInput.split()
        if (inputParts[0] == "exit"):
            break
        elif (inputParts[0] == "cd"):
            fileSystem.cd(inputParts[1])
        elif (inputParts[0] == "ls"):
            fileSystem.ls()  
        elif (inputParts[0] == "mkdir"):
            fileSystem.mkdir(inputParts[1])
        elif (inputParts[0] == "rmdir"):
            fileSystem.rmdir(inputParts[1]) 
        elif (inputParts[0] == "stat"):
            fileSystem.stat(inputParts[1])
        elif (inputParts[0] == "rm"):
            fileSystem.rm(inputParts[1]) 
        elif (inputParts[0] == "touch"):
            fileSystem.touch(inputParts[1]) 
        elif (inputParts[0] == "formata"):
            fileSystem.formata() 
