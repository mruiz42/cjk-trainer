from PySide2.QtWidgets import *
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
        self.DATABASE_PATH = '../data/vocab.db'
        self.indexOfAddedRowsSet = set()        # Index of queued row numbers to be added from wordTable
        self.indexOfModifiedRowsSet = set()     # Index of queued row numbers to be modified from wordTable
        self.indexOfDeletedRowsSet = set()      # Index of queued row numbers to be deleted from wordTable
        self.indexOfCurrentTable = 0            # Index of current table in the deckList
        self.indexOfCurrentTab = 0              # Index of current tab in the tabBar
        self.nameOfCurrentTable = ""            # Name of current table_name for the SQL TableName
        self.wordDeck = VocabWordDeck(self)     # Storage container for vocabWord objects
        self.typingExercise = TypingExercise(self, self.wordDeck)           # Object for controlling typing module
        self.flashcardExercise = FlashcardExercise(self, self.wordDeck)     # Object for controlling flashcard module
        self.quizExercise = QuizExercise(self, self.wordDeck)               # Object for controlling quiz module
        # UI adjustments
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.progressBar_typing.reset()
        self.ui.progressBar_flashcards.reset()
        self.ui.progressBar_quiz.reset()
        self.ui.pushButton_enter.clicked.connect(self.typingExercise.checkAnswer)
        self.ui.pushButton_notSure_Skip.clicked.connect(self.typingExercise.nextWord)
        self.ui.pushButton_notSure_Skip.hide()
        self.ui.lineEdit_answer.textEdited['QString'].connect(self.setTextEnter)
        self.ui.pushButton_wordList_select.clicked.connect(self.loadStudySet)
        self.ui.tab_flashcards.setEnabled(False)
        self.ui.tab_typing.setEnabled(False)
        self.ui.tab_quiz.setEnabled(False)
        self.ui.wordTable.installEventFilter(self)
        # Added - Prevent user from dragging list view objs
        self.ui.deckList.setDragEnabled(False)
        self.ui.deckList.clicked.connect(self.loadWordTable)
        self.ui.deckList.customContextMenuRequested.connect(self.requestDeckViewContextMenu)
        # Added - Connect
        self.ui.pushButton_wordList_select.clicked.connect(self.loadWordTable)        #Added - toolButton menu
        self.ui.toolButton_add.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        addMenu = QtWidgets.QMenu("addMenu", self.ui.toolButton_add)
        newListTableAction = addMenu.addAction("Add new deck")
        importCSVAction = addMenu.addAction("Import CSV")
        self.ui.toolButton_add.setMenu(addMenu)
        self.ui.toolButton_add.clicked.connect(self.openNewTableDialog)
        newListTableAction.triggered.connect(self.openNewTableDialog)
        importCSVAction.triggered.connect(self.openImportCSVDialogue)
        # I changed this stuff to initialize to standard size
        self.ui.wordTable.setColumnCount(7)
        self.ui.wordTable.setRowCount(1)
        # Added Header Labels
        # {:>7}{:>15.2f}{:>11.2f}".format
        self.ui.wordTable.setHorizontalHeaderLabels(
            ['Index', '*', 'Vocabulary', 'Definition', 'Pronunciation', 'Correct', 'Attempted', 'Date Studied'])
        self.ui.wordTable.setColumnHidden(0, True)
        self.ui.wordTable.setColumnWidth(1, 48)
        self.ui.wordTable.setColumnWidth(2, 300)
        self.ui.wordTable.setColumnWidth(3, 300)
        self.ui.wordTable.setColumnWidth(4, 256)
        self.ui.wordTable.setColumnWidth(5, 84)
        self.ui.wordTable.setColumnWidth(6, 96)
        self.ui.wordTable.setColumnWidth(7, 200)
        self.ui.wordTable.customContextMenuRequested.connect(self.requestWordTableContextMenu)
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
        self.ui.checkBox_shuffle.stateChanged.connect(self.shuffleButtonAction)
        self.show()

    def shuffleButtonAction(self):

        state = self.ui.checkBox_shuffle.checkState()
        print(state)
        if state == QtCore.Qt.CheckState.Checked:
            self.ui.wordTable.clear()
            self.ui.wordTable.setHorizontalHeaderLabels(
                ['Index', '*', 'Vocabulary', 'Definition', 'Pronunciation', 'Correct', 'Attempted', 'Date Studied'])
            self.wordDeck.shuffleStudySet()
            lineNo = 0
            for i in self.wordDeck.studyList:
                self.ui.wordTable.insertRow(lineNo)
                self.ui.wordTable.setItem(lineNo, 1, QtWidgets.QTableWidgetItem(str(i.isStarred)))
                self.ui.wordTable.setItem(lineNo, 2, QtWidgets.QTableWidgetItem(str(i.vocabulary)))
                self.ui.wordTable.setItem(lineNo, 3, QtWidgets.QTableWidgetItem(str(i.definition)))
                self.ui.wordTable.setItem(lineNo, 4, QtWidgets.QTableWidgetItem(str(i.pronunciation)))
                self.ui.wordTable.setItem(lineNo, 5, QtWidgets.QTableWidgetItem(str(i.timesCorrect)))
                self.ui.wordTable.setItem(lineNo, 6, QtWidgets.QTableWidgetItem(str(i.timesAttempted)))

                lineNo += 1
                #self.ui.wordTable.setItem(i, 0).QtWidgets.QTableWidgetItem(str(data))
                #self.ui.wordTable.insertRow(i)

                    #print("Row data: ", j[colNo])

                    # if column_number == 0:
                    #     self.ui.wordTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                    # else:
                    #     self.ui.wordTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))


        else:
            self.reloadWordTable()



    def loadExercises(self):
        self.typingExercise = VocabWordDeck()

    # TODO Im pretty sure there is a logic flaw here, should rethink this
    def enableSave(self):
        ''' This function will enable the buttonBox_wordList features to enable table modification'''
        self.ui.buttonBox_wordList.setEnabled(True)
        if self.ui.wordTable.currentRow() not in self.indexOfModifiedRowsSet:
            if self.ui.wordTable.rowCount() == 0:
                self.indexOfModifiedRowsSet.add(0)
                print("Modified index:", self.ui.wordTable.currentRow())
            elif self.ui.wordTable.currentRow() >= 0:
                self.indexOfModifiedRowsSet.add(self.ui.wordTable.currentRow())
                print("Modified index:", self.ui.wordTable.currentRow())

    # TODO DOESNT CONSISTENTLY WORK, NEED TO WORK OUT LOGIC BUGS
    def saveTable(self):
        print("save table")

        self.indexOfModifiedRowsSet = self.indexOfModifiedRowsSet - self.indexOfDeletedRowsSet
        self.indexOfModifiedRowsSet = self.indexOfModifiedRowsSet - self.indexOfAddedRowsSet
        print("modified rows:", self.indexOfModifiedRowsSet, "added rows", self.indexOfAddedRowsSet, "Del rows: ", self.indexOfDeletedRowsSet)
        # Create Sql Connection
        db = SqlTools(self.DATABASE_PATH)
        # Update modified rows, if exist
        if len(self.indexOfModifiedRowsSet) != 0:
            print("SENDING MODIFIED ENTRIES TO DATABASE")
            for rowIndex in self.indexOfModifiedRowsSet:
                rowData = []
                for j in range(0, self.ui.wordTable.columnCount()):
                    print(j, "Table data", self.ui.wordTable.item(rowIndex, j).text())
                    rowData.append(self.ui.wordTable.item(rowIndex, j).text())
                print(rowData)
                # Update the database
                db.modifyTableRows(self.nameOfCurrentTable, rowData, rowIndex)
        # Add rows, if exist
        # TODO ) GETTING AN ERROR WHERE IF THERES NO BLANK ROW AT END, IT WILL DISREGARD THE LAST LINE
        # EVEN IF I HAS VALID DATA
        if len(self.indexOfAddedRowsSet) != 0:
            # Check if last row has valid data
            try:
                print(self.ui.wordTable.item(self.ui.wordTable.rowCount() - 1, 1).text())
            except (AttributeError, ValueError):
                print("garbage data in last row")
                try:
                    self.indexOfAddedRowsSet.remove(self.ui.wordTable.rowCount() -1)
                except KeyError:
                    print("last row seems good")
            # Begin reading added rows
            print("SENDING INSERTED ROWS INTO DATABASE")
            for rowIndex in self.indexOfAddedRowsSet:
                rowData = []
                for j in range(0, self.ui.wordTable.columnCount()):
                    print(j, "Table data", self.ui.wordTable.item(rowIndex, j).text())
                    rowData.append(self.ui.wordTable.item(rowIndex, j).text())
                print(rowIndex, j, rowData)
                if rowData[1] == '' or rowData[2] == '':
                    print(rowData)
                    print("Empty critical slot found, refusing insert into table")
                else:
                    print("INSERTING TABLE DATA!", rowData)
                    print("Updating table at row:", rowIndex)
                    db.addTableRow(self.nameOfCurrentTable, rowData)

        # Delete rows, if exist
        print(self.indexOfDeletedRowsSet)
        if len(self.indexOfDeletedRowsSet) != 0:
            # Now we must remove the rows user does not want anymore
            # Try to delete the item from the table by primary key
            for rowIndex in self.indexOfDeletedRowsSet:
                db.deleteTableRow(self.nameOfCurrentTable, rowIndex)

        db.closeDatabase()
        self.indexOfAddedRowsSet.clear()
        self.indexOfModifiedRowsSet.clear()
        self.indexOfDeletedRowsSet.clear()
        self.ui.buttonBox_wordList.setEnabled(False)

    def reloadTableList(self, reset_checked=False):
        print("REFRESHING TABLE LIST")
        if reset_checked==True:
            self.ui.checkBox_starredOnly.setChecked(False)
            self.ui.checkBox_shuffle.setChecked(False)

        db = SqlTools(self.DATABASE_PATH)
        tableList = db.getTableList()
        tableDict = {}

        try:
            print("Attempting to remove: sqlite_sequence from database.")
            tableList.remove('sqlite_sequence')
        except ValueError:
            print("ValueError: sqlite_sequence not in database.")

        for table_name in tableList:
            tableDict.update({table_name:db.getLastTimeStudied(table_name)})
        db.closeDatabase()
        print(tableDict)

        tableList = [key for (key, value) in sorted(tableDict.items(), key=lambda t: t[1])]
        tableList.reverse()
        print(tableList)
        if tableList == 0:
            print("Empty table.. Creating a starting point..")
            # TODO CALL CREATE DB FROM SQLTOOLS (MUST BE DEFINED THO)

        self.ui.deckList.clear()

        for i in tableList:
            # if i != 'sqlite_sequence':
            self.ui.deckList.addItem(i)
        self.ui.deckList.show()
        return tableList

    def loadWordTable(self, index):
        print(self.ui.wordTable.rowCount())
        #self.ui.checkBox_starredOnly.setChecked(False)
        if index == self.indexOfCurrentTable or index == False:  # I guess sometimes its false :S
            print("nothing to do")
        else:
            self.indexOfCurrentTable = index
            self.nameOfCurrentTable = index.data()
            self.indexOfDeletedRowsSet.clear()
            self.indexOfModifiedRowsSet.clear()
            self.indexOfAddedRowsSet.clear()
            self.ui.wordTable.setSortingEnabled(False)
            self.ui.wordTable.setRowCount(0)
            self.ui.wordTable.clearContents()
            self.ui.wordTable.reset()
            self.ui.wordTable.blockSignals(True)  # Prevent a bug where cell changes would occur on table loading

            self.ui.label_selectedDeck.setText(index.data())
            db = SqlTools(self.DATABASE_PATH)
            result = db.getTableData(self.nameOfCurrentTable)
            db.closeDatabase()
            for row_number, row_data in enumerate(result):
                self.ui.wordTable.insertRow(row_number)
                print("Row number: ", row_number)
                for column_number, data in enumerate(row_data):
                    print("Row data: ", row_data[column_number])
                    if column_number == 0:
                        self.ui.wordTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                    else:
                        self.ui.wordTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        self.ui.wordTable.blockSignals(False)  # Prevent a bug where cell changes would occur on table loading
        self.ui.wordTable.itemChanged.connect(self.enableSave)
        self.ui.buttonBox_wordList.setEnabled(False)
        self.loadStudySet()

    def reloadWordTable(self):
        self.indexOfDeletedRowsSet.clear()
        self.indexOfModifiedRowsSet.clear()
        self.indexOfAddedRowsSet.clear()
        self.ui.wordTable.setSortingEnabled(False)
        self.ui.wordTable.setRowCount(0)
        self.ui.wordTable.clearContents()
        self.ui.wordTable.reset()
        self.ui.wordTable.blockSignals(True)  # Prevent a bug where cell changes would occur on table loading
        print("reverting changes")

        db = SqlTools(self.DATABASE_PATH)
        result = db.getTableData(self.nameOfCurrentTable)
        db.closeDatabase()

        for row_number, row_data in enumerate(result):
            print("Row number: ", row_number)
            self.ui.wordTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                print("Row data: ", row_data[column_number])
                if column_number == 0:
                    self.ui.wordTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                else:
                    self.ui.wordTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        self.ui.wordTable.blockSignals(False)  # Prevent a bug where cell changes would occur on table loading
        self.ui.buttonBox_wordList.setEnabled(False)

    # TODO FINISH QTABLEWIDGET LOGIC WILL NEED SOME REVISIONS TO PRIOR SQL QUERIES
    #   BECAUSE CARD NUMBERS ARE UNACCOUNT FOR DURING THESE TYPES OF INSERTS
    #   IF WE HAVE A DATA STRUCTURE TO WORK WITH ON EVERY DECK LOAD, WE CAN FIND
    #   THE CORRECT CARD NUM

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
        print("CUSTOME MENU REQ")
        self.loadWordTable(self.ui.deckList.currentIndex())
        contextMenuDeckView = QtWidgets.QMenu("contextMenu")
        addAction = contextMenuDeckView.addAction("Add Table")
        deleteAction = contextMenuDeckView.addAction("Delete Table")
        action = contextMenuDeckView.exec_(self.ui.deckList.mapToGlobal(position))
        if action == addAction:
            print("Creating a new deck..")
            self.openNewTableDialog()
        elif action == deleteAction:
            print("Deleting selected deck..")
            print("Are you sure you want to do this?")
            self.openDropTableDialog()

    def insertTableRow(self):
        # To complete, this must be able to GUESS which is the correct cardNum
        # UNLESS, AUTOINCREMENT gives us a primary key automagically

        print("Number of rows before insert: ", self.ui.wordTable.rowCount())

        if self.ui.wordTable.rowCount() == 0:
            self.ui.wordTable.insertRow(0)
            self.indexOfAddedRowsSet.add(0)
        # We can assume that since we add it to the end, the index of the inserted row will be at the end
        else:
            self.ui.wordTable.insertRow(self.ui.wordTable.rowCount())
            self.indexOfAddedRowsSet.add(self.ui.wordTable.rowCount()-1)
            print("Inserting row..", self.ui.wordTable.rowCount()-1)

        for i in range (0, 7):
            newItem = QtWidgets.QTableWidgetItem()
            self.ui.wordTable.setItem(self.ui.wordTable.rowCount()-1, i, newItem)
            if i > 4 or i == 1:
                newItem.setText("0")
            print(newItem.text())
        print("Number of rows after insert: ", self.ui.wordTable.rowCount())

    def updateTableRow(self):
        print("Updating row..",self.ui.wordTable.currentRow(), self.ui.wordTable.currentColumn())
        self.ui.wordTable.setCurrentCell(self.ui.wordTable.currentRow(), self.ui.wordTable.currentColumn())
        self.ui.wordTable.editItem(self.ui.wordTable.item(self.ui.wordTable.currentRow(),self.ui.wordTable.currentColumn()))

    def deleteTableRow(self):
        print("Deleting row: ", self.ui.wordTable.currentRow())

        cardNumToDel = self.ui.wordTable.item(self.ui.wordTable.currentRow(), 0).text()

        self.indexOfDeletedRowsSet.add(cardNumToDel)
        self.ui.wordTable.removeRow(self.ui.wordTable.currentRow())
        self.ui.buttonBox_wordList.setEnabled(True)
        print(self.indexOfDeletedRowsSet)

    def openNewTableDialog(self):
        print("adding new table")
        self.w = DeckNamePrompt(self)
        self.w.show()

    def openDropTableDialog(self):
        print("Deleting table..")
        self.w = ConfirmDeleteTable(self)
        self.w.setTableName(self.nameOfCurrentTable)
        self.w.show()

    def openImportCSVDialogue(self):
        print("open impirt csv dialge")
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

    def loadStudySet(self, shuffle=False):
        self.wordDeck.cardNum = 0

        db = SqlTools(self.DATABASE_PATH)
        result = db.getTableData(self.nameOfCurrentTable)
        #db.setLastTimeStudied(self.nameOfCurrentTable)
        db.closeDatabase()
        #We have a tuple, now lets make a list of VocabWord objects
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
            self.reloadTableList(reset_checked=True)
            #self.ui.deckList.setCurrentRow(0)
            print("Loaded :", self.nameOfCurrentTable)

            return True
        else:
            print("Cannot load an empty table!")
            return False

    def reloadWordLabels(self):
        win.ui.label_typingWord.setText(self.wordDeck.studyList[self.wordDeck.cardNum].vocabulary)
        win.ui.label_flashWord.setText(self.wordDeck.studyList[self.wordDeck.cardNum].vocabulary)
        win.ui.label_quizWord.setText(self.wordDeck.studyList[self.wordDeck.cardNum].vocabulary)

    def loadStarredStudySet(self):
        pass

    def breakdownSummary(self):
        print(self.wordDeck.cardNum, len(self.wordDeck.studyList) - 1)

    def starredButtonAction(self):

        self.typingExercise.studyList = []
        self.indexOfDeletedRowsSet.clear()
        self.indexOfModifiedRowsSet.clear()
        self.indexOfAddedRowsSet.clear()
        self.ui.wordTable.setSortingEnabled(False)
        self.ui.wordTable.setRowCount(0)
        self.ui.wordTable.clearContents()
        self.ui.wordTable.reset()
        self.ui.wordTable.blockSignals(True)                    # Prevent a bug where cell changes would occur on table loading
        if self.ui.checkBox_starredOnly.checkState() == QtCore.Qt.CheckState.Checked:
            db = SqlTools(self.DATABASE_PATH)
            result = db.getStarredTableData(self.nameOfCurrentTable)
            db.closeDatabase()
            for row_number, row_data in enumerate(result):
                print("Row number: ", row_number)
                self.ui.wordTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    print("Row data: ", row_data[column_number])
                    if column_number == 0:
                        self.ui.wordTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                    else:
                        self.ui.wordTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

            if len(result) != 0:
                self.wordDeck.studyList = [VocabWord(*t) for t in result]

                for i in range(10, len(self.wordDeck.studyList), 10):
                    self.summaryIndexList.append(i)
                    # print(i)

                print(self.wordDeck.studyList)
                self.resetProgressBars()
                # win.ui.label_typingWord.setText(self.exercise.studyList[self.cardNum].vocabulary)
                # win.ui.label_flashWord.setText(self.studyList[self.cardNum].vocabulary)
                # win.ui.label_quizWord.setText(self.studyList[self.cardNum].vocabulary)
                self.reloadWordLabels()
                self.ui.tab_flashcards.setEnabled(True)
                self.ui.tab_typing.setEnabled(True)
                self.ui.tab_quiz.setEnabled(True)
                self.ui.wordTable.itemChanged.connect(win.enableSave)
                self.reloadTableList()
                # self.ui.deckList.setCurrentRow(0)
                print("Loaded :", self.nameOfCurrentTable)
                return True
            else:
                print("Cannot load an empty table!")
                return False

            self.ui.wordTable.blockSignals(False)       # Prevent a bug where cell changes would occur on table loading
            self.ui.buttonBox_wordList.setEnabled(False)
            self.loadStudySet()
        elif self.ui.checkBox_starredOnly.isChecked() == False:
            self.reloadWordTable()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    win.reloadTableList()
    win.nameOfCurrentTable = win.ui.deckList.item(0).data(0)
    print(win.nameOfCurrentTable)
    win.loadWordTable(0)
    win.reloadWordTable()

    sys.exit(app.exec_())