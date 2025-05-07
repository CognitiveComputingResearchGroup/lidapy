#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

"""
Responsible for storing and retrieving associations between perceptual
elements. Interacts with Sensory Memory, Situational Model, and Global Workspace.
Input: Sensory Stimuli and cues from Sensory Memory
Output: Local Associations, passed to others
"""
from threading import Thread


from source.Framework.Shared.LinkImpl import LinkImpl
from source.Framework.Shared.NodeStructureImpl import NodeStructureImpl
from source.GlobalWorkspace.GlobalWorkSpaceImpl import GlobalWorkSpaceImpl
from source.PAM.PAM import PerceptualAssociativeMemory
from source.SensoryMemory.SensoryMemoryImpl import SensoryMemoryImpl
from source.Workspace.WorkspaceImpl import WorkspaceImpl


class PAMImpl(PerceptualAssociativeMemory):
    def __init__(self):
        super().__init__()
        self.state = None
        self.PAMNodeStructure = NodeStructureImpl()
        self.state = None
        self.map_columns = 4
        self.feature_detector = {"Feature" : None, "Desired" : False}

    def start(self):
        self.logger.debug("Initialized PerceptualAssociativeMemory")

    def get_state(self):
        return self.state

    def notify(self, module):
        if isinstance(module, SensoryMemoryImpl):
            cue = module.get_sensory_content(module)
            self.form_associations(cue)
        elif isinstance(module, WorkspaceImpl):
            cue = module.get_module_content(module)
            if isinstance(cue, NodeStructureImpl):
                self.logger.debug(f"Cue received from Workspace")
                thread = Thread(target=self.learn, args=(cue,))
                thread.start()
                thread.join()
        elif isinstance(module, GlobalWorkSpaceImpl):
            winning_coalition = module.get_broadcast()
            broadcast = winning_coalition.getContent()
            self.logger.debug(
                f"Received conscious broadcast: {broadcast}")
            thread = Thread(target=self.learn, args=(broadcast,))
            thread.start()


    def form_associations(self, cue):
        for node in cue['cue']:
            self.state = node
            node.decay(0.01)
            state = node.getLabel()["observation_space"]
            if state == 0:
                node.extended_id.setLinkCategory("infinity")
                self.add_association(node)
                action_space = node.getLabel()["action_space"]
                self.form_links(state, node, action_space)
            else:
                links = self.associations.links
                action_space = node.getLabel()["action_space"]
                self.form_links(state, node, action_space)
                for link in links:
                    source = link.getSource()
                    source_state = source.getLabel()["observation_space"]
                    potential = None
                    #The current node is connected to the sink by the link
                    if source_state - state == -1:
                        link.setSink(node)
                        potential = 1.0 - link.getActivation()
                    #The current node is connected to the source by the link
                    elif (source_state - state == 1 or
                          source_state - state == 0):
                        link.setSink(node)
                        #Backward link
                        potential = link.getActivation()
                    elif (source_state - state == self.map_columns or
                          source_state - state == 0):
                        link.setSink(node)
                        potential = link.getActivation()
                    elif source_state - state == -self.map_columns:
                        link.setSink(node)
                        #forward link
                        potential = 1.0 - link.getActivation()
                    if potential > 0.0:
                        flow = self.min(potential, source.getActivation())
                        link.setActivation(flow)
                self.add_association(node)
        self.notify_observers()

    def form_links(self, state, current_node, action_space):
        if isinstance(action_space, list):
            for action in action_space:
                link = LinkImpl()
                link.setSource(current_node)
                link.setActivation(0.0)
                link.setCategory(state, {"action": action})
                link.label = current_node.getLabel()["content"]
                self.associations.addDefaultLink__(link)
        elif isinstance(action_space, dict):
            for key, value in action_space.items():
                link = LinkImpl()
                link.setSource(current_node)
                link.setActivation(0.0)
                link.setCategory(state, {"action": value})
                link.label = current_node.getLabel()["content"]
                if isinstance (link.label, dict):
                    link.label = link.label[key]
                self.associations.addDefaultLink__(link)

    def min(self, num1, num2):
        if num1 > num2:
            return num2
        return num1

    def learn(self, broadcast):
        nodes = broadcast.getNodes()
        links = broadcast.getLinks()
        if len(nodes) > 0:
            for node in nodes:
                if node.isRemovable():
                    self.associations.removeNode(node)
                else:
                    content = node.getLabel()["content"]
                    if isinstance(content, dict):
                        for key, value in content.items():
                            if (self.feature_detector["Feature"] == value and
                                not self.feature_detector["Desired"]):
                                if node in self.associations:
                                    self.associations.removeNode(node)
                    elif isinstance(content, list):
                        for value in content:
                            if (self.feature_detector["Feature"] == value and
                                not self.feature_detector["Desired"]):
                                if node in self.associations:
                                    self.associations.removeNode(node)
                    elif self.feature_detector["Feature"] in content:
                            if node in self.associations:
                                self.associations.removeNode(node)
                    else:
                        self.add_association(node)
        if len(links) > 0:
            for link in links:
                if link.isRemovable():
                    self.associations.removeLink(link)
                else:
                    content = link.label
                    if isinstance(content, dict):
                        for key, value in content.items():
                            if (self.feature_detector["Feature"] == value and
                                not self.feature_detector["Desired"]):
                                if link in self.associations.link:
                                    self.associations.links.removeLink(link)
                    elif isinstance(content, list):
                        for value in content:
                            if (self.feature_detector["Feature"] == value and
                                not self.feature_detector["Desired"]):
                                if link in self.associations.link:
                                    self.associations.links.removeLink(link)
                    elif self.feature_detector["Feature"] in content:
                        if link in self.associations.link:
                            self.associations.links.removeLink(link)
                    else:
                        self.associations.addDefaultLink__(link)
