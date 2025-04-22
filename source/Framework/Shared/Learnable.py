from lidapy.Framework.Shared.Activatible import Activatible

DEFAULT_LEARNABLE_REMOVAL_THRESHOLD = -1.0
DEFAULT_BASE_LEVEL_ACTIVATION = 0.5
DEFAULT_BASE_LEVEL_INCENTIVE_SALIENCE = 0.0

class Learnable(Activatible):
    def __init__(self):
        super().__init__()

    def getBaseLevelActivation(self):
        pass

    def setBaseLevelActivation(self, amount):
        pass

    def reinforceBaseLevelActivation(self, amount):
        pass

    def decayBaseLevelActivation(self, ticks):
        pass

    def getBaseLevelIncentiveSalience(self):
        pass

    def setBaseLevelIncentiveSalience(self, amount):
        pass

    def reinforceBaseLevelIncentiveSalience(self, amount):
        pass

    def decayBaseLevelIncentiveSalience(self, ticks):
        pass

    def setBaseLevelExciteStrategy(self, strategy):
        pass

    def getBaseLevelExciteStrategy(self):
        pass

    def setBaseLevelRemovalThreshold(self, threshold):
        pass

    def getBaseLevelRemovalThreshold(self):
        pass

    def getTotalActivationStrategy(self):
        pass

    def setTotalActivationStrategy(self, strategy):
        pass


