from source.ModuleInitialization.ModuleInterface import Module


class Workspace(Module):
    def __init__(self):
        super().__init__()
        self.observers = []
        self.percepts = []

    def addCueListener(self, cue_listener):
        pass

    def addWorkspaceListener(self, workspace_listener):
        pass

    def cueEpisodicMemories(self, node_structure):
        pass

    def notify(self, module):
        pass