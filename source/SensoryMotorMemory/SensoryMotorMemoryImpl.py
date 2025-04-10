#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG481
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

"""
This module can temporarily store sensory data from the environment and then
process and transfer to further working memory.
"""
import random

from source.ActionSelection.ActionSelection import ActionSelection
from source.Framework.Shared.NodeImpl import NodeImpl
from source.GlobalWorkspace.GlobalWorkSpace import GlobalWorkspace
from source.GlobalWorkspace.GlobalWorkSpaceImpl import GlobalWorkSpaceImpl
from source.Module.Initialization.DefaultLogger import getLogger
from source.SensoryMemory.SensoryMemory import SensoryMemory
from source.SensoryMotorMemory.SensoryMotorMemory import SensoryMotorMemory


class SensoryMotorMemoryImpl(SensoryMotorMemory):
    def __init__(self):
        super().__init__()
        self.action_event = None
        self.action_plan = None
        self.logger = getLogger(__class__.__name__).logger
        #self.logger.debug("Initialized SensoryMotorMemory")

    def run(self):
        self.logger.debug("Initialized SensoryMotorMemory")

    def notify(self, module):
        """The selected action from action selection"""
        #Logic to gather information from the environment
        #Example: Reading the current state or rewards
        self.action_plan = []
        if isinstance(module, SensoryMemory):
            cue = module.get_sensory_content(module)["cue"]
            iterations = random.randint(0, len(cue) - 1)
            while cue[iterations].getCategory("label") == "hole":
                iterations = random.randint(0, len(cue) - 1)
            self.action_event = cue[iterations].getCategory("id")

            if self.action_event is not None:
                self.logger.debug("Retrieved motor plan(s) from action plan")
                if isinstance(self.action_event, list):
                    for action in self.action_event:
                        self.action_plan.append(action)
                #self.notify_observers()

        elif isinstance(module, ActionSelection):
            self.action_event = module.get_action()
            if self.action_event is not None:
                self.logger.debug("Retrieved motor plan(s) from action plan")
                if isinstance(self.action_event, list):
                    for action in self.action_event:
                        self.action_plan.append(action)
                self.notify_observers()

        elif isinstance(module, GlobalWorkSpaceImpl):
            winning_coalition = module.get_broadcast()
            broadcast = winning_coalition.getContent()
            """Get the nodes that have been previously visited and learn from 
            them"""
            links = []
            for link in broadcast.getLinks():
                source = link.getSource()
                if isinstance(source, NodeImpl):
                    if link.getSource().getActivation() < 1:
                        links.append(link)
            if len(links) == 0:
                source = broadcast.containsNode()
                links = broadcast.getConnectedSinks(source)
            self.logger.debug(f"Received conscious broadcast: {broadcast}")
            self.learn(links)

    def send_action_event(self):
        return self.action_event

    def send_action_execution_command(self):
        return self.action_plan

    def learn(self, broadcast):
        pass