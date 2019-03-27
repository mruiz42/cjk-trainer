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

        self.ui.setupUi(self)
        self.ui.pushButton_wordList_add.clicked.connect(self.openImportDialog)

        self.show()

    def doNothing(self):
        print("nothing")

  #  def loadDatabase(self):

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

    conn = sqlite3.connect('../data/vocab.db')
    result = conn.execute('Select * FROM asd2')
    win.ui.wordList.setRowCount(0)
    win.ui.wordList.setColumnCount(6)
    for row_number, row_data in enumerate(result):
        win.ui.wordList.insertRow(row_number)
        for column_number, data in enumerate(row_data):
            print(data)
            win.ui.wordList.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))




    # Generate list of tables for listWidget
    vocabTableList = db.tables()
    print(vocabTableList)
    listWidget = win.ui.deckList
    for i in vocabTableList:
        if i != 'sqlite_sequence':
            listWidget.addItem(i)
    listWidget.show()







    db.close()
    sys.exit(app.exec_())