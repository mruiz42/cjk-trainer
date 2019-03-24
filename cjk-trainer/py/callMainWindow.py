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
        self.ui.pushButton_wordList_edit.clicked.connect(self.openImportDialog)

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

    tableModel = QSqlTableModel()
    queryModel = QSqlQueryModel()

    # db.exec_(query='CREATE TABLE allChineseVocab('
    #                       'CARDNUM INTEGER PRIMARY KEY AUTOINCREMENT,'
    #                       'HANZI CHAR UNIQUE,'
    #                       'PINYIN CHAR,'
    #                       'DEFINITION CHAR,'
    #                       'STARRED INTEGER,'
    #                       'ATTEMPTED INTEGER,'
    #                       'CORRECT INTEGER);')

    print(queryModel.lastError())

    queryModel.setQuery('Select * FROM allChineseVocab', db)
    projectView = QTableView()
    projectView = win.ui.tableView

    projectView.setModel(queryModel)
    projectView.setColumnWidth(2, 300)
    projectView.show()

    vocabTableList = db.tables()
    # Generate list of tables for listWidget
    print(vocabTableList)
    listWidget = win.ui.listWidget
    for i in vocabTableList:
        if i != 'sqlite_sequence':
            listWidget.addItem(i)

    listWidget.show()
    db.close()
    sys.exit(app.exec_())
