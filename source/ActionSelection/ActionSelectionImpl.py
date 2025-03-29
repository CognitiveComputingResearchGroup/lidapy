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

    def select_action(self):
        return self.scheme

    def notify(self, module):
        if isinstance(module, ProceduralMemory):
            state = module.environment.get_state()["state"]
            actions = module.get_action(state, "goal")

            if not actions:
                actions = module.get_action(state, "safe")
            if not actions:
                actions = module.get_action(state, "start")
            if not actions:
                self.logger.warning("Danger ahead, falling back to safety!")

            action = random.choice(actions)
            self.scheme = action
        elif isinstance(module, GlobalWorkspace):
            winning_coalition = module.getWinningCoalition()

        self.notify_observers()
