from abc import ABC, abstractmethod

class Environment(ABC):

    @abstractmethod
    def get_state(self):
        pass