from source.Module.Initialization.DefaultLogger import getLogger
from source.Module.Initialization.ModuleInterface import Module


class Workspace(Module):
    def __init__(self):
        super().__init__()
        self.logger = getLogger(self.__class__.__name__).logger

    def cueEpisodicMemories(self, node_structure):
        pass

    def notify(self, module):
        pass