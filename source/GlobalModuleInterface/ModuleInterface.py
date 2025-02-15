from abc import ABC, abstractmethod

class Module(ABC):

    @abstractmethod
    def notify(self, module):
        pass