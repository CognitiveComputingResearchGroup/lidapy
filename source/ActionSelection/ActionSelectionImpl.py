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
            action = module.get_action(state["state"], state["scheme"])

            self.scheme = action
            if self.scheme is not None:
                self.notify_observers()
        elif isinstance(module, GlobalWorkspace):
            winning_coalition = module.__getstate__()
