import random


from source.ActionSelection.ActionSelection import ActionSelection
from source.GlobalWorkspace.GlobalWorkSpaceImpl import GlobalWorkSpaceImpl
from source.Module.Initialization.DefaultLogger import getLogger
from source.ProceduralMemory.ProceduralMemoryImpl import ProceduralMemoryImpl


class ActionSelectionImpl(ActionSelection):
    def __init__(self):
        super().__init__()
        # Add modules relevant to action selection
        self.behaviors = {}
        self.action = None
        self.state = None
        self.logger = getLogger(self.__class__.__name__).logger

    def start(self):
        self.logger.debug(f"Initialized ActionSelection")

    def add_behavior(self, state, behavior):
        if not self.behaviors or state not in self.behaviors:
            self.behaviors[state] = []  # add new scheme to memory
        if behavior not in self.behaviors[state]:
            self.behaviors[state].append(behavior)

    def remove_behavior(self, state, behavior):
        if self.behaviors and state in self.behaviors:
            self.behaviors[state].remove(behavior)

    def get_state(self):
        return self.state

    def get_behaviors(self, state):
        if self.behaviors and state in self.behaviors:
            return self.behaviors[state]

    def select_action_plan(self, state):
        if self.behaviors and state in self.behaviors:
            return self.behaviors[state]
        # return corresponding action(s) or None if not found

    def notify(self, module):
        if isinstance(module, ProceduralMemoryImpl):
            state = module.get_state()
            self.state = state
            schemes = module.get_schemes(state)
            if schemes:
                scheme = random.choice(schemes)
                self.add_behavior(state,scheme)

            if self.behaviors is not None:
                self.logger.debug(
                    f"Behaviors retrieved from instantiated schemes")
            else:
                self.logger.debug("No behaviors found for the selected scheme")
            self.notify_observers()

        elif isinstance(module, GlobalWorkSpaceImpl):
            winning_coalition = module.get_broadcast()
            broadcast = winning_coalition.getContent()
            self.logger.debug(f"Received conscious broadcast: {broadcast}")
            self.update_behaviors(broadcast)


    def update_behaviors(self, broadcast):
        behaviors = []
        for node in broadcast.getNodes():
            if node.getActivation() < 0.5 and node.getIncentiveSalience() <= 0:
                    saved_behaviors = self.get_behaviors(node)
                    if saved_behaviors is not None:
                        if isinstance(saved_behaviors, list):
                            for behavior in saved_behaviors:
                                self.remove_behavior(node, behavior)
                                behaviors.append(behavior)
                        else:
                            self.remove_behavior(node, saved_behaviors)
                            behaviors.append(saved_behaviors)

            else:
                content = node.getLabel()
                if content and isinstance(content, dict):
                    for key, value in content.items():
                        self.add_behavior(node, key)
                        behaviors.append(key)
        self.logger.debug(f"Updated {len(behaviors)} instantiated behaviors")