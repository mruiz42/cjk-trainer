class VocabWord:

    def __init__(self, cn, v, d, p="", starred=False, tc = 0, tm = 0):
        self.cardNum = cn
        self.vocabulary = v
        self.definition = d
        self.pronunciation = p
        self.timesCorrect = tc
        self.timesAttempted = tm
        self.isStarred = False

    def __str__(self):
        return self.vocabulary + "," + self.definition + self.pronunciation + str(self.timescorrect) + str(self.timesattempted) + str(self.isStarred)
