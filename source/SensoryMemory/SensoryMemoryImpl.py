# LIDA Cognitive Framework
# Pennsylvania State University, Course : SWENG480
# Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

from source.Environment.Environment import Environment
from source.Framework.Agents.Agent import Agent
from source.SensoryMemory.SensoryMemory import SensoryMemory


"""
This module can temporarily store sensory data from the environment and then
process and transfer to further working memory.
"""


class SensoryMemoryImpl(SensoryMemory):
    def __init__(self, environment=None, pam=None, sensory_motor_memory=None):
        super().__init__()
        # Add observers to the subject
        if pam is not None:
            self.add_observer(pam)
        if sensory_motor_memory is not None:
            self.add_observer(sensory_motor_memory)

        self.state = None
        self.action = None

    def notify(self, module):
        if isinstance(module, Agent):
            self.state = module.get_state()
            self.run_sensors(self.state, module)

    def run_sensors(self, state=None, module=None):
        """All sensors associated will run with the memory"""
        # Logic to gather information from the environment
        # Example: Reading the current state or rewards
        # Sample an action from environment action space
        self.action = module.environment.env.action_space.sample()
        self.notify_observers()

    def get_sensory_content(self, modality=None, params=None):
        """
        Returning the content from this Sensory Memory
        :param modality: Specifying the modality
        :param params: optional parameters to filter or specify the content
        :return: content corresponding to the modality
        """

        # Logic to retrieve and return data based on the modality.
        return {"state": self.state, "action": self.action,
                "modality": modality, "params": params}