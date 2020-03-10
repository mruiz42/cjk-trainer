from py.setupUi.Review import *
from PySide2.QtSql import *
class ReviewDialog(QtWidgets. QDialog):

    def __init__(self, mainWindow, parent=None):
        if not parent:
            parent = mainWindow
        super(ReviewDialog, self).__init__(parent)
        self.rd  = Ui_Dialog()
        self.mainWindow = mainWindow
        self.rd.setupUi(self)
