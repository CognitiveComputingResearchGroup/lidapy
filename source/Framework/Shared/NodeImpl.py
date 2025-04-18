from source.Framework.Shared.ActivatibleImpl import ActivatibleImpl
from source.Framework.Shared.Node import Node

class NodeImpl(Node, ActivatibleImpl):
    def __init__(self):
        super().__init__()
        self.groundingPAMNode = None

    def getGroundingPamNode(self):
        return self.groundingPAMNode

    def setGroundingPamNode(self, node):
        self.groundingPAMNode = node

    def updateNodeValues(self, node):
        if isinstance(node, NodeImpl):
            self.setIncentiveSalience(node.getIncentiveSalience())
