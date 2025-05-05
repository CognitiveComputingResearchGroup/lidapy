#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG481
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

"""
This module can temporarily store sensory data from the environment and then
process and transfer to further working memory.
"""
from ActionSelection.ActionSelection import ActionSelection
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
            self.logger.debug(f"Received conscious broadcast: {broadcast}")
            self.learn(broadcast)

    def send_action_execution_command(self):
        return self.action_plan

    def get_state(self):
        return self.state

    def learn(self, broadcast):
        for node in broadcast.getNodes():
            if (node.getActivation() >= 0.5 and node.getIncentiveSalience() >=
                    0.1):
                for key, value in node.getLabel().items():
                    self.action_plan.append(key)