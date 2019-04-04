from py.setupUi.GenericDialog import *
class GenericDialog(QtWidgets. QDialog):

    def __init__(self, mainWindow, parent=None):
        super(GenericDialog,self).__init__(parent)
        self.gd  = Ui_GenericDialog()
        self.mainWindow = mainWindow
        self.gd.setupUi(self)
        self.gd.buttonBox.accepted.connect(self.acceptInput)
        self.allowTabChange = False



    def acceptInput(self):
        self.allowTabChange = True