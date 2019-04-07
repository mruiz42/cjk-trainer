from py.VocabWord import VocabWord
import csv
def importCSV(file_path):
    #def delimiterCommaToParenthesis_Pronun:
    #inFile_Path = input("Enter path to input file:")
    inFile = open(file_path, "r")
    #outFile_Path = input("Enter file name of new file:")

    outFile = open("outFile.txt", "w")
    with inFile as f:
        for line in inFile:
            lineCopy = ""
            if line[0] != '#':
                pos1 = line.find(',')
                pos2 = line.find(',', pos1 +1)
                lineCopy += line[0:pos1] + "("
                lineCopy += line[pos1+1:pos2] + "),"
                lineCopy += line[pos2+1:]
                print(lineCopy)
                #print(pos1)
                #print(pos2)
                outFile.write(lineCopy)

    #outFile = open(outFile_Path + ".txt")

# TODO MAKE THIS FUNCTION MORE RELIABLE, ACCOUNT FOR USER INCLUDING SPACES IN BETWEEN COMMAS?
'''This function will return a list of strings to input into database'''
def importDialogHelper(line_list, delim=","):
    '''
    Pre: line_list: A list of user-inputted csv strings. eg.(['word1,def1', 'word2,def2']
        delim: the delimiter used to separate words (default = ',')
    Post: returns a (SQL compatible) list of user defined words and default values. eg. ['word1','word2','',0,0]
    Purpose: Provides a means to take user inputted data and send it to SqlTools
    '''
    vocab_list = []
    validLine = True
    for line in line_list:
        word_split = line.split(delim)
        # Check for empty line
        if len(line) == 0:
            print("Empty line.")
            pass
        # Check for comment line
        elif line.lstrip()[0] == '#':
            print("Comment line.")
            pass
        # Check for vocab and definition critical slots
        else:
            try:
                print(word_split[0])
            except IndexError:
                print("Cannot import this line, missing Vocabulary slot!")
                validLine = False
            try:
                print(word_split[1])
            except IndexError:
                print("Cannot import this line, missing Definition slot!")
                validLine = False
            try:
                print(word_split[2])
            except IndexError:
                word_split.append('')
            # if line is acceptable
            if validLine == True:
                word_split.append('0')
                word_split.append('0')
                word_split.append('0')
                vocab_list.append(word_split)
            else:
                print("Inputted line not valid at line num: ", line_list.index(line), "Line skipped.")
                pass
            validLine = True

    return vocab_list
