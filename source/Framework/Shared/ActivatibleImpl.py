from multiprocessing import Process, Value
from threading import Thread

from source.Framework.Strategies.LinearDecayStrategy import LinearDecayStrategy
from source.Framework.Strategies.LinearExciteStrategy import \
    LinearExciteStrategy
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
        self.decayStrategy = LinearDecayStrategy()
        self.exciteStrategy = LinearExciteStrategy()
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
            """self.logger.debug(f"Before decaying {self} has current "
                              f"activation: {self.getActivation()}")"""

            """Sharing of values between threads, d stands for float (double)
            Otherwise LinearDecayStrategy returns none without sharing"""
            activation = Value("d", self.getActivation())
            _ticks = Value("d", ticks)
            t = Thread(target=self.decayStrategy.decay, args=(activation,
                                                               _ticks))
            t.start()
            t.join()
            self.activation = activation.value
            incentiveSalience = Value("d", self.getIncentiveSalience())
            t = Thread(target=self.decayStrategy.decay,
                        args=(incentiveSalience, _ticks))
            t.start()
            t.join()

            self.incentiveSalience = incentiveSalience.value
            """self.logger.debug(f"After decaying {self} has current "
                                  f"activation: {self.getActivation()}")"""

    def exciteActivation(self, amount):
        if self.exciteStrategy is not None:
            """self.logger.debug(f"Before excitation {self} has current "
                              f"activation: {self.getActivation()}")"""

            """Sharing of values between threads, d stands for float (double)
               Otherwise LinearDecayStrategy returns none without sharing"""
            activation = Value("d", self.getActivation())
            _amount = Value("d", amount)
            t = Thread(target=self.exciteStrategy.excite, args=(activation,
                                                               _amount))
            t.start()
            t.join()
            self.activation = activation.value

            """self.logger.debug(f"After excitation {self} has current "
                              f"activation: {self.getActivation()}")"""

    def exciteIncentiveSalience(self, amount):
        if self.exciteStrategy is not None:
            self.logger.debug(f"Before excitation {self} has current "
                              f"incentive salience: "
                              f"{self.getIncentiveSalience()}")

            """Sharing of values between threads, d stands for float (double)
                Otherwise LinearDecayStrategy returns none without sharing"""
            incentiveSalience = Value("d", self.getIncentiveSalience())
            _amount = Value("d", amount)

            t = Thread(target=self.exciteStrategy.excite,
                       args=(incentiveSalience, _amount))
            t.start()
            t.join()

            self.incentiveSalience = incentiveSalience.value

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