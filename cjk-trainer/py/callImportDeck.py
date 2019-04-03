from py.setupUi.ImportDeck import *
class ImportDeck(QtWidgets. QDialog):

    def __init__(self, mainWindow, parent=None):
        super(ImportDeck,self).__init__(parent)
        self.iD  = Ui_importDialog()
        self.mainWindow = mainWindow
        self.iD.setupUi(self)
        self.iD.pushButton_Import.clicked.connect(self.accepted)  # ADD
        self.iD.pushButton_Cancel.clicked.connect(self.reject) #ADD



    def accepted(self):
        table_name = self.lineEdit.text()
        vocab_list = self.plainTextEdit.toPlainText().splitlines()
        headers, word_list = importDialogHelper(vocab_list)
        for i in word_list:
            print(i)
        print(table_name)
        db = SqlTools()
        db.openDatabase('../data/vocab.db')
        db.createTable(table_name)
        db.insertVocabWordList(table_name, headers, word_list)
        db.closeDatabase()
        self.refreshTableList()