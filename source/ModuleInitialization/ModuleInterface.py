from abc import ABC, abstractmethod
from source.ModuleSubject.ModuleObservable import ModuleSubject
from src.ModuleObserver.ModuleObserver import ModuleObserver


class Module(ModuleObserver, ModuleSubject, ABC):

    @abstractmethod
    def notify(self, module):
        pass