from PySide2.QtWidgets import *
from py.setupUi.MainWindow import *
from py.callGenericDialog import *
from py.callImportDeck import *
from py.utilities.SQLTools import *
from py.VocabWord import *
DATABASE_PATH = '../data/vocab.db'
#Developer notes:
# TODO SEPARATE "BUILT IN TABLES" (NON MODIFYABLE) & "USER DEFINED TABLES" (MODIFYABLE)
# TODO 04) MANAGE BUILT IN DATA STRUCTURE TO STORE STUDY SET DATA
# TODO 06) ADD OPTION FOR SHUFFLE AND SWAP DEFINITION/PRONUNCIATION/VOCABULARY FOR Q/A
# TODO 07) CHECK IF THERES A BETTER WAY TO DISABLE TABS
# TODO 08) INDEX, DECKNAME, STARRED, VOCABULARY, DEFINITION, PRONUN(OPTIONAL), CORR#, ATT#
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.indexOfAddedRowsSet = set()        # Index of queued row numbers to be added from wordTable
        self.indexOfModifiedRowsSet = set()     # Index of queued row numbers to be modified from wordTable
        self.indexOfDeletedRowsSet = set()      # Index of queued row numbers to be deleted from wordTable
        self.indexOfCurrentTable = 0            # Index of current table in the deckList
        self.nameOfCurrentTable = ""            # Name of current table_name for the SQL TableName
        self.nameOfCurrentDeck = ""             # Name of current deck name as defined by the user
        self.studySet = []                      # List of VocabWord objects that the user has selected
        self.summaryIndexList = []              # List of indexes for studySet to save and break down statistics to user
        self.cardNum = 0                        # Iterator for the studySet
        self.ui = Ui_MainWindow()

        # # ADDED KEYPRESS EATER TAB BAR
        # self.ui.tabBar = QtWidgets.QTabBar()
        # self.ui.tabWidget.setTabBar(self.ui.tabBar)
        # eater = KeyPressEater(self.ui.tabBar)
        # self.ui.tabBar.installEventFilter(eater)

        self.ui.setupUi(self)

        self.ui.progressBar.reset()

        self.ui.pushButton_enter.clicked.connect(self.checkAnswer)
        self.ui.pushButton_notSure_Skip.clicked.connect(self.nextWord)
        self.ui.pushButton_notSure_Skip.hide()
        self.ui.lineEdit_answer.textEdited['QString'].connect(self.setTextEnter)
        self.ui.pushButton_wordList_select.clicked.connect(self.loadStudySet)
        self.ui.tab_flashcards.setEnabled(False)
        self.ui.tab_typing.setEnabled(False)
        self.ui.tab_quiz.setEnabled(False)

        self.ui.wordTable.installEventFilter(self)

        # Added - Prevent user from dragging list view objs
        self.ui.deckList.setDragEnabled(False)
        self.ui.deckList.clicked.connect(self.on_clicked)
        self.ui.deckList.customContextMenuRequested.connect(self.requestDeckViewContextMenu)
        # Added - Connect
        self.ui.pushButton_wordList_select.clicked.connect(self.on_clicked)        #Added - toolButton menu
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
        self.ui.wordTable.setHorizontalHeaderLabels(
            ['Index', 'Vocabulary', 'Definition', 'Pronunciation', 'Attempted', 'Correct', 'Starred'])
        self.ui.wordTable.setColumnHidden(0, True)
        self.ui.wordTable.setColumnWidth(1, 210)
        self.ui.wordTable.setColumnWidth(2, 210)
        self.ui.wordTable.setColumnWidth(3, 186)
        self.ui.wordTable.customContextMenuRequested.connect(self.requestWordTableContextMenu)
        #self.wordTable.itemSelectionChanged.connect(self.autoInsertTableRow)
        #self.wordTable.currentCellChanged.connect(self.autoInsertTableRow)
        # Added Modified - be careful
        self.ui.buttonBox_wordList.button(QtWidgets.QDialogButtonBox.Cancel).setText("Revert")
        self.ui.buttonBox_wordList.setCenterButtons(False)
        self.ui.buttonBox_wordList.setObjectName("buttonBox_wordList")
        # Added buttonBox_wordList bindings
        self.ui.buttonBox_wordList.accepted.connect(self.saveTable)
        self.ui.buttonBox_wordList.rejected.connect(self.revertTable)

        eater = KeyPressEater(self.ui.tabBar)
        self.ui.tabBar.installEventFilter(eater)
        self.ui.tabBar.tabBarClicked.connect(self.tab_changed)
        self.show()

    # TODO INSTALL EVENT FILTER TO DISABLE TAB SWITCHING WHILE STUDY SESSION IN PROG
    def tab_changed(self):
        #self.ui.tabBar.blockSignals(True)
        print("tab changed?")
        self.cardNum = 1
        if self.cardNum != 0:
            self.w = GenericDialog(self)
            self.w.show()
            print(self.w.allowTabChange)

    # TODO Im pretty sure there is a logic flaw here, should rethink this
    def enableSave(self):
        ''' This function will enable the buttonBox_wordList features to enable table modification'''
        self.ui.buttonBox_wordList.setEnabled(True)
        if self.ui.wordTable.currentRow() not in self.indexOfModifiedRowsSet:
            self.indexOfModifiedRowsSet.add(self.wordTable.currentRow())
        print("Modified index:", self.wordTable.currentRow())

    # TODO CHANGE LOGIC WHEN SQLTOOLS IS UPDATED
    def saveTable(self):
        print("save table")

        self.indexOfModifiedRowsSet = self.indexOfModifiedRowsSet - self.indexOfDeletedRowsSet
        self.indexOfModifiedRowsSet = self.indexOfModifiedRowsSet - self.indexOfAddedRowsSet
        print("modified rows:", self.indexOfModifiedRowsSet, "added rows", self.indexOfAddedRowsSet, "Del rows: ", self.indexOfDeletedRowsSet)

        if len(self.indexOfModifiedRowsSet) != 0:
            print("SENDING MODIFIED ENTRIES TO DATABASE")
            conn = sqlite3.connect(DATABASE_PATH)
            for i in self.indexOfModifiedRowsSet:
                rowData = []
                for j in range(0, self.ui.wordTable.columnCount()):
                    print(j, "Table data", self.wordTable.item(i, j).text())
                    rowData.append(self.ui.wordTable.item(i, j).text())

                print(rowData)

                if rowData[0] == "" or rowData[1] == "" or rowData[2] == "":
                    print("Empty critical slot found, refusing update into table")
                else:
                    self.checkUserTableEdit(rowData)
                    print("UPDATING TABLE DATA!", rowData)
                    print("Updating table at card Num:", i)

                    command = "UPDATE " + self.nameOfCurrentTable + " SET VOCABULARY=?, DEFINITION=?, PRONUNCIATION=?, " \
                                                                    "ATTEMPTED=?, CORRECT=?, STARRED=? " \
                                                                    " WHERE CARDNUM= " + str(rowData.pop(0))
                    print(command)
                    conn.execute(command, rowData)
                    conn.commit()
            conn.close()



        if len(self.indexOfAddedRowsSet) != 0:
            # Check if last row has valid data
            try:
                print(self.ui.wordTable.item(self.ui.wordTable.rowCount(), 1).text())
            except (AttributeError, ValueError):
                print("garbage data in last row")
                try:
                    self.indexOfAddedRowsSet.remove(self.ui.wordTable.rowCount() -1)
                except KeyError:
                    print("last row seems good")

            # Begin reading added rows
            conn = sqlite3.connect(DATABASE_PATH)
            print("SENDING INSERTED ROWS INTO DATABASE")
            for i in self.indexOfAddedRowsSet:
                rowData = []
                for j in range(1, self.ui.wordTable.columnCount()):
                    print(j, "Table data", self.wordTable.item(i, j).text())
                    rowData.append(self.ui.wordTable.item(i, j).text())

                print(i, j, rowData)
                if rowData[0] == '' or rowData[1] == '':
                    print("Empty critical slot found, refusing insert into table")
                else:
                    self.checkUserTableEdit(rowData)
                    print("INSERTING TABLE DATA!", rowData)
                    print("Updating table at card Num:", i + 1)  # cardnum is one ahead of actual index?

                    command = "INSERT INTO " + self.nameOfCurrentTable + " (VOCABULARY, DEFINITION, PRONUNCIATION," \
                                                                         "ATTEMPTED, CORRECT, STARRED) VALUES (?,?,?,?,?,?)"
                    print(command)
                    conn.execute(command, rowData)
                    conn.commit()
            conn.close()

        print(self.indexOfDeletedRowsSet)
        if len(self.indexOfDeletedRowsSet) != 0:
            conn = sqlite3.connect(DATABASE_PATH)
            # Now we must remove the rows user does not want anymore
            # Try to delete the item from the table by primary key
            for i in self.indexOfDeletedRowsSet:
                command = "DELETE FROM " + self.nameOfCurrentTable + " WHERE CARDNUM = " + i
                conn.execute(command)
                conn.commit()
            conn.close()

        self.indexOfAddedRowsSet.clear()
        self.indexOfModifiedRowsSet.clear()
        self.indexOfDeletedRowsSet.clear()
        self.ui.buttonBox_wordList.setEnabled(False)

    def refreshTableList(self):
        print("REFRESHING TABLE LIST")
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(DATABASE_PATH)
        db.open()

        vocabTableList = db.tables()
        if vocabTableList == 0:
            print("Empty table.. Creating a starting point..")

        print(vocabTableList)
        listWidget = self.ui.deckList
        listWidget.clear()
        for i in vocabTableList:
            if i != 'sqlite_sequence':
                listWidget.addItem(i)

        listWidget.show()
        db.close()

    def revertTable(self):
        self.ui.wordTable.setSortingEnabled(False)
        print("reverting changes")
        self.ui.wordTable.setRowCount(0)
        self.ui.wordTable.clearContents()
        self.ui.wordTable.reset()
        self.ui.wordTable.blockSignals(True)  # Prevent a bug where cell changes would occur on table loading
        conn = sqlite3.connect(DATABASE_PATH)
        result = conn.execute('SELECT * FROM {}'.format(self.nameOfCurrentTable))
        for row_number, row_data in enumerate(result):
            print("Row number: ", row_number)
            self.ui.wordTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                print("Row data: ", row_data[column_number])
                if column_number == 0:
                    self.ui.wordTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                else:
                    self.ui.wordTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        conn.close()
        self.ui.wordTable.blockSignals(False)  # Prevent a bug where cell changes would occur on table loading
        self.ui.buttonBox_wordList.setEnabled(False)

    # TODO FINISH QTABLEWIDGET LOGIC WILL NEED SOME REVISIONS TO PRIOR SQL QUERIES
    # BECAUSE CARD NUMBERS ARE UNACCOUNT FOR DURING THESE TYPES OF INSERTS
    # IF WE HAVE A DATA STRUCTURE TO WORK WITH ON EVERY DECK LOAD, WE CAN FIND
    # THE CORRECT CARD NUM

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
        self.on_clicked(self.ui.deckList.currentIndex())
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
        # UNLESS, AUTOINCREMENT gives us a primary key automagically, we'll see
        self.ui.wordTable.insertRow(self.ui.wordTable.rowCount())
        # We can assume that since we add it to the end, the index of the inserted row will be at the end
        self.indexOfAddedRowsSet.add(self.ui.wordTable.rowCount()-1)
        print("Inserting row..", self.ui.wordTable.rowCount()-1)
        for i in range (0, 7):
            newItem = QtWidgets.QTableWidgetItem()
            self.ui.wordTable.setItem(self.ui.wordTable.rowCount()-1, i, newItem)
            if i > 3:
                newItem.setText("0")
            print(newItem.text())

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
        self.w = ImportDeck(self)
        self.w.show()

    @QtCore.Slot(QtCore.QModelIndex)
    def on_clicked(self, index):
        if index == self.indexOfCurrentTable or index == False:  # I guess sometimes its false :S
            print("nothing to do")
        else:
            self.indexOfDeletedRowsSet.clear()
            self.indexOfModifiedRowsSet.clear()
            self.indexOfAddedRowsSet.clear()


            self.ui.wordTable.setSortingEnabled(False)
            self.indexOfCurrentTable = index
            self.nameOfCurrentTable = index.data()
            self.ui.wordTable.setRowCount(0)
            self.ui.wordTable.clearContents()
            self.ui.wordTable.reset()

            self.ui.wordTable.blockSignals(True)  # Prevent a bug where cell changes would occur on table loading
            self.ui.label_deckName.setText("Selected Deck: {}".format(index.data()))
            conn = sqlite3.connect(DATABASE_PATH)
            result = conn.execute('SELECT * FROM {}'.format(index.data()))
            for row_number, row_data in enumerate(result):
                self.ui.wordTable.insertRow(row_number)
                print("Row number: ", row_number)
                for column_number, data in enumerate(row_data):
                    print("Row data: ", row_data[column_number])
                    if column_number == 0:
                        self.ui.wordTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                    else:
                        self.ui.wordTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
            conn.close()
            self.ui.wordTable.blockSignals(False)  # Prevent a bug where cell changes would occur on table loading
        self.ui.wordTable.itemChanged.connect(self.enableSave)
        self.ui.buttonBox_wordList.setEnabled(False)
    def checkUserTableEdit(self, row):
        '''This function will check the data types of a list to make sure 0, 4, 5, 6 are integers'''
        # THIS LOGIC IS FLAWED UNLESS YOU CHECK FOR A LEN6 AND LEN7 LIST
        # TODO CHANGE LOGIC HERE PROBABLY

        try:
            row[0] = int(row[0])
        except ValueError:
            print("FATAL ERROR, PRIMARY KEY HAS BEEN EDITED!")
            return False
        if row[6] != 0 and row[6] != 1:
            print("Resetting isStarred to 0")
            row[6] = 0
        indexesToConvert = [4, 5, 6]
        for i in indexesToConvert:
            try:
                row[i] = int(row[i])
            except ValueError:
                print("VALUE ERROR: INTEGER FIELDS CANNOT CONTAIN A CHARACTER! RESETTING STATISTICS TO DEFAULT VALUES")
                row[4] = 0
                row[5] = 0
                # row[i] = 0

    def eventFilter(self, source, event):
        #print("entered event filter ")
        #print(event.type())
        # If tab press signaled in wordTable widget
        if (event.type() == QtCore.QEvent.KeyRelease and source == self.ui.wordTable):
            if event.key() == QtCore.Qt.Key_Tab:
                #print(self.ui.wordTable.currentIndex().row(), self.wordTable.currentIndex().column(), "/", bself.wordTable.rowCount(), self.wordTable.columnCount()

                if self.ui.wordTable.currentColumn() == 4:
                    if self.ui.wordTable.currentIndex().row() == self.ui.wordTable.rowCount() - 1:
                        self.ui.insertTableRow()
                    self.ui.wordTable.setCurrentCell(self.ui.wordTable.currentRow() +1, 1)
                    self.ui.wordTable.editItem(self.ui.wordTable.currentItem())


            elif event.key() == QtCore.Qt.Key_Backtab:
                if self.ui.wordTable.currentColumn() == 6:
                    self.ui.wordTable.setCurrentCell(self.ui.wordTable.currentRow(), 3)
                    self.ui.wordTable.editItem(self.ui.wordTable.currentItem())

            return False
        return super(MainWindow, self).eventFilter(source, event)

    def calcPercentageCorrect(self):
        return (self.studySet[self.cardNum].timesCorrect/self.studySet[self.cardNum].timesAttempted) * 100

    def setTextEnter(self):
        win.ui.pushButton_enter.setText("Enter")

    def loadStudySet(self):
        db = sqlite3.connect(DATABASE_PATH)
        c = db.execute('SELECT * FROM {}'.format(win.ui.nameOfCurrentTable))
        result = c.fetchall()

        #We have a tuple, now lets make a list of VocabWord objects

        db.close()
        self.studySet = [VocabWord(*t) for t in result]

        for i in range(10, len(self.studySet),10):
            self.summaryIndexList.append(i)
            #print(i)

        print(self.studySet)
        win.ui.progressBar.reset()
        win.ui.progressBar.setRange(0, len(self.studySet)+1)
        win.ui.label_typingWord.setText(self.studySet[self.cardNum].vocabulary)
        self.ui.tab_flashcards.setEnabled(True)
        self.ui.tab_typing.setEnabled(True)
        self.ui.tab_quiz.setEnabled(True)
        self.ui.wordTable.itemChanged.connect(win.enableSave)

    def checkAnswer(self):
        textValue = win.ui.lineEdit_answer.text()
        answerList = self.studySet[self.cardNum].definition.split(";")
        print("You entered: " + textValue + " $? " + ", ".join(answerList))
        print(self.studySet[self.cardNum])

        if textValue in answerList:
            print("Correct!")
            win.ui.lineEdit_answer.clear()

            self.studySet[self.cardNum].timesCorrect += 1
            self.studySet[self.cardNum].timesAttempted += 1

            percent = self.calcPercentageCorrect()
            win.ui.label_fractionCorrect.setText("%" + str(percent))

            win.ui.label_typingWord.setText("Correct!\n " + ",".join(answerList))
            win.ui.pushButton_enter.setText("Continue")
            win.ui.lineEdit_answer.setPlaceholderText("Press Enter to continue")
            win.ui.lineEdit_answer.setDisabled(True)
            win.ui.pushButton_enter.clicked.disconnect()
            win.ui.pushButton_enter.clicked.connect(self.nextWord)
        else:
            self.studySet[self.cardNum].timesAttempted += 1
            percent = self.calcPercentageCorrect()
            self.ui.label_fractionCorrect.setText("%" + str(percent))
            print("Incorrect!")
            print("Card number: " + str(self.cardNum))
            win.ui.pushButton_enter.setText("Enter")
            win.ui.pushButton_notSure_Skip.show()
            win.ui.lineEdit_answer.clear()
            win.ui.label_typingWord.setText("Oops! Correct answer is: \n" + self.studySet[self.cardNum].definition)
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
        elif self.cardNum in self.summaryIndexList:
            print("fuq")
        else:
            self.cardNum += 1
            win.ui.lineEdit_answer.setEnabled(True)
            win.ui.pushButton_notSure_Skip.hide()
            win.ui.lineEdit_answer.setFocus()
            win.ui.lineEdit_answer.clear()
            win.ui.lineEdit_answer.setPlaceholderText("Enter your answer")
            win.ui.pushButton_enter.setText("Don't Know")
            win.ui.label_typingWord.setText(self.studySet[self.cardNum].vocabulary)
            win.ui.pushButton_enter.clicked.disconnect()
            win.ui.pushButton_enter.clicked.connect(self.checkAnswer)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    db = QSqlDatabase.addDatabase("QSQLITE", connectionName="prim_conn")
    db.setDatabaseName(DATABASE_PATH)
    db.open()

    # Generate list of tables for listWidget
    # Add to SQLTools so we have a local db and cur object to call from main without making a mess in main
    # Call this function to update the list of decks
    vocabTableList = db.tables()
    if vocabTableList == 0:
        print("Empty table.. Creating a starting point..")

    print(vocabTableList)
    listWidget = win.ui.deckList
    for i in vocabTableList:
        if i != 'sqlite_sequence':
            listWidget.addItem(i)

    listWidget.show()
    db.close()

    win.ui.nameOfCurrentTable = listWidget.item(0).data(0)
    print(win.ui.nameOfCurrentTable)
    dbname = win.ui.nameOfCurrentTable
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.execute('SELECT * FROM {}'.format(dbname))
    result = c.fetchall()
    conn.close()
    print(result)

    sys.exit(app.exec_())