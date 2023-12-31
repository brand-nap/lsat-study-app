
from tkinter import *
from tkinter.filedialog import askopenfilename

def main():
    
    # Selects a File
    inputFileName = input('Please enter the lsat file name: ')

    lines = processFile(inputFileName)

    print(lines)


def processFile(fileName):
    
    readFile = open(fileName, "r") # open for read
    
    lines = []

    # Turns each line into a Student and adds each to list
    line = readFile.readline()
    while line != "":
        lines.append(line)
        line = inFile.readline()
    
    readFile.close() # close file
    return lines;
