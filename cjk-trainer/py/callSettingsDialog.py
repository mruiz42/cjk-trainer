from py.setupUi.SettingsDialog import *
from py.Settings import *

class SettingsDialog(QtWidgets. QDialog):

    def __init__(self, mainWindow, parent=None):
        super(SettingsDialog,self).__init__(parent)
        self.sD  = Ui_SettingsDialog()
        self.mainWindow = mainWindow
        self.sD.setupUi(self)