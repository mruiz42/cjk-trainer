from py.DeckNamePrompt import *
class DeckNamePrompt(QtWidgets. QDialog):

    def __init__(self):
        super().__init__()
        self.nameOfNewDeck = ""
        self.DNPD  = Ui_DeckNamePromptDialog()
        self.DNPD.setupUi(self)