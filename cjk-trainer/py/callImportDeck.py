from py.setupUi.ImportCsvDialog import *
from py.utilities.CsvTools import importDialogHelper
from py.utilities.SqlTools import *

class ImportCSVDialog(QtWidgets. QDialog):

    def __init__(self, mainWindow, parent=None):
        super(ImportCSVDialog, self).__init__(parent)
        self.icd  = Ui_ImportCsvDialog()
        self.mainWindow = mainWindow
        self.icd.setupUi(self)



    def acceptInput(self):
        table_name = self.iD.lineEdit.text()
        vocab_list = self.iD.plainTextEdit.toPlainText().splitlines()
        headers, word_list = importDialogHelper(vocab_list)
        for i in word_list:
            print(i)
        print(table_name)
        db = SqlTools(self.mainWindow.DATABASE_PATH)
        db.createTable(table_name)
        db.insertFromCSV(table_name, headers, word_list)
        db.closeDatabase()
        self.mainWindow.reloadTableList()