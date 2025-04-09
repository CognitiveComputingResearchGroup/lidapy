from abc import ABC, abstractmethod

from source.Module.ModuleSubject import ModuleSubject
from source.Module.ModuleObserver import ModuleObserver


class Module(ModuleObserver, ModuleSubject, ABC):

    @abstractmethod
    def notify(self, module):
        pass
