from source.PAM.PAM import PerceptualAssociativeMemory
from source.Workspace.CurrentSituationModel.CurrentSituationModelImpl import \
    CurrentSituationalModelImpl
from source.Workspace.Workspace import Workspace
from source.ModuleInitialization.DefaultLogger import getLogger


class WorkspaceImpl(Workspace):
    def __init__(self, csm):
        super().__init__()
        self.logger = getLogger(self.__class__.__name__)
        self.nodes = []
        self.add_observer(PerceptualAssociativeMemory)
        self.csm = csm
        self.winning_coalition = None

    def cueEpisodicMemories(self, node_structure):
        self.notify_observers()
        self.logger.info("Cue performed.")

    def get_module_content(self , params=None):
        return {"Nodes" : self.nodes,
                "Winning Coalition" : self.winning_coalition}

    def receive_broadcast(self, coalition):
        self.winning_coalition = coalition
        self.csm.receiveCoalition(coalition)
        self.csm.notify_observers()

    def receive_percept(self, percept):
        workspace_buffer = CurrentSituationalModelImpl()
        workspace_buffer.addBufferContent(percept)

    def receiveLocalAssociation(self, node_structure):
        workspace_buffer = CurrentSituationalModelImpl()
        workspace_buffer.addBufferContent(node_structure)
        self.observers.notifyObservers()

    def decayModule(self, time):
        pass

    def notify(self, module):
        if isinstance(module, PerceptualAssociativeMemory):
            state = module.get_state()["state"]["state"]
            percept = module.retrieve_associations(state)
            self.receive_percept(percept)