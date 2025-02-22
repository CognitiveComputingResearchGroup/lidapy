from src.ActionSelection.ActionSelection import ActionSelection
from src.ModuleObserver.ModuleObserver import ModuleObserver


class ActionSelectionAdapter(ModuleObserver):
    def __init__(self):
        super().__init__()
        self.outcome = None
        #self.ActionSelection = ActionSelection()

    def notify(self, outcome=None):
        return ActionSelection.notify(self.outcome)