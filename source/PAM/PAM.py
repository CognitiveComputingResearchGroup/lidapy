#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

"""
Responsible for storing and retrieving associations between perceptual
elements. Interacts with Sensory Memory, Situational Model, and Global Workspace.
Input: Sensory Stimuli and cues from Sensory Memory
Output: Local Associations, passed to others
"""
from source.Framework.Shared.NodeImpl import NodeImpl
from source.Framework.Shared.NodeStructureImpl import NodeStructureImpl
from source.ModuleInitialization.DefaultLogger import getLogger
from source.ModuleInitialization.ModuleInterface import Module


class PerceptualAssociativeMemory(Module):
    def __init__(self):
        #Storing associations
        super().__init__()
        self.associations = NodeStructureImpl()
        self.logger = getLogger(self.__class__.__name__).logger

    def notify(self, module):
        pass

    def add_association(self, cue : NodeImpl):
        #Add new associations
        self.logger.debug(f"Storing node {cue}")
        self.associations.addNode_(cue)

    def retrieve_associations(self, cue : NodeStructureImpl):
        #Retreiving associations for the given cue
        self.logger.info(f"Retrieved {len(cue.getLinkCount())} associations")
        return cue.getLinks()

    def receive_broadcast(self, coalition):
        self.logger.debug(f"Received broadcast coalition {coalition}")
        map(self.add_association, coalition.getContent())

    def learn(self, cue):
        pass

    """
    NEED: to connect to sensory memory, use data as cue for PAM
    Possible implement of function that can extract patterns
    """

    """
    NEED: To communication with the situational Model
    Passes patterns or local associations for updates to Current Situational Model
    """

    """
    NEED: Implement the Perceptual Learning 
    """