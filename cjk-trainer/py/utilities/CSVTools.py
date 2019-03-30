from py.VocabWord import VocabWord
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


'''This function will return a list of '''
def importDialogHelper(line_list):
    '''This function will return a list of VocabWord objects'''
    # determine the format of input
    # i[0]
    headers = line_list[0].strip('<').strip('>').split('><')
    word_list = []
    for i in line_list[1:]:
        word_split = i.split(',')
        if i.lstrip()[0] == '#':
            pass
        word_list.append(word_split)
    return headers, word_list

#def