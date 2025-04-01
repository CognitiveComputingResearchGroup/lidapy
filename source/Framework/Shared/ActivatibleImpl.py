from source.ModuleInitialization.DefaultLogger import getLogger
from source.Framework.Shared.Activatible import Activatible

DECAY_DEFAULT_SLOPE = 0.1
DECAY_DEFAULT_LOWER_BOUND = 0.0
EXCITE_DEFAULT_SLOPE = 1.0
EXCITE_DEFAULT_UPPER_BOUND=1.0
EXCITE_DEFAULT_LOWER_BOUND = 0.0

class ActivatibleImpl(Activatible):
    def __init__(self):
        super().__init__()
        self.decayStrategy = None
        self.exciteStrategy = None
        self.incentiveSalienceDecayStrategy = None
        self.activation = 0.0
        self.logger = getLogger(self.__class__.__name__).logger

    def setActivation(self, value):
        if value > 1.0:
            self.activation = 1.0
        elif value < -1.0:
            self.activation = -1.0
        else:
            self.activation = value

    def getActivation(self):
        return self.activation

    def setIncentiveSalience(self, value):
        if value > 1.0:
            self.incentiveSalience = 1.0
        elif value < -1.0:
            self.incentiveSalience = -1.0
        else:
            self.incentiveSalience = value

    def getIncentiveSalience(self):
        return self.incentiveSalience

    def setActivatibleRemovalThreshold(self, threshold):
        self.removal_threshold = threshold

    def getActivatibleRemovalThreshold(self):
        return self.removal_threshold

    def isRemovable(self):
        return (self.activation <= self.removal_threshold and
                abs(self.incentiveSalience) <= self.removal_threshold)

    def decay(self, ticks):
        if self.decayStrategy is not None:
            self.logger.debug(f"Before decaying {self} has current "
                              f"activation: {self.getActivation()}")
            self.activation = self.calcActivationLinearDecay(
                    self.activation, ticks)
            self.incentiveSalience = self.calcActivationLinearDecay(
                    self.incentiveSalience, ticks)
            self.logger.debug(f"After decaying {self} has current "
                                  f"activation: {self.getActivation()}")
        else:
            """self.logger.debug(f"Before decaying {self} has current "
                              f"activation: {self.getActivation()}")"""
            self.setActivation(self.calcActivationLinearDecay(
                self.getActivation(), ticks))
            self.setIncentiveSalience(self.calcActivationLinearDecay(
                self.incentiveSalience, ticks))

            """self.logger.debug(f"After decaying {self} has current "
                              f"activation: {self.getActivation()}")"""

    def exciteActivation(self, amount):
        if self.exciteStrategy is not None:
            self.logger.debug(f"Before excitation {self} has current "
                              f"activation: {self.getActivation()}")
            self.activation = self.calcActivationLinearExcite(
                    self.getActivation(), amount)

            self.logger.debug(f"After excitation {self} has current "
                              f"activation: {self.getActivation()}")
        else:
            """self.logger.debug(f"Before excitation {self} has current "
                              f"activation: {self.getActivation()}")"""
            self.activation = self.calcActivationLinearExcite(
                    self.getActivation(), amount)

            """self.logger.debug(f"After excitation {self} has current "
                              f"activation: {self.getActivation()}")"""

    def exciteIncentiveSalience(self, amount):
        if self.exciteStrategy is not None:
            self.logger.debug(f"Before excitation {self} has current "
                              f"incentive salience: "
                              f"{self.getIncentiveSalience()}")
            self.activation = self.calcActivationLinearExcite(
                    self.getIncentiveSalience(), amount)

            self.logger.debug(f"After excitation {self} has current "
                              f"incentive salience: "
                              f"{self.getIncentiveSalience()}")

    def calcActivationLinearDecay(self, current_activation, ticks):
        slope = DECAY_DEFAULT_SLOPE
        lower_bound = DECAY_DEFAULT_LOWER_BOUND
        current_activation -= slope * ticks
        if current_activation > lower_bound:
            return current_activation
        else:
            return lower_bound

    def calcActivationLinearExcite(self, current_activation, ticks):
        slope = EXCITE_DEFAULT_SLOPE
        upper_bound = EXCITE_DEFAULT_UPPER_BOUND
        lower_bound = EXCITE_DEFAULT_LOWER_BOUND
        current_activation += slope * ticks
        if current_activation > upper_bound:
                return upper_bound
        elif current_activation < lower_bound:
            return lower_bound
        return current_activation

    def setExciteStrategy(self, strategy):
        self.exciteStrategy = strategy

    def getExciteStrategy(self):
        return self.exciteStrategy

    def setDecayStrategy(self, strategy):
        self.decayStrategy = strategy

    def getDecayStrategy(self):
        return self.decayStrategy

    def setIncentiveSalienceDecayStrategy(self, strategy):
        self.incentiveSalienceDecayStrategy = strategy

    def getIncentiveSalienceDecayStrategy(self):
        return self.incentiveSalienceDecayStrategy