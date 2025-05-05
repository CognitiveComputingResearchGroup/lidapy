from AttentionCodelets.AttentionCodelet import AttentionCodelet
from Framework.Shared.NodeStructureImpl import NodeStructureImpl
from Module.Initialization.DefaultLogger import getLogger
from SensoryMemory.SensoryMemory import SensoryMemory
from Workspace.CurrentSituationalModel.CurrentSituationalModel import (
    CurrentSituationalModel)


class CurrentSituationalModelImpl(CurrentSituationalModel):
    def __init__(self):
        super().__init__()
        self.node_structure = NodeStructureImpl()
        self.received_coalition = None
        self.state = None
        self.logger = getLogger(__class__.__name__).logger

    def run_task(self):
        self.logger.debug("Initialized CurrentSituationalModel")

    def addBufferContent(self, workspace_content):
        self.node_structure.mergeWith(workspace_content)

    def getBufferContent(self):
        return self.node_structure

    def get_state(self):
        return self.state

    def decayModule(self, time):
        self.node_structure.decayNodeStructure(time)

    def receiveVentralStream(self, stream):
        self.addBufferContent(stream)

    def getModuleContent(self):
        return self.received_coalition

    def receiveCoalition(self, coalition):
        self.received_coalition = coalition
        self.notify_observers()

    def notify(self, module):
        if isinstance(module, SensoryMemory):
            cue = module.get_sensory_content()
            nodes = cue["cue"]
            stream = NodeStructureImpl()
            for node in nodes:
                stream.addNode_(node)
            self.logger.debug(f"Received {len(nodes)} cues from ventral "
                              f"stream")
            self.receiveVentralStream(stream)
        elif isinstance(module, AttentionCodelet):
            coalition = module.getModuleContent()
            self.logger.debug(f"Received new coalition")
            self.receiveCoalition(coalition)