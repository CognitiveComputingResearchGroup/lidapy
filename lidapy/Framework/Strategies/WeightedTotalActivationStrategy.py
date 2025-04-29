from Framework.Strategies.TotalActivationStrategy import \
    TotalActivationStrategy

DEFAULT_BLA_WEIGHT = 0.1

class WeightedTotalActivationStrategyImpl(TotalActivationStrategy):
    def __init__(self):
        super().__init__()
        self.bla_weight = DEFAULT_BLA_WEIGHT

    def calculateTotalActivation(self, baseLevelActivation, currentActivation):
        sum = (self.bla_weight * baseLevelActivation + (
                    1 - self.bla_weight) * currentActivation) / 2
        if sum > 1.0:
            return 1.0
        else:
            return sum