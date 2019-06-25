from VocabWord import *
from VocabWordDeck import *
from callReview import *
from datetime import *

class TypingExercise():
    def __init__(self, main_window, word_deck, parent=None):
        super(TypingExercise, self).__init__()
        self.win = main_window
        self.wordDeck = word_deck
        self.missedWorkDeck = list()
        self.startTime = datetime.now()
        print("Started session at: ", self.startTime)

    def resetUi(self):
        #self.mainWindow.ui.progressBar_typing.reset()
        self.setStatLabels()
        self.win.ui.pushButton_enter.setEnabled(True)
        self.win.ui.pushButton_enter.clicked.connect(self.submitAnswer)
        self.win.ui.pushButton_notSure_Skip.clicked.connect(self.nextWord)
        self.win.ui.pushButton_notSure_Skip.hide()
        self.win.ui.lineEdit_answer.textEdited['QString'].connect(lambda: self.win.ui.pushButton_enter.setText("Enter"))

    def setStatLabels(self):
        cn = self.wordDeck.cardNum
        timesCorrect = self.wordDeck.studyList[cn].timesCorrect
        timesMissed = str(self.wordDeck.studyList[cn].timesAttempted - timesCorrect)
        self.win.ui.label_typingCorrect.setText("Times Correct: " + str(timesCorrect))
        self.win.ui.label_typingMissed.setText("Times Missed: " + str(timesMissed))

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
            # if '(' in ans:
            #     # optionalAns = ans.replace(")", "").split("(")
            #     # ansList.append(self.sanitizeInput(optionalAns[0]))
            #     # ansList.append(self.sanitizeInput(optionalAns[1]))
            pos = ans.find('(')
            if pos != -1:
                ans = ans[pos:]
            a = self.sanitizeInput(ans)
            if len(a) > 0 and a != " ":
                ansList.append(a)
        return ansList

    def compareAnswerLists(self, user_input_list:list, answer_list:list):
        for u in user_input_list:
            if u in answer_list:
                return True
        return False

    def submitAnswer(self):
        userInput = self.win.ui.lineEdit_answer.text()
        answer = self.wordDeck.studyList[self.wordDeck.cardNum].definition
        userInputList = self.buildAnswerList(userInput)
        answerList = self.buildAnswerList(answer)
        print("user input:",userInputList, " answer:", answerList)
        # Check answer list against user input list
        if self.compareAnswerLists(userInputList, answerList):
            self.proceedUi()
            print("Current word data: ", self.wordDeck.studyList[self.wordDeck.cardNum])

        else:
            self.pauseUi(answerList)
            print("Current word data: ", self.wordDeck.studyList[self.wordDeck.cardNum])

    def pauseUi(self, answer_list:list):

        cn = self.wordDeck.cardNum
        self.wordDeck.studyList[cn].timesAttempted += 1
        self.setStatLabels()

        self.wordDeck.missedWordList.append(self.wordDeck.studyList[cn])  # Add to incorrect list
        # how to prevent attempted from increasing on "enter it correctly" call
        self.win.ui.lineEdit_answer.textChanged.connect(lambda: self.unpauseUi(answer_list))
        percentLabelStr = self.wordDeck.calcPercentageCorrect()
        answerLabelStr = self.wordDeck.studyList[cn].definition
        self.missedWorkDeck.append(self.wordDeck.studyList[cn])

        self.win.ui.label_typingFractionCorrect.setText("%" + str(percentLabelStr))
        #self.mainWindow.ui.pushButton_enter.setText("Enter")


        self.win.ui.pushButton_notSure_Skip.show()
        self.win.ui.lineEdit_answer.clear()

        self.win.ui.label_typingWord.setText("Oops! Correct answer is:\n" + answerLabelStr)
        self.win.ui.pushButton_notSure_Skip.setText("I was right")
        self.win.ui.pushButton_notSure_Skip.clicked.disconnect()
        self.win.ui.pushButton_notSure_Skip.clicked.connect(self.wasRight)
        self.win.ui.lineEdit_answer.setPlaceholderText("Enter the correct answer")

    def wasRight(self):
        cn = self.wordDeck.cardNum
        print(self.wordDeck.studyList[cn])
        self.wordDeck.studyList[cn].timesAttempted -= 1
        print(self.wordDeck.studyList[cn])
        self.nextWord()

    def unpauseUi(self, answer_list:str):
        userInputList = self.sanitizeInput(self.win.ui.lineEdit_answer.text())
        if userInputList in answer_list:
            print("ui unpauesd")
            self.win.ui.pushButton_enter.setText("Enter")
            self.win.ui.pushButton_enter.setEnabled(True)
            # self.mainWindow.ui.lineEdit_answer.textChanged.disconnect()
            self.win.ui.pushButton_enter.clicked.disconnect()
            self.win.ui.pushButton_enter.clicked.connect(self.nextWord)
        else:
            self.win.ui.pushButton_enter.setEnabled(False)

    def proceedUi(self):
        cn = self.wordDeck.cardNum
        answer = self.wordDeck.studyList[cn].definition
        self.wordDeck.studyList[cn].timesCorrect += 1
        self.wordDeck.studyList[cn].timesAttempted += 1
        self.setStatLabels()
        percent = self.wordDeck.calcPercentageCorrect()
        self.win.ui.lineEdit_answer.clear()
        self.win.ui.label_fractionCorrect.setText("%" + str(percent))
        self.win.ui.label_typingWord.setText("Correct!\n" + answer)
        self.win.ui.pushButton_enter.setText("Continue")
        if self.wordDeck.cardNum in self.wordDeck.summaryIndexList:
            print("OVERVIEW")
            print("Here are the words most commonly missed:")
            for i in self.missedWorkDeck:
                timesMissed = i.timesAttempted - i.timesCorrect
                print(i, timesMissed)
        self.win.ui.lineEdit_answer.setPlaceholderText("Press Enter to continue")
        self.win.ui.lineEdit_answer.setDisabled(True)
        self.win.ui.pushButton_enter.clicked.disconnect()
        self.win.ui.pushButton_enter.clicked.connect(self.nextWord)

    def intermission(self):
        ''' This function will serve as a breakpoint in the typing module where the user can review their progress
        and the program will make a call to save session data into the database. '''
        review = ReviewDialog(self.win)
        review.show()


    def nextWord(self):
        self.win.ui.progressBar_typing.setValue(self.wordDeck.cardNum + 1)
        self.win.ui.label_typingFractionCorrect.clear()
        print(self.wordDeck.cardNum+1, " of ", len(self.wordDeck.studyList))
        if self.wordDeck.cardNum == len(self.wordDeck.studyList):
            print("END GAME")

        else:
            self.wordDeck.cardNum += 1
            self.setStatLabels()
            self.win.ui.lineEdit_answer.setEnabled(True)
            self.win.ui.pushButton_notSure_Skip.hide()
            self.win.ui.lineEdit_answer.setFocus()
            self.win.ui.lineEdit_answer.clear()
            self.win.ui.lineEdit_answer.setPlaceholderText("Enter your answer")
            self.win.ui.pushButton_enter.setText("Don't Know")
            self.win.ui.label_typingWord.setText(self.wordDeck.studyList[self.wordDeck.cardNum].vocabulary)
            self.win.ui.pushButton_enter.clicked.disconnect()
            self.win.ui.pushButton_enter.clicked.connect(self.submitAnswer)
            try:
                self.win.ui.lineEdit_answer.textChanged.disconnect()
            except RuntimeError:
                print("didnt have connection?")
            self.win.ui.pushButton_enter.setEnabled(True)


    def sanitizeInput(self, input_str:str):
        punct = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ '
        return input_str.translate({ord(ch): '' for ch in punct}).lower()