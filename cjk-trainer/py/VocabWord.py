class VocabWord:

    def __init__(self, cn, isStarred, v, d, p = "", tc = 0, ta = 0, ds = ""):
        self.cardNum = cn
        self.isStarred = isStarred
        self.vocabulary = v
        self.definition = d
        self.pronunciation = p
        self.timesAttempted = ta
        self.timesCorrect = tc
        self.dateStudied = ds
    def __str__(self):

        return self.vocabulary + "," + self.definition + "," + self.pronunciation +\
               ", c" + str(self.timesCorrect) + ":a" + str(self.timesAttempted)

