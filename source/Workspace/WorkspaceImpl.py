from time import sleep


from source.Framework.Shared.NodeStructureImpl import NodeStructureImpl
from source.PAM.PAM import PerceptualAssociativeMemory
from source.Workspace.Workspace import Workspace



class WorkspaceImpl(Workspace):
    def __init__(self):
        super().__init__()
        self.nodes = None
        self.csm = None
        self.coalition = None
        self.episodic_memory = None
        self.state = None
        self.logger.debug("Initialized Workspace")

    def start(self):
        self.nodes = []

    def cueEpisodicMemories(self, node_structure):
        self.episodic_memory = node_structure
        self.logger.debug(f"{len(self.episodic_memory.getLinks())} episodic "
                         f"memories cued")
        self.notify_observers()

    def get_state(self):
        return self.state

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
        self.notify_observers()
        sleep(25)

    def receiveLocalAssociation(self, node_structure):
        self.csm.addBufferContent(node_structure)

    def decayModule(self, ticks):
        pass

    def notify(self, module):
        if isinstance(module, PerceptualAssociativeMemory):
            self.state = module.get_state()
            percept = module.retrieve_association(self.state)
            self.logger.debug(f"Received new percept")
            self.receive_percept(percept)
