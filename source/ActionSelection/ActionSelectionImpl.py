import random
from time import sleep


from source.ActionSelection.ActionSelection import ActionSelection
from source.Framework.Shared.NodeImpl import NodeImpl
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

    def run(self):
        self.logger.debug(f"Initialized ActionSelection")

    def add_behavior(self, state, behavior):
        if not self.behaviors or state not in self.behaviors:
            self.behaviors[state] = []  # add new scheme to memory
        self.behaviors[state].append(behavior)

    def remove_behavior(self, state, behavior):
        if self.behaviors and state in self.behaviors:
            self.behaviors[state].remove(behavior)

    def get_action(self):
        return self.action

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
            action = None

            random_index = random.randint(0, len(schemes) - 1)
            while schemes[random_index].getActivation() <= 0.5:
                random_index = random.randint(0, len(schemes) - 1)

            self.add_behavior(state,
        {schemes[random_index].getCategory("label") :
                schemes[random_index].getCategory("id")})

            schemes[random_index].decay(0.01)
            if schemes[random_index].isRemovable():
                module.schemes.remove(schemes[random_index])
            else:
                self.action = module.get_action(state, schemes[random_index])

            if self.behaviors is not None:
                self.logger.debug(
                    f"Behaviors retrieved from instantiated schemes")
                self.notify_observers()
            else:
                self.logger.debug("No behaviors found for the selected scheme")

        elif isinstance(module, GlobalWorkSpaceImpl):
            winning_coalition = module.get_broadcast()
            broadcast = winning_coalition.getContent()
            self.logger.debug(f"Received conscious broadcast: {broadcast}")
            """Get the nodes that have been previously visited and update
            the connected sink links"""
            links = []
            for link in broadcast.getLinks():
                source = link.getSource()
                if isinstance(source, NodeImpl):
                    if link.getSource().getActivation() < 1:
                        links.append(link)
            if len(links) == 0:
                source = broadcast.containsNode()
                links = broadcast.getConnectedSinks(source)
            self.update_behaviors(links)


    def update_behaviors(self, broadcast):
        for link in broadcast:
            if link.getCategory("label") != "hole":
                self.add_behavior(link.getSource(), {
                    link.getCategory("label"): link.getCategory("id")})
            behaviors = self.get_behaviors(link.getSource())
            if behaviors is not None:
                for behavior in behaviors:
                    for key, value in behavior.items():
                        if key == "hole":
                            self.remove_behavior(link.getSource(), behavior)

        self.logger.debug("Updated instantiated behaviors")