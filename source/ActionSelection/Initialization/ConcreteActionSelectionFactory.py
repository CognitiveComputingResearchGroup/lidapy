from source.ActionSelection.Initialization.ActionSelectionFactory import \
    ActionSelectionFactory
from source.GlobalModuleInterface.GlobalModuleFactory import GlobalModuleFactory


class ConcreteActionSelectionFactory(ActionSelectionFactory,
                                     GlobalModuleFactory):
    def __init__(self):
        super().__init__()

    def create_action_selection(self, action_selection):
        return action_selection

    def select_action(self, percept, action, module):
        pass

    def notify(self, scheme):
        pass