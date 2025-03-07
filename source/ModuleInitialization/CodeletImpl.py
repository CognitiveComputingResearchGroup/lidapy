from source.ModuleInitialization.Codelet import Codelet
from source.ModuleInitialization.ModuleInterface import Module


class CodeletImpl(Codelet):
    def __init__(self):
        super().__init__()
        self.soughtContent  = Module()

    def getSoughtContent(self):
        return self.soughtContent

    def setSoughtContent(self, content):
        self.soughtContent = content