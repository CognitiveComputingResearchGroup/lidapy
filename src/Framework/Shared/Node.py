from Framework.Shared.Activatible import Activatible


class Node(Activatible):
    def __init__(self):
        super().__init__()
        self.id = 0
        self.label = "Node"
        self.name = ""

    def getGroundingPamNode(self):
        pass

    def setGroundingPamNode(self, node):
        pass

    def getId(self):
        return self.id

    def setId(self, identity):
        self.id = identity
        self.updateName()

    def getLabel(self):
        return self.label

    def setLabel(self, label):
        self.label = label
        self.updateName()

    def getName(self):
        return self.name

    def updateName(self):
        self.name = self.label + "[" + str(self.id) + "]"

    def updateNodeValues(self, node):
        pass