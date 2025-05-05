from Module.Initialization.DefaultLogger import getLogger
from Module.Initialization.ModuleInterface import Module


class Workspace(Module):
    def __init__(self):
        super().__init__()
        self.buffer = None
        self.logger = getLogger(self.__class__.__name__).logger

    def cueEpisodicMemories(self, node_structure):
        pass

    def notify(self, module):
        pass