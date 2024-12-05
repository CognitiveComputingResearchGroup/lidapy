#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

class ActionSelection:
    def __init__(self, action_space, procedural_memory, sensory_motor_memory):
        self.action_space = action_space # initialize with action space of the environment
        self.procedural_memory = procedural_memory
        self.sensory_motor_memory = sensory_motor_memory

    def select_action(self, percepts):
        for percept in percepts:
            action = self.procedural_memory.get_action(percept)
            if action is not None:
                self.notify_sensory_motor_memory(action)    #Notify sensory_motor_memory of the selected action
                return action

        self.notify_sensory_motor_memory(self.action_space.sample())
        return self.action_space.sample()  # if no action is found, use random action

    def notify_sensory_motor_memory(self, action):
        #The selected action is used to call sensory_motor_memory to action
        self.sensory_motor_memory.receive_action(action)