#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo
from time import sleep

from source.ModuleInitialization.DefaultLogger import getLogger
from source.ModuleInitialization.ModuleInterface import Module


class ProceduralMemory(Module):
    def __init__(self):
        super().__init__()
        self.scheme = None
        self.state = None
        self.schemes = {}  # initialize empty memory for schemes
        self.logger = getLogger(__class__.__name__).logger

    def run(self, scheme):
        self.scheme = scheme
        while self.state is None:
            sleep(45)

    def add_scheme(self, state, percept):
        if not self.schemes or state not in self.schemes:
            self.schemes[state] = []  # add new scheme to memory
        self.schemes[state].append(percept)

    def receive_broadcast(self, coalition):
        self.logger.debug(f"Received broadcast coalition {coalition}")

    def get_action(self, state, percept):
        if self.schemes and state in self.schemes:
            if percept in self.schemes[state]:
                return percept.getCategory("id")
        # return corresponding action(s) or None if not found

    def get_schemes(self, state):
        if self.schemes and state in self.schemes:
            return self.schemes[state]

    def __getstate__(self):
        return self.state

    def notify(self, module):
        pass