#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo
from source.ModuleInitialization.DefaultLogger import getLogger
from source.ModuleInitialization.ModuleInterface import Module


class ProceduralMemory(Module):
    def __init__(self):
        super().__init__()
        self.schemes = {}  # initialize empty memory for schemes
        self.logger = getLogger(__class__.__name__).logger

    def add_scheme(self, state, percept, action):
        if not self.schemes or state not in self.schemes:
            self.schemes[state] = {}  # add new scheme to memory
        self.schemes[state][action] = percept

    def receive_broadcast(self, coalition):
        self.logger.debug(f"Received broadcast coalition {coalition}")

    def get_action(self, state, percept):
        actions = []
        for key, value in self.schemes[state].items():
            if value == percept:
                actions.append(key)
        return actions              # get all possible action for the percept
        # return corresponding action or None if not found

    def notify(self, module):
        pass