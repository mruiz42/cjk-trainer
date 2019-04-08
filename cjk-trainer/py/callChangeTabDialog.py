from py.callGenericDialog import *
class ChangeTabDialog(GenericDialog):
    def __init__(self, mainWindow, index):
        super(ChangeTabDialog, self).__init__(mainWindow)
        self.index = index
        self.gd.label.setText("Switching tabs will result in unsaved progress.\n "
                                     "Would you like to proceed?")
        self.setWindowTitle("Tab Switching")
        self.gd.buttonBox.accepted.connect(self.acceptInput)


    def acceptInput(self):
        print("before or after")
        self.mainWindow.ui.tabBar.setCurrentIndex(self.index)
