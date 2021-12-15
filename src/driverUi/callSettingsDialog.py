from src.setupUi.SettingsDialog import *
from src.Settings import *

class SettingsDialog(QtWidgets. QDialog):

    def __init__(self, mainWindow, parent=None):
        self.shuffle = False
        self.starredOnly = False
        self.showPronunciationField = False
        self.showVocabularyFirst = True

        super(SettingsDialog,self).__init__(parent)
        self.sD  = Ui_SettingsDialog()
        self.mainWindow = mainWindow
        self.sD.setupUi(self)

