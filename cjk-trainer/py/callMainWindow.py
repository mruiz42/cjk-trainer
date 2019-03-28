import sys
from PySide2.QtWidgets import *
from PySide2.QtSql import QSqlQueryModel, QSqlDatabase, QSqlTableModel
from py.MainWindow import *
from py.callImportDeck import *
from py.utilities.SQLTools import *
#Developer notes:
# TODO 01) Manage user interation with vocabulary data
# TODO 02) Allow user to right click tables in QTableView
# TODO SEPARATE "BUILT IN TABLES" (NON MODIFYABLE) & "USER DEFINED TABLES" (MODIFYABLE)
# TODO 03) RCLICK = MODIFY TABLE, DELETE TABLE

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.studySet = []
        self.cardNum = 0
        self.ui.setupUi(self)
        self.ui.progressBar.reset()
        self.ui.pushButton_enter.clicked.connect(self.checkAnswer)
        self.ui.pushButton_notSure_Skip.clicked.connect(self.nextWord)
        self.ui.pushButton_notSure_Skip.hide()
        self.ui.lineEdit_answer.textEdited['QString'].connect(self.setTextEnter)
        self.ui.pushButton_wordList_add.clicked.connect(self.openImportDialog)
        self.ui.pushButton_wordList_select.clicked.connect(self.loadStudySet)
        self.show()

    def setTextEnter(self):
        win.ui.pushButton_enter.setText("Enter")

    def loadStudySet(self):
        db = sqlite3.connect('../data/vocab.db')
        c = db.execute('SELECT * FROM {}'.format(win.ui.nameOfCurrentDeck))
        result = c.fetchall()
        db.close()
        print(result)
        self.studySet = result
        win.ui.progressBar.reset()
        win.ui.progressBar.setRange(0, len(self.studySet)+1)
        win.ui.label_typingWord.setText(self.studySet[self.cardNum][1])


    def checkAnswer(self):
        textValue = win.ui.lineEdit_answer.text()
        answerList = self.studySet[self.cardNum][3].split(";")
        print("You entered: " + textValue + " $? " + ", ".join(answerList))
        if textValue in answerList:
            print("Correct!")
            win.ui.lineEdit_answer.clear()

            #self.studySet[self.cardNum][5] += 1
            #self.studySet[self.cardNum][6] += 1

            #percent = self.calcPercentageCorrect()
            #win.ui.label_fractionCorrect.setText("%" + str(percent))

            win.ui.label_typingWord.setText("Correct!\n " + ",".join(answerList))
            win.ui.pushButton_enter.setText("Continue")
            win.ui.lineEdit_answer.setPlaceholderText("Press Enter to continue")
            win.ui.lineEdit_answer.setDisabled(True)
            win.ui.pushButton_enter.clicked.disconnect()
            win.ui.pushButton_enter.clicked.connect(self.nextWord)
        else:
            #self.studySet[self.cardNum][5] += 1
            #percent = self.calcPercentageCorrect()
            #self.ui.labelNumCorrect.setText("%" + str(percent))
            print("Incorrect!")
            print("Card number: " + str(self.cardNum))
            win.ui.pushButton_enter.setText("Enter")
            win.ui.pushButton_notSure_Skip.show()
            win.ui.lineEdit_answer.clear()
            win.ui.label_typingWord.setText("Oops! Correct answer is: \n" + self.studySet[self.cardNum][3])
            win.ui.pushButton_notSure_Skip.setText("I was right")
            win.ui.pushButton_notSure_Skip.clicked.disconnect()
            win.ui.pushButton_notSure_Skip.clicked.connect(self.nextWord)
            win.ui.lineEdit_answer.setPlaceholderText("Enter the correct answer")



    def nextWord(self):
        win.ui.progressBar.setValue(self.cardNum +1)
        win.ui.label_fractionCorrect.clear()
        print(self.cardNum, len(self.studySet))
        if self.cardNum == len(self.studySet):
            print("END GAME")
        else:
            self.cardNum += 1
            win.ui.lineEdit_answer.setEnabled(True)
            win.ui.pushButton_notSure_Skip.hide()
            win.ui.lineEdit_answer.setFocus()
            win.ui.lineEdit_answer.clear()
            win.ui.lineEdit_answer.setPlaceholderText("Enter your answer")
            win.ui.pushButton_enter.setText("Don't Know")
            win.ui.label_typingWord.setText(self.studySet[self.cardNum][1])
            win.ui.pushButton_enter.clicked.disconnect()
            win.ui.pushButton_enter.clicked.connect(self.checkAnswer)


    def openImportDialog(self):
        self.w = ImportDeck()
        self.w.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    db = QSqlDatabase.addDatabase("QSQLITE", connectionName="prim_conn")
    db.setDatabaseName("../data/vocab.db")


    db.open()

    # Generate list of tables for listWidget
    # Add to SQLTools so we have a local db and cur object to call from main without making a mess in main
    # Call this function to update the list of decks
    vocabTableList = db.tables()
    print(vocabTableList)
    listWidget = win.ui.deckList
    for i in vocabTableList:
        if i != 'sqlite_sequence':
            listWidget.addItem(i)
    listWidget.show()
    db.close()

    win.ui.nameOfCurrentDeck = listWidget.item(0).data(0)
    print(win.ui.nameOfCurrentDeck)
    dbname = win.ui.nameOfCurrentDeck
    conn = sqlite3.connect('../data/vocab.db')
    c = conn.execute('SELECT * FROM {}'.format(dbname))
    result = c.fetchall()
    conn.close()
    print(result)


    sys.exit(app.exec_())