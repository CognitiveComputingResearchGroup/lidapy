from source.ModuleInitialization.Codelet import Codelet
from source.ModuleInitialization.ModuleInterface import Module


class AttentionCodelet(Module, Codelet):
    def __init__(self, current_situational_model, global_workspace):
        super().__init__()
        self.observers = []

    def notify(self, module):
        pass