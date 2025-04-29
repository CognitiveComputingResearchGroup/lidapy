#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG481
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

"""
This module can temporarily store sensory data from the environment and then
process and transfer to further working memory.
"""

from ActionSelection.ActionSelection import ActionSelection
from Framework.Shared.NodeImpl import NodeImpl
from GlobalWorkspace.GlobalWorkSpaceImpl import GlobalWorkSpaceImpl
from Module.Initialization.DefaultLogger import getLogger
from SensoryMotorMemory.SensoryMotorMemory import SensoryMotorMemory


class SensoryMotorMemoryImpl(SensoryMotorMemory):
    def __init__(self):
        super().__init__()
        self.action_plan = None
        self.state = None
        self.logger = getLogger(__class__.__name__).logger
        self.logger.debug("Initialized SensoryMotorMemory")

    def start(self):
        pass

    def notify(self, module):
        """The selected action from action selection"""
        #Logic to gather information from the environment
        #Example: Reading the current state or rewards
        self.action_plan = []
        if isinstance(module, ActionSelection):
            state = module.get_state()
            self.state = state
            self.action_event = module.select_action_plan(state)
            if self.action_event is not None:
                self.logger.debug("Retrieved motor plan(s) from action plan")
                if isinstance(self.action_event, list):
                    for action_plan in self.action_event:
                        self.action_plan.append(action_plan)
                self.notify_observers()

        elif isinstance(module, GlobalWorkSpaceImpl):
            winning_coalition = module.get_broadcast()
            broadcast = winning_coalition.getContent()
            """Get the nodes that have been previously visited and learn from 
            them"""
            links = []
            self.logger.debug(f"Received conscious broadcast: {broadcast}")
            for link in broadcast.getLinks():
                source = link.getSource()
                if isinstance(source, NodeImpl):
                    if source.getActivation() < 1:
                        links.append(link)
                else:
                    source_node = broadcast.containsNode(source)
                    if isinstance(source_node, NodeImpl):
                        if source_node.getActivation() < 1:
                            links.append(link)
            self.learn(links)

    def send_action_execution_command(self):
        return self.action_plan

    def get_state(self):
        return self.state

    def learn(self, broadcast):
        for link in broadcast:
            if (link.getActivation() >= 0.5 and link.getIncentiveSalience() >=
                    0.1):
                self.action_plan.append({link.getCategory("label") :
                                             link.getCategory("id")})