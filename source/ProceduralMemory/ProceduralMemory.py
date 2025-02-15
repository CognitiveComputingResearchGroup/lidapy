#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

from source.ActionSelection.ActionSelectionAdapter import ActionSelectionAdapter
from source.Module.ModuleSubject import ModuleNotifier
from source.ProceduralMemory.Initialization.ConcreteProceduralMemoryFactory import \
    ConcreteProceduralMemoryFactory


class ProceduralMemory(ConcreteProceduralMemoryFactory):
    def __init__(self, action_selection=None):
        super().__init__()
        # Add relevant modules
        self.add_module("ActionSelectionAdapter",
                        ActionSelectionAdapter())
        self.add_module("notifier", ModuleNotifier())
        self.get_module("notifier").add_observer(self.get_module(
            "ActionSelectionAdapter"))
        self.add_module("action_selection", action_selection)

        # Add attributes relevant to module
        self.add_attribute("percept", None)

        # initialize empty memory for schemes
        self.schemes = {}

    def add_scheme(self, percept, action):
        self.schemes[percept] = action # add new scheme to memory
        # percept: percept cue ("goal", "safe", or "danger")
        # action: corresponding action or scheme

    def get_action(self, percept):
        return self.get_attribute("schemes").get(percept, None) # get action for the percept
        # return corresponding action or None if not found

    def notify(self, percept):
        self.update_attribute("percept",  percept["Percept"])
        self.add_scheme(self.get_attribute("percept"), percept["Action"])
        self.get_module("ActionSelectionAdapter").notify(percept,
                                        self.get_module("action_selection"))