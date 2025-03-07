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
            state = module.environment.get_state()["state"]
            action = module.get_action(state, "goal")

            if action is None:
                action = module.get_action(state, "safe")
            if action is None:
                action = module.get_action(state, "start")
            if action is None:
                action = module.get_action(state, "danger")

            self.scheme = action
            self.notify_observers()