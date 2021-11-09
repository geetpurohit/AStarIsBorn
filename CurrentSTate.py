import numpy as np

class currstate:
    def __init__(self, x, y, actualBlockedStatus: bool):
        self.location = np.array([x, y])
        self.actualBlockStatus = actualBlockedStatus
        self.discoveredBlockStatus = False
        self.search = self.g = self.h = 0
        self.f = self.g + self.h
        self.treePointer = None

    def updatef(self):
        self.f = self.g + self.h
