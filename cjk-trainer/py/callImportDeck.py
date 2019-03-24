from py.ImportDeck import *
class ImportDeck(QtWidgets. QDialog):

    def __init__(self):
        super().__init__()
        self.iD  = Ui_importDialog()
        self.iD.setupUi(self)
