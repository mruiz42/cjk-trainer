from VocabWord import *
from VocabWordDeck import *
class TypingExercise():
    def __init__(self, main_window, word_deck, parent=None):
        super(TypingExercise, self).__init__()
        self.mainWindow = main_window
        self.wordDeck = word_deck

    def buildAnswerList(self, input_str):
        '''This function will build a list of answers from the database string'''
        tempAnsList = []
        ansList = []
        # Check if there are multiple definitions separated by semicolon
        if ';' in input_str:
            tempAnsList = input_str.split(';')
        # If not, add the single string to a list
        else:
            tempAnsList.append(input_str)

        for ans in tempAnsList:
            if '(' in ans:
                optionalAns = ans.replace(")", "").split("(")
                ansList.append(self.sanitizeInput(optionalAns[0]))
                ansList.append(self.sanitizeInput(optionalAns[1]))
            a = self.sanitizeInput(ans)
            ansList.append(a)
        return ansList

    def submitAnswer(self):
        userInput = self.mainWindow.ui.lineEdit_answer.text()
        answer = self.wordDeck.studyList[self.wordDeck.cardNum].definition
        userInputList = self.buildAnswerList(userInput)
        answerList = self.buildAnswerList(answer)

        print(self.wordDeck.studyList[self.wordDeck.cardNum])
        if self.compareAnswerLists(userInputList, answerList):
            print("Correct!")
            self.mainWindow.ui.lineEdit_answer.clear()
            self.wordDeck.studyList[self.wordDeck.cardNum].timesCorrect += 1
            self.wordDeck.studyList[self.wordDeck.cardNum].timesAttempted += 1
            percent = self.wordDeck.calcPercentageCorrect()
            self.proceedUi(percent)
        else:
            self.wordDeck.studyList[self.wordDeck.cardNum].timesAttempted += 1
            percent = self.wordDeck.calcPercentageCorrect()
            self.wordDeck.missedWordList.append(self.wordDeck.studyList[self.wordDeck.cardNum])                    # Add to incorrect list
            self.pauseUi(percent)

    def compareAnswerLists(self, user_input_list:list, answer_list:list):
        for u in user_input_list:
            if u in answer_list:
                return True
        return False

    def pauseUi(self, percent:str):
        answer = self.wordDeck.studyList[self.wordDeck.cardNum].definition
        print("Incorrect!")
        print("Card number: " + str(self.wordDeck.cardNum))
        self.mainWindow.ui.label_fractionCorrect.setText("%" + str(percent))
        self.mainWindow.ui.pushButton_enter.setText("Enter")
        self.mainWindow.ui.pushButton_notSure_Skip.show()
        self.mainWindow.ui.lineEdit_answer.clear()
        self.mainWindow.ui.label_typingWord.setText("Oops! Correct answer is:\n" + answer)
        self.mainWindow.ui.pushButton_notSure_Skip.setText("I was right")
        self.mainWindow.ui.pushButton_notSure_Skip.clicked.disconnect()
        self.mainWindow.ui.pushButton_notSure_Skip.clicked.connect(self.nextWord)
        self.mainWindow.ui.lineEdit_answer.setPlaceholderText("Enter the correct answer")

    def proceedUi(self, percent:str):
        answer = self.wordDeck.studyList[self.wordDeck.cardNum].definition
        self.mainWindow.ui.label_fractionCorrect.setText("%" + str(percent))
        self.mainWindow.ui.label_typingWord.setText("Correct!\n" + answer)
        self.mainWindow.ui.pushButton_enter.setText("Continue")
        self.mainWindow.ui.lineEdit_answer.setPlaceholderText("Press Enter to continue")
        self.mainWindow.ui.lineEdit_answer.setDisabled(True)
        self.mainWindow.ui.pushButton_enter.clicked.disconnect()
        self.mainWindow.ui.pushButton_enter.clicked.connect(self.nextWord)

    def nextWord(self):
        self.mainWindow.ui.progressBar_typing.setValue(self.wordDeck.cardNum +1)
        self.mainWindow.ui.label_fractionCorrect.clear()
        print(self.wordDeck.cardNum, len(self.wordDeck.studyList))
        if self.wordDeck.cardNum == len(self.wordDeck.studyList) -1:
            print("END GAME")

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
            self.mainWindow.ui.pushButton_enter.clicked.connect(self.submitAnswer)


    def sanitizeInput(self, input_str:str):
        punct = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ '
        return input_str.translate({ord(ch): '' for ch in punct}).lower()

# for i in range(4):
#     userInput = input("Enter your answer: ")
#     print("Answer:", userInput)
#     check(userInput)
#
# if '(' in BASESTRING and ')' in BASESTRING:
#         temp = BASESTRING.split('(')
#         if userInput == temp[0] or temp[1].strip(')') in userInput:
#             print('yay')
#             return