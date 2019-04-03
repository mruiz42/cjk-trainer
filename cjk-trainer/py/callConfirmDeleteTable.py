from py.ConfirmDeleteTable import *
class ConfirmDeleteTable(QtWidgets. QDialog):

    def __init__(self):
        super().__init__()
        self.cDTD  = Ui_ConfirmDeleteTableDialog()
        self.cDTD.setupUi(self)


    def setTableName(self, tableName):
        self.cDTD.label.setText("Are you sure you want to delete the table:\n"+ tableName + "\nTHIS CANNOT BE UNDONE ")
