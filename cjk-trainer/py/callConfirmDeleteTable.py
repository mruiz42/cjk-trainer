from py.setupUi.MainWindow import *
from py.setupUi.ConfirmDeleteTable import *
from py.utilities.SqlTools import *


class ConfirmDeleteTable(QtWidgets.QDialog):

    def __init__(self, mainWindow, parent=None):
        super(ConfirmDeleteTable, self).__init__(parent)
        self.cDTD  = Ui_ConfirmDeleteTableDialog()
        self.mainWindow = mainWindow
        self.cDTD.setupUi(self)
        self.cDTD.buttonBox.accepted.connect(self.deleteConfirmed)
        self.tableName = ""

    def setTableName(self, tableName):
        self.tableName = tableName
        self.cDTD.label.setText("Are you sure you want to delete the table:\n"+ tableName + "\nTHIS CANNOT BE UNDONE ")

    def deleteConfirmed(self):
        print("Deleting table: ", self.tableName)
        db = SqlTools(self.mainWindow.DATABASE_PATH)
        db.dropTable(self.tableName)
        db.closeDatabase()
        self.mainWindow.reloadTableList()
        self.mainWindow.ui.wordTable.clear()
        self.ui.wordTable.setHorizontalHeaderLabels(
            ['Index', '*', 'Vocabulary', 'Definition', 'Pronunciation', 'Correct', 'Attempted', 'Date Studied'])


