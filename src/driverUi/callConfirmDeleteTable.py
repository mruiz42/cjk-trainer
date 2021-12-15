from src.setupUi.MainWindow import *
from src.setupUi.ConfirmDeleteTable import *
from src.utilities.SqlTools import *


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
        self.cDTD.label.setText("Are you sure you want to delete the table:\n"+ tableName + "\nTHIS CANNOT BE UNDONE!")

    def deleteConfirmed(self):
        print("Deleting table: ", self.tableName)
        self.mainWindow.database.deleteDeck(self.tableName)
        self.mainWindow.loadDeckList()
        #self.mainWindow.ui.wordTable.clear()
        #self.mainWindow.ui.wordTable.setHorizontalHeaderLabels(['Index', 'Starred', 'Vocabulary', 'Definition', 'Pronunciation'])


