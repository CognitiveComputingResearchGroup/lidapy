from source.AttentionCodelets.AttentionCodelet import AttentionCodelet
from source.Framework.Shared.NodeImpl import NodeImpl
from source.Framework.Shared.NodeStructureImpl import NodeStructureImpl
from source.GlobalWorkspace.GlobalWorkSpace import GlobalWorkspace
from source.SensoryMemory.SensoryMemory import SensoryMemory
from source.Workspace.CurrentSituationModel.CurrentSituationalModel import CurrentSituationalModel


class CurrentSituationalModelImpl(CurrentSituationalModel):
    def __init__(self):
        super().__init__()
        self.node_structure = NodeStructureImpl()
        self.add_observer(GlobalWorkspace)
        self.winning_coalition = None

    def addBufferContent(self, workspace_content):
        self.node_structure.mergeWith(workspace_content)

    def getBufferContent(self):
        return self.node_structure

    def decayModule(self, time):
        self.node_structure.decayNodeStructure(time)

    def receiveVentralStream(self, stream):
        activation = 0
        incentive_salience = 0
        for outcome in stream["outcome"]:
            if outcome == 'G':
                activation = 2
                incentive_salience = 2
            elif outcome == 'H':
                activation = -1
                incentive_salience = 2
            else:
                activation = 1
                incentive_salience = 1

        index = 1   #Id of the corresponding node
        ven_stream_node = NodeImpl()
        ven_stream_node.setId(index)
        ven_stream_node.setLabel("ven_stream state" + str(stream["state"]))
        ven_stream_node.setActivation(activation)
        ven_stream_node.setIncentiveSalience(incentive_salience)
        self.addBufferContent(ven_stream_node)

    def getCoalition(self):
        return self.winning_coalition

    def receiveCoalition(self, coalition):
        self.winning_coalition = coalition
        self.notify_observers()

    def notify(self, module):
        if isinstance(module, SensoryMemory):
            self.receiveVentralStream(module.get_sensory_content())
        elif isinstance(module, AttentionCodelet):
            self.receiveCoalition(module.getSoughtContent())