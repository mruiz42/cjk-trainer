from setupUi.DeckNamePrompt import *
from PySide2 import QtWidgets
from utilities.SqlTools import *

class DeckNamePrompt(QtWidgets.QDialog):
    def __init__(self, mainWindow, parent=None):
        super(DeckNamePrompt, self).__init__(parent)
        self.DNPD  = Ui_DeckNamePromptDialog()
        self.DNPD.setupUi(self)
        self.mainWindow = mainWindow
        self.languages = ["", "Chinese (Simplified)", "Chinese (Traditional)", "Chinese (Pinyin)", "Spanish", "English", "Hindi", "Arabic",
                          "Portuguese", "Russian", "Japanese", "Japanese (Romanji)", "Punjabi", "German", "Javanese", "Malay", "Telugu",
                          "Vietnamese", "Korean", "French", "Turkish", "Italian", "Thai", "Persian", "Polish",
                          "Romanian", "Dutch", "Czech", "Swedish"]
        self.languages = sorted(self.languages)
        self.DNPD.comboBox_vocabulary.addItems(self.languages)
        self.DNPD.comboBox_definition.addItems(self.languages)

    def createDeck(self):
        table_name = self.DNPD.lineEdit_enterDeckName.text()
        language_vocabulary = self.DNPD.comboBox_vocabulary.currentText()
        language_definition = self.DNPD.comboBox_definition.currentText()
        print("Creating table: ", table_name, " using ", language_vocabulary ," & ", language_definition)
        try:
            self.mainWindow.database.insertDeck(table_name, language_vocabulary, language_definition)
        except sqlite3.IntegrityError:
            #raise window saying that u cant do that
            print("You cannot create a deck with a preexisting name. Please try another name or name it something else.")
        self.mainWindow.loadDeckList()

        #initialRowData = ['1', '0', "", "", "", '0', '0']
        #self.mainWindow.database.addTableRow(table_name, initialRowData)
        #self.mainWindow.database.setLastTimeStudied(table_name, date_time="min")
        #self.mainWindow.reloadTableList()

    def modifyDeck(self):
        table_name = self.DNPD.lineEdit_enterDeckName.text()
        language_vocabulary = self.DNPD.comboBox_vocabulary.currentText()
        language_definition = self.DNPD.comboBox_definition.currentText()
        table_name_old = self.mainWindow.nameOfCurrentDeck
        try:
            self.mainWindow.database.executeModify(table_name, language_vocabulary, language_definition, table_name_old)
            self.mainWindow.nameOfCurrentDeck = table_name
            self.mainWindow.definitionLanguage = language_definition
            self.mainWindow.vocabularyLanguage = language_vocabulary
        except sqlite3.IntegrityError:
            #raise window saying that u cant do that
            print("You cannot create a deck with a preexisting name. Please try another name or name it something else.")
        self.mainWindow.loadDeckList()



