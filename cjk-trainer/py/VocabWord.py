class VocabWord:

    def __init__(self, cn, isStarred, v, d, p = "", tc = 0, ta = 0, da = ""):
        self.cardNum = cn
        self.isStarred = isStarred
        self.vocabulary = v
        self.definition = d
        self.pronunciation = p
        self.timesAttempted = ta
        self.timesCorrect = tc
        self.dateStudied = da
    def __str__(self):
        return self.vocabulary + "," + self.definition + self.pronunciation + str(self.timesCorrect) + str(self.timesAttempted)

