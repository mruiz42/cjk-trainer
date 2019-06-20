from PySide2.QtWidgets import *
from PySide2.QtSql import *
from setupUi.MainWindow import *
from utilities.KeyPressEater import *
from callDeckNamePrompt import *
from callGenericDialog import *
from callImportCsvDialog import *
from callConfirmDeleteTable import *
from utilities.SqlTools import *
from VocabWord import *
from VocabWordDeck import *
from TypingExercise import *
from FlashcardExercise import *
from QuizExercise import *

from PySide2.QtCore import *
from StarDelegate import *

# ADDED KEYPRESS EATER TAB BAR
# self.tabBar = QtWidgets.QTabBar()
# self.tabWidget.setTabBar(self.tabBar)
#Developer notes:
# TODO SEPARATE "BUILT IN TABLES" (NON MODIFYABLE) & "USER DEFINED TABLES" (MODIFYABLE)
# TODO 04) MANAGE BUILT IN DATA STRUCTURE TO STORE STUDY SET DATA
# TODO 06) ADD OPTION FOR SHUFFLE AND SWAP DEFINITION/PRONUNCIATION/VOCABULARY FOR Q/A
# TODO 07) CHECK IF THERES A BETTER WAY TO DISABLE TABS
# TODO 08) INDEX, DECKNAME, STARRED, VOCABULARY, DEFINITION, PRONUN(OPTIONAL), CORR#, ATT#
# TODO 09) AUTO LOAD THE MOST RECENTLY STUDIED DECK.
# TODO 10) NORMALIZE FONTS ACROSS UI WIDGETS
# TODO 11) ADD EXPORT TO CSV FUNCTION
# TODO 12) ADD STAR THIS WORD CONTEXT MENU
# TODO 13) ADD ABILITY TO RESET STATS
# TODO 14) PARSE FOR PUNCTUATION ON CHECK ANSWER
#   puncList = [".",";",":","!","?","/","\\",",","#","@","$","&",")","(","\""]
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Member attributes
        self.DATABASE_PATH = '../data/vocab2.db'
        self.database = SqlTools(self.DATABASE_PATH)
        self.db = QSqlDatabase.addDatabase("QSQLITE", "SQLITE")
        self.db.setDatabaseName("../data/vocab2.db")
        self.db.open()
        self.model = QSqlTableModel(db=self.db)
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.model.dataChanged.connect(self.enableSave)
        # Check if tables exist
        # self.database.createDeckTable()
        # self.database.createCardsTable()
        # self.database.createSessionsTable()
        # self.database.createStatisticsTable()
        self.definitionLanguage = ""
        self.vocabularyLanguage = ""
        self.indexOfAddedRowsSet = set()        # Index of queued card ids to be added from wordTable
        self.indexOfModifiedRowsSet = set()     # Index of queued card ids to be modified from wordTable
        self.indexOfDeletedCardsSet = set()      # Index of queued card ids to be deleted from wordTable

        self.deckListIndex = -1            # Index of current table in the deckList
        self.indexOfCurrentTab = 0              # Index of current tab in the tabBar
        self.nameOfCurrentDeck = ""            # Name of current table_name for the SQL TableName
        self.wordDeck = VocabWordDeck(self)     # Storage container for vocabWord objects
        self.typingExercise = TypingExercise(self, self.wordDeck)           # Object for controlling typing module
        self.flashcardExercise = FlashcardExercise(self, self.wordDeck)     # Object for controlling flashcard module
        self.quizExercise = QuizExercise(self, self.wordDeck)               # Object for controlling quiz module
        # UI adjustments
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.deckList.itemSelectionChanged.connect(lambda: self.deckListClicked(self.ui.deckList.currentIndex()))

        self.ui.progressBar_typing.reset()
        self.ui.progressBar_flashcards.reset()
        self.ui.progressBar_quiz.reset()
        self.ui.pushButton_enter.clicked.connect(self.typingExercise.checkAnswer)
        self.ui.pushButton_notSure_Skip.clicked.connect(self.typingExercise.nextWord)
        self.ui.pushButton_notSure_Skip.hide()
        self.ui.lineEdit_answer.textEdited['QString'].connect(self.setTextEnter)
        self.ui.pushButton_wordList_select.clicked.connect(self.deckListClicked)
        self.ui.tab_flashcards.setEnabled(False)
        self.ui.tab_typing.setEnabled(False)
        self.ui.tab_quiz.setEnabled(False)
        # self.ui.wordTable.installEventFilter(self)
        # Added - Prevent user from dragging list view objs
        self.ui.deckList.setDragEnabled(False)
        self.ui.deckList.customContextMenuRequested.connect(self.requestDeckViewContextMenu)
        # Added - Connect
        self.ui.pushButton_wordList_select.clicked.connect(self.deckListClicked)        #Added - toolButton menu
        self.ui.toolButton_add.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        addMenu = QtWidgets.QMenu("addMenu", self.ui.toolButton_add)
        newListTableAction = addMenu.addAction("Add new deck")
        importCSVAction = addMenu.addAction("Import CSV")
        self.ui.toolButton_add.setMenu(addMenu)
        self.ui.toolButton_add.clicked.connect(lambda: self.openNewTableDialog("create"))
        newListTableAction.triggered.connect(lambda: self.openNewTableDialog("create"))
        importCSVAction.triggered.connect(self.openImportCSVDialogue)
        # I changed this stuff to initialize to standard size
        # self.ui.wordTable.setColumnCount(5)
        # self.ui.wordTable.setRowCount(0)
        # Added Header Labels
        # {:>7}{:>15.2f}{:>11.2f}".format
        # self.ui.wordTable.setHorizontalHeaderLabels(['Card No', 'Starred', 'Vocabulary', 'Definition', 'Pronunciation'])
        # self.ui.wordTable.setColumnHidden(0, True)
        # self.ui.wordTable.setColumnWidth(1, 48)
        # self.ui.wordTable.setColumnWidth(2, 300)
        # self.ui.wordTable.setColumnWidth(3, 300)
        # self.ui.wordTable.setColumnWidth(4, 300)

        # self.ui.wordTable.customContextMenuRequested.connect(self.requestWordTableContextMenu)
        # Added Modified - be careful
        self.ui.buttonBox_wordList.button(QtWidgets.QDialogButtonBox.Cancel).setText("Revert")
        self.ui.buttonBox_wordList.setCenterButtons(False)
        self.ui.buttonBox_wordList.setObjectName("buttonBox_wordList")
        # Added buttonBox_wordList bindings
        self.ui.buttonBox_wordList.accepted.connect(self.saveTable)
        self.ui.buttonBox_wordList.rejected.connect(self.reloadWordTable)
        # Install tabBar Scroll event filter
        eater = KeyPressEater(self, self.ui.tabBar)
        self.ui.tabBar.installEventFilter(eater)
        self.ui.checkBox_starredOnly.stateChanged.connect(self.starredButtonAction)
        self.ui.pushButton_shuffleDeck.clicked.connect(self.shuffleButtonAction)
        self.ui.actionToggle_Pronunciation.changed.connect(self.showPronunciationColumnAction)
        self.indexOfAddedRowsSet.add(0)
        # self.ui.wordTable.setCurrentCell(0, 1)
        self.show()

    def printHi(self):
        pass
    def shuffleButtonAction(self):
        starredState = self.ui.checkBox_starredOnly.checkState()
        self.ui.wordTable.blockSignals(True)  # Prevent a bug where cell changes would occur on table loading
        self.ui.wordTable.clearContents()
        self.wordDeck.shuffleStudySet()
        lineNo = 0
        for i in self.wordDeck.studyList:
            cell_widget = self.createStarCellWidget(i.isStarred)
            self.ui.wordTable.setCellWidget(lineNo, 1, cell_widget)
            self.ui.wordTable.setItem(lineNo, 2, QtWidgets.QTableWidgetItem(str(i.vocabulary)))
            self.ui.wordTable.setItem(lineNo, 3, QtWidgets.QTableWidgetItem(str(i.definition)))
            self.ui.wordTable.setItem(lineNo, 4, QtWidgets.QTableWidgetItem(str(i.pronunciation)))
            lineNo += 1
        self.ui.wordTable.blockSignals(False)  # Prevent a bug where cell changes would occur on table loading
        self.ui.wordTable.itemChanged.connect(self.enableSave)
        self.reloadWordLabels()


    def loadExercises(self):
        self.typingExercise = VocabWordDeck()

    def enableSave(self):
        ''' This function will enable the buttonBox_wordList features to enable table modification'''
        self.ui.buttonBox_wordList.setEnabled(True)

    def saveTable(self):
        self.model.submitAll()
        self.ui.buttonBox_wordList.setDisabled(True)


    def deckListClicked(self, index:QtCore.QModelIndex):
        print(self.deckListIndex, index.row())
        if index.row() == self.deckListIndex:
            print("Nothing to do")
        else:
            self.ui.checkBox_starredOnly.setChecked(False)
            self.deckListIndex = index.row()
            self.nameOfCurrentDeck = index.data()
            self.loadWordTable(self.deckListIndex)
            self.ui.label_selectedDeck.setText(index.data())
            self.ui.tableView.setColumnWidth(2, 30)
            self.ui.tableView.setColumnWidth(3, 200)
            self.ui.tableView.setColumnWidth(4, 200)
            self.ui.tableView.setColumnWidth(5, 200)
            self.ui.buttonBox_wordList.setDisabled(True)





    def loadWordTable(self, index:int, shuffle:bool=False, starredOnly:bool=False):
        self.model.setTable("CARDS")
        self.model.setFilter("DECK_ID=\"{}\"".format(self.nameOfCurrentDeck))
        self.ui.tableView.hideColumn(0)
        self.ui.tableView.hideColumn(1)

        n = StarDelegate(self.ui.tableView)
        self.model.select()
        self.model.setHeaderData(2, Qt.Horizontal, "⭐")
        self.ui.tableView.setItemDelegateForColumn(2, n)
        self.ui.tableView.setModel(self.model)

        self.ui.tableView.hideColumn(0)
        self.ui.tableView.hideColumn(1)


    def reloadWordTable(self):
        self.model.revertAll()

    ########### CONTEXT MENU STUFF ###############
    def requestWordTableContextMenu(self, position):
        contextMenu = QtWidgets.QMenu("contextMenu")
        insertAction = contextMenu.addAction("Insert Row")
        updateAction = contextMenu.addAction("Update Row")
        deleteAction = contextMenu.addAction("Delete Row")
        action = contextMenu.exec_(self.ui.wordTable.mapToGlobal(position))
        if action == insertAction:
            self.insertTableRow()
        elif action == updateAction:
            self.updateTableRow()
        elif action == deleteAction:
            self.deleteTableRow()

    def requestDeckViewContextMenu(self, position):
        self.loadWordTable(self.ui.deckList.currentIndex())
        contextMenuDeckView = QtWidgets.QMenu("contextMenu")
        updateAction = contextMenuDeckView.addAction("Modify Deck")
        addAction = contextMenuDeckView.addAction("Add New Deck")
        deleteAction = contextMenuDeckView.addAction("Delete Deck")
        action = contextMenuDeckView.exec_(self.ui.deckList.mapToGlobal(position))
        if action == addAction:
            print("Creating a new deck..")
            self.openNewTableDialog()
        elif action == deleteAction:
            print("Deleting selected deck..")
            print("Are you sure you want to do this?")
            self.openDropTableDialog()
        elif action == updateAction:
            self.openNewTableDialog(type="modify")

    def insertTableRow(self):
        if self.ui.wordTable.rowCount() == 0:
            self.ui.wordTable.setRowCount(1)
            cell_widget = self.createStarCellWidget()
            self.ui.wordTable.setCellWidget(0, 1, cell_widget)
            self.indexOfAddedRowsSet.add(0)
            self.ui.wordTable.setCurrentCell(0,1)
        else:
            cell_widget = self.createStarCellWidget()
            self.ui.wordTable.insertRow(self.ui.wordTable.rowCount())
            self.ui.wordTable.setCellWidget(self.ui.wordTable.rowCount()-1, 1, cell_widget)
            self.indexOfAddedRowsSet.add(self.ui.wordTable.rowCount() - 1)
            print("Inserting row..", self.ui.wordTable.rowCount()-1)

    def updateTableRow(self):
        print("Updating row..",self.ui.wordTable.currentRow(), self.ui.wordTable.currentColumn())
        self.ui.wordTable.setCurrentCell(self.ui.wordTable.currentRow(), self.ui.wordTable.currentColumn())
        self.ui.wordTable.editItem(self.ui.wordTable.item(self.ui.wordTable.currentRow(),self.ui.wordTable.currentColumn()))

    def deleteTableRow(self):
        print("Deleting row: ", self.ui.wordTable.currentRow())

        cardNumToDel = self.ui.wordTable.item(self.ui.wordTable.currentRow(), 0).text()
        self.indexOfDeletedCardsSet.add(cardNumToDel)
        self.ui.wordTable.removeRow(self.ui.wordTable.currentRow())
        self.ui.buttonBox_wordList.setEnabled(True)
        print(self.indexOfDeletedCardsSet)

    def openNewTableDialog(self, type:str="create"):
        if type == "create":
            self.w = DeckNamePrompt(self)
            self.w.DNPD.buttonBox.accepted.connect(self.w.createDeck)
            self.w.show()
        elif type == "modify":
            self.w = DeckNamePrompt(self)
            self.w.setWindowTitle("Modify Deck")
            langList = self.database.getCurrentLanguages(self.nameOfCurrentDeck)
            self.w.DNPD.lineEdit_enterDeckName.setText(self.nameOfCurrentDeck)
            self.w.DNPD.comboBox_vocabulary.setCurrentText(langList[0])
            self.w.DNPD.comboBox_definition.setCurrentText(langList[1])
            self.w.DNPD.buttonBox.accepted.connect(self.w.modifyDeck)
            self.w.show()

    def openDropTableDialog(self):
        self.w = ConfirmDeleteTable(self)
        self.w.setTableName(self.nameOfCurrentDeck)
        self.w.show()

    def openImportCSVDialogue(self):
        self.w = ImportCSVDialog(self)
        self.w.show()

    def eventFilter(self, source, event):
        #print("entered event filter ")
        #print(event.type())
        # If tab press signaled in wordTable widget
        if (event.type() == QtCore.QEvent.KeyRelease and source == self.ui.wordTable):
            if event.key() == QtCore.Qt.Key_Tab:
                #print(self.ui.wordTable.currentIndex().row(), self.wordTable.currentIndex().column(), "/", bself.wordTable.rowCount(), self.wordTable.columnCount()

                if self.ui.wordTable.currentColumn() == 5:
                    if self.ui.wordTable.currentIndex().row() == self.ui.wordTable.rowCount() - 1:
                        self.insertTableRow()
                    self.ui.wordTable.setCurrentCell(self.ui.wordTable.currentRow() +1, 2)
                    self.ui.wordTable.editItem(self.ui.wordTable.currentItem())


            elif event.key() == QtCore.Qt.Key_Backtab:
                if self.ui.wordTable.currentColumn() == 1:
                    self.ui.wordTable.setCurrentCell(self.ui.wordTable.currentRow() - 1, 4)
                    self.ui.wordTable.editItem(self.ui.wordTable.currentItem())
            return False
        return super(MainWindow, self).eventFilter(source, event)

    def setTextEnter(self):
        win.ui.pushButton_enter.setText("Enter")

    def resetProgressBars(self):
        win.ui.progressBar_typing.reset()
        win.ui.progressBar_typing.setRange(0, len(self.wordDeck.studyList))
        win.ui.progressBar_flashcards.reset()
        win.ui.progressBar_flashcards.setRange(0, len(self.wordDeck.studyList))
        win.ui.progressBar_quiz.reset()
        win.ui.progressBar_quiz.setRange(0, len(self.wordDeck.studyList))

    def loadStudySet(self, result:tuple):
        self.wordDeck.cardNum = 0

        if len(result) != 0:

            self.wordDeck.studyList = [VocabWord(*t) for t in result]
            #self.wordDeck.shuffleStudySet()

            for i in range(10, len(self.wordDeck.studyList), 10):
                self.wordDeck.summaryIndexList.append(i)
                #print(i)
            print("loaded study set: ", self.wordDeck.studyList)
            self.resetProgressBars()
            self.reloadWordLabels()
            self.ui.tab_flashcards.setEnabled(True)
            self.ui.tab_typing.setEnabled(True)
            self.ui.tab_quiz.setEnabled(True)
            self.ui.wordTable.itemChanged.connect(win.enableSave)
            #self.reloadTableList(reset_checked=True)
            self.loadDeckList()
            #self.ui.deckList.setCurrentRow(0)
            print("Loaded :", self.nameOfCurrentDeck)
            return True
        else:
            print("Cannot load an empty table!")
            return False

    def reloadWordLabels(self):
        win.ui.label_typingWord.setText(self.wordDeck.studyList[self.wordDeck.cardNum].vocabulary)
        win.ui.label_flashWord.setText(self.wordDeck.studyList[self.wordDeck.cardNum].vocabulary)
        win.ui.label_quizWord.setText(self.wordDeck.studyList[self.wordDeck.cardNum].vocabulary)


    def breakdownSummary(self):
        print(self.wordDeck.cardNum, len(self.wordDeck.studyList) - 1)


    def showPronunciationColumnAction(self):
        if self.ui.actionToggle_Pronunciation.isChecked():
            self.ui.wordTable.showColumn(4)
        else:
            self.ui.wordTable.hideColumn(4)

    def starredButtonAction(self):
        starredState = self.ui.checkBox_starredOnly.isChecked()
        self.loadWordTable(self.deckListIndex, starredOnly=starredState)
        self.reloadWordLabels()

    def loadDeckList(self):
        self.ui.deckList.clear()
        listOfDecks = self.database.getDecks()
        for i in listOfDecks:
            # if i != 'sqlite_sequence':
            self.ui.deckList.addItem(i[0])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    win.loadDeckList()



    #win.reloadTableList()
    # win.nameOfCurrentTable = win.ui.deckList.item(0).data(0)
    # print(win.nameOfCurrentTable)
    # win.loadWordTable(0)
    # win.reloadWordTable()



    #win.database.closeDatabase()
    sys.exit(app.exec_())