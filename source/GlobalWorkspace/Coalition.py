from source.Framework.Shared.Activatible import Activatible
from source.Module.Initialization.ModuleInterface import Module


class Coalition(Module, Activatible):
    def __init__(self):
        super().__init__()
        self.observers = []

    def notify(self, module):
        pass

    def getContent(self):
        pass

    def setContent(self, broadcast_content):
        pass

    def getCreatingAttentionCodelet(self):
        pass

    def setCreatingAttentionCodelet(self, attention_codelet):
        pass

    def getID(self):
        pass