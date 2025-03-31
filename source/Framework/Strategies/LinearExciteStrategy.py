from source.Framework.Strategies.ExciteStrategy import ExciteStrategy

DEFAULT_SLOPE = 1.0
DEFAULT_UPPER_BOUND=1.0
DEFAULT_LOWER_BOUND = 0.0
class LinearExciteStrategy(ExciteStrategy):
    def __init__(self):
        super().__init__()
        self.slope = DEFAULT_SLOPE
        self.upper_bound = DEFAULT_UPPER_BOUND
        self.lower_bound = DEFAULT_LOWER_BOUND

    def excite(self, current_activation, ticks, params=None):
        if params is not None and params.length != 0:
            self.slope = params[0]
        self.calcActivation(current_activation, ticks)

    def excite_(self, current_activation, ticks, params=None):
        if params is not None and params["slope"] is not None:
            self.slope = params["slope"]
        self.calcActivation(current_activation, ticks)

    def calcActivation(self, current_activation, ticks):
        current_activation += self.slope * ticks
        if current_activation > self.upper_bound:
                return self.upper_bound
        elif current_activation < self.lower_bound:
            return self.lower_bound

        return current_activation