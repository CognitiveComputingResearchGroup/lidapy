#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

from source.Module.ModuleSubject import ModuleNotifier
from source.PAM.PAMAdapter import PAMAdapter
from source.SensoryMemory.Initialization.ConcreteSensoryMemoryFactory import \
    ConcreteSensoryMemoryFactory

"""
This module can temporarily store sensory data from the environment and then
process and transfer to further working memory.
"""

class CliffWalkingSensoryMem(ConcreteSensoryMemoryFactory):
    def __init__(self, environment=None, pam=None, agent=None):
        super().__init__()
        # store environment reference
        self.add_module("environment", environment)

        # reference to perceptual associative memory
        self.add_module("pam", pam)

        # current agent
        self.add_module("agent", agent)

        # PAM observer/notifier
        self.add_module("notifier", ModuleNotifier())
        self.add_module("PAMAdapter", PAMAdapter())

        #self.listeners = [] #initializing listener class
        self.add_attribute("state", None)

    def notify(self, state):
        self.update_attribute("state", state)

    def run_sensors(self, state=None, col=None, row=None, agent=None):
        """All sensors associated will run with the memory"""
        #Logic to gather information from the environment
        #Example: Reading the current state or rewards
        if state is None:
            # Use environment instance to reset
            state, info, col, row = (
                self.get_module("environment").reset(self))
        else:
            col, row = (self.get_module("environment").get_attribute("col"),
                        self.get_module("environment").get_attribute("row"))

        #Sample an action from environment action space
        action = (self.get_module("environment").get_attribute("action_space").
                  sample())

        #Bundle state, environment, and action info into dictionary
        event = {"state": state, "position": [row, col],
                 "action": action}

        #Notify PAM of agent's state, surroundings and possible actions
        self.get_module("PAMAdapter").notify(event, self.get_module("pam"))

    def get_sensory_content(self, state, outcome, modality=None, params=None):
        """
        Returning the content from this Sensory Memory
        :param modality: Specifying the modality
        :param params: optional parameters to filter or specify the content
        :return: content corresponding to the modality
        """
        self.get_module("pam").learn(state, outcome)
        #Logic to retrieve and return data based on the modality.
        return {"modality": modality, "params": params}