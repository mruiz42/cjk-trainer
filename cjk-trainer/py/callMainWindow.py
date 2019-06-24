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
from PySide2 import QtGui

from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl
from PySide2 import QtQml
# ADDED KEYPRESS EATER TAB BAR
# self.tabBar = QtWidgets.QTabBar()
# self.tabWidget.setTabBar(self.tabBar)
#Developer notes:
# TODO 04) MANAGE BUILT IN DATA STRUCTURE TO STORE STUDY SET DATA
# TODO 06) ADD OPTION FOR SHUFFLE AND SWAP DEFINITION/PRONUNCIATION/VOCABULARY FOR Q/A
# TODO 07) CHECK IF THERES A BETTER WAY TO DISABLE TABS
# TODO 08) INDEX, DECKNAME, STARRED, VOCABULARY, DEFINITION, PRONUN(OPTIONAL), CORR#, ATT#
# TODO 09) AUTO LOAD THE MOST RECENTLY STUDIED DECK.
# TODO 10) NORMALIZE FONTS ACROSS UI WIDGETS
# TODO 11) ADD EXPORT TO CSV FUNCTION
# TODO 12) ADD STAR THIS WORD CONTEXT MENU
# TODO 13) ADD ABILITY TO RESET STATS
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





        self.ui.tab_flashcards.setEnabled(False)
        self.ui.tab_typing.setEnabled(False)
        self.ui.tab_quiz.setEnabled(False)
        self.n = StarDelegate(self.ui.tableView)
        self.ui.deckList.itemSelectionChanged.connect(lambda: self.deckListClicked(self.ui.deckList.currentIndex()))
        self.ui.pushButton_wordList_select.clicked.connect(self.deckListClicked)
        self.ui.lineEdit_searchQuery.textChanged.connect(lambda: self.loadWordTable(starredOnly=self.ui.checkBox_starredOnly.isChecked()))


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

        self.ui.tableView.customContextMenuRequested.connect(self.requestWordTableContextMenu)
        # Added Modified - be careful
        self.ui.buttonBox_wordList.button(QtWidgets.QDialogButtonBox.Cancel).setText("Revert")
        self.ui.buttonBox_wordList.setCenterButtons(False)
        self.ui.buttonBox_wordList.setObjectName("buttonBox_wordList")
        # Added buttonBox_wordList bindings
        self.ui.buttonBox_wordList.accepted.connect(self.saveTable)
        self.ui.buttonBox_wordList.rejected.connect(self.revertWordTable)
        # Install tabBar Scroll event filter
        eater = KeyPressEater(self, self.ui.tabBar)
        self.ui.tabBar.installEventFilter(eater)
        self.ui.checkBox_starredOnly.stateChanged.connect(self.starredButtonAction)
        self.ui.pushButton_shuffleDeck.clicked.connect(self.shuffleButtonAction)
        self.ui.actionToggle_Pronunciation.changed.connect(self.showPronunciationColumnAction)

        self.loadDeckList()
        self.show()

    def shuffleButtonAction(self):
        starredState = self.ui.checkBox_starredOnly.checkState()
        #self.wordDeck.shuffleStudySet()
        self.loadWordTable(shuffle=True, starredOnly=starredState)
        self.reloadWordLabels()

    def enableSave(self):
        ''' This function will enable the buttonBox_wordList features to enable table modification'''
        self.ui.buttonBox_wordList.setEnabled(True)
        self.ui.tableView.setSortingEnabled(False)

    def saveTable(self):
        success = self.model.submitAll()
        if success:
            print("Table has been successfully updated!")
        else:
            print("Error updating table!")
            print(self.model.lastError().databaseText())
            print(self.model.lastError().text())
        self.ui.buttonBox_wordList.setDisabled(True)
        self.ui.tableView.setSortingEnabled(True)

    def deckListClicked(self, index:QtCore.QModelIndex):
        print(self.deckListIndex, index.row())
        self.ui.lineEdit_searchQuery.clear()
        if index.row() == self.deckListIndex:
            print("Nothing to do")
        else:
            self.ui.checkBox_starredOnly.setChecked(False)
            self.deckListIndex = index.row()
            self.nameOfCurrentDeck = index.data()
            self.loadWordTable()
            self.ui.label_selectedDeck.setText(index.data())
            self.ui.tableView.setColumnWidth(2, 30)
            self.ui.tableView.setColumnWidth(3, 200)
            self.ui.tableView.setColumnWidth(4, 200)
            self.ui.tableView.setColumnWidth(5, 200)
            self.ui.buttonBox_wordList.setDisabled(True)
            self.ui.tableView.setSortingEnabled(True)

    def loadWordTable(self, shuffle:bool=False, starredOnly:bool=False):
        query = self.ui.lineEdit_searchQuery.text()
        deckName = self.ui.deckList.currentItem().text()
        self.model.setTable("CARDS")
        command = ("DECK_ID=\"{}\""
                 " AND (DEFINITION LIKE \"%{}%\""
                 " OR VOCABULARY LIKE \"%{}%\""
                 " OR PRONUNCIATION LIKE \"%{}%\")").format(deckName, query, query, query)
        if starredOnly:
            command += "AND IS_STARRED=TRUE"
        if shuffle:
            command += " ORDER BY RANDOM()"
            self.ui.tableView.setSortingEnabled(False)

        self.model.setFilter(command)
        self.ui.tableView.hideColumn(0)
        self.ui.tableView.hideColumn(1)
        print(self.model.selectStatement())
        self.model.select()
        self.model.setHeaderData(2, Qt.Horizontal, "⭐")
        if self.model.rowCount() > 0:
            self.ui.tableView.setItemDelegateForColumn(2, self.n)
            while self.model.canFetchMore():
                self.model.fetchMore()
                print(self.model.rowCount())
            self.ui.tableView.setModel(self.model)

            self.ui.tableView.hideColumn(0)
            self.ui.tableView.hideColumn(1)
            # load study deck
            deck = []
            for row in range(0, self.model.rowCount()):
                cn = (self.model.data(self.model.index(row, 0)))
                star = (self.model.data(self.model.index(row, 2)))
                vocab = (self.model.data(self.model.index(row, 3)))
                defin = (self.model.data(self.model.index(row, 4)))
                pronun = (self.model.data(self.model.index(row, 5)))
                card = VocabWord(cn, star, vocab, defin, pronun)
                deck.append(card)
            self.loadStudySet(deck)
            self.typingExercise.resetUi()
            self.quizExercise.resetUi()
            self.flashcardExercise.resetUi()

    def revertWordTable(self):
        self.model.revertAll()
        self.ui.buttonBox_wordList.setDisabled(True)
        print(self.model.lastError().databaseText())
        print(self.model.lastError().text())

    ########### CONTEXT MENU STUFF ###############
    def requestWordTableContextMenu(self, position):
        contextMenu = QtWidgets.QMenu("contextMenu")
        insertAction = contextMenu.addAction("Insert Row")
        updateAction = contextMenu.addAction("Update Row")
        deleteAction = contextMenu.addAction("Delete Row")
        action = contextMenu.exec_(self.ui.tableView.mapToGlobal(position))
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
        record = self.model.record()
        field0 = QSqlField("CARD_ID")
        field1 = QSqlField("DECK_ID")
        field2 = QSqlField("IS_STARRED")
        field3 = QSqlField("VOCABULARY")
        field4 = QSqlField("DEFINITION")
        field5 = QSqlField("PRONUNCIATION")
        field6 = QSqlField("IMAGE_DATA")
        field1.setValue(self.nameOfCurrentDeck)
        record.insert(0, field0)
        record.insert(1, field1)
        record.insert(2, field2)
        record.insert(3, field3)
        record.insert(4, field4)
        record.insert(5, field5)
        record.insert(6, field6)




        self.model.insertRecord(self.model.rowCount(), record)
        print(record.count())

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
        # if (event.type() == QtCore.QEvent.KeyRelease and source == self.ui.wordTable):
        #     if event.key() == QtCore.Qt.Key_Tab:
        #         #print(self.ui.wordTable.currentIndex().row(), self.wordTable.currentIndex().column(), "/", bself.wordTable.rowCount(), self.wordTable.columnCount()
        #
        #         if self.ui.wordTable.currentColumn() == 5:
        #             if self.ui.wordTable.currentIndex().row() == self.ui.wordTable.rowCount() - 1:
        #                 self.insertTableRow()
        #             self.ui.wordTable.setCurrentCell(self.ui.wordTable.currentRow() +1, 2)
        #             self.ui.wordTable.editItem(self.ui.wordTable.currentItem())
        #
        #
        #     elif event.key() == QtCore.Qt.Key_Backtab:
        #         if self.ui.wordTable.currentColumn() == 1:
        #             self.ui.wordTable.setCurrentCell(self.ui.wordTable.currentRow() - 1, 4)
        #             self.ui.wordTable.editItem(self.ui.wordTable.currentItem())
        #     return False
        # return super(MainWindow, self).eventFilter(source, event)
        pass

    def resetProgressBars(self):
        win.ui.progressBar_typing.reset()
        win.ui.progressBar_typing.setRange(0, len(self.wordDeck.studyList))
        win.ui.progressBar_flashcards.reset()
        win.ui.progressBar_flashcards.setRange(0, len(self.wordDeck.studyList))
        win.ui.progressBar_quiz.reset()
        win.ui.progressBar_quiz.setRange(0, len(self.wordDeck.studyList))

    def loadStudySet(self, result:list):
        self.wordDeck.cardNum = 0

        if len(result) != 0:
            # self.wordDeck.studyList = [VocabWord(*t) for t in result]
            #self.wordDeck.shuffleStudySet()
            self.wordDeck.setStudyList(result)
            for i in range(10, len(self.wordDeck.studyList), 10):
                self.wordDeck.summaryIndexList.append(i)
            self.resetProgressBars()
            self.reloadWordLabels()
            self.ui.tab_flashcards.setEnabled(True)
            self.ui.tab_typing.setEnabled(True)
            self.ui.tab_quiz.setEnabled(True)
            #self.reloadTableList(reset_checked=True)
            #self.loadDeckList()
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
        self.loadWordTable(shuffle=False, starredOnly=starredState)
        self.reloadWordLabels()

    def loadDeckList(self):
        self.ui.deckList.clear()
        listOfDecks = self.database.getDecks()
        for i in listOfDecks:
            # if i != 'sqlite_sequence':
            self.ui.deckList.addItem(i[0])

def setDarkStyleSheet(qApp:QApplication):
    qApp.setStyle(QStyleFactory.create("Fusion"))
    darkPalette = QtGui.QPalette()
    darkPalette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    darkPalette.setColor(QtGui.QPalette.WindowText, Qt.white)
    darkPalette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
    darkPalette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
    darkPalette.setColor(QtGui.QPalette.ToolTipBase, Qt.white)
    darkPalette.setColor(QtGui.QPalette.ToolTipText, Qt.white)
    darkPalette.setColor(QtGui.QPalette.Text, Qt.white)
    darkPalette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    darkPalette.setColor(QtGui.QPalette.ButtonText, Qt.white)
    darkPalette.setColor(QtGui.QPalette.BrightText, Qt.red)
    darkPalette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
    darkPalette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
    darkPalette.setColor(QtGui.QPalette.HighlightedText, Qt.black)
    qApp.setPalette(darkPalette)
    qApp.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    setDarkStyleSheet(app)

    # view = QQuickView()
    # url = QUrl("../ui/view.qml")
    # view.setSource(url)
    # view.show()
    win = MainWindow()
    #win.show()
    #win.loadDeckList()
    view = QQuickView()

    view.setSource(QUrl("../ui/view.qml"))

    view.setMinimumHeight(430)
    view.setMinimumWidth(800)
    # win.ui.horizontalLayout_2.addWidget(QWidget.createWindowContainer(view, win))
    view.show()


    #win.reloadTableList()
    # win.nameOfCurrentTable = win.ui.deckList.item(0).data(0)
    # print(win.nameOfCurrentTable)
    # win.loadWordTable(0)



    #win.database.closeDatabase()
    sys.exit(app.exec_())