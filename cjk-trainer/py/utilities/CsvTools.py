from VocabWord import VocabWord

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
def importDialogHelper(line_list: list, deck_name:str, line_format:str, sep: str = ",") -> list:
    '''
    Pre: line_list: A list of user-inputted csv strings. eg.(['word1,def1', 'word2,def2']
        delim: the delimiter used to separate words (default = ',')
    Post: returns a (SQL compatible) list of user defined words and default values.
        eg. ['Deck_ID','Vocabulary','definition','pronunciation',False]
    Purpose: Provides a means to take user inputted data and send it to SqlTools
    :rtype: list
    '''
    # First read the line format and determine which fields we actually need and in what order
    hasPronun = False
    line_format = line_format.strip("][")
    line_format = line_format.replace("][", ",")
    list_order = line_format.split(",")
    conv_dict = {"Vocabulary":0, "Definition":1, "Pronunciation":2}
    for i in range(0, len(list_order)):
        list_order[i] = conv_dict[list_order[i]]
    vocab_list = []
    validLine = True
    for line in line_list:
        word_split = line.split(sep)
        word_split = [word_split[i]for i in list_order]
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
                print("Cannot import this line: missing Vocabulary slot! :(")
                validLine = False
            try:
                print(word_split[1])
            except IndexError:
                print("Cannot import this line: missing Definition slot! :(")
                validLine = False

            try:
                print(word_split[2])
            except IndexError:
                word_split.append('')
            # if line is acceptable
            if validLine == True:
                print("Valid line! :)")
                #word_split[1], word_split[2] = word_split[2], word_split[1]
                word_split.insert(0, deck_name)
                word_split.append(False)
                vocab_list.append(word_split)
            else:
                print("Inputted line not valid at line num: ", line_list.index(line), "Line skipped.")
            validLine = True

    return vocab_list
