#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo
from source.ModuleInitialization.ModuleInterface import Module


class ProceduralMemory(Module):
    def __init__(self, environment):
        super().__init__()
        self.schemes = {}  # initialize empty memory for schemes
        self.observers = []
        self.environment = environment

    def add_scheme(self, state, percept, action):
        if self.schemes.__eq__(None) or state not in self.schemes:
            self.schemes[state] = {}  # add new scheme to memory
            self.schemes[state][percept] = action
        # percept: percept cue ("goal", "safe", or "danger")
        # action: corresponding action or scheme

    def get_action(self, state, percept):
        return self.schemes[state].get(percept, None)  # get action for the percept
        # return corresponding action or None if not found

    def notify(self, module):
        pass