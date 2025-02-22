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
    def __init__(self):
        super().__init__()

    def learn(self, state, outcome=None):
        if outcome == "goal":
            self.add_association(state, "goal" + state)
        elif outcome == "hole":
            self.add_association(state, "danger" + state)
        else:
            self.add_association(state, "safe" + state)

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