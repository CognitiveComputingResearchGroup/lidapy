from source.Framework.Shared.Link import Link


class LinkImpl(Link):
    def __init__(self):
        super().__init__()
        self.grounding_pam_link = None
        self.category = {"id" : self.id,
                         "label" : self.label}

    def getSource(self):
        return self.source

    def setSource(self, source):
        self.source = source

    def getSink(self):
        return self.sink

    def setSink(self, sink):
        self.sink = sink

    def getCategory(self):
        return self.category

    def setCategory(self, key, value):
        self.category[key] = value

    def setGroundingPamLink(self, grounding_pam_link):
        self.grounding_pam_link = grounding_pam_link

    def getGroundingPamLink(self):
        return self.grounding_pam_link