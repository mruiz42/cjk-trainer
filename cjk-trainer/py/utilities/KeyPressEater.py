from PySide2.QtCore import QObject, QEvent

class KeyPressEater(QObject):
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Wheel:
            print("Ate key press")
            return True
        else:
            # standard event processing
            return QObject.eventFilter(self, obj, event)
        # print(event.type())