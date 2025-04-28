import random


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
        self.logger.debug(f"Initialized ActionSelection")

    def start(self):
        pass

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
            schemes = module.get_schemes_(state, module.optimized_schemes)

            if schemes is None or len(schemes) <= 0:
                schemes = module.get_schemes(state)

            scheme = random.choice(schemes)
            self.add_behavior(state, scheme)

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
                    if source.getActivation() < 1:
                        links.append(link)
                else:
                    source_node = broadcast.getNode(source)
                    if isinstance(source_node, NodeImpl):
                        if source_node.getActivation() < 1:
                            links.append(link)
            self.update_behaviors(links)


    def update_behaviors(self, broadcast):
        behaviors = []
        for link in broadcast:
            source = link.getSource()
            if isinstance(source, NodeImpl):
                if (link.getActivation() < 0.5 and
                        link.getIncentiveSalience() <= 0.1):
                    behaviors = self.get_behaviors(source)
                    if behaviors is not None:
                        if isinstance(behaviors, list):
                            for behavior in behaviors:
                                self.remove_behavior(source, behavior)
                                behaviors.append(behavior)
                        else:
                            self.remove_behavior(source, behaviors)
                            behaviors.append(behaviors)

                else:
                    self.add_behavior(source, {
                        link.getCategory("label"): link.getCategory("id")})
                    behaviors.append({link.getCategory("label"):
                                          link.getCategory("id")})
        self.logger.debug(f"Updated {len(behaviors)} instantiated behaviors")