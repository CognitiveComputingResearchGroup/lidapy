#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo
from source.ModuleInitialization.ModuleInterface import Module


"""
This module can temporarily store sensory data from the environment and then
process and transfer to further working memory.
"""

class SensoryMemory(Module):
    def __init__(self, pam=None, sensory_motor_memory=None):
        super().__init__()
        self.observers = []

    def notify(self, module):
        pass

    def run_sensors(self, state=None, module=None):
        """All sensors associated will run with the memory"""
        #Logic to gather information from the environment
        #Example: Reading the current state or rewards
        pass

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