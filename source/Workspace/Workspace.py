from source.ModuleInitialization.ModuleInterface import Module


class Workspace(Module):
    def __init__(self):
        super().__init__()
        self.observers = []

    def cueEpisodicMemories(self, node_structure):
        pass

    def notify(self, module):
        pass