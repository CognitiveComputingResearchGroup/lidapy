from time import sleep

from source.AttentionCodelets.AttentionCodelet import AttentionCodelet
from source.Framework.Shared.NodeStructureImpl import NodeStructureImpl
from source.ModuleInitialization.DefaultLogger import getLogger
from source.SensoryMemory.SensoryMemory import SensoryMemory
from source.Workspace.CurrentSituationModel.CurrentSituationalModel import (
    CurrentSituationalModel)


class CurrentSituationalModelImpl(CurrentSituationalModel):
    def __init__(self):
        super().__init__()
        self.node_structure = NodeStructureImpl()
        self.formed_coalition = None
        self.logger = getLogger(__class__.__name__).logger
        self.logger.debug("Initialized CurrentSituationalModel")

    def run_task(self):
        self.node_structure = NodeStructureImpl()

    def addBufferContent(self, workspace_content):
        self.node_structure.mergeWith(workspace_content)

    def getBufferContent(self):
        return self.node_structure

    def decayModule(self, time):
        self.node_structure.decayNodeStructure(time)

    def receiveVentralStream(self, stream):
        self.addBufferContent(stream)
        """sleep(0.5)  # Seed control to other modules"""

    def getModuleContent(self):
        return self.formed_coalition

    def receiveCoalition(self, coalition):
        self.formed_coalition = coalition
        self.logger.debug(f"Received new coalition")
        self.notify_observers()

    def notify(self, module):
        if isinstance(module, SensoryMemory):
            link_list = module.get_sensory_content()["cue"]
            stream = NodeStructureImpl()
            for link in link_list:
                stream.addDefaultLink__(link)
            self.logger.debug(f"Received {len(link_list)} cues from ventral "
                              f"stream")
            self.receiveVentralStream(stream)
        elif isinstance(module, AttentionCodelet):
            self.receiveCoalition(module.getModuleContent())