from VocabWord import *
from VocabWordDeck import *
class TypingExercise():
    def __init__(self, main_window, word_deck, parent=None):
        super(TypingExercise, self).__init__()
        self.mainWindow = main_window
        self.wordDeck = word_deck
        print("constructor", self.wordDeck.studyList)



    def checkAnswer(self):
        textValue = self.mainWindow.ui.lineEdit_answer.text()
        print(self.wordDeck.studyList)
        answerList = self.wordDeck.studyList[self.wordDeck.cardNum].definition.split(";")

        print("You entered: " + textValue + " $? " + ", ".join(answerList))
        print(self.wordDeck.studyList[self.wordDeck.cardNum])

        if textValue.lower() in (answer.lower() for answer in answerList):

            print("Correct!")
            self.mainWindow.ui.lineEdit_answer.clear()
            self.wordDeck.studyList[self.wordDeck.cardNum].timesCorrect += 1
            self.wordDeck.studyList[self.wordDeck.cardNum].timesAttempted += 1

            percent = self.wordDeck.calcPercentageCorrect()
            self.mainWindow.ui.label_fractionCorrect.setText("%" + str(percent))

            self.mainWindow.ui.label_typingWord.setText("Correct!\n " + ",".join(answerList))
            self.mainWindow.ui.pushButton_enter.setText("Continue")
            self.mainWindow.ui.lineEdit_answer.setPlaceholderText("Press Enter to continue")
            self.mainWindow.ui.lineEdit_answer.setDisabled(True)
            self.mainWindow.ui.pushButton_enter.clicked.disconnect()
            self.mainWindow.ui.pushButton_enter.clicked.connect(self.nextWord)
        else:
            self.wordDeck.studyList[self.wordDeck.cardNum].timesAttempted += 1
            percent = self.wordDeck.calcPercentageCorrect()
            self.mainWindow.ui.label_fractionCorrect.setText("%" + str(percent))
            self.wordDeck.missedWordList.append(self.wordDeck.studyList[self.wordDeck.cardNum])                    # Add to incorrect list
            print("Incorrect!")
            print("Card number: " + str(self.wordDeck.cardNum))
            self.mainWindow.ui.pushButton_enter.setText("Enter")
            self.mainWindow.ui.pushButton_notSure_Skip.show()
            self.mainWindow.ui.lineEdit_answer.clear()
            self.mainWindow.ui.label_typingWord.setText("Oops! Correct answer is: \n"
                                                        + self.wordDeck.studyList[self.wordDeck.cardNum].definition)
            self.mainWindow.ui.pushButton_notSure_Skip.setText("I was right")
            self.mainWindow.ui.pushButton_notSure_Skip.clicked.disconnect()
            self.mainWindow.ui.pushButton_notSure_Skip.clicked.connect(self.nextWord)
            self.mainWindow.ui.lineEdit_answer.setPlaceholderText("Enter the correct answer")

    def nextWord(self):
        self.mainWindow.ui.progressBar_typing.setValue(self.wordDeck.cardNum +1)
        self.mainWindow.ui.label_fractionCorrect.clear()
        print(self.wordDeck.cardNum, len(self.wordDeck.studyList))
        if self.wordDeck.cardNum == len(self.wordDeck.studyList) -1:
            print("END GAME")
        # elif self.cardNum in self.summaryIndexList:
        #     print("fuq")
        else:
            self.wordDeck.cardNum += 1
            self.mainWindow.ui.lineEdit_answer.setEnabled(True)
            self.mainWindow.ui.pushButton_notSure_Skip.hide()
            self.mainWindow.ui.lineEdit_answer.setFocus()
            self.mainWindow.ui.lineEdit_answer.clear()
            self.mainWindow.ui.lineEdit_answer.setPlaceholderText("Enter your answer")
            self.mainWindow.ui.pushButton_enter.setText("Don't Know")
            self.mainWindow.ui.label_typingWord.setText(self.wordDeck.studyList[self.wordDeck.cardNum].vocabulary)
            self.mainWindow.ui.pushButton_enter.clicked.disconnect()
            self.mainWindow.ui.pushButton_enter.clicked.connect(self.checkAnswer)