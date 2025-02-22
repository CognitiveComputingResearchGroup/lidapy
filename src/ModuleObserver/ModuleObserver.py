from abc import ABC, abstractmethod


class ModuleObserver(ABC):
    def __init__(self):
        self.state = None

    @abstractmethod
    def notify(self, state):
        pass