# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/MainWindow.ui',
# licensing of './ui/MainWindow.ui' applies.
#
# Created: Sat Mar 30 01:38:09 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!


from py.utilities.KeyPressEater import KeyPressEater
from PySide2 import QtCore, QtGui, QtWidgets
from py.callImportDeck import *
import sqlite3
from PySide2 import QtCore, QtGui, QtWidgets

#TODO CHECK IF THE USER IS INPUTTING BLANK TABLE FIELDS
#TODO CAN USE SETCELLWIDGET TO INCLUDE A CHECKBOX FOR STARRED -- CUSTOM ICON?
class Ui_MainWindow(object):


    def __init__(self):
        self.indexOfAddedRowsSet = set()
        self.indexOfModifiedRowsSet = set()
        self.indexOfDeletedRowsSet = set()
        self.indexOfCurrentTable = 0
        self.nameOfCurrentTable = ""

    # def getListSelection(self):
    #     model = self.deckList.model()
    #     string = model.index(0)
    #     print(string.toString)

    def tab_changed(self):
        print("tab changed?")
        pass


    # TODO Im pretty sure there is a logic flaw here, should rethink this
    def enableSave(self):
        ''' This function will enable the buttonBox_wordList features to enable table modification'''
        self.buttonBox_wordList.setEnabled(True)
        # if self.wordTable.row(self.wordTable.selectedItems()[0]) not in self.indexOfModifiedRowsList:
        #     self.indexOfModifiedRowsList.append(self.wordTable.row(self.wordTable.selectedItems()[0]))
        if self.wordTable.currentRow() not in self.indexOfModifiedRowsSet:
            self.indexOfModifiedRowsSet.add(self.wordTable.currentRow())
        print("Modified index:", self.wordTable.currentRow())

    def saveTable(self):
        print("save table")



        # # chekc for empty fields before input
        # newModifyIndices = set()
        # for i in self.indexOfModifiedRowsSet:
        #     print(i, "in", self.indexOfModifiedRowsSet)
        #     try:
        #         for j in range(0, self.wordTable.columnCount()):
        #             print(j, " Table data '", self.wordTable.item(i, j).text(), "'", sep='')
        #
        #         newModifyIndices.add(i)
        #
        #     except (AttributeError, ValueError):
        #         print("ValueError: removing index: ", i, " from edit queue")
        #
        # self.indexOfModifiedRowsSet = newModifyIndices




        print("SENDING MODIFIED ENTRIES TO DATABASE")
        conn = sqlite3.connect('../data/vocab.db')
        for i in self.indexOfModifiedRowsSet:
            rowData = []
            for j in range(0, self.wordTable.columnCount()):
                print(j, "Table data", self.wordTable.item(i, j).text())
                rowData.append(self.wordTable.item(i, j).text())

        if rowData[0] or rowData[1] or rowData[2] == "":
            print(rowData)
            print("Empty critical slot found, refusing insert into table") ### WTF? it shouldnt hit this condition tho

        else:
            self.checkUserTableEdit(rowData)
            print("UPDATING TABLE DATA!", rowData)
            print("Updating table at card Num:", i + 1)  # cardnum is one ahead of actual index?

            command = "UPDATE " + self.nameOfCurrentTable + " SET VOCABULARY=?, DEFINITION=?, PRONUNCIATION=?, " \
                                                            "ATTEMPTED=?, CORRECT=?, STARRED=? " \
                                                            " WHERE CARDNUM= " + str(rowData.pop(0))
            print(command)
            conn.execute(command, rowData)
            conn.commit()
        conn.close()

        # Check if last row has valid data
        try:
            print(self.wordTable.item(self.wordTable.rowCount(), 1).text())
        except (AttributeError, ValueError):
            print("garbage data in last row")
            try:
                self.indexOfAddedRowsSet.remove(self.wordTable.rowCount())
            except KeyError:
                print("last row seems good")

        conn = sqlite3.connect('../data/vocab.db')
        for i in self.indexOfAddedRowsSet:
            print("SENDING INSERTED TABLES INTO DATABASE")
            rowData = []
            print(i)
            for j in range(0, self.wordTable.columnCount()):
                print(j, "Table data", self.wordTable.item(i, j).text())
                rowData.append(self.wordTable.item(i, j).text())

            print(rowData)
            if rowData[1] or rowData[2] == '':
                continue
                print("Empty critical slot found, refusing insert into table")
            else:
                self.checkUserTableEdit(rowData)
                print("INSERTING TABLE DATA!", rowData)
                print("Updating table at card Num:", i + 1)  # cardnum is one ahead of actual index?

                command = "INSERT INTO " + self.nameOfCurrentTable + " (VOCABULARY, DEFINITION, PRONUNCIATION" \
                                                                     "ATTEMPTED, CORRECT, STARRED) VALUES (?,?,?,?,?,?)"
                print(command)
                conn.execute(command, rowData)
                conn.commit()
        conn.close()

        self.indexOfAddedRowsSet.clear()
        self.indexOfModifiedRowsSet.clear()
        self.buttonBox_wordList.setEnabled(False)



    def revertTable(self):
        self.wordTable.setSortingEnabled(False)
        print("reverting changes")
        self.wordTable.setRowCount(0)
        self.wordTable.clearContents()
        self.wordTable.reset()
        self.wordTable.blockSignals(True)  # Prevent a bug where cell changes would occur on table loading
        conn = sqlite3.connect('../data/vocab.db')
        result = conn.execute('SELECT * FROM {}'.format(self.nameOfCurrentTable))
        for row_number, row_data in enumerate(result):
            print("Row number: ", row_number)
            self.wordTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                print("Row data: ", row_data[column_number])
                if column_number == 0:
                    self.wordTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                else:
                    self.wordTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        conn.close()
        self.wordTable.blockSignals(False)  # Prevent a bug where cell changes would occur on table loading
        self.buttonBox_wordList.setEnabled(False)
    # TODO FINISH QTABLEWIDGET LOGIC WILL NEED SOME REVISIONS TO PRIOR SQL QUERIES
    # BECAUSE CARD NUMBERS ARE UNACCOUNT FOR DURING THESE TYPES OF INSERTS
    # IF WE HAVE A DATA STRUCTURE TO WORK WITH ON EVERY DECK LOAD, WE CAN FIND
    # THE CORRECT CARD NUM
    def requestWordTableContextMenu(self, position):
        print("CUSTOME MENU REQ")
        contextMenu = QtWidgets.QMenu("contextMenu")
        insertAction = contextMenu.addAction("Insert Row")
        updateAction = contextMenu.addAction("Update Row")
        deleteAction = contextMenu.addAction("Delete Row")
        action = contextMenu.exec_(self.wordTable.mapToGlobal(position))
        if action == insertAction:
            self.insertTableRow()
        elif action == updateAction:
            self.updateTableRow()
        elif action == deleteAction:
            self.deleteTableRow()

    def requestDeckViewContextMenu(self, position):
        print("CUSTOME MENU REQ")
        self.on_clicked(self.deckList.currentIndex())
        contextMenuDeckView = QtWidgets.QMenu("contextMenu")
        addAction = contextMenuDeckView.addAction("Add Table")
        deleteAction = contextMenuDeckView.addAction("Delete Table")
        action = contextMenuDeckView.exec_(self.deckList.mapToGlobal(position))
        if action == addAction:
            print("Creating a new deck..")
            self.addNewTable()
        elif action == deleteAction:
            print("Deleting selected deck..")
            print("Are you sure you want to do this?")
            self.dropTable()

    def insertTableRow(self):
        # To complete, this must be able to GUESS which is the correct cardNum
        # UNLESS, AUTOINCREMENT gives us a primary key automagically, we'll see
        self.wordTable.insertRow(self.wordTable.rowCount())
        # We can assume that since we add it to the end, the index of the inserted row will be at the end
        self.indexOfAddedRowsSet.add(self.wordTable.rowCount())
        print("Inserting row..", self.wordTable.rowCount())
        for i in range (0, 7):
            newItem = QtWidgets.QTableWidgetItem()
            self.wordTable.setItem(self.wordTable.rowCount() - 1, i, newItem)
            if i > 3:
                newItem.setText("0")
            print(newItem.text())




    def autoInsertTableRow(self):
        #TODO USING TAB SHIFT TO GO BACKWARDS MAKES YOU GO EDIT THE 3 NUMERICAAL FIELDS.
        # MAYBE DISABLE THESE 3 DURING EDITING??
        '''This function will insert a new row when the user switches off of the last tab'''
        print(self.wordTable.currentIndex().row(), self.wordTable.currentIndex().column(), "/", self.wordTable.rowCount(), self.wordTable.columnCount())

        # Check if we are on the pronun col, if so, hop to the next row
        if self.wordTable.currentIndex().column() == 3:
            print ("Last column")
            # However, if the next row doesn't exist, we must first create it
            if self.wordTable.currentIndex().row() == self.wordTable.rowCount() - 1:
                self.insertTableRow()
            self.wordTable.setCurrentCell(self.wordTable.currentRow() + 1, 0)

            #self.wordTable.editItem(self.wordTable.currentItem())

        #fix going backwards bug
        #TODO unexpected behavior here~~~~
        # need a way to send us back to the first or third column, but this has an intermediary step (at isstarred)

        # elif self.wordTable.currentIndex().column() == 6:
        #     print(self.wordTable.currentIndex().column())
        #     self.wordTable.setCurrentCell(self.wordTable.currentRow(), 2)
        #     self.wordTable.selectColumn(self.wordTable.currentRow())


    def updateTableRow(self):
        print("Updating row..")

    def deleteTableRow(self):
        print("Deleting row..")
        self.wordTable.removeRow(self.wordTable.currentRow())
        self.buttonBox_wordList.setEnabled(True)
    def addNewTable(self):
        print("adding new table")
    def dropTable(self):
        print("Deleting table..")

    def openImportCSVDialogue(self):
        print("open impirt csv dialge")
        self.w = ImportDeck()
        self.w.show()


    @QtCore.Slot(QtCore.QModelIndex)
    def on_clicked(self, index):
        if index == self.indexOfCurrentTable or index == False:  # I guess sometimes its false :S
            print("nothing to do")
        else:
            self.wordTable.setSortingEnabled(False)
            self.indexOfCurrentTable = index
            self.nameOfCurrentTable = index.data()
            self.wordTable.setRowCount(0)
            self.wordTable.clearContents()
            self.wordTable.reset()

            self.wordTable.blockSignals(True)  # Prevent a bug where cell changes would occur on table loading
            self.label_deckName.setText("Selected Deck: {}".format(index.data()))
            conn = sqlite3.connect('../data/vocab.db')
            result = conn.execute('SELECT * FROM {}'.format(index.data()))
            for row_number, row_data in enumerate(result):
                self.wordTable.insertRow(row_number)
                print("Row number: ", row_number)
                for column_number, data in enumerate(row_data):
                    print("Row data: ", row_data[column_number])
                    if column_number == 0:
                        self.wordTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                    else:
                        self.wordTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
            conn.close()
            self.wordTable.blockSignals(False)  # Prevent a bug where cell changes would occur on table loading
        self.wordTable.itemChanged.connect(self.enableSave)
        self.buttonBox_wordList.setEnabled(False)



    def checkUserTableEdit(self, row):
        '''This function will check the data types of a list to make sure 0, 4, 5, 6 are integers'''
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

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 720)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(960, 720))
        icon = QtGui.QIcon()
        # Added path
        icon.addPixmap(QtGui.QPixmap("../ico/appicon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(600, 400))
        self.centralwidget.setMaximumSize(QtCore.QSize(960, 720))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())


        # ADDED KEYPRESS EATER TAB BAR
        self.tabBar = QtWidgets.QTabBar()
        self.tabWidget.setTabBar(self.tabBar)
        eater = KeyPressEater(self.tabBar)
        self.tabBar.installEventFilter(eater)



        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.tabWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget.setIconSize(QtCore.QSize(16, 16))
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_wordTable = QtWidgets.QWidget()
        self.tab_wordTable.setObjectName("tab_wordTable")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tab_wordTable)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem)
        self.label_deckList = QtWidgets.QLabel(self.tab_wordTable)
        self.label_deckList.setAlignment(QtCore.Qt.AlignCenter)
        self.label_deckList.setObjectName("label_deckList")
        self.horizontalLayout_12.addWidget(self.label_deckList)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem1)
        self.verticalLayout_5.addLayout(self.horizontalLayout_12)
        self.deckList = QtWidgets.QListWidget(self.tab_wordTable)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deckList.sizePolicy().hasHeightForWidth())
        self.deckList.setSizePolicy(sizePolicy)
        self.deckList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.deckList.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.deckList.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.deckList.setAlternatingRowColors(True)
        self.deckList.setMovement(QtWidgets.QListView.Free)
        self.deckList.setResizeMode(QtWidgets.QListView.Adjust)
        self.deckList.setObjectName("deckList")

        # Added - Prevent user from dragging list view objs
        self.deckList.setDragEnabled(False)
        self.deckList.clicked.connect(self.on_clicked)
        self.deckList.customContextMenuRequested.connect(self.requestDeckViewContextMenu)


        self.verticalLayout_5.addWidget(self.deckList)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_wordList_select = QtWidgets.QPushButton(self.tab_wordTable)
        self.pushButton_wordList_select.setObjectName("pushButton_wordList_select")


        # Added - Connect
        self.pushButton_wordList_select.clicked.connect(self.on_clicked)


        self.gridLayout.addWidget(self.pushButton_wordList_select, 0, 1, 1, 1)
        self.toolButton_add = QtWidgets.QToolButton(self.tab_wordTable)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_add.sizePolicy().hasHeightForWidth())
        self.toolButton_add.setSizePolicy(sizePolicy)
        self.toolButton_add.setCheckable(False)
        self.toolButton_add.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        self.toolButton_add.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolButton_add.setArrowType(QtCore.Qt.NoArrow)
        self.toolButton_add.setObjectName("toolButton_add")

        #Added - toolButton menu
        self.toolButton_add.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        addMenu = QtWidgets.QMenu("addMenu", self.toolButton_add)
        newListTableAction = addMenu.addAction("Add new deck")
        importCSVAction = addMenu.addAction("Import CSV")
        self.toolButton_add.setMenu(addMenu)
        self.toolButton_add.clicked.connect(self.addNewTable)
        newListTableAction.triggered.connect(self.addNewTable)
        importCSVAction.triggered.connect(self.openImportCSVDialogue)


        self.gridLayout.addWidget(self.toolButton_add, 0, 0, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout)
        self.horizontalLayout_3.addLayout(self.verticalLayout_5)
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_deckName = QtWidgets.QLabel(self.tab_wordTable)
        self.label_deckName.setAlignment(QtCore.Qt.AlignCenter)
        self.label_deckName.setObjectName("label_deckName")
        self.horizontalLayout_10.addWidget(self.label_deckName)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem2)
        self.lineEdit_searchQuery = QtWidgets.QLineEdit(self.tab_wordTable)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_searchQuery.sizePolicy().hasHeightForWidth())
        self.lineEdit_searchQuery.setSizePolicy(sizePolicy)
        self.lineEdit_searchQuery.setObjectName("lineEdit_searchQuery")
        self.horizontalLayout_10.addWidget(self.lineEdit_searchQuery)
        self.pushButton_search = QtWidgets.QPushButton(self.tab_wordTable)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_search.sizePolicy().hasHeightForWidth())
        self.pushButton_search.setSizePolicy(sizePolicy)
        self.pushButton_search.setMaximumSize(QtCore.QSize(64, 16777215))
        self.pushButton_search.setIconSize(QtCore.QSize(16, 16))
        self.pushButton_search.setObjectName("pushButton_search")
        self.horizontalLayout_10.addWidget(self.pushButton_search)
        self.verticalLayout_12.addLayout(self.horizontalLayout_10)
        self.wordTable = QtWidgets.QTableWidget(self.tab_wordTable)
        font = QtGui.QFont()
        font.setFamily("Noto Sans CJK HK")
        self.wordTable.setFont(font)
        self.wordTable.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.wordTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.wordTable.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.wordTable.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.wordTable.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed|QtWidgets.QAbstractItemView.SelectedClicked)
        self.wordTable.setAlternatingRowColors(True)
        self.wordTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.wordTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.wordTable.setTextElideMode(QtCore.Qt.ElideRight)
        self.wordTable.setShowGrid(True)
        self.wordTable.setGridStyle(QtCore.Qt.DotLine)
        self.wordTable.setRowCount(1)
        self.wordTable.setColumnCount(7)
        self.wordTable.setObjectName("wordTable")
        self.wordTable.setColumnCount(7)
        self.wordTable.setRowCount(1)

        # I changed this stuff to initialize to standard size
        self.wordTable.setColumnCount(7)
        self.wordTable.setRowCount(1)
        # Added Header Labels
        self.wordTable.setHorizontalHeaderLabels(
            ['Index', 'Vocabulary', 'Definition', 'Pronunciation', 'Attempted', 'Correct', 'Starred'])
        self.wordTable.setColumnHidden(0, True)
        self.wordTable.setColumnWidth(1, 210)
        self.wordTable.setColumnWidth(2, 210)
        self.wordTable.setColumnWidth(3, 186)
        self.wordTable.customContextMenuRequested.connect(self.requestWordTableContextMenu)

        #self.wordTable.itemSelectionChanged.connect(self.autoInsertTableRow)
        self.wordTable.currentCellChanged.connect(self.autoInsertTableRow)

        self.verticalLayout_12.addWidget(self.wordTable)
        self.buttonBox_wordList = QtWidgets.QDialogButtonBox(self.tab_wordTable)
        self.buttonBox_wordList.setEnabled(False)
        self.buttonBox_wordList.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox_wordList.setCenterButtons(False)
        self.buttonBox_wordList.setObjectName("buttonBox_wordList")


        # Added Modified - be careful
        self.buttonBox_wordList.button(QtWidgets.QDialogButtonBox.Cancel).setText("Revert")

        self.buttonBox_wordList.setCenterButtons(False)
        self.buttonBox_wordList.setObjectName("buttonBox_wordList")
        # Added buttonBox_wordList bindings
        self.buttonBox_wordList.accepted.connect(self.saveTable)
        self.buttonBox_wordList.rejected.connect(self.revertTable)


        self.verticalLayout_12.addWidget(self.buttonBox_wordList)
        self.horizontalLayout_3.addLayout(self.verticalLayout_12)
        self.tabWidget.addTab(self.tab_wordTable, "")
        self.tab_typing = QtWidgets.QWidget()
        self.tab_typing.setObjectName("tab_typing")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_typing)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.label_typingWord = QtWidgets.QLabel(self.tab_typing)
        font = QtGui.QFont()
        font.setFamily("Noto Sans CJK JP")
        font.setPointSize(26)
        self.label_typingWord.setFont(font)
        self.label_typingWord.setWordWrap(True)
        self.label_typingWord.setObjectName("label_typingWord")
        self.horizontalLayout_5.addWidget(self.label_typingWord)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem5)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem6)
        self.line_2 = QtWidgets.QFrame(self.tab_typing)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_7.addWidget(self.line_2)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.lineEdit_answer = QtWidgets.QLineEdit(self.tab_typing)
        font = QtGui.QFont()
        font.setFamily("Noto Sans CJK JP")
        self.lineEdit_answer.setFont(font)
        self.lineEdit_answer.setText("")
        self.lineEdit_answer.setObjectName("lineEdit_answer")
        self.horizontalLayout_6.addWidget(self.lineEdit_answer)
        self.pushButton_enter = QtWidgets.QPushButton(self.tab_typing)
        self.pushButton_enter.setAutoDefault(False)
        self.pushButton_enter.setDefault(True)
        self.pushButton_enter.setObjectName("pushButton_enter")
        self.horizontalLayout_6.addWidget(self.pushButton_enter)
        self.verticalLayout_7.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.progressBar = QtWidgets.QProgressBar(self.tab_typing)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_7.addWidget(self.progressBar)
        self.label_fractionCorrect = QtWidgets.QLabel(self.tab_typing)
        self.label_fractionCorrect.setObjectName("label_fractionCorrect")
        self.horizontalLayout_7.addWidget(self.label_fractionCorrect)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem7)
        self.pushButton_notSure_Skip = QtWidgets.QPushButton(self.tab_typing)
        self.pushButton_notSure_Skip.setObjectName("pushButton_notSure_Skip")
        self.horizontalLayout_7.addWidget(self.pushButton_notSure_Skip)
        self.verticalLayout_7.addLayout(self.horizontalLayout_7)
        self.verticalLayout_4.addLayout(self.verticalLayout_7)
        self.tabWidget.addTab(self.tab_typing, "")
        self.tab_flashcards = QtWidgets.QWidget()
        self.tab_flashcards.setObjectName("tab_flashcards")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_flashcards)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem8)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem9)
        self.label_flashWord = QtWidgets.QLabel(self.tab_flashcards)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_flashWord.setFont(font)
        self.label_flashWord.setWordWrap(True)
        self.label_flashWord.setObjectName("label_flashWord")
        self.horizontalLayout_2.addWidget(self.label_flashWord)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem10)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem11)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_nextWord = QtWidgets.QPushButton(self.tab_flashcards)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_nextWord.sizePolicy().hasHeightForWidth())
        self.pushButton_nextWord.setSizePolicy(sizePolicy)
        self.pushButton_nextWord.setObjectName("pushButton_nextWord")
        self.horizontalLayout_4.addWidget(self.pushButton_nextWord)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem12)
        self.checkBox_autoPlay = QtWidgets.QCheckBox(self.tab_flashcards)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_autoPlay.sizePolicy().hasHeightForWidth())
        self.checkBox_autoPlay.setSizePolicy(sizePolicy)
        self.checkBox_autoPlay.setObjectName("checkBox_autoPlay")
        self.horizontalLayout_4.addWidget(self.checkBox_autoPlay)
        self.verticalLayout_6.addLayout(self.horizontalLayout_4)
        self.verticalLayout_3.addLayout(self.verticalLayout_6)
        self.tabWidget.addTab(self.tab_flashcards, "")
        self.tab_quiz = QtWidgets.QWidget()
        self.tab_quiz.setObjectName("tab_quiz")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.tab_quiz)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        spacerItem13 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_8.addItem(spacerItem13)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem14)
        self.label_quizWord = QtWidgets.QLabel(self.tab_quiz)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_quizWord.setFont(font)
        self.label_quizWord.setWordWrap(True)
        self.label_quizWord.setObjectName("label_quizWord")
        self.horizontalLayout_8.addWidget(self.label_quizWord)
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem15)
        self.verticalLayout_8.addLayout(self.horizontalLayout_8)
        spacerItem16 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_8.addItem(spacerItem16)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.pushButton_quizChoice1 = QtWidgets.QPushButton(self.tab_quiz)
        self.pushButton_quizChoice1.setObjectName("pushButton_quizChoice1")
        self.verticalLayout_9.addWidget(self.pushButton_quizChoice1)
        self.pushButton_quizChoice2 = QtWidgets.QPushButton(self.tab_quiz)
        self.pushButton_quizChoice2.setObjectName("pushButton_quizChoice2")
        self.verticalLayout_9.addWidget(self.pushButton_quizChoice2)
        self.horizontalLayout_9.addLayout(self.verticalLayout_9)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.pushButton_quizChoice3 = QtWidgets.QPushButton(self.tab_quiz)
        self.pushButton_quizChoice3.setObjectName("pushButton_quizChoice3")
        self.verticalLayout_10.addWidget(self.pushButton_quizChoice3)
        self.pushButton_quizChoice4 = QtWidgets.QPushButton(self.tab_quiz)
        self.pushButton_quizChoice4.setObjectName("pushButton_quizChoice4")
        self.verticalLayout_10.addWidget(self.pushButton_quizChoice4)
        self.horizontalLayout_9.addLayout(self.verticalLayout_10)
        self.verticalLayout_8.addLayout(self.horizontalLayout_9)
        self.verticalLayout_11.addLayout(self.verticalLayout_8)
        self.tabWidget.addTab(self.tab_quiz, "")
        self.tab_tones = QtWidgets.QWidget()
        self.tab_tones.setObjectName("tab_tones")
        self.tabWidget.addTab(self.tab_tones, "")
        self.tab_statistics = QtWidgets.QWidget()
        self.tab_statistics.setObjectName("tab_statistics")
        self.tabWidget.addTab(self.tab_statistics, "")
        self.tab_settings = QtWidgets.QWidget()
        self.tab_settings.setObjectName("tab_settings")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.tab_settings)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout.addLayout(self.gridLayout_2)
        spacerItem17 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem17)
        self.verticalLayout_13.addLayout(self.horizontalLayout)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        spacerItem18 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem18)
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_settings)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_13.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.tab_settings)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_13.addWidget(self.pushButton)
        self.verticalLayout_13.addLayout(self.horizontalLayout_13)
        self.tabWidget.addTab(self.tab_settings, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 960, 30))
        self.menubar.setObjectName("menubar")
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        self.menu_help = QtWidgets.QMenu(self.menubar)
        self.menu_help.setObjectName("menu_help")
        MainWindow.setMenuBar(self.menubar)
        self.actionFrom_Template = QtWidgets.QAction(MainWindow)
        self.actionFrom_Template.setObjectName("actionFrom_Template")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionTemplate_Data = QtWidgets.QAction(MainWindow)
        self.actionTemplate_Data.setObjectName("actionTemplate_Data")
        self.actionUser_Data = QtWidgets.QAction(MainWindow)
        self.actionUser_Data.setObjectName("actionUser_Data")
        self.actionImport_Data = QtWidgets.QAction(MainWindow)
        self.actionImport_Data.setObjectName("actionImport_Data")
        self.actionHow_to_play = QtWidgets.QAction(MainWindow)
        self.actionHow_to_play.setObjectName("actionHow_to_play")
        self.actionUserGuide = QtWidgets.QAction(MainWindow)
        self.actionUserGuide.setObjectName("actionUserGuide")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionDonate = QtWidgets.QAction(MainWindow)
        self.actionDonate.setObjectName("actionDonate")
        self.menu_file.addAction(self.actionOpen)
        self.menu_file.addAction(self.actionQuit)
        self.menu_help.addAction(self.actionUserGuide)
        self.menu_help.addSeparator()
        self.menu_help.addAction(self.actionAbout)
        self.menu_help.addAction(self.actionDonate)
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.lineEdit_answer, QtCore.SIGNAL("returnPressed()"), self.pushButton_enter.click)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "cjk_trainer 0.2", None, -1))
        self.label_deckList.setText(QtWidgets.QApplication.translate("MainWindow", "Deck List", None, -1))
        self.pushButton_wordList_select.setText(QtWidgets.QApplication.translate("MainWindow", "Select", None, -1))
        self.toolButton_add.setText(QtWidgets.QApplication.translate("MainWindow", "Add", None, -1))
        self.label_deckName.setText(QtWidgets.QApplication.translate("MainWindow", "Selected Deck: ", None, -1))
        self.lineEdit_searchQuery.setPlaceholderText(QtWidgets.QApplication.translate("MainWindow", "Search for a word", None, -1))
        self.pushButton_search.setText(QtWidgets.QApplication.translate("MainWindow", "Search", None, -1))
        self.wordTable.setSortingEnabled(True)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_wordTable), QtWidgets.QApplication.translate("MainWindow", "Word List", None, -1))
        self.label_typingWord.setText(QtWidgets.QApplication.translate("MainWindow", "null", None, -1))
        self.lineEdit_answer.setPlaceholderText(QtWidgets.QApplication.translate("MainWindow", "Enter your answer", None, -1))
        self.pushButton_enter.setText(QtWidgets.QApplication.translate("MainWindow", "Enter", None, -1))
        self.label_fractionCorrect.setText(QtWidgets.QApplication.translate("MainWindow", "0/0", None, -1))
        self.pushButton_notSure_Skip.setText(QtWidgets.QApplication.translate("MainWindow", "Not sure", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_typing), QtWidgets.QApplication.translate("MainWindow", "Typing", None, -1))
        self.label_flashWord.setText(QtWidgets.QApplication.translate("MainWindow", "null", None, -1))
        self.pushButton_nextWord.setText(QtWidgets.QApplication.translate("MainWindow", "Next Word", None, -1))
        self.checkBox_autoPlay.setText(QtWidgets.QApplication.translate("MainWindow", "Autoplay", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_flashcards), QtWidgets.QApplication.translate("MainWindow", "Flashcards", None, -1))
        self.label_quizWord.setText(QtWidgets.QApplication.translate("MainWindow", "null", None, -1))
        self.pushButton_quizChoice1.setText(QtWidgets.QApplication.translate("MainWindow", "Word1", None, -1))
        self.pushButton_quizChoice2.setText(QtWidgets.QApplication.translate("MainWindow", "Word2", None, -1))
        self.pushButton_quizChoice3.setText(QtWidgets.QApplication.translate("MainWindow", "Word3", None, -1))
        self.pushButton_quizChoice4.setText(QtWidgets.QApplication.translate("MainWindow", "Word4", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_quiz), QtWidgets.QApplication.translate("MainWindow", "Quiz", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_tones), QtWidgets.QApplication.translate("MainWindow", "Tones", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_statistics), QtWidgets.QApplication.translate("MainWindow", "Statistics", None, -1))
        self.pushButton_2.setText(QtWidgets.QApplication.translate("MainWindow", "Revert", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("MainWindow", "Apply", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_settings), QtWidgets.QApplication.translate("MainWindow", "Settings", None, -1))
        self.menu_file.setTitle(QtWidgets.QApplication.translate("MainWindow", "Fi&le", None, -1))
        self.menu_help.setTitle(QtWidgets.QApplication.translate("MainWindow", "&Help", None, -1))
        self.actionFrom_Template.setText(QtWidgets.QApplication.translate("MainWindow", "From Template...", None, -1))
        self.actionQuit.setText(QtWidgets.QApplication.translate("MainWindow", "&Quit", None, -1))
        self.actionOpen.setText(QtWidgets.QApplication.translate("MainWindow", "&Open", None, -1))
        self.actionTemplate_Data.setText(QtWidgets.QApplication.translate("MainWindow", "&Template Data", None, -1))
        self.actionUser_Data.setText(QtWidgets.QApplication.translate("MainWindow", "&User Data", None, -1))
        self.actionImport_Data.setText(QtWidgets.QApplication.translate("MainWindow", "&Import Data", None, -1))
        self.actionHow_to_play.setText(QtWidgets.QApplication.translate("MainWindow", "How to play", None, -1))
        self.actionUserGuide.setText(QtWidgets.QApplication.translate("MainWindow", "&User Guide", None, -1))
        self.actionAbout.setText(QtWidgets.QApplication.translate("MainWindow", "About", None, -1))
        self.actionDonate.setText(QtWidgets.QApplication.translate("MainWindow", "Donate", None, -1))

