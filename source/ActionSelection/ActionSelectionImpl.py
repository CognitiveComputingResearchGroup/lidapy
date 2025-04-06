import random
from time import sleep

from numpy import broadcast

from source.ActionSelection.ActionSelection import ActionSelection
from source.GlobalWorkspace.GlobalWorkSpaceImpl import GlobalWorkSpaceImpl
from source.Module.Initialization.DefaultLogger import getLogger
from source.ProceduralMemory.ProceduralMemory import ProceduralMemory
from source.ProceduralMemory.ProceduralMemoryImpl import ProceduralMemoryImpl


class ActionSelectionImpl(ActionSelection):
    def __init__(self):
        super().__init__()
        # Add modules relevant to action selection
        self.behaviors = {}
        self.action = None
        self.state = None
        self.logger = getLogger(self.__class__.__name__).logger

    def run(self):
        self.logger.debug(f"Initialized ActionSelection")

    def get_action(self):
        return self.action

    def select_action(self, percept):
        if self.behaviors and percept in self.behaviors:
            return self.behaviors[percept]
        # return corresponding action(s) or None if not found

    def notify(self, module):
        if isinstance(module, ProceduralMemoryImpl):
            state = module.get_state()
            self.state = state
            if (module.get_schemes_(state, module.near_goal_schemes) is not
                    None and len(
                        module.get_schemes_(state, module.near_goal_schemes))
                    > 0):
                schemes = module.get_schemes_(state, module.near_goal_schemes)
            else:
                schemes = module.get_schemes(state)
            action = None

            for scheme in schemes:
                self.behaviors[scheme.getCategory("label")] = (
                    scheme.getCategory("id"))

            random_index = random.randint(0, len(schemes) - 1)
            while schemes[random_index].getActivation() <= 0.5:
                random_index = random.randint(0, len(schemes) - 1)

            self.action = module.get_action(state, schemes[random_index])

            if self.action is not None:
                self.logger.debug(
                    f"Action plan retrieved from instantiated "
                    f"schemes")
                sleep(0.2)
                self.notify_observers()
            else:
                self.logger.debug("No action found plan for the selected "
                                  "scheme")

        elif isinstance(module, GlobalWorkSpaceImpl):
            winning_coalition = module.get_broadcast()
            broadcast = winning_coalition.get_broadcast()
            self.logger.debug(f"Received conscious broadcast: {broadcast}")
            self.update_behaviors(broadcast.getConnectedSinks(self.state))


    def update_behaviors(self, broadcast):
        links = broadcast.get_links()
        for link in links:
            if link.getAction() >= 0.5:
                if self.behaviors[link.getCategory("label")] is not None:
                    #If the link exists in current behaviors, update behavior
                    if (link.getSource() ==
                        self.behaviors[link.getCategory("label")].getSource()):
                            self.behaviors[link.getCategory("label"
                                                            )] = link
        self.logger.debug("Updated instantiated behaviors")