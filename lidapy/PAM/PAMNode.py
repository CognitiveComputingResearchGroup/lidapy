from Framework.Shared.Node import Node


class PAMNode(Node):
    def __init__(self):
        super().__init__()
        self.groundingPamNode = None
        self.learnable = None

    def updateNodeValues(self, node):
        pass

    def getActivation(self):
        pass

    def setActivation(self, value):
        pass

    def getTotalActivation(self):
        pass

    def excite(self, amount):
        pass

    def exciteActivation(self, amount):
        pass

    def exciteIncentiveSalience(self, amount):
        pass

    def getIncentiveSalience(self):
        pass

    def getTotalIncentiveSalience(self):
        pass

    def setIncentiveSalience(self, value):
        pass

    def setExciteStrategy(self, strategy):
        pass

    def getExciteStrategy(self):
        pass

    def decay(self, ticks):
        pass

    def setDecayStrategy(self, strategy):
        pass

    def getDecayStrategy(self):
        pass

    def setActivatibleRemovalThreshold(self, threshold):
        pass

    def getActivatibleRemovalThreshold(self):
        pass

    def isRemovable(self):
        pass

    def getBaseLevelActivation(self):
        pass

    def setBaseLevelActivation(self, value):
        pass

    def reinforceBaseLevelActivation(self, amount):
        pass

    def setBaseLevelExciteStrategy(self, strategy):
        pass

    def getBaseLevelExciteStrategy(self):
        pass

    def decayBaseLevelActivation(self, ticks):
        pass

    def setBaseLevelDecayStrategy(self, strategy):
        pass

    def getBaseLevelDecayStrategy(self):
        pass

    def setBaseLevelRemovalThreshold(self, threshold):
        pass

    def getBaseLevelRemovalThreshold(self):
        pass

    def getTotalActivationStrategy(self):
        pass

    def setTotalActivationStrategy(self, strategy):
        pass

    def getBaseLevelIncentiveSalience(self):
        pass

    def setBaseLevelIncentiveSalience(self, value):
        pass

    def decayBaseLevelIncentiveSalience(self, ticks):
        pass

    def reinforceBaseLevelIncentiveSalience(self, amount):
        pass

    def notify(self, module):
        pass