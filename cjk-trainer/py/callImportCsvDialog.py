from py.setupUi.ImportCsvDialog import *
from py.utilities.CsvTools import importDialogHelper
from py.utilities.SqlTools import *

class ImportCSVDialog(QtWidgets. QDialog):

    def __init__(self, mainWindow, parent=None):
        super(ImportCSVDialog, self).__init__(parent)
        self.icd  = Ui_ImportCsvDialog()
        self.mainWindow = mainWindow
        self.icd.setupUi(self)
        self.icd.buttonBox.accepted.connect(self.acceptInput)
        self.icd.comboBox_separator.currentIndexChanged.connect(self.comboBox_changeEvent)
        self.icd.buttonBox.setDisabled(True)
        self.icd.lineEdit_tableName.textEdited.connect(self.enableButtonBox)
        self.icd.plainTextEdit.textChanged.connect(self.enableButtonBox)
        # Member variables
        self.sep = self.icd.comboBox_separator.currentText()


    def enableButtonBox(self):
        lineEdit = self.icd.lineEdit_tableName
        plainTextEdit = self.icd.plainTextEdit
        if lineEdit.text() != '' and plainTextEdit.toPlainText() != '':
            self.icd.buttonBox.setDisabled(False)
        else:
            self.icd.buttonBox.setDisabled(True)



    def comboBox_changeEvent(self):
        '''This function will set the self.sep variable to the current text as well as adjust the placeholder text in
        plainTextEdit'''
        self.sep = self.icd.comboBox_separator.currentText()
        if self.sep == ',':
            self.icd.plainTextEdit.setPlaceholderText(
                QtWidgets.QApplication.translate("ImportCsvDialog", "Vocabulary,Definition,Pronunciation(optional)\n"
                                                                    "Vocabulary,Definition,Pronunciation(optional)\n",
                                                 None, -1))
        elif self.sep == 'tab':
            self.sep = '\t'
            self.icd.plainTextEdit.setPlaceholderText(
                QtWidgets.QApplication.translate("ImportCsvDialog", "Vocabulary    Definition    "
                                                                    "Pronunciation(optional)\n"
                                                                    "Vocabulary    Definition    "
                                                                    "Pronunciation(optional)\n",
                                                 None, -1))
        elif self.sep == '-':
            self.icd.plainTextEdit.setPlaceholderText(
             QtWidgets.QApplication.translate("ImportCsvDialog", "Vocabulary-Definition-Pronunciation(optional)\n"
                                                                "Vocabulary-Definition-Pronunciation(optional)\n",
                                                None, -1))
        elif self.sep == '/':
            self.icd.plainTextEdit.setPlaceholderText(
                QtWidgets.QApplication.translate("ImportCsvDialog", "Vocabulary/Definition/Pronunciation(optional)\n"
                                                                    "Vocabulary/Definition/Pronunciation(optional)\n",
                                                 None, -1))

    def acceptInput(self):
        table_name = self.icd.lineEdit_tableName.text()
        vocab_list = self.icd.plainTextEdit.toPlainText().splitlines()
        print(vocab_list)

        word_list = importDialogHelper(vocab_list, self.sep)


        for i in word_list:
            print(i)
        print(table_name)
        db = SqlTools(self.mainWindow.DATABASE_PATH)
        db.createTable(table_name)
        db.insertManyFromList(table_name, word_list)
        db.closeDatabase()
        self.mainWindow.reloadTableList()