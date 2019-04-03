from PySide2.QtCore import QObject, QEvent
from PySide2 import QtCore


class KeyPressEater(QObject):
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Wheel:
            print("Ate key press")
            return True
        else:
            # standard event processing
            return QObject.eventFilter(self, obj, event)
        # print(event.type())



    def mousePressEvent(self, obj, event):
        if event.type() == QtCore.QtRightButton:
            print("hi")
        elif event.type() == QtCore.QtLeftButton:
            print("hi2")
