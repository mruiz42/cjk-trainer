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
from PySide2.QtCore import *
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
        # Check if tables exist
        self.database.createDeckTable()
        self.database.createCardsTable()
        self.database.createSessionsTable()
        self.database.createStatisticsTable()

        self.indexOfAddedCardsSet = set()        # Index of queued card ids to be added from wordTable
        self.indexOfModifiedCardsSet = set()     # Index of queued card ids to be modified from wordTable
        self.indexOfDeletedCardsSet = set()      # Index of queued card ids to be deleted from wordTable

        self.indexOfCurrentTable = 0            # Index of current table in the deckList
        self.indexOfCurrentTab = 0              # Index of current tab in the tabBar
        self.nameOfCurrentDeck = ""            # Name of current table_name for the SQL TableName
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
        self.ui.wordTable.setColumnCount(5)
        self.ui.wordTable.setRowCount(0)
        # Added Header Labels
        # {:>7}{:>15.2f}{:>11.2f}".format
        self.ui.wordTable.setHorizontalHeaderLabels(['Card No', 'Starred', 'Vocabulary', 'Definition', 'Pronunciation'])
        self.ui.wordTable.setColumnHidden(0, True)
        self.ui.wordTable.setColumnWidth(1, 48)
        self.ui.wordTable.setColumnWidth(2, 300)
        self.ui.wordTable.setColumnWidth(3, 300)
        self.ui.wordTable.setColumnWidth(4, 300)

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



        self.ui.actionToggle_Pronunciation.changed.connect(self.showPronunciationColumnAction)
        self.indexOfAddedCardsSet.add(0)
        self.ui.wordTable.setCurrentCell(0, 1)
        self.show()

    def shuffleButtonAction(self):

        state = self.ui.checkBox_shuffle.checkState()
        if state == QtCore.Qt.CheckState.Checked:
            self.ui.wordTable.clear()
            # self.ui.wordTable.setHorizontalHeaderLabels(
            #     ['Index', 'Starred', 'Vocabulary', 'Definition', 'Pronunciation'])
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

    def enableSave(self):
        ''' This function will enable the buttonBox_wordList features to enable table modification'''
        self.ui.checkBox_shuffle.setDisabled(True)
        self.ui.checkBox_starredOnly.setDisabled(True)
        self.ui.buttonBox_wordList.setEnabled(True)
        if self.ui.wordTable.currentRow() not in self.indexOfModifiedCardsSet:
            if self.ui.wordTable.rowCount() == 0:
                self.indexOfModifiedCardsSet.add(0)
                print("Modified index:", self.ui.wordTable.currentRow())
            elif self.ui.wordTable.currentRow() >= 0:
                self.indexOfModifiedCardsSet.add(self.ui.wordTable.currentRow())
                print("Modified index:", self.ui.wordTable.currentRow())

    def saveTable(self):
        # print("save table")
        self.indexOfModifiedCardsSet = self.indexOfModifiedCardsSet - self.indexOfDeletedCardsSet
        self.indexOfModifiedCardsSet = self.indexOfModifiedCardsSet - self.indexOfAddedCardsSet
        print("modified rows:", self.indexOfModifiedCardsSet, "added rows", self.indexOfAddedCardsSet,
              "Del rows: ", self.indexOfDeletedCardsSet)
        # # Update modified rows, if exist
        if len(self.indexOfModifiedCardsSet) != 0:
            print("SENDING MODIFIED ENTRIES TO DATABASE")
            for rowIndex in self.indexOfModifiedCardsSet:
                rowData = []
                for j in range(1, self.ui.wordTable.columnCount()):
                    if j == 1:
                        rowData.append(self.ui.wordTable.cellWidget(rowIndex,1).isChecked())
                    else:
                        print(j, "Table data", self.ui.wordTable.item(rowIndex, j).text())
                        print("RI", rowIndex, "j", j)
                        rowData.append(self.ui.wordTable.item(rowIndex, j).text())
                rowData.append(self.ui.wordTable.item(rowIndex, 0).text())
                self.database.modifyTableRows(rowData, rowIndex)
        # # Add rows, if exist
        # # TODO ) GETTING AN ERROR WHERE IF THERES NO BLANK ROW AT END, IT WILL DISREGARD THE LAST LINE
        # # EVEN IF I HAS VALID DATA
        # if len(self.indexOfAddedCardsSet) != 0:
        #     # Check if last row has valid data
        #     try:
        #         print(self.ui.wordTable.item(self.ui.wordTable.rowCount() - 1, 1).text())
        #     except (AttributeError, ValueError):
        #         print("garbage data in last row")
        #         try:
        #             self.indexOfAddedCardsSet.remove(self.ui.wordTable.rowCount() -1)
        #         except KeyError:
        #             print("last row seems good")
            # Begin reading added rows
        print("SENDING INSERTED ROWS INTO DATABASE")
        for rowIndex in self.indexOfAddedCardsSet:
            rowData = []
            rowData.append(self.nameOfCurrentDeck)
            rowData.append(self.ui.wordTable.cellWidget(rowIndex,1).isChecked())
            for j in range(2, self.ui.wordTable.columnCount()):
                print(j, "Table data", self.ui.wordTable.item(rowIndex, j).text())
                rowData.append(self.ui.wordTable.item(rowIndex, j).text())
            print(rowIndex, j, rowData)
            if rowData[1] == '' or rowData[2] == '':
                print(rowData)
                print("Empty critical slot found, refusing insert into table")
            else:
                print("INSERTING TABLE DATA!", rowData)
                print("Updating table at row:", rowIndex)
                #self.database.addTableRow(self.nameOfCurrentTable, rowData)
                self.database.insertCard(rowData)
        # Delete rows, if exist
        print(self.indexOfDeletedCardsSet)
        if len(self.indexOfDeletedCardsSet) != 0:
            print("DELETING SELECTED ROWS INTO DATABASE")
            # Now we must remove the rows user does not want anymore
            # Try to delete the item from the table by primary key
            for rowIndex in self.indexOfDeletedCardsSet:
                self.database.deleteTableRow(self.nameOfCurrentDeck, rowIndex)

        self.indexOfAddedCardsSet.clear()
        self.indexOfModifiedCardsSet.clear()
        self.indexOfDeletedCardsSet.clear()
        self.ui.buttonBox_wordList.setEnabled(False)
        self.ui.checkBox_shuffle.setEnabled(True)
        self.ui.checkBox_starredOnly.setEnabled(True)

    def loadWordTable(self, index):
        print(self.ui.wordTable.rowCount())
        #self.ui.checkBox_starredOnly.setChecked(False)
        if index == self.indexOfCurrentTable or index == False:  # I guess sometimes its false :S
            print("nothing to do")
        else:
            self.indexOfCurrentTable = index
            self.nameOfCurrentDeck = index.data()
            self.indexOfDeletedCardsSet.clear()
            self.indexOfModifiedCardsSet.clear()
            self.indexOfAddedCardsSet.clear()
            self.ui.wordTable.setSortingEnabled(False)
            self.ui.wordTable.setRowCount(0)
            self.ui.wordTable.clearContents()
            self.ui.wordTable.reset()
            self.ui.wordTable.blockSignals(True)  # Prevent a bug where cell changes would occur on table loading
            self.ui.label_selectedDeck.setText(index.data())
            result = self.database.getTableData(self.nameOfCurrentDeck)
            for row_number, row_data in enumerate(result):
                self.ui.wordTable.insertRow(row_number)
                #print("Row number: ", row_number)
                for column_number, data in enumerate(row_data):
                    if column_number == 1:
                        cell_widget = self.createStarCellWidget(data)
                        self.ui.wordTable.setCellWidget(row_number, column_number, cell_widget)
                    else:
                        #print("Row data: ", row_data[column_number])
                        self.ui.wordTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        self.ui.wordTable.blockSignals(False)  # Prevent a bug where cell changes would occur on table loading
        self.ui.wordTable.itemChanged.connect(self.enableSave)
        self.ui.buttonBox_wordList.setEnabled(False)
        self.loadStudySet()

    def reloadWordTable(self):
        self.indexOfDeletedCardsSet.clear()
        self.indexOfModifiedCardsSet.clear()
        self.indexOfAddedCardsSet.clear()
        self.ui.wordTable.setSortingEnabled(False)
        self.ui.wordTable.setRowCount(0)
        self.ui.wordTable.clearContents()
        self.ui.wordTable.reset()
        self.ui.wordTable.blockSignals(True)  # Prevent a bug where cell changes would occur on table loading
        print("reverting changes")

        result = self.database.getTableData(self.nameOfCurrentDeck)

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
        self.ui.checkBox_shuffle.setEnabled(True)
        self.ui.checkBox_starredOnly.setEnabled(True)
        self.ui.buttonBox_wordList.setEnabled(False)

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
        addAction = contextMenuDeckView.addAction("Add Table")
        updateAction = contextMenuDeckView.addAction("Update Table")
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

        if self.ui.wordTable.rowCount() == 0:
            self.ui.wordTable.setRowCount(1)
            cell_widget = self.createStarCellWidget()
            self.ui.wordTable.setCellWidget(0, 1, cell_widget)
            self.indexOfAddedCardsSet.add(0)
            self.ui.wordTable.setCurrentCell(0,1)
        else:
            cell_widget = self.createStarCellWidget()
            self.ui.wordTable.insertRow(self.ui.wordTable.rowCount())
            self.ui.wordTable.setCellWidget(self.ui.wordTable.rowCount()-1, 1, cell_widget)
            self.indexOfAddedCardsSet.add(self.ui.wordTable.rowCount()-1)
            print("Inserting row..", self.ui.wordTable.rowCount()-1)

    def createStarCellWidget(self, checked=0):

        #print("Creating ⭐ cell widget")
        chk_bx = QCheckBox()
        chk_bx.setStyleSheet("QCheckBox::indicator { width: 32px; height: 32px}"
                             "QCheckBox::indicator:checked{image: url(../ico/starred.png)}"
                             "QCheckBox::indicator:unchecked{image: url(../ico/unstarred.png)}")
        if checked == 0:
            chk_bx.setCheckState(QtCore.Qt.CheckState.Unchecked)
        elif checked == 1:
            chk_bx.setCheckState(QtCore.Qt.CheckState.Checked)
        #lay_out = QHBoxLayout(chk_bx)
        #lay_out.addWidget(chk_bx)
        #lay_out.setAlignment(QtCore.Qt.AlignCenter)
        #lay_out.setContentsMargins(0,0,0,0)
        chk_bx.stateChanged.connect(self.updateStarredValue)
        return chk_bx

    def updateStarredValue(self):
        rowData = []
        rowIndex = self.ui.wordTable.currentRow()
        rowData.append(self.ui.wordTable.cellWidget(rowIndex, 1).isChecked())
        rowData.append(self.ui.wordTable.item(rowIndex, 0).text())
        print(rowData)
        self.database.setStarred(rowData)

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

    def openNewTableDialog(self):
        self.w = DeckNamePrompt(self)
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

    def loadStudySet(self, shuffle:bool=False):
        self.wordDeck.cardNum = 0

        result = self.database.getTableData(self.nameOfCurrentDeck)
        #db.setLastTimeStudied(self.nameOfCurrentTable)
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

    def loadStarredStudySet(self):
        pass

    def breakdownSummary(self):
        print(self.wordDeck.cardNum, len(self.wordDeck.studyList) - 1)


    def showPronunciationColumnAction(self):
        if self.ui.actionToggle_Pronunciation.isChecked():
            self.ui.wordTable.showColumn(4)
        else:
            self.ui.wordTable.hideColumn(4)

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
            result = self.database.getStarredTableData(self.nameOfCurrentDeck)
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
                self.loadDeckList()
                # self.ui.deckList.setCurrentRow(0)
                print("Loaded :", self.nameOfCurrentDeck)
                return True
            else:
                print("Cannot load an empty table!")
                return False

            self.ui.wordTable.blockSignals(False)       # Prevent a bug where cell changes would occur on table loading
            self.ui.buttonBox_wordList.setEnabled(False)
            self.loadStudySet()
        elif self.ui.checkBox_starredOnly.isChecked() == False:
            self.reloadWordTable()


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