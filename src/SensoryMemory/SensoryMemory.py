#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

#from Environment import Environment as env

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

    def run_sensors(self, procedural_memory, state_id: int=None, state=None, col=None, row=None):
        """All sensors associated will run with the memory"""
        #Logic to gather information from the environment
        #Example: Reading the current state or rewards
        if state_id == 0:
            state, info, col, row = self.environment.reset() # use environment instance to reset
        action = self.environment.action_space.sample() #Take a random action
        observation = self.environment.env.spec.kwargs.get("desc")
        start_tile = observation[0][0]

        state_str = "state-"
        state_id_str = state_id.__str__()
        state_str += state_id_str
        procedural_memory.add_scheme(state_str, action)
        percept = self.pam.retrieve_associations(state_str)  # retrieve percept from PAM
        return state, percept, action, self.environment, col, row # get state and percept from environment instance

    def get_sensory_content(self, state, outcome, modality=None, params=None):
        """
        Returning the content from this Sensory Memory
        :param modality: Specifing the modality
        :param params: optional parameters to filter or specify the content
        :return: content corresponding to the modality
        """
        self.pam.learn(state, outcome)
        #Logic to retrieve and return data based on the modality.
        return {"modality": modality, "params": params}
    '''
    def get_next_cell(self, observation, action, state, col, row):
        if action == 0:
            if col != 0:
                col -= 1
        elif action == 1:
            row += 1
        elif action == 2:
            col += 1
        elif action == 3:
            if row != 0:
                row -= 1

        cellContent = observation[row][col]
        if cellContent == 'H':
            action = self.self_correcting(observation, action, state, col, row, cellContent)
        return cellContent, action, col, row

    def self_correcting(self, observation, action, state, col, row, cellContent):
        action = self.environment.action_space.sample()  # Generate a new random action
        cellContent = self.get_next_cell(observation, action, state, col, row)
        return action
    '''