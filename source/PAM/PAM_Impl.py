#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

"""
Responsible for storing and retrieving associations between perceptual
elements. Interacts with Sensory Memory, Situational Model, and Global Workspace.
Input: Sensory Stimuli and cues from Sensory Memory
Output: Local Associations, passed to others
"""
from threading import RLock

from source.Framework.Shared.LinkImpl import LinkImpl
from source.Framework.Shared.NodeImpl import NodeImpl
from source.Framework.Shared.NodeStructureImpl import NodeStructureImpl
from source.GlobalWorkspace.GlobalWorkSpaceImpl import GlobalWorkSpaceImpl
from source.PAM.PAM import PerceptualAssociativeMemory
from source.SensoryMemory.SensoryMemoryImpl import SensoryMemoryImpl
from source.Workspace.WorkspaceImpl import WorkspaceImpl


class PAMImpl(PerceptualAssociativeMemory):
    def __init__(self):
        super().__init__()
        self.state = None
        self.memory = NodeStructureImpl()
        self.current_node = None
        self.position = None
        self.logger.debug("Initialized PerceptualAssociativeMemory")

    def start(self):
        pass

    def get_state(self):
        return self.current_node

    def get_stored_nodes(self):
        return self.memory.getNodes()

    def notify(self, module):
        if isinstance(module, SensoryMemoryImpl):
            cue = module.get_sensory_content(module)
            self.learn(cue)
        elif isinstance(module, WorkspaceImpl):
            cue = module.csm.getBufferContent()
            if isinstance(cue.getNodes(), NodeImpl):
                self.logger.debug(f"Cue received from Workspace, "
                                  f"forming associations")
                self.learn(cue.getNodes())
        elif isinstance(module, GlobalWorkSpaceImpl):
            winning_coalition = module.get_broadcast()
            broadcast = winning_coalition.getContent()
            self.logger.debug(
                f"Received conscious broadcast: {broadcast}")

            """Get the nodes that have been previously visited"""
            nodes = broadcast.getNodes()
            for node in nodes:
                if node.getActivation() < 1.0:
                    self.learn(node)


    def learn(self, cue):
        for node in cue['cue']:
            lock = RLock()
            with lock:
                self.position = node.extended_id.sinkLinkCategory["position"]
                self.current_node = node
                node_activation = node.getActivation()

                if node_activation >= 0.01:
                    node.decay(0.01)

                if node.isRemovable():
                    self.associations.remove(node)

                self.add_association(node)
                link = LinkImpl()
                category = {"id" : node.extended_id.sinkNode1Id,
                            "label" : node.label}
                self.associations.addDefaultLink(node, link,
                                            category,
                                             activation=1.0,
                                             removal_threshold=0.0)

        self.notify_observers()
