#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

"""
Responsible for storing and retrieving associations between perceptual
elements. Interacts with Sensory Memory, Situational Model, and Global Workspace.
Input: Sensory Stimuli and cues from Sensory Memory
Output: Local Associations, passed to others
"""

from threading import Thread, Lock
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
        self.lock = Lock()
        self.state = None
        self.learnThread = None
        self.action_space = {}
        self.action_value = {
            "3": "up",
            "2": "right",
            "1": "down",
            "0": "left",
        }
    def __getstate__(self):
        return self.state

    def notify(self, module):
        if isinstance(module, SensoryMemoryImpl):
            cue = module.get_sensory_content(module)
            self.state = cue
            self.learn(cue["state"])

    def learn(self, cue, outcome=None):
        for index in range(len(self.action_value)):
            action_str = self.action_value[str(index)]
            #Form percepts for each action and outcome
            if cue["outcome"][action_str] == "G":
                self.add_association(cue["state"], {"goal":
                                                          index})
            elif cue["outcome"][action_str] == "H":
                self.add_association(cue["state"], {"danger":
                                                          index})
            elif cue["outcome"][action_str] == "S":
                self.add_association(cue["state"], {"start":
                                                          index})
            else:
                self.add_association(cue["state"], {"safe":
                                                          index})

        self.notify_observers()

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