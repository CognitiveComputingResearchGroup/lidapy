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
        if not self.schemes or state not in self.schemes:
            self.schemes[state] = {}  # add new scheme to memory
        self.schemes[state][action] = percept
        # percept: percept cue ("goal", "safe", or "danger")
        # action: corresponding action or scheme

    def get_action(self, state, percept):
        actions = []
        for key, value in self.schemes[state].items():
            if value == percept:
                actions.append(key)
        return actions              # get all possible action for the percept
        # return corresponding action or None if not found

    def notify(self, module):
        pass