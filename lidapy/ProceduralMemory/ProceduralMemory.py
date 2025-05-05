#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo
from threading import Lock, RLock

from Module.Initialization.DefaultLogger import getLogger
from Module.Initialization.ModuleInterface import Module


class ProceduralMemory(Module):
    def __init__(self):
        super().__init__()
        self.scheme = None
        self.state = None
        self.schemes = {}  # initialize empty memory for schemes
        self.logger = getLogger(__class__.__name__).logger

    def start(self, scheme):
        pass

    def add_scheme(self, state, percept):
        lock = RLock()
        with lock:
            if not self.schemes or state not in self.schemes:
                self.schemes[state] = []  # add new scheme to memory
            if percept not in self.schemes[state]:
                self.schemes[state].append(percept)

    def add_scheme_(self, state, percept, schemes):
        lock = RLock()
        with lock:
            if not schemes or state not in schemes:
                schemes[state] = []  # add new scheme to memory
            schemes[state].append(percept)

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

    def get_schemes_(self, state, schemes):
        if schemes and state in schemes:
            return schemes[state]

    def get_state(self):
        return self.state

    def notify(self, module):
        pass