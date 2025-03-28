#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

"""
Responsible for storing and retrieving associations between perceptual
elements. Interacts with Sensory Memory, Situational Model, and Global Workspace.
Input: Sensory Stimuli and cues from Sensory Memory
Output: Local Associations, passed to others
"""
from source.ModuleInitialization.ModuleInterface import Module


class PerceptualAssociativeMemory(Module):
    def __init__(self, workspace=None):
        #Storing associations
        super().__init__()
        self.associations = {}
        self.observers = []

    def notify(self, module):
        pass

    def add_association(self, cue, pattern):
        #Add new associations
        if not self.associations or cue not in self.associations:
            self.associations[cue] = []
        self.associations[cue].append(pattern)
        return pattern

    def retrieve_associations(self, cue):
        #Retreiving associations for the given cue
        if self.associations and cue in self.associations:
            return self.associations[cue]
        else:
            # create default association
            pattern = self.add_association(cue,
                                           f"default-pattern-{cue}")
            return pattern

    def learn(self, cue, outcome=None):
        pass

    def get_state(self):
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