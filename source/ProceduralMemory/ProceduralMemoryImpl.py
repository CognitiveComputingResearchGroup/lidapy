#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

from threading import Lock

from source.GlobalWorkspace.GlobalWorkSpace import GlobalWorkspace
from source.PAM.PAM_Impl import PAMImpl
from source.ProceduralMemory.ProceduralMemory import ProceduralMemory


class ProceduralMemoryImpl(ProceduralMemory):
    def __init__(self):
        super().__init__()

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
