#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

from threading import Lock

from source.GlobalWorkspace.GlobalWorkSpace import GlobalWorkspace
from source.PAM.PAM_Impl import PAMImpl
from source.ProceduralMemory.ProceduralMemory import ProceduralMemory


class PerceptualAssociativeMemoryImpl:
    pass


class ProceduralMemoryImpl(ProceduralMemory):
    def __init__(self, action_selection, environment):
        super().__init__(environment=environment)
        if action_selection is not None:
            self.add_observer(action_selection)
        self.lock = Lock()

    def notify(self, module):
        if isinstance(module, PAMImpl):
            state = module.__getstate__()["state"]["state"]
            associations = module.retrieve_associations(state)

            for association in associations:
                for key, value in association.items():
                    action = value
                    self.add_scheme(state, key, action)
            self.notify_observers()
        elif isinstance(module, GlobalWorkspace):
            winning_coalition = module.getWinningCoalition()
