#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

#from Environment import Environment as env
from Environment.Environment import FrozenLakeEnvironment
from PAM.PAM import PerceptualAssociativeMemory

"""
This module can temporarily store sensory data from the environment and then
process and transfer to further working memory.
"""

class SensoryMemory:
    def __init__(self, environment, pam):
        self.listeners = [] #initializing an empty list to store the listeners
        self.environment = environment  # store environment reference
        self.pam = pam # reference to perceptual associative memory

    def add_sensory_listener(self, listener):
        """Adding the listener to the memory"""
        self.listeners.append(listener) #appending the listener to the list

    def run_sensors(self):
        """All sensors associated will run with the memory"""
        #Logic to gather information from the environment
        #Example: Reading the current state or rewards
        state, info = self.environment.reset() # use environment instance to reset
        percept = self.pam.retrieve_associations(state) # retrieve percept from PAM
        #return state, percept # get state and percept from environment instance
        return state, info # get state and info from environment instance

    def get_sensory_content(self, modality=None, params=None):
        """
        Returning the content from this Sensory Memory
        :param modality: Specifing the modality
        :param params: optional parameters to filter or specify the content
        :return: content corresponding to the modality
        """
        #Logic to retrieve and return data based on the modality.
        return {"modality": modality, "params": params}