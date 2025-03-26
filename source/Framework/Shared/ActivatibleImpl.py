from source.Framework.Strategies.LinearDecayStrategy import LinearDecayStrategy
from source.Framework.Strategies.LinearExciteStrategy import \
    LinearExciteStrategy
from source.ModuleInitialization.DefaultLogger import getLogger
from source.Framework.Shared.Activatible import Activatible


class ActivatibleImpl(Activatible):
    def __init__(self):
        super().__init__()
        self.decayStrategy = LinearDecayStrategy()
        self.exciteStrategy = LinearExciteStrategy()
        self.incentiveSalienceDecayStrategy = LinearDecayStrategy()
        self.logger = getLogger(self.__class__.__name__).logger

    def setActivation(self, value):
        if value > 1.0:
            with self.lock:
                self.activation = 1.0
        elif value < -1.0:
            with self.lock:
                self.activation = -1.0
        else:
            with self.lock:
                self.activation = value

    def getActivation(self):
        return self.activation

    def setIncentiveSalience(self, value):
        if value > 1.0:
            with self.lock:
                self.incentiveSalience = 1.0
        elif value < -1.0:
            with self.lock:
                self.incentiveSalience = -1.0
        else:
            with self.lock:
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
        if self.exciteStrategy is not None:
            self.logger.debug(f"Before decaying {self} has current "
                              f"activation: {self.getActivation()}")
            with self.lock:
                self.activation = self.decayStrategy.decay(
                    self.getActivation(), ticks)
                self.incentiveSalience = self.incentiveSalienceDecayStrategy.decay(
                    self.getIncentiveSalience(), ticks)

            self.logger.debug(f"After decaying {self} has current "
                              f"activation: {self.getActivation()}")

    def exciteActivation(self, amount):
        if self.exciteStrategy is not None:
            self.logger.debug(f"Before excitation {self} has current "
                              f"activation: {self.getActivation()}")
            with self.lock:
                self.activation = self.exciteStrategy.excite(
                    self.getActivation(), amount)

            self.logger.debug(f"After excitation {self} has current "
                              f"activation: {self.getActivation()}")

    def exciteIncentiveSalience(self, amount):
        if self.exciteStrategy is not None:
            self.logger.debug(f"Before excitation {self} has current "
                              f"incentive salience: "
                              f"{self.getIncentiveSalience()}")
            with self.lock:
                self.activation = self.exciteStrategy.excite(
                    self.getIncentiveSalience(), amount)

            self.logger.debug(f"After excitation {self} has current "
                              f"incentive salience: "
                              f"{self.getIncentiveSalience()}")

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