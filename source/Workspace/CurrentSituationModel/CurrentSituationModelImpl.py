from source.AttentionCodelets.AttentionCodelet import AttentionCodelet
from source.Framework.Shared.NodeImpl import NodeImpl
from source.Framework.Shared.NodeStructureImpl import NodeStructureImpl
from source.GlobalWorkspace.GlobalWorkSpace import GlobalWorkspace
from source.SensoryMemory.SensoryMemory import SensoryMemory
from source.Workspace.CurrentSituationModel.CurrentSituationalModel import (
    CurrentSituationalModel)


class CurrentSituationalModelImpl(CurrentSituationalModel):
    def __init__(self):
        super().__init__()
        self.node_structure = NodeStructureImpl()
        self.add_observer(GlobalWorkspace)
        self.formed_coalition = None
        self.action_value = {
            "up" : 3,
            "right" : 2,
            "down" : 1,
            "left" : 0,
        }

    def addBufferContent(self, workspace_content):
        self.node_structure.mergeWith(workspace_content)

    def getBufferContent(self):
        return self.node_structure

    def decayModule(self, time):
        self.node_structure.decayNodeStructure(time)

    def receiveVentralStream(self, stream):
        activation = 0
        incentive_salience = 0
        #Initial observations of surrounding tiles
        index = 0  # Id of the corresponding node
        for key, value in stream["outcome"]:
            ven_stream_node = NodeImpl()
            if value == 'G':
                activation = 2
                ven_stream_node.setLabel("goal")
                incentive_salience = 2
            elif value == 'H':
                ven_stream_node.setLabel("danger")
                activation = -1
                incentive_salience = 2
            elif value == 'S':
                ven_stream_node.setLabel("start")
            else:
                ven_stream_node.setLabel("safe")
                activation = 1
                incentive_salience = 1
            index = self.action_value[key]
            ven_stream_node.setId(index)
            ven_stream_node.setActivation(activation)
            ven_stream_node.setIncentiveSalience(incentive_salience)
            self.addBufferContent(ven_stream_node)

    def getCoalition(self):
        return self.formed_coalition

    def receiveCoalition(self, coalition):
        self.formed_coalition = coalition
        self.addBufferContent(self.formed_coalition)
        self.notify_observers()

    def notify(self, module):
        if isinstance(module, SensoryMemory):
            self.receiveVentralStream(module.get_sensory_content())
        elif isinstance(module, AttentionCodelet):
            self.receiveCoalition(module.FormCoalition())