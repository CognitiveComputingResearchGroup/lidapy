#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

"""
Responsible for storing and retrieving associations between perceptual
elements. Interacts with Sensory Memory, Situational Model, and Global Workspace.
Input: Sensory Stimuli and cues from Sensory Memory
Output: Local Associations, passed to others
"""
from threading import Lock


from Framework.Shared.LinkImpl import LinkImpl
from Framework.Shared.NodeImpl import NodeImpl
from Framework.Shared.NodeStructureImpl import NodeStructureImpl
from GlobalWorkspace.GlobalWorkSpaceImpl import GlobalWorkSpaceImpl
from PAM.PAM import PerceptualAssociativeMemory
from SensoryMemory.SensoryMemoryImpl import SensoryMemoryImpl
from Workspace.WorkspaceImpl import WorkspaceImpl


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
            self.learn(broadcast.getConnectedSinks())

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
                self.logger.debug(
                    f"Found an association, agent's position: "
                    f" {node}")
                """Considering the current cell node as the percept
                i.e agent recognizing position within environment"""
                self.current_cell = node
                self.add_association(self.current_cell)
        self.form_associations(cue["cue"])

    def form_associations(self, cue):
        lock = Lock()
        lock.acquire(blocking=True)
        # Set links to surrounding cell nodes if none exist
        for link in cue:
            # Priming data for scheme instantiation
            if link.getCategory("label") == 'S':
                link.setCategory(link.getCategory("id"), "start")
                link.setActivation(0.5)
            elif link.getCategory("label") == 'G':
                link.setCategory(link.getCategory("id"), "goal")
                link.setActivation(1.0)
            elif link.getCategory("label") == 'F':
                link.setCategory(link.getCategory("id"), "safe")
                link.setActivation(0.75)
            elif link.getCategory("label") == 'H':
                link.setCategory(link.getCategory("id"), "hole")
                link.setActivation(0.1)
            else:
                link.setActivation(1.0)

            link.setSource(self.current_cell)

            # Add links to surrounding cells
            if link not in self.associations.getLinks():
                self.associations.addDefaultLink(self.current_cell, link,
                            category = {"id": link.getCategory("id"),
                                        "label": link.getCategory("label")},
                                            activation=link.getActivation(),
                                            removal_threshold=0.0)

        lock.release()
        self.notify_observers()
