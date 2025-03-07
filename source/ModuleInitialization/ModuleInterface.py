from abc import ABC, abstractmethod
from source.ModuleSubject.ModuleObservable import ModuleSubject
from source.ModuleSubject.ModuleObserver import ModuleObserver


class Module(ModuleObserver, ModuleSubject, ABC):

    @abstractmethod
    def notify(self, module):
        pass
