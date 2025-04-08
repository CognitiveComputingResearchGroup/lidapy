from abc import ABC, abstractmethod


class ModuleObserver(ABC):

    @abstractmethod
    def notify(self, module):
        pass