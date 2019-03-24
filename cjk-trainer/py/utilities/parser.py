from py.VocabWord import *
import random
# Parser will
# Parser.py will parse a file and import VocabWord objects


def makeflashcarddeck(file):
    inputfile = open(file, mode='r')
    deflist = []                 # list of definitions per each word
    deck = []                    # list of VocabWord objectstypo
    cardsindeck = 0              # number of cards added in deck

    for i in inputfile:
        line = i                 # set line string equal to input
        if len(line) != 0:       # if the line is not empty
            pos0 = line.find(",")
            pos1 = line.find("(")
            pos2 = line.find(")")
            # Begin 'slicing'
            vocab = line[0:pos0]                # hanzi + pinyin
            pronunciation = line[pos1+1:pos2]   # pinyin
            hanzi = line[0:pos1]                # hanzi
            definition = line[pos0+1:]
            #print(definition)
            definition = definition.strip('\n')
            deflist += definition.split("; ")
            #print(deflist)
            timesmissed = 0
            timesattempted = 0
            flashcard = VocabWord(vocab, pronunciation, deflist, hanzi, timesmissed, timesattempted)
            deck.append(flashcard)
            deflist = []
            cardsindeck += 1
        else:
            print("EMPTY LINE!")
    inputfile.close()
    print("Import of ", end="")
    print(cardsindeck, end="")
    print(" entries")
    return deck

def shuffledeck(deck):

    random.shuffle(deck)
    #for i in range(0, len(deck)):
    #    print(deck[i])
    return deck



def savesession():
    # This funciton will output the list for restoration
    print("null")