#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG481
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

"""
This module can temporarily store sensory data from the environment and then
process and transfer to further working memory.
"""
from multiprocessing import Process
from threading import Thread
from time import sleep

from source.ActionSelection.ActionSelection import ActionSelection
from source.GlobalWorkspace.GlobalWorkSpaceImpl import GlobalWorkSpaceImpl
from source.Module.Initialization.DefaultLogger import getLogger
from source.SensoryMotorMemory.SensoryMotorMemory import SensoryMotorMemory


class SensoryMotorMemoryImpl(SensoryMotorMemory):
    def __init__(self):
        super().__init__()
        self.action_plan = []
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
            behaviors = module.select_action_plan(state)
            if behaviors:
                self.logger.debug("Retrieved behavior(s) from action plan")
                if isinstance(behaviors, list):
                    for behavior in behaviors:
                        action_plans = behavior.getCategory("label")
                        if action_plans and isinstance(action_plans, list):
                            for action_plan in action_plans:
                                self.action_plan.append(action_plan)
                        elif action_plans and isinstance(action_plans, dict):
                            for key, value in action_plans.items():
                                self.action_plan.append(value)
                        else:
                            if action_plans:
                                self.action_plan.append(action_plans)
                else:
                    self.action_plan.append(behaviors.getCategory("label"))
            self.notify_observers()

        elif isinstance(module, GlobalWorkSpaceImpl):
            winning_coalition = module.get_broadcast()
            broadcast = winning_coalition.getContent()
            self.logger.debug(f"Received conscious broadcast: {broadcast}")
            thread = Thread(target=self.learn, args=(broadcast,))
            thread.start()

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