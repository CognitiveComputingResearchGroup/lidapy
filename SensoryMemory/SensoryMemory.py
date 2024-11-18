#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

from Environment import Environment as env

class SensoryMemory:
    def __init__(self):
        self.listeners = [] #initializing an empty list to store the listeners

    def add_sensory_listener(self, listener):
        """Adding the listener to the memory"""
        self.listeners.append(listener) #appending the listener to the list

    def run_sensors(self):
        """All sensors associated will run with the memory"""
        #Logic to gather information from the environment
        #Example: Reading the current state or rewards
        state, _ = env.reset()
        return state

    def get_sensory_content(self, modality=None, params=None):
        """
        Returning the content from this Sensory Memory
        :param modality: Specifing the modality
        :param params: optional parameters to filter or specify the content
        :return: content corresponding to the modality
        """

        #Logic to retrieve and return data based on the modality.
        return {"modality": modality, "params": params}