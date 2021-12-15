from src.VocabWordDeck import *
class FlashcardExercise():
    def __init__(self, main_window, word_deck, parent=None):
        super(FlashcardExercise, self).__init__()
        self.mainWindow = main_window
        self.wordDeck = word_deck

    def resetUi(self):
        self.mainWindow.ui.progressBar_flashcards.reset()
