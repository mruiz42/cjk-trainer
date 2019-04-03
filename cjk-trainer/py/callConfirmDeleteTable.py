from py.ConfirmDeleteTable import *
from py.MainWindow import *
class ConfirmDeleteTable(QtWidgets.QDialog):

    def __init__(self, mainWindow, parent=None):
        super(ConfirmDeleteTable, self).__init__(parent)
        self.cDTD  = Ui_ConfirmDeleteTableDialog()
        self.mainWindow = mainWindow
        self.cDTD.setupUi(self)
        self.cDTD.buttonBox.accepted.connect(self.accepted2)


    def setTableName(self, tableName):
        self.cDTD.label.setText("Are you sure you want to delete the table:\n"+ tableName + "\nTHIS CANNOT BE UNDONE ")

    def accepted2(self):
        #TODO RENAME NECESSARY -- CONFLICTING FUNCTION NAME
        print("hi")
        self.mainWindow.refreshTableList()
