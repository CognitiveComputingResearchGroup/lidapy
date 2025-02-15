#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

from source.ActionSelection.Initialization.ConcreteActionSelectionFactory import \
    ConcreteActionSelectionFactory
from source.Module.ModuleSubject import ModuleNotifier
from source.SensoryMotorMemory.SensoryMotorAdapter import SensoryMotorAdapter


class ActionSelection(ConcreteActionSelectionFactory):
    def __init__(self, environment, sensory_motor):
        super().__init__()
        # Add modules relevant to action selection
        self.add_module("SensoryMotorAdapter",
                        SensoryMotorAdapter())
        self.add_module("environment", environment)
        self.add_module("notifier", ModuleNotifier())
        self.add_module("sensory_motor", sensory_motor)
        self.get_module("notifier").add_observer(
            self.get_module("SensoryMotorAdapter"))

        # Add attributes for this module
        self.add_attribute("scheme", None)
        self.add_attribute("state", None)

    def select_action(self, percept, action, module):
        self.get_module("SensoryMotorAdapter").notify_(
            self.get_attribute("state"), module, percept, action)

    def notify(self, scheme):
        self.update_attribute("scheme", scheme)
        self.update_attribute("state", scheme["State"])
        self.select_action(scheme["Percept"], scheme["Action"],
                           self.get_module("sensory_motor"))


















