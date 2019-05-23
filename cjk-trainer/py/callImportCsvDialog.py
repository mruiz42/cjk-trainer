from setupUi.ImportCsvDialog import *
from utilities.CsvTools import importDialogHelper
from utilities.SqlTools import *

class ImportCSVDialog(QtWidgets. QDialog):

    def __init__(self, mainWindow, parent=None):
        super(ImportCSVDialog, self).__init__(parent)
        self.icd  = Ui_ImportCsvDialog()
        self.mainWindow = mainWindow
        self.icd.setupUi(self)
        self.languages = ["Chinese (Simplified)", "Chinese (Traditional)", "Spanish", "English", "Hindi", "Arabic",
                          "Portuguese", "Russian", "Japanese", "Punjabi", "German", "Javanese", "Malay", "Telugu",
                          "Vietnamese", "Korean", "French", "Turkish", "Italian", "Thai", "Persian", "Polish",
                          "Romanian", "Dutch", "Czech", "Swedish"]
        self.icd.comboBox_definition.addItems(sorted(self.languages))
        self.icd.comboBox_vocabulary.addItems(sorted(self.languages))
        self.icd.buttonBox.accepted.connect(self.acceptInput)
        self.icd.comboBox_separator.currentIndexChanged.connect(self.comboBox_changeEvent)
        self.icd.buttonBox.setDisabled(True)
        self.icd.lineEdit_tableName.textEdited.connect(self.enableButtonBox)
        self.icd.plainTextEdit_deckName.textChanged.connect(self.enableButtonBox)
        # Member variables


    def enableButtonBox(self):
        lineEdit = self.icd.lineEdit_tableName
        if lineEdit.text() != '' and self.icd.plainTextEdit_deckName.toPlainText() != '':
            self.icd.buttonBox.setDisabled(False)
        else:
            self.icd.buttonBox.setDisabled(True)

    def comboBox_changeEvent(self):
        '''This function will set the self.sep variable to the current text as well as adjust the placeholder text in
        plainTextEdit'''
        self.sep = self.icd.comboBox_separator.currentText()
        if self.sep == ',':
            self.icd.plainTextEdit_deckName.setPlaceholderText(
                QtWidgets.QApplication.translate("ImportCsvDialog", "Vocabulary,Definition,Pronunciation(optional)\n"
                                                                    "Vocabulary,Definition,Pronunciation(optional)\n",
                                                 None, -1))
        elif self.sep == 'tab':
            self.sep = '\t'
            self.icd.plainTextEdit_deckName.setPlaceholderText(
                QtWidgets.QApplication.translate("ImportCsvDialog", "Vocabulary    Definition    "
                                                                    "Pronunciation(optional)\n"
                                                                    "Vocabulary    Definition    "
                                                                    "Pronunciation(optional)\n",
                                                 None, -1))
        elif self.sep == '-':
            self.icd.plainTextEdit_deckName.setPlaceholderText(
             QtWidgets.QApplication.translate("ImportCsvDialog", "Vocabulary-Definition-Pronunciation(optional)\n"
                                                                "Vocabulary-Definition-Pronunciation(optional)\n",
                                                None, -1))
        elif self.sep == '/':
            self.icd.plainTextEdit_deckName.setPlaceholderText(
                QtWidgets.QApplication.translate("ImportCsvDialog", "Vocabulary/Definition/Pronunciation(optional)\n"
                                                                    "Vocabulary/Definition/Pronunciation(optional)\n",
                                                 None, -1))

    def acceptInput(self):
        table_name = self.icd.lineEdit_tableName.text()
        vocab_list = self.icd.plainTextEdit_deckName.toPlainText().splitlines()
        vocabularyLang = self.icd.comboBox_vocabulary.currentText()
        definitionLang = self.icd.comboBox_definition.currentText()
        line_format = self.icd.comboBox_format.currentText()
        separator = self.icd.comboBox_separator.currentText()

        print(vocab_list)

        # Parse the file and return a list of vocabulary data
        word_list = importDialogHelper(vocab_list, table_name, line_format, separator)

        for i in word_list:
            print(i)
        print(table_name)
        db = self.mainWindow.database
        db.insertDeck(table_name, vocabularyLang, definitionLang)
        db.insertManyCards(word_list)
        self.mainWindow.loadDeckList()