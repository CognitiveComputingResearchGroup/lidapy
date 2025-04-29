from abc import ABC, abstractmethod

from Module.ModuleSubject import ModuleSubject
from Module.ModuleObserver import ModuleObserver


class Module(ModuleObserver, ModuleSubject, ABC):

    @abstractmethod
    def notify(self, module):
        pass
