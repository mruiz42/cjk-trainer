from setupUi.GenericDialog import *
class GenericDialog(QtWidgets. QDialog):

    def __init__(self, mainWindow, parent=None):
        if not parent:
            parent = mainWindow
        super(GenericDialog,self).__init__(parent)
        self.gd  = Ui_GenericDialog()
        self.mainWindow = mainWindow
        self.gd.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)



