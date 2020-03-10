from py.setupUi.ImportCsvDialog import *
from py.utilities.CsvTools import importDialogHelper
from py.utilities.SqlTools import *
from PySide2 import QtWidgets
class ImportCSVDialog(QtWidgets. QDialog):

    def __init__(self, mainWindow, parent=None):
        super(ImportCSVDialog, self).__init__(parent)
        self.icd  = Ui_ImportCsvDialog()
        self.mainWindow = mainWindow
        self.icd.setupUi(self)
        self.comboBox_changeEvent()
        self.languages = ["", "Chinese (Simplified)", "Chinese (Traditional)", "Chinese (Pinyin)", "Spanish", "English", "Hindi", "Arabic",
                          "Portuguese", "Russian", "Japanese", "Japanese (Romanji)", "Punjabi", "German", "Javanese", "Malay", "Telugu",
                          "Vietnamese", "Korean", "French", "Turkish", "Italian", "Thai", "Persian", "Polish",
                          "Romanian", "Dutch", "Czech", "Swedish"]
        self.icd.comboBox_definition.addItems(sorted(self.languages))
        self.icd.comboBox_vocabulary.addItems(sorted(self.languages))
        self.icd.comboBox_definition.setCurrentText(" ")
        self.icd.comboBox_vocabulary.setCurrentText(" ")
        self.icd.buttonBox.accepted.connect(self.acceptInput)
        self.icd.comboBox_separator.currentIndexChanged.connect(self.comboBox_changeEvent)
        self.icd.comboBox_format.currentIndexChanged.connect(self.comboBox_changeEvent)
        self.icd.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setDisabled(True)
        self.icd.lineEdit_tableName.textEdited.connect(self.enableButtonBox)
        self.icd.plainTextEdit_deckName.textChanged.connect(self.enableButtonBox)
        self.icd.comboBox_definition.currentIndexChanged.connect(self.enableButtonBox)
        self.icd.comboBox_vocabulary.currentIndexChanged.connect(self.enableButtonBox)



    def enableButtonBox(self):
        lineEdit = self.icd.lineEdit_tableName
        deckName = self.icd.plainTextEdit_deckName
        definition = self.icd.comboBox_definition
        vocabulary = self.icd.comboBox_vocabulary
        if (lineEdit.text() != '' and deckName.toPlainText() != ''
                and definition.currentText() != "" and vocabulary.currentText() != ""):
            self.icd.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setDisabled(False)
        else:
            self.icd.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setDisabled(True)

    def comboBox_changeEvent(self):
        '''This function will set the self.sep variable to the current text as well as adjust the placeholder text in
        plainTextEdit'''
        sep = self.icd.comboBox_separator.currentText()
        format = self.icd.comboBox_format.currentText()
        if sep == "tab":
            sep = "\t"

        placeholderText = format.strip("][")
        placeholderText = placeholderText.replace("][", sep)
        placeholderText += "\n"
        self.icd.plainTextEdit_deckName.setPlaceholderText(
            QtWidgets.QApplication.translate("ImportCsvDialog", placeholderText * 3,
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
