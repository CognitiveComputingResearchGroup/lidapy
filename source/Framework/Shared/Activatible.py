import threading

DEFAULT_INCENTIVE_SALIENCE = 0.0
DEFAULT_ACTIVATION = 0.0
DEFAULT_ACTIVATIBLE_REMOVAL_THRESHOLD = 0.0

class Activatible:
    def __init__(self):
        self.incentiveSalience = DEFAULT_INCENTIVE_SALIENCE
        self.activation = DEFAULT_ACTIVATION
        self.removal_threshold = DEFAULT_ACTIVATIBLE_REMOVAL_THRESHOLD
        self.lock = threading.Lock()

    def setActivation(self, value):
        pass

    def getActivation(self):
        return self.activation

    def setIncentiveSalience(self, value):
        pass

    def getIncentiveSalience(self):
        pass

    def setActivatibleRemovalThreshold(self, threshold):
        pass

    def getActivatibleRemovalThreshold(self):
        pass

    def isRemovable(self):
        pass

    def exciteActivation(self, amount):
        pass

    def exciteIncentiveSalience(self, amount):
        pass

    def setExciteStrategy(self, strategy):
        pass

    def getExciteStrategy(self):
        pass

    def setDecayStrategy(self, strategy):
        pass

    def getDecayStrategy(self):
        pass