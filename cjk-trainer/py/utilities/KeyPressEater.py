from PySide2.QtCore import QObject, QEvent
from py.callChangeTabDialog import *

class KeyPressEater(QObject):
    def __init__(self, mainWindow, parent=None):
        if not parent:
            parent = mainWindow
        super(KeyPressEater, self).__init__(parent)
        self.mainWindow = mainWindow

    def eventFilter(self, obj, event):


        if event.type() == QEvent.Type.Wheel:
            print("Ate key press")
            return True


        elif event.type() == QEvent.Type.MouseButtonPress:
                if self.mainWindow.cardNum > 0 and self.mainWindow.indexOfCurrentTab != self.mainWindow.ui.tabBar.tabAt(event.pos()):
                    self.index = self.mainWindow.ui.tabBar.tabAt(event.pos())
                    self.tabDialog = ChangeTabDialog(self.mainWindow, self.index)
                    self.tabDialog.show()
                    return True
                else:
                    self.mainWindow.indexOfCurrentTab = self.mainWindow.ui.tabBar.tabAt(event.pos())
                    return False
        else:
            # standard event processing
            return QObject.eventFilter(self, obj, event)



    def mousePressEvent(self, obj, event):
        if event.type() == QtCore.QtRightButton:
            print("hi")
        elif event.type() == QtCore.QtLeftButton:
            print("hi2")
