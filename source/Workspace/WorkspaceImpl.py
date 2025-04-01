from time import sleep

from source.Framework.Shared.NodeImpl import NodeImpl
from source.Framework.Shared.NodeStructureImpl import NodeStructureImpl
from source.PAM.PAM import PerceptualAssociativeMemory
from source.Workspace.CurrentSituationModel.CurrentSituationalModel import \
    CurrentSituationalModel
from source.Workspace.Workspace import Workspace
from source.ModuleInitialization.DefaultLogger import getLogger


class WorkspaceImpl(Workspace):
    def __init__(self):
        super().__init__()
        self.logger = getLogger(self.__class__.__name__)
        self.nodes = []
        self.csm = None
        self.coalition = None
        self.logger = getLogger(self.__class__.__name__).logger
        self.episodic_memory = None
        self.logger.debug("Initialized Workspace")

    def cueEpisodicMemories(self, node_structure):
        self.episodic_memory = node_structure
        self.logger.info(f"{len(self.episodic_memory.getLinks())} episodic "
                         f"memories cued")
        self.notify_observers()

    def get_module_content(self , params=None):
        return self.episodic_memory

    def receive_broadcast(self, coalition):
        self.coalition = coalition
        self.csm.receiveCoalition(coalition)
        self.csm.notify_observers()

    def receive_percept(self, percept):
        workspace_buffer = NodeStructureImpl()
        workspace_buffer.addLinks(percept, "Adjacent node")
        self.csm.addBufferContent(workspace_buffer)

    def receiveLocalAssociation(self, node_structure):
        self.csm.addBufferContent(node_structure)

    def decayModule(self, time):
        pass

    def notify(self, module):
        if isinstance(module, PerceptualAssociativeMemory):
            state = module.__getstate__()
            percept = None
            if isinstance(state, NodeImpl):
                percept = module.retrieve_association(state)
            self.receive_percept(percept)
        elif isinstance(module, CurrentSituationalModel):
            cue = module.getBufferContent()
            self.cueEpisodicMemories(cue)
