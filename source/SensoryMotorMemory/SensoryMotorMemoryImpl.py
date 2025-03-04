#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

"""
This module can temporarily store sensory data from the environment and then
process and transfer to further working memory.
"""
from source.ActionSelection.ActionSelection import ActionSelection
from source.SensoryMemory.SensoryMemory import SensoryMemory
from source.SensoryMotorMemory.SensoryMotorMemory import SensoryMotorMemory


class SensoryMotorMemoryImpl(SensoryMotorMemory):
    def __init__(self, environment):
        super().__init__()
        if environment is not None:
            self.add_observer(environment)

        self.event = None

    def notify(self, module):
        """The selected action from action selection"""
        #Logic to gather information from the environment
        #Example: Reading the current state or rewards
        if isinstance(module, SensoryMemory):
            self.event = module.get_sensory_content(module)["action"]
        elif isinstance(module, ActionSelection):
            self.event = module.select_action()
        self.notify_observers()

    def receive_action(self):
        return self.event