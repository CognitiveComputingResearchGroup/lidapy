from Framework.Shared.Activatible import Activatible


class Link(Activatible):
    def __init__(self):
        super().__init__()
        self.sink = None
        self.src = None
        self.label = ""
        self.id = 0

    def getSource(self):
        pass

    def setSource(self, src):
        pass

    def getSink(self):
        pass

    def setSink(self, sink):
        pass

    def setType(self, link_type):
        pass

    def getType(self):
        pass

    def getCategory(self, key):
        pass

    def setCategory(self, key, value):
        pass

    def setGroundingPamLink(self, grounding_pam_link):
        pass

    def getGroundingPamLink(self):
        pass
