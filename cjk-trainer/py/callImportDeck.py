from py.setupUi.ImportDeck import *
from py.utilities.CsvTools import importDialogHelper


class ImportDeck(QtWidgets. QDialog):

    def __init__(self, mainWindow, parent=None):
        super(ImportDeck,self).__init__(parent)
        self.iD  = Ui_importDialog()
        self.mainWindow = mainWindow
        self.iD.setupUi(self)
        self.iD.pushButton_Import.clicked.connect(self.acceptInput)  # ADD
        self.iD.pushButton_Cancel.clicked.connect(self.reject) #ADD


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