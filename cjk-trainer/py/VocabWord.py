class VocabWord:

    def __init__(self, cn, v, d, p="", isStarred=False, ta = 0, tc = 0):
        self.cardNum = cn
        self.vocabulary = v
        self.definition = d
        self.pronunciation = p
        self.isStarred = isStarred
        self.timesAttempted = ta
        self.timesCorrect = tc

    def __str__(self):
        return self.vocabulary + "," + self.definition + self.pronunciation + str(self.timesCorrect) + str(self.timesAttempted)
