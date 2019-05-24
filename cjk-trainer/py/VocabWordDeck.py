from random import shuffle

class VocabWordDeck:
    def __init__(self, mainWindow, parent=None):
        super(VocabWordDeck, self).__init__()
        self.mainWindow = mainWindow
        self.studyList = []                     # List of VocabWord objects that the user has selected
        self.summaryIndexList = []              # List of indexes for studySet to save and break down statistics to user
        self.missedWordList = []                # List of words to be recirculated into studyList
        self.cardNum = 0                        # Iterator for the studySet

    def calcPercentageCorrect(self):
        return (self.studyList[self.cardNum].timesCorrect / self.studyList[self.cardNum].timesAttempted) * 100

    def shuffleStudySet(self):
        print("Shuffled study set")
        print(self.studyList)
        shuffle(self.studyList)
        #self.mainWindow.reloadWordLabels()

    def setStudyList(self, new_list):
        self.studyList = new_list
        return True
