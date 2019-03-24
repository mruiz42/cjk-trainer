import sys
import parser
from PySide2.QtWidgets import *
from PySide2 import QtWidgets

# Ordered by ease/priority
# TODO 01) enable user to shuffle the deck
# TODO 03) center answer feedback for some words
# TODO 06) add randomized feedback ex. (Good job!) (Correct!) (You're right!) etc..
# TODO 07) add a second deck containing missed words (Starred deck)
# TODO 08) add a "start menu"
# TODO 04) track user statistical information on commonly missed words and store the data to disk to be reloaded
# TODO 05) add actions to menu entries
# TODO 09) transition .CSV format to .JSON?
# TODO 10) Add number of times entered correctly
# Todo 11) Add percentage of estimated knowlege of word
# Todo 12) Press ALT to enable shortcuts!

from py.TypingWindow import *

class TypingWindow(QtWidgets. QMainWindow):

    textvalue = ""
    cardnum = 0                                                    # intialize card number from 1
    def __init__(self):
        super().__init__()
        self.ui = Ui_Typing()
        self.ui.setupUi(self)
        self.ui.progressBar.reset()
        self.ui.pushButtonEnter.clicked.connect(self.checkanswer)
        self.ui.pushButtonSkip.clicked.connect(self.nextword)
        self.ui.pushButtonSkip.hide()
        self.ui.lineEditAnswer.textEdited['QString'].connect(self.settextenter)
        self.show()

    def checkanswer(self):
        textvalue = self.ui.lineEditAnswer.text()
        print("You entered: " + textvalue + " $? " + ", ".join(deck[self.cardnum].deflist))
        if textvalue in deck[self.cardnum].deflist:
            print("Correct!")
            self.ui.lineEditAnswer.clear()

            deck[self.cardnum].timescorrect += 1
            deck[self.cardnum].timesattempted += 1

            percent = self.calcPercentageCorrect()
            self.ui.labelNumCorrect.setText("%" + str(percent))

            self.ui.labelVocab.setText("Correct!\n " + ", ".join(deck[self.cardnum].deflist))
            self.ui.pushButtonEnter.setText("Continue")
            self.ui.lineEditAnswer.setPlaceholderText("Press Enter to continue")
            self.ui.lineEditAnswer.setDisabled(True)
            self.ui.pushButtonEnter.clicked.disconnect()
            self.ui.pushButtonEnter.clicked.connect(self.nextword)

        else:
            deck[self.cardnum].timesattempted += 1
            percent = self.calcPercentageCorrect()
            self.ui.labelNumCorrect.setText("%" + str(percent))
            print("Incorrect!")
            print("Card number: " + str(self.cardnum))
            self.ui.pushButtonEnter.setText("Enter")
            self.ui.pushButtonSkip.show()
            self.ui.lineEditAnswer.clear()
            self.ui.labelVocab.setText("Oops! Correct answer is: \n" + str(deck[self.cardnum]))
            self.ui.pushButtonSkip.setText("I was right")
            self.ui.lineEditAnswer.setPlaceholderText("Enter the correct answer")

    def nextword(self):
        self.ui.progressBar.setValue(self.cardnum + 1)
        self.ui.labelNumCorrect.clear()
        print(self.cardnum, numofcards)
        if self.cardnum == numofcards:
            self.cardnum += 1
            print("SHOW STATISTICS")
            self.ui.labelVocab.setText("You got" + "correct!\n" + "Your score: " + "69")

        else:
            self.cardnum += 1
            self.ui.lineEditAnswer.setEnabled(True)
            self.ui.pushButtonSkip.hide()
            self.ui.lineEditAnswer.setFocus()
            self.ui.lineEditAnswer.clear()
            self.ui.lineEditAnswer.setPlaceholderText("Enter your answer")
            self.ui.pushButtonEnter.setText("Dont know")
            self.ui.labelVocab.setText(deck[self.cardnum].vocab)
            self.ui.pushButtonEnter.disconnect()
            self.ui.pushButtonEnter.clicked.connect(self.checkanswer)

    def settextenter(self):
        self.ui.pushButtonEnter.setText("Enter")

    def calcPercentageCorrect(self):
        return (deck[self.cardnum].timescorrect/deck[self.cardnum].timesattempted) * 100

if __name__ == "__main__":

    deck = parser.makeflashcarddeck("./decks/chinese/chineseVocabL4.txt")
    numofcards = len(deck) - 1  # adjust 1 for including 0

    parser.shuffledeck(deck)
    app = QApplication(sys.argv)
    win = TypingWindow()
    win.show()
    win.ui.progressBar.reset()
    win.ui.progressBar.setRange(0, numofcards + 1)

    win.ui.labelVocab.setText(deck[TypingWindow.cardnum].vocab)
    sys.exit(app.exec_())
