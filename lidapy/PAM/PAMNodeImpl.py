from Framework.Shared.LearnableImpl import LearnableImpl
from Framework.Shared.NodeImpl import NodeImpl


class PAMNodeImpl(NodeImpl):
    def __init__(self):
        super().__init__()
        self.groundingPamNode = self
        self.learnable = LearnableImpl()

    def updateNodeValues(self, node):
        if isinstance(node, NodeImpl):
            self.learnable.setBaseLevelActivation(node.getActivation())

    def getActivation(self):
        return self.learnable.getActivation()

    def setActivation(self, value):
        self.learnable.setActivation(value)

    def getTotalActivation(self):
        self.learnable.getTotalActivation()

    def excite(self, amount):
        self.learnable.exciteActivation(amount)

    def exciteActivation(self, amount):
        self.learnable.exciteActivation(amount)

    def exciteIncentiveSalience(self, amount):
        self.learnable.exciteIncentiveSalience(amount)

    def getIncentiveSalience(self):
        return self.learnable.getIncentiveSalience()

    def getTotalIncentiveSalience(self):
        return self.learnable.getTotalIncentiveSalience()

    def setIncentiveSalience(self, value):
        self.learnable.setIncentiveSalience(value)

    def setExciteStrategy(self, strategy):
        self.learnable.setExciteStrategy(strategy)

    def getExciteStrategy(self):
        return self.learnable.getExciteStrategy()

    def decay(self, ticks):
        self.learnable.decay(ticks)

    def setDecayStrategy(self, strategy):
        self.learnable.setDecayStrategy(strategy)

    def getDecayStrategy(self):
       return self.learnable.getDecayStrategy()

    def setActivatibleRemovalThreshold(self, threshold):
        self.learnable.setActivatibleRemovalThreshold(threshold)

    def getActivatibleRemovalThreshold(self):
        return self.learnable.getActivatibleRemovalThreshold()

    def isRemovable(self):
        return self.learnable.isRemovable()

    def getBaseLevelActivation(self):
        return self.learnable.getBaseLevelActivation()

    def setBaseLevelActivation(self, value):
        self.learnable.setBaseLevelActivation(value)

    def reinforceBaseLevelActivation(self, amount):
        self.learnable.reinforceBaseLevelActivation(amount)

    def setBaseLevelExciteStrategy(self, strategy):
        self.learnable.setBaseLevelExciteStrategy(strategy)

    def getBaseLevelExciteStrategy(self):
        return self.learnable.getBaseLevelExciteStrategy()

    def decayBaseLevelActivation(self, ticks):
        self.learnable.decayBaseLevelActivation(ticks)

    def setBaseLevelDecayStrategy(self, strategy):
        self.learnable.setBaseLevelDecayStrategy(strategy)

    def getBaseLevelDecayStrategy(self):
        return self.learnable.getBaseLevelDecayStrategy()

    def setBaseLevelRemovalThreshold(self, threshold):
        self.learnable.setBaseLevelRemovalThreshold(threshold)

    def getBaseLevelRemovalThreshold(self):
        return self.learnable.getBaseLevelRemovalThreshold()

    def getTotalActivationStrategy(self):
        return self.learnable.getTotalActivationStrategy()

    def setTotalActivationStrategy(self, strategy):
        self.learnable.setTotalActivationStrategy(strategy)

    def getBaseLevelIncentiveSalience(self):
        return self.learnable.getBaseLevelIncentiveSalience()

    def setBaseLevelIncentiveSalience(self, value):
        self.learnable.setBaseLevelIncentiveSalience(value)

    def decayBaseLevelIncentiveSalience(self, ticks):
        self.learnable.decayBaseLevelIncentiveSalience(ticks)

    def reinforceBaseLevelIncentiveSalience(self, amount):
        self.learnable.reinforceBaseLevelIncentiveSalience(amount)