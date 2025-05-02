#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

"""
Responsible for storing and retrieving associations between perceptual
elements. Interacts with Sensory Memory, Situational Model, and Global Workspace.
Input: Sensory Stimuli and cues from Sensory Memory
Output: Local Associations, passed to others
"""
from source.Framework.Shared.LinkImpl import LinkImpl
from source.Framework.Shared.NodeStructureImpl import NodeStructureImpl
from source.GlobalWorkspace.GlobalWorkSpaceImpl import GlobalWorkSpaceImpl
from source.PAM.PAM import PerceptualAssociativeMemory
from source.PAM.PAMLink import PAMLink
from source.PAM.PAMLinkImpl import PAMLinkImpl
from source.PAM.PAMNodeImpl import PAMNodeImpl
from source.SensoryMemory.SensoryMemoryImpl import SensoryMemoryImpl
from source.Workspace.WorkspaceImpl import WorkspaceImpl


class PAMImpl(PerceptualAssociativeMemory):
    def __init__(self):
        super().__init__()
        self.state = None
        self.PAMNodeStructure = NodeStructureImpl()
        self.current_node = None
        self.position = None
        self.feature_detector = {"Feature" : None, "Desired" : False}

    def start(self):
        self.logger.debug("Initialized PerceptualAssociativeMemory")

    def get_state(self):
        return self.current_node

    def notify(self, module):
        if isinstance(module, SensoryMemoryImpl):
            cue = module.get_sensory_content(module)
            self.form_associations(cue)
        elif isinstance(module, WorkspaceImpl):
            cue = module.get_module_content(module)
            if isinstance(cue, NodeStructureImpl):
                self.logger.debug(f"Cue received from Workspace")
                self.learn(cue)
        elif isinstance(module, GlobalWorkSpaceImpl):
            winning_coalition = module.get_broadcast()
            broadcast = winning_coalition.getContent()
            self.logger.debug(
                f"Received conscious broadcast: {broadcast}")
            self.learn(broadcast)


    def form_associations(self, cue):
        for node in cue['cue']:
            self.position = node.extended_id.sinkLinkCategory["position"]
            self.current_node = node
            node_activation = node.getActivation()
            pam_node = PAMNodeImpl()
            pam_node.setId(node.getId())
            pam_node.setActivation(node_activation)
            pam_node.extended_id.setSinkLinkCategory({"position":
                                                          self.position})
            self.PAMNodeStructure.addNode_(pam_node)

            if node_activation >= 0.01:
                self.current_node.decay(0.01)
                node.decay(0.01)

            if node.isRemovable():
                self.associations.remove(node)
                self.PAMNodeStructure.removeNode(pam_node)

            self.add_association(node)
            pam_link = PAMLinkImpl()
            category = {"id" : node.extended_id.sinkNode1Id,
                        "label" : node.getLabel(),}
            pam_link.extended_id.setSinkLinkCategory({"position":
                                                         self.position})
            pam_link.setCategory(category["id"], category["label"])
            pam_link.setActivation(1.0)
            pam_link.setActivatibleRemovalThreshold(0.0)
            link = LinkImpl()
            link.setSource(node)
            link.setCategory(category["id"], category["label"])
            link.setActivation(1.0)
            link.setActivatibleRemovalThreshold(0.0)
            link.setGroundingPamLink(pam_link)
            self.associations.addDefaultLink__(link)

                
        self.notify_observers()

    def learn(self, broadcast):
        nodes = broadcast.getNodes()
        links = broadcast.getLinks()
        if len(nodes) > 0:
            for node in nodes:
                if node.isRemovable():
                    self.associations.remove(node)

                elif self.feature_detector["Feature"] in node.label:
                    if not self.feature_detector["Desired"]:
                        for association in self.associations:
                            if (node.getId() == association.getId() and
                                    node.getName() == association.getName()):
                                self.associations.remove(node)
                    else:
                        self.add_association(node)
        if len(links) > 0:
            for link in links:
                if link.isRemovable():
                    self.associations.remove(link)

                elif (self.feature_detector["Feature"] in
                                                    link.getCategory("label")):
                    if not self.feature_detector["Desired"]:
                        for association in self.associations:
                            if (link.getCategory("id") == association.getId() and
                                    link.getCategory("label") ==
                                    association.getLabel()):
                                self.associations.links.remove(link)
                    else:
                        self.associations.addDefaultLink__(link)
