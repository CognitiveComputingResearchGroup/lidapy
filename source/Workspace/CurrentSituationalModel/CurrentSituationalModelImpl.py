from time import sleep

from source.AttentionCodelets.AttentionCodelet import AttentionCodelet
from source.Framework.Shared.NodeStructureImpl import NodeStructureImpl
from source.Module.Initialization.DefaultLogger import getLogger
from source.SensoryMemory.SensoryMemory import SensoryMemory
from source.Workspace.CurrentSituationalModel.CurrentSituationalModel import (
    CurrentSituationalModel)


class CurrentSituationalModelImpl(CurrentSituationalModel):
    def __init__(self):
        super().__init__()
        self.node_structure = NodeStructureImpl()
        self.formed_coalition = None
        self.state = None
        self.logger = getLogger(__class__.__name__).logger
        self.logger.debug("Initialized CurrentSituationalModel")

    def run_task(self):
        self.node_structure = NodeStructureImpl()

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
        return self.formed_coalition

    def receiveCoalition(self, coalition):
        self.formed_coalition = coalition
        self.notify_observers()

    def notify(self, module):
        if isinstance(module, SensoryMemory):
            cue = module.get_sensory_content()
            link_list = cue["cue"]
            """State here is a Frozen Lake state variable"""
            #TODO Change it to a general state for other environments
            self.state = cue["params"]["state"]["state"]
            stream = NodeStructureImpl()
            for link in link_list:
                stream.addDefaultLink__(link)
            self.logger.debug(f"Received {len(link_list)} cues from ventral "
                              f"stream")
            self.receiveVentralStream(stream)
        elif isinstance(module, AttentionCodelet):
            coalition = module.getModuleContent()
            self.logger.debug(f"Received new coalition")
            self.receiveCoalition(coalition)