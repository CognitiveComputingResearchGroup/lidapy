#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

"""
Responsible for storing and retrieving associations between perceptual
elements. Interacts with Sensory Memory, Situational Model, and Global Workspace.
Input: Sensory Stimuli and cues from Sensory Memory
Output: Local Associations, passed to others
"""
class PerceptualAssociativeMemory:
    def __init__(self):
        #Storing associations
        self.associations = {}

    def add_association(self, cue, pattern):
        #Add new associations
        if cue not in self.associations:
            self.associations[cue] = []
            self.associations[cue].append(pattern)

    def retrieve_associations(self, cue):
        #Retreiving associations for the given cue
        return self.associations.get(cue, [])

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