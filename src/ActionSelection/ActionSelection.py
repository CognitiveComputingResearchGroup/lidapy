#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

class ActionSelection:
    def __init__(self, action_space, procedural_memory):
        self.action_space = action_space # initialize with action space of the environment
        self.procedural_memory = procedural_memory
       #self.sensory_motor_memory = sensory_motor_memory

    def select_action(self, percepts, state_id, sensory_motor_memory):
        for percept in percepts:
            action = self.procedural_memory.get_action(percept)
            if action is not None:
                state, reward, done, truncated, info = (
                    self.notify_sensory_motor_memory(action, sensory_motor_memory))    #Notify sensory_motor_memory of the selected action
                state_id += 1    #Increment the state identifier
                return state, state_id, reward, done, truncated, info

        state, reward, done, truncated, info = (
            self.notify_sensory_motor_memory(self.action_space.sample(), sensory_motor_memory))
            #self.notify_sensory_motor_memory(self.action_space.sample()))  # if no action is found, use random action
        #return state, reward, done, truncated, info
        return state, state_id, reward, done, truncated, info

    def notify_sensory_motor_memory(self, action, sensory_motor_memory):
        #The selected action is used to call sensory_motor_memory to action
        state, reward, done, truncated, info = sensory_motor_memory.receive_action(action)
        return state, reward, done, truncated, info


















