from source.Module.Initialization.ModuleInterface import Module


class CurrentSituationalModel(Module):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.coalition = None

    def addBufferContent(self, workspace_content):
        pass

    def getBufferContent(self):
        pass

    def decayModule(self, time):
        pass

    def getModuleContent(self):
        pass

    def receiveVentralStream(self, stream):
        pass

    def receiveCoalition(self, coalition):
        pass

    def notify(self, module):
        pass