#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

"""
Responsible for storing and retrieving associations between perceptual
elements. Interacts with Sensory Memory, Situational Model, and Global Workspace.
Input: Sensory Stimuli and cues from Sensory Memory
Output: Local Associations, passed to others
"""


from source.PAM.PAM import PerceptualAssociativeMemory
from source.SensoryMemory.SensoryMemoryImpl import SensoryMemoryImpl


class PAMImpl(PerceptualAssociativeMemory):
    def __init__(self, procedural_memory=None, workspace=None):
        super().__init__()
        if procedural_memory is not None:
            self.add_observer(procedural_memory)
        if workspace is not None:
            self.add_observer(workspace)
        self.action = None
        self.state = None
        self.action_value = {
            "3": "up",
            "2": "right",
            "1": "down",
            "0": "left",
        }

    def notify(self, module):
        if isinstance(module, SensoryMemoryImpl):
            self.state = module.get_sensory_content(module)
            self.learn(self.state["state"], self.state["action"])

    def learn(self, state, outcome=None):
        action_str = self.action_value[str(outcome)]

        if state["outcome"][action_str] == "G":
            self.add_association(state["state"], "goal")
        elif state["outcome"][action_str] == "H":
            self.add_association(state["state"], "danger")
        elif state["outcome"][action_str] == "S":
            self.add_association(state["state"], "start")
        else:
            self.add_association(state["state"], "safe")

        self.notify_observers()

    def get_state(self):
        return self.state

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