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
        db = SqlTools(self.mainWindow.DATABASE_PATH)
        db.createDeckTable(table_name)

        initialRowData = ['1', '0', "", "", "", '0', '0']
        db.addTableRow(table_name, initialRowData)
        db.setLastTimeStudied(table_name, date_time="min")
        db.closeDatabase()
        self.mainWindow.reloadTableList()
