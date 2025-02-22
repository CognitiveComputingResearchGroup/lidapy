from source.ActionSelection.ActionSelection import ActionSelection
from source.ProceduralMemory.ProceduralMemory import ProceduralMemory


class ActionSelectionImpl(ActionSelection):
    def __init__(self, procedural_memory):
        super().__init__()
        # Add modules relevant to action selection
        self.add_observer(procedural_memory)
        self.scheme = {}

    def select_action(self):
        return self.scheme

    def notify(self, module):
        if isinstance(module, ProceduralMemory):
            self.scheme = module.get_action(module)