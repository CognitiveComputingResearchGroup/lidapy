from source.Framework.Strategies.DecayStrategy import DecayStrategy

DEFAULT_SLOPE = 0.1
DEFAULT_LOWER_BOUND = 0.0
class LinearDecayStrategy(DecayStrategy):
    def __init__(self):
        super().__init__()
        self.slope = DEFAULT_SLOPE
        self.lower_bound = DEFAULT_LOWER_BOUND

    def decay(self, current_activation, ticks, params=None):
        slope = self.slope
        if params is not None and params.length != 0:
            slope = params[0]
        self.calcActivation(current_activation, ticks, slope)

    def decay_(self, current_activation, ticks, params=None):
        slope = self.slope
        if params is not None and params["slope"] is not None:
            slope = params["slope"]
        self.calcActivation(current_activation, ticks, slope)

    def calcActivation(self, current_activation, ticks, slope):
        current_activation -= slope * ticks
        if current_activation > self.lower_bound:
            return current_activation
        else:
            return self.lower_bound