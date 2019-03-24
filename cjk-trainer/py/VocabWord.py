class VocabWord:

    def __init__(self, v, r, d, tc = 0, tm = 0):
        self.vocabulary = v
        self.romanization = r
        self.definition = d
        self.timescorrect = tc
        self.timesattempted = tm
        self.isStarred = False

    def __str__(self):
        return self.vocabulary + "," + self.definition
