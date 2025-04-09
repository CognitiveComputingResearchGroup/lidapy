from source.Framework.Shared.ActivatibleImpl import ActivatibleImpl
from source.Framework.Shared.Link import Link


class LinkImpl(Link, ActivatibleImpl):
    def __init__(self):
        super().__init__()
        self.grounding_pam_link = None
        self.category = {"id" : self.id,
                         "label" : self.label}
        self.type = None

    def getSource(self):
        return self.src

    def setSource(self, src):
        self.src = src

    def getSink(self):
        return self.sink

    def setType(self, link_type):
        self.type = link_type

    def getType(self):
        return self.type

    def setSink(self, sink):
        self.sink = sink

    def getCategory(self, key):
        return self.category[key]

    def setCategory(self, id, label):
        self.category["id"] = id
        self.category["label"] = label

    def setGroundingPamLink(self, grounding_pam_link):
        self.grounding_pam_link = grounding_pam_link

    def getGroundingPamLink(self):
        return self.grounding_pam_link