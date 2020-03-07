from PySide2.QtCore import QObject, QEvent
from py.callChangeTabDialog import *
from py.TypingExercise import *
from py.FlashcardExercise import *
from py.QuizExercise import *
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
                if self.mainWindow.wordDeck.cardNum > 0 and self.mainWindow.indexOfCurrentTab != self.mainWindow.ui.tabBar.tabAt(event.pos()):
                    self.index = self.mainWindow.ui.tabBar.tabAt(event.pos())
                    self.tabDialog = ChangeTabDialog(self.mainWindow, self.index)
                    self.tabDialog.show()
                    return True
                else:
                    if self.mainWindow.ui.tabBar.tabAt(event.pos()) == 1:
                        print("BEGIN NEW SESSION, CREATE TYPING EXERCISE OBJECTS AND ADD DATE TO DATABASE")
                        self.typingExercise = TypingExercise(self.mainWindow, self.mainWindow.wordDeck)
                        self.typingExercise.resetUi()

                    elif self.mainWindow.ui.tabBar.tabAt(event.pos()) == 2:
                        self.flashcardExercise = FlashcardExercise(self.mainWindow, self.mainWindow.wordDeck)
                        self.flashcardExercise.resetUi()

                        print("BEGIN NEW SESSION, CREATE FLASHCARD EXERCISE OBJECTS AND ADD DATE TO DATABASE")

                    elif self.mainWindow.ui.tabBar.tabAt(event.pos()) == 3:
                        self.quizExercise = QuizExercise(self.mainWindow, self.mainWindow.wordDeck)  # Object for controlling quiz module
                        print("BEGIN NEW SESSION, CREATE QUIZ EXERCISE OBJECTS AND ADD DATE TO DATABASE")
                        self.quizExercise.resetUi()

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
