from multiprocessing import Value
from threading import Lock, Thread, RLock

from source.Framework.Shared.Learnable import Learnable, \
    DEFAULT_BASE_LEVEL_ACTIVATION, DEFAULT_LEARNABLE_REMOVAL_THRESHOLD, \
    DEFAULT_BASE_LEVEL_INCENTIVE_SALIENCE
from source.Framework.Strategies.LinearDecayStrategy import LinearDecayStrategy
from source.Framework.Shared.ActivatibleImpl import ActivatibleImpl
from source.Framework.Strategies.LinearExciteStrategy import LinearExciteStrategy
from source.Framework.Strategies.WeightedTotalActivationStrategy import \
    WeightedTotalActivationStrategyImpl


class LearnableImpl(Learnable, ActivatibleImpl):
    def __init__(self):
        super().__init__()
        self.baseLevelActivation = DEFAULT_BASE_LEVEL_ACTIVATION
        self.learnableRemovalThreshold = DEFAULT_LEARNABLE_REMOVAL_THRESHOLD
        self.baseLevelIncentiveSalience = (
            DEFAULT_BASE_LEVEL_INCENTIVE_SALIENCE)
        self.baseLevelExciteStrategy = LinearExciteStrategy()
        self.baseLevelDecayStrategy = LinearDecayStrategy()
        self.totalActivationStrategy = WeightedTotalActivationStrategyImpl()

    def decay(self, ticks):
        self.decayBaseLevelActivation(ticks)
        self.decayBaseLevelIncentiveSalience(ticks)
        super().decay(ticks)

    def isRemovable(self):
        return (self.baseLevelActivation <= self.learnableRemovalThreshold and
                abs(self.baseLevelIncentiveSalience) <=
                self.learnableRemovalThreshold)

    def getTotalIncentiveSalience(self):
        return self.totalActivationStrategy.calculateTotalActivation(
            self.getBaseLevelIncentiveSalience(), self.getIncentiveSalience())

    def getTotalActivation(self):
        return self.totalActivationStrategy.calculateTotalActivation(
            self.getBaseLevelActivation(), self.getActivation())

    def getBaseLevelActivation(self):
        return self.baseLevelActivation

    def setBaseLevelActivation(self, amount):
        if amount > 1.0:
            self.baseLevelActivation = 1.0
        elif amount < -1.0:
            self.baseLevelActivation = -1.0
        else:
            self.baseLevelActivation = amount

    def reinforceBaseLevelActivation(self, amount):
        if self.baseLevelExciteStrategy is not None:
            """self.logger.debug(f"Before reinforcement {self} has base-level "
                            f"activation: {self.getBaseLevelActivation()}")"""

            """Sharing of values between threads, d stands for float (double)
               Otherwise LinearDecayStrategy returns none without sharing"""
            lock = RLock()
            with lock:
                activation = Value("d", self.getBaseLevelActivation())
                _amount = Value("d", amount)
                t = Thread(target=self.baseLevelExciteStrategy.excite,
                           args=(activation, _amount))
                t.start()
                t.join()
                self.activation = activation.value
            """self.logger.debug(f"After reinforcement {self} has base-level "
                            f"activation: {self.getBaseLevelActivation()}")"""

    def decayBaseLevelActivation(self, ticks):
        if self.baseLevelDecayStrategy is not None:
            """self.logger.debug(f"Before decaying {self} has base-level "
                            f"activation: {self.getBaseLevelActivation()}")"""

            """Sharing of values between threads, d stands for float (double)
               Otherwise LinearDecayStrategy returns none without sharing"""
            lock = RLock()
            with lock:
                activation = Value("d", self.getBaseLevelActivation())
                _amount = Value("d", ticks)
                t = Thread(target=self.baseLevelDecayStrategy.decay,
                           args=(activation, _amount))
                t.start()
                t.join()
                self.activation = activation.value
            """self.logger.debug(f"After decaying {self} has base-level "
                            f"activation: {self.getBaseLevelActivation()}")"""

    def getBaseLevelIncentiveSalience(self):
        return self.baseLevelIncentiveSalience

    def setBaseLevelIncentiveSalience(self, amount):
        if amount > 1.0:
            self.baseLevelIncentiveSalience = 1.0
        elif amount < -1.0:
            self.baseLevelIncentiveSalience = -1.0
        else:
            self.baseLevelIncentiveSalience = amount

    def reinforceBaseLevelIncentiveSalience(self, amount):
        if self.baseLevelExciteStrategy is not None:
            """self.logger.debug(f"Before reinforcement {self} has base-level "
               f"IncentiveSalience: {self.getBaseLevelIncentiveSalience()}")"""

            """Sharing of values between threads, d stands for float (double)
               Otherwise LinearDecayStrategy returns none without sharing"""
            lock = RLock()
            with lock:
                incentiveSalience = Value("d",
                                          self.getBaseLevelIncentiveSalience())
                _amount = Value("d", amount)
                t = Thread(target=self.baseLevelExciteStrategy.excite,
                           args=(incentiveSalience, _amount))
                t.start()
                t.join()
                self.incentiveSalience = incentiveSalience.value
            """self.logger.debug(f"After reinforcement {self} has base-level "
               f"IncentiveSalience: {self.getBaseLevelIncentiveSalience()}")"""

    def decayBaseLevelIncentiveSalience(self, ticks):
        if self.baseLevelDecayStrategy is not None:
            """self.logger.debug(f"Before decaying {self} has base-level "
               f"IncentiveSalience: {self.getBaseLevelIncentiveSalience()}")"""

            """Sharing of values between threads, d stands for float (double)
               Otherwise LinearDecayStrategy returns none without sharing"""
            lock = RLock()
            with lock:
                incentiveSalience = Value("d",
                                          self.getBaseLevelIncentiveSalience())
                _amount = Value("d", ticks)
                t = Thread(target=self.baseLevelDecayStrategy.decay,
                           args=(incentiveSalience, _amount))
                t.start()
                t.join()
                self.incentiveSalience = incentiveSalience.value
            """self.logger.debug(f"After decaying {self} has base-level "
               f"IncentiveSalience: {self.getBaseLevelIncentiveSalience()}")"""

    def setBaseLevelExciteStrategy(self, strategy):
        self.baseLevelExciteStrategy = strategy

    def getBaseLevelExciteStrategy(self):
        return self.baseLevelExciteStrategy

    def setBaseLevelDecayStrategy(self, strategy):
        self.baseLevelDecayStrategy = strategy

    def getBaseLevelDecayStrategy(self):
        return self.baseLevelDecayStrategy

    def setBaseLevelRemovalThreshold(self, threshold):
        self.learnableRemovalThreshold = threshold

    def getBaseLevelRemovalThreshold(self):
        return self.learnableRemovalThreshold

    def getTotalActivationStrategy(self):
        return self.totalActivationStrategy

    def setTotalActivationStrategy(self, strategy):
        self.totalActivationStrategy = strategy