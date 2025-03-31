#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

"""
Responsible for storing and retrieving associations between perceptual
elements. Interacts with Sensory Memory, Situational Model, and Global Workspace.
Input: Sensory Stimuli and cues from Sensory Memory
Output: Local Associations, passed to others
"""
from time import sleep

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
        #self.logger.debug("Initialized PerceptualAssociativeMemory")

        """Create node for each cell the agent could visit"""
        for cell in range(16):
            node = NodeImpl()
            """Set the cell identifier to the corresponding state"""
            node.setId(cell)
            """Store the node in memory"""
            self.memory.addNode_(node)

    def __getstate__(self):
        return self.current_cell

    def get_stored_nodes(self):
        return self.memory.getNodes()

    def notify(self, module):
        if isinstance(module, SensoryMemoryImpl):
            cue = module.get_sensory_content(module)
            self.learn(cue)
        elif isinstance(module, WorkspaceImpl):
            cue = module.get_module_content(module)
            for link in cue.getLinks():
                self.add_association(link.getSource())
        elif isinstance(module, GlobalWorkSpaceImpl):
            winning_coalition = module.__getstate__()

    def learn(self, cue):
        position = cue["params"]["position"]
        state = cue["params"]["state"]["state"]
        links = None
        #Check all cells for the corresponding one
        for node in self.memory.getNodes():
            if (node.getActivation() is not None and
                                            node.getActivation() >= 1.0):
                node.decay(0.05)
                if node.isRemovable():
                    self.associations.remove(node)
            """If the result of the function to obtain the cell state 
            equals the node id, activate the corresponding node"""
            if position["row"] * 4 + position["col"] == node.getId():
                node.setActivation(2)
                node.setLabel(str(position["row"]) + str(position["col"]))
                self.logger.debug(
                    f"Found an association, agent's position: "
                    f" {node}")
                """Considering the current cell node as the percept
                i.e agent recognizing position within environment"""
                self.add_association(node)
                self.current_cell = node

        #Set links to surrounding cell nodes if none exist
        for link in cue["cue"]:
            if (link.getActivation() is not None and
                                            link.getActivation() >= 1.0):
                link.decay(0.05)
                if link.isRemovable():
                    self.associations.removeLink(link)
            # Priming data for scheme instantiation
            if link.getCategory("label") == 'S':
                link.setCategory(link.getCategory("id"), "start")
            elif link.getCategory("label") == 'G':
                link.setCategory(link.getCategory("id"), "goal")
            elif link.getCategory("label") == 'F':
                link.setCategory(link.getCategory("id"), "safe")
            else:
                link.setCategory(link.getCategory("id"), "hole")

            # Add links to surrounding cells
            self.associations.addDefaultLink(self.current_cell, link,
                                             {"id": link.getCategory("id"),
                                              "label": link.getCategory(
                                                  "label")}
                                             , 0, 0)
        self.notify_observers()