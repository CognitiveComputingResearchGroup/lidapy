#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

class ActionSelection:
    def __init__(self, action_space, procedural_memory):
        self.action_space = action_space # initialize with action space of the environment
        self.procedural_memory = procedural_memory

    def select_action(self, percepts):
        for percept in percepts:
            action = self.procedural_memory.get_action(percept)
            if action is not None:
                return action

        return self.action_space.sample()  # if no action is found, use random action