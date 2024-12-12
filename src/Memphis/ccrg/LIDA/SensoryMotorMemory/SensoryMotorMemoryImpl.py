#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

#from Environment import Environment as env

"""
This module can temporarily store sensory data from the environment and then
process and transfer to further working memory.
"""

class SensoryMotorMemoryImpl:
    def __init__(self, action, motor_plan):
        self.listeners = [] #initializing an empty list to store the listeners
        self.action = action  # store selected_action reference
        self.motor_plan = motor_plan # reference to the motor_plan that will be executed

    def add_sensory_listener(self, listener):
        """Adding the listener to the memory"""
        self.listeners.append(listener) #appending the listener to the list

    def receive_action(self, action):
        """The selected action from action selection"""
        #Logic to gather information from the environment
        #Example: Reading the current state or rewards
        self.action = action
        state, reward, done, truncated, info = self.send_action_execution_command(action)
        '''
        #state, info = self.environment.reset() # use environment instance to reset
        #percept = self.pam.retrieve_associations(state) # retrieve percept from PAM
        #return state, percept # get state and percept from environment instance
        #return state, info # get state and info from environment instance
        '''
        return state, reward, done, truncated, info


    def send_action_execution_command(self, action_plan):
        """
        Returning the content from this Sensory Motor Memory
        :param action_plan: Specifying the action(s) to take
        :return: content corresponding to the action_plan
        """
        #Logic to retrieve and return data based on the modality.
        state, reward, done, truncated, info = self.motor_plan.execute(action_plan)
        return state, reward, done, truncated, info
        #return {"modality": modality, "params": params}