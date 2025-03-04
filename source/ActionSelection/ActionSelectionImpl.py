from source.ActionSelection.ActionSelection import ActionSelection
from source.ProceduralMemory.ProceduralMemory import ProceduralMemory


class ActionSelectionImpl(ActionSelection):
    def __init__(self, sensory_motor_memory):
        super().__init__()
        # Add modules relevant to action selection
        self.add_observer(sensory_motor_memory)
        self.scheme = {}

    def select_action(self):
        return self.scheme

    def notify(self, module):
        if isinstance(module, ProceduralMemory):
            action = module.get_action("goal")

            if action is None:
                action = module.get_action("safe")
            if action is None:
                action = module.get_action("start")
            """if action is None:
                action = module.get_action("danger")"""

            self.scheme = action
            self.notify_observers()