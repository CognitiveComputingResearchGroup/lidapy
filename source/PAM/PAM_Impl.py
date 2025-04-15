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
        self.current_cell = None
        self.position = None
        self.logger.debug("Initialized PerceptualAssociativeMemory")


        """Create node for each cell the agent could visit"""
        for cell in range(16):
            node = NodeImpl()
            """Set the cell identifier to the corresponding state"""
            node.setId(cell)
            """Store the node in memory"""
            self.memory.addNode_(node)

    def run(self):
        pass

    def get_state(self):
        return self.current_cell

    def get_stored_nodes(self):
        return self.memory.getNodes()

    def notify(self, module):
        if isinstance(module, SensoryMemoryImpl):
            cue = module.get_sensory_content(module)
            self.position = cue["params"]["position"]
            self.learn(cue)
        elif isinstance(module, WorkspaceImpl):
            cue = module.csm.getBufferContent()
            if isinstance(cue.getLinks(), LinkImpl):
                self.logger.debug(f"Cue received from Workspace, "
                                  f"forming associations")
                self.learn(cue.getLinks())
        elif isinstance(module, GlobalWorkSpaceImpl):
            winning_coalition = module.get_broadcast()
            broadcast = winning_coalition.getContent()
            self.logger.debug(
                f"Received conscious broadcast: {broadcast}")

            """Get the nodes that have been previously visited and update
                        the connected sink links"""
            links = []
            for link in broadcast.getLinks():
                source = link.getSource()
                if isinstance(source, NodeImpl):
                    if link.getSource().getActivation() < 1:
                        links.append(link)
                else:
                    source_node = broadcast.containsNode(source)
                    if isinstance(source_node, NodeImpl):
                        if link.getSource().getActivation() < 1:
                            links.append(link)
            self.learn(links)

    def learn(self, cue):
        #Check all cells for the corresponding node
        for node in self.memory.getNodes():
            if (node.getActivation() is not None and
                                            node.getActivation() >= 0.01):
                node.decay(0.01)
                if node.isRemovable():
                    self.associations.remove(node)
            """If the result of the function to obtain the cell state 
            equals the node id, activate the corresponding node"""
            if self.position["row"] * 4 + self.position["col"] == node.getId():
                if node.getActivation() is None:
                    node.setActivation(1.0)
                    node.setLabel(str(self.position["row"]) +
                                  str(self.position["col"]))

                """Considering the current cell node as the percept
                i.e agent recognizing position within environment"""
                self.current_cell = node
                self.add_association(self.current_cell)
        if isinstance(cue, list):
            self.form_associations(cue)
        else:
            self.form_associations(cue["cue"])

    def form_associations(self, cue):
        # Set links to surrounding cell nodes if none exist
        for link in cue:
            # Priming data for scheme instantiation
            if link.getCategory("label") == 'S':
                link.setCategory(link.getCategory("id"), "start")
                link.setActivation(0.5)
                link.setIncentiveSalience(0.3)
            elif link.getCategory("label") == 'G':
                link.setCategory(link.getCategory("id"), "goal")
                link.setActivation(1.0)
                link.setIncentiveSalience(1.0)
            elif link.getCategory("label") == 'F':
                link.setCategory(link.getCategory("id"), "safe")
                link.setActivation(0.75)
                link.setIncentiveSalience(0.5)
            elif link.getCategory("label") == 'H':
                link.setCategory(link.getCategory("id"), "hole")
                link.setActivation(0.1)
            else:
                if (link.getActivation() == 0.0 and
                        link.getIncentiveSalience() == 0.0):
                    link.setActivation(0.1)

            link.setSource(self.current_cell)

            # Add links to surrounding cells
            if link not in self.associations.getLinks():
                self.associations.addDefaultLink(link.getSource(), link,
                            category = {"id": link.getCategory("id"),
                                        "label": link.getCategory("label")},
                                            activation=link.getActivation(),
                                            removal_threshold=0.0)

        self.notify_observers()
