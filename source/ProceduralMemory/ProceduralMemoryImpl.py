#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

from source.PAM.PAM import PerceptualAssociativeMemory
from source.ProceduralMemory.ProceduralMemory import ProceduralMemory


class ProceduralMemoryImpl(ProceduralMemory):
    def __init__(self, action_selection, environment):
        super().__init__(environment=environment)
        if action_selection is not None:
            self.add_observer(action_selection)

    def notify(self, module):
        if isinstance(module, PerceptualAssociativeMemory):
            state = module.get_state()["state"]["state"]
            associations = module.retrieve_associations(state)
            action = module.get_state()["action"]
            for association in associations:
                self.add_scheme(state, association, action)
            self.notify_observers()
