from abc import abstractmethod

from Module.Initialization.ModuleInterface import Module


class Environment(Module):
    def __init__(self):
        super().__init__()
        self.args = None

    def notify(self, module):
        pass

    def get_state(self):
        pass

    # Resetting the environment to start a new episode
    def reset(self):
        pass

    # perform an action in environment:
    def step(self, action):
         pass

    # close the environment:
    def close(self):
        pass

    def get_stimuli(self):
        pass

    def get_position(self):
        pass