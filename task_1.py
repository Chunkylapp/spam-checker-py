import os
import math

# function reads the filenames from a given
# directory file
def readFilenames(dirPath):
    files = os.listdir(dirPath)
    files.sort(key=int)
    return files


# function reads keywords from the given file
# the 1st item of the dictionary is the number
# of keywords held
def readKeywords(filePath):

    inputBuffer = open(filePath, 'r')
    keywords = {}
    markup = 0
    for line in inputBuffer:
        if (markup == 0):
            markup = 1
            continue
        keywords[line.strip()] = 0

    return keywords


# function uses a dictionary initiated with 0 as
# a frequency array to determine the frequency of
# words in a file
def new_spread(files, keywords, spread):
    for file in files:
        for key in keywords:
            spread[file+key] = 0


# function uses a file, a keyword dictionary
# and a spread dictionary to count the occurences
# of every keyword in a file
def frequencyInFile(file, keywords, spread):

    inputBuffer = open('data/emails/'+file, 'r')

    markup = 0

    for line in inputBuffer:
        # looking for the body
        if(line.find('Body:') == 0):
            markup = 1

        if(markup == 1):
            # clearing the line
            line = line.strip()
            # making it lowercase
            line = line.lower()
            # counting the keywords
            for key in keywords:
                if (line.count(key) != 0):
                    keywords[key] = int(keywords[key]) + line.count(key)
                    spread[file + key] = spread[file + key] + line.count(key)


# function does the work
def doWork(files, keywords, spread):

    output = open('statistics.out', 'w')

    for key in keywords:

        spreadValue = 0

        ma = 0
        ma = float('{:.6f}'.format(keywords[key]/len(files)))

        for file in files:

            spreadValue = ((spread[file+key] - ma) *
                           (spread[file+key] - ma)) + spreadValue

        spreadValue = float('{:.6f}'.format(spreadValue/len(files)))
        spreadValue = float('{:.6f}'.format(math.sqrt(spreadValue)))
        output.write(str(key) + ' ' +
                     str(keywords[key]) + ' {:.6f}'.format(spreadValue) + '\n')
    output.close()

# takes care of task 1
def task_1():

    files = readFilenames('data/emails')
    keywords = readKeywords('data/keywords')

    spread = {}

    new_spread(files, keywords, spread)

    for file in files:
        frequencyInFile(file, keywords, spread)

    doWork(files, keywords, spread)
