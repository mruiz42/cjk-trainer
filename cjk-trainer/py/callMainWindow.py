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


    # print(listWidget.indexAt(0))
    # dbname = win.ui.nameOfCurrentDeck
    # db = sqlite3.connect("../data/vocab.db")
    # conn = sqlite3.connect('../data/vocab.db')
    # c = conn.execute('SELECT * FROM {}'.format(dbname))
    # result = c.fetchall()
    # conn.close()
    # print(result)


    db.close()


    sys.exit(app.exec_())