from setupUi.DeckNamePrompt import *
from PySide2 import QtWidgets
from utilities.SqlTools import *

class DeckNamePrompt(QtWidgets.QDialog):

    def __init__(self, mainWindow, parent=None):
        super(DeckNamePrompt, self).__init__(parent)
        self.DNPD  = Ui_DeckNamePromptDialog()
        self.DNPD.setupUi(self)
        self.mainWindow = mainWindow
        # ADD
        self.DNPD.buttonBox.accepted.connect(self.acceptInput)


    def acceptInput(self):
        table_name = self.DNPD.lineEdit.text()
        print("Creating table: ", table_name)
        self.mainWindow.database.insertDeck(table_name)

        #initialRowData = ['1', '0', "", "", "", '0', '0']
        #self.mainWindow.database.addTableRow(table_name, initialRowData)
        #self.mainWindow.database.setLastTimeStudied(table_name, date_time="min")
        #self.mainWindow.reloadTableList()
