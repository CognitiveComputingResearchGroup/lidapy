import random

from source.ActionSelection.ActionSelection import ActionSelection
from source.GlobalWorkspace.GlobalWorkSpace import GlobalWorkspace
from source.ModuleInitialization.DefaultLogger import getLogger
from source.ProceduralMemory.ProceduralMemory import ProceduralMemory


class ActionSelectionImpl(ActionSelection):
    def __init__(self):
        super().__init__()
        # Add modules relevant to action selection
        self.scheme = {}
        self.logger = getLogger(self.__class__.__name__).logger
        self.logger.debug(f"Initialized ActionSelection")

    def select_action(self):
        return self.scheme

    def notify(self, module):
        if isinstance(module, ProceduralMemory):
            state = module.__getstate__()
            schemes = module.get_schemes(state)
            action = None

            random_index = random.randint(0, len(schemes) - 1)
            while schemes[random_index].getActivation() <= 0.5:
                random_index = random.randint(0, len(schemes) - 1)

            action = module.get_action(state, schemes[random_index])

            self.scheme = action
            if self.scheme is not None:
                self.logger.debug(
                    f"Action plan retrieved from instantiated "
                    f"schemes")
                self.notify_observers()
            else:
                self.logger.debug("No action found plan for the selected "
                                  "scheme")

        elif isinstance(module, GlobalWorkspace):
            winning_coalition = module.__getstate__()
