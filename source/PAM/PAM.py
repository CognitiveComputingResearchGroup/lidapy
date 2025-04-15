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

from source.Framework.Shared.NodeImpl import NodeImpl
from source.Framework.Shared.NodeStructureImpl import NodeStructureImpl
from source.Module.Initialization.DefaultLogger import getLogger
from source.Module.Initialization.ModuleInterface import Module


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
        if cue is not None and cue not in self.associations.getNodes():
            self.logger.debug(f"Storing association, node: {cue}")
            lock = Lock()
            lock.acquire()
            self.associations.addNode_(cue)
            lock.release()

    def retrieve_associations(self, cue : NodeStructureImpl):
        #Retreiving associations for the given cue
        self.logger.debug(f"Retrieved {len(cue.getLinkCount())} associations")
        return cue.getLinks()

    def retrieve_association(self, cue: NodeImpl):
        links = None
        if not NodeImpl:
            self.logger.debug(f"Unable to retrieve association for {cue}")
        else:
            if cue in self.associations.getNodes():
                links = self.associations.getConnectedSinks(cue)
                self.logger.debug(f"Retrieved {len(links)} associations")
            else:
                self.logger.debug(f"Unable to retrieve association for {cue}")
        return links

    def receive_broadcast(self, coalition):
        self.logger.debug(f"Received broadcast coalition {coalition}")
        map(self.add_association, coalition.getContent())

    def get_stored_nodes(self):
        pass

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