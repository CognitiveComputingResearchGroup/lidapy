#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo
from source.ModuleInitialization.ModuleInterface import Module


class ActionSelection(Module):
    def __init__(self):
        super().__init__()
        self.observers = []

    def select_action(self):
        pass

    def notify(self, module):
        pass


















