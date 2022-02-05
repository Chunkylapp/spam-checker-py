from task_1 import *

# reads the keywords from data/keywords and from
# additional_keywords files
def readAllKeywords(filePath):

    inputBuffer = open(filePath, 'r')

    keywords = {}  # keywords dictionary
    markup = 0

    for line in inputBuffer:
        # skipping the 1st line
        if (markup == 0):
            markup = 1
            continue
        # clearing the line
        line = line.strip()
        # putting the lowercase version
        keywords[line.lower()] = 0

    inputBuffer.close()

    inputBuffer = open('additional_keywords')

    markup = 0

    for line in inputBuffer:
        # skipping the 1st line
        if (markup == 0):
            markup = 1
            continue
        # clearing the line
        line = line.strip()
        # putting the lowercase version
        keywords[line.lower()] = 0

    inputBuffer.close()

    return keywords

# calculates the average email size
def getAvgSize(files):

    emailsCount = 0
    allWordCount = 0

    for file in files:

        inputBuffer = open('data/emails/'+file, 'r')
        markup = 0

        for line in inputBuffer:
            # checking to see if we found the start of the body
            if(line.find('Body:') == 0):
                markup = 1

            if(markup == 1):
                # clearing the line of characters we don't need
                line = line.strip()
                words = line.split(' ')
                # counting
                for word in words:

                    if (word != ''):
                        allWordCount = allWordCount + 1

        emailsCount = emailsCount + 1

    return allWordCount/emailsCount

# returns the ammount of keywords in an emails
def keywordsScore(file, keywords):

    inputBuffer = open('data/emails/'+file, 'r')
    keywordsCount = 0

    for line in inputBuffer:
        # clearing the line of characters we don't need
        line = line.strip()
        # splitting it into words by spaces
        words = line.split(' ')

        for word in words:
            # making everything lowercase
            word = word.lower()

            for key in keywords:

                if (word.count(key) != 0):
                    # making the sum of occurences
                    keywords[key] = int(keywords[key]) + word.count(key)
                    keywordsCount = keywordsCount + 1

    return keywordsCount

# returns the email lenght in words
def emailLenWords(file):
    inputBuffer = open('data/emails/' + file, 'r')

    size = 0
    markup = 0

    for line in inputBuffer:
        # checking to see if we found the start of the body
        if(line.find('Body:') == 0):
            markup = 1

        if(markup == 1):

            line = line.strip()
            words = line.split(' ')
            # counting the words
            for word in words:

                if (word != ''):
                    size = size + 1

    return size

# returns the email lenght in characters
def emailLenChars(file):
    inputBuffer = open('data/emails/' + file, 'r')

    size = 0
    markup = 0
    # stuff we need to ignore
    stuff = ' \n\t'
    for line in inputBuffer:
        # checking to see if we found the start of the body
        if(line.find('Body:') == 0):
            markup = 1

        if(markup == 1):

            for char in line:

                if(stuff.find(char) != -1):
                    size = size + 1
    return size

# counts the number of capitalized
# characters in a file
def capsCount(file):
    inputBuffer = open('data/emails/'+file, 'r')

    capsNumber = 0
    markup = 0

    for line in inputBuffer:
        # checking to see if we found the start of the body
        if(line.find('Body:') == 0):
            markup = 1

        if(markup == 1):

            for char in line:

                if (char >= 'A' and char <= 'Z'):
                    capsNumber = capsNumber + 1

    return capsNumber

# checks whether the capitalized characters
# make up for more than half of the file
def hasCaps(file, lenght):
    if(capsCount(file) > (lenght//2)):
        return 1
    return 0

# returns the email adress from a given file
def getEmail(file):
    inputBuffer = open('data/emails/'+file, 'r')

    for line in inputBuffer:

        if(line.find('From:') != -1):

            line = line[line.find('From:') + 1:]
            line = line[line.find('<')+1: line.find('>')]
            return line


# checks weather an email is sent from a spammer
# and returns the value found inside the spammers
# file or 0 if the email is not found there
def isSpammer(file):
    email = getEmail(file)
    inputBuffer = open('data/spammers', 'r')

    markdown = 0

    for line in inputBuffer:
        # skipping the 1st line
        if (markdown == 0):
            markdown = 1
            continue

        if (markdown == 1):

            if(line.find(email) != -1):
                line = line.strip()
                line = line.split()
                return int(line[1])

    return 0

# takes care of task 2
def task_2():
    output = open('prediction.out', 'w')

    keywords = readAllKeywords('data/keywords')
    files = readFilenames('data/emails')

    avgSize = getAvgSize(files)

    for file in files:
        keywordsCount = keywordsScore(file, keywords)
        # print(keywordsCount)

        lenghtWords = emailLenWords(file)
        lenghtChars = emailLenChars(file)

        # print(lenghtChars)
        # print(lenghtWords)
        # print()
        keywordsResult = int(
            keywordsCount * ((avgSize * 1.0) / (lenghtWords * 1.0)))

        capsBool = hasCaps(file, lenghtChars)

        spammer = isSpammer(file)

        score = 2 * keywordsResult + 30 * capsBool + spammer
        print(score)
        if (score > 55):
            output.write(str(1) + '\n')
        else:
            output.write(str(0) + '\n')

    output.close()
