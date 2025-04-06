from abc import ABC, abstractmethod
from source.Module.Initialization.ModuleInterface import Module

class Agent(Module, ABC):

    # Implement to start to interact with an environment
    @abstractmethod
    def run(self):
        pass

    def notify(self, module):
        pass

    def get_state(self):
        pass