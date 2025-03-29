from source.Framework.Shared.NodeImpl import NodeImpl
from source.Framework.Shared.NodeStructureImpl import NodeStructureImpl
from source.PAM.PAM import PerceptualAssociativeMemory
from source.Workspace.CurrentSituationModel.CurrentSituationModelImpl import \
    CurrentSituationalModelImpl
from source.Workspace.Workspace import Workspace
from source.ModuleInitialization.DefaultLogger import getLogger


class WorkspaceImpl(Workspace):
    def __init__(self):
        super().__init__()
        self.logger = getLogger(self.__class__.__name__)
        self.nodes = []
        self.csm = None
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
        global node
        workspace_buffer = NodeStructureImpl()
        for association in percept:
            for key, value in association.items():
                action = value
                node = NodeImpl()
                #Temp frozen lake impl.
                node.setId(action)      #Set the node ID as the action value
                node.setLabel(key)      #The key contains the percept

                if key == 'goal':
                    activation = 2
                    incentive_salience = 2
                elif key == 'danger':
                    activation = -1
                    incentive_salience = 2
                else:
                    activation = 1
                    incentive_salience = 1

                node.setActivation(activation)
                node.setIncentiveSalience(incentive_salience)

        workspace_buffer.addNode_(node)
        self.csm.addBufferContent(workspace_buffer)

    def receiveLocalAssociation(self, node_structure):
        self.csm.addBufferContent(node_structure)

    def decayModule(self, time):
        pass

    def notify(self, module):
        if isinstance(module, PerceptualAssociativeMemory):
            state = module.get_state()["state"]["state"]
            percept = module.retrieve_associations(state)
            self.receive_percept(percept)