from abc import ABC, abstractmethod

from source.Module.ModuleSubject import ModuleSubject
from source.Module.ModuleObserver import ModuleObserver
from src.Framework.Tasks.TaskManager import TaskManager


class Module(ModuleObserver, ModuleSubject, TaskManager, ABC):

    @abstractmethod
    def notify(self, module):
        pass
