#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

"""
This module can temporarily store sensory data from the environment and then
process and transfer to further working memory.
"""
import random

from source.ActionSelection.ActionSelection import ActionSelection
from source.GlobalWorkspace.GlobalWorkSpace import GlobalWorkspace
from source.ModuleInitialization.DefaultLogger import getLogger
from source.SensoryMemory.SensoryMemory import SensoryMemory
from source.SensoryMotorMemory.SensoryMotorMemory import SensoryMotorMemory


class SensoryMotorMemoryImpl(SensoryMotorMemory):
    def __init__(self):
        super().__init__()
        self.event = None
        self.logger = getLogger(__class__.__name__).logger
        #self.logger.debug("Initialized SensoryMotorMemory")

    def run(self):
        self.logger.debug("Initialized SensoryMotorMemory")

    def notify(self, module):
        """The selected action from action selection"""
        #Logic to gather information from the environment
        #Example: Reading the current state or rewards
        if isinstance(module, SensoryMemory):
            cue = module.get_sensory_content(module)["cue"]
            iterations = random.randint(1, 5)
            index = 0
            for link in cue:
                if (link.getCategory("label") == "G" or
                        link.getCategory("label") == "F" or
                        link.getCategory("label") == "S"):
                    self.event = link.getCategory("id")
                    if index == iterations:
                        break
                    else:
                        index += 1
            if self.event is not None:
                self.notify_observers()
                self.logger.debug("Retrieved motor plan(s) from action plan")
        elif isinstance(module, ActionSelection):
            self.event = module.select_action()
            if self.event is not None:
                self.logger.debug("Retrieved motor plan(s) from action plan")
                self.notify_observers()
        elif isinstance(module, GlobalWorkspace):
            winning_coalition = module.__getstate__()

    def receive_action(self):
        return self.event