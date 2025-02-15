#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

"""
Responsible for storing and retrieving associations between perceptual
elements. Interacts with Sensory Memory, Situational Model, and Global Workspace.
Input: Sensory Stimuli and cues from Sensory Memory
Output: Local Associations, passed to others
"""

from source.Module.ModuleSubject import ModuleNotifier as Notifier
from source.PAM.Initialization.ConcretePAMFactory import PAMConcreteFactory
from source.ProceduralMemory.ProceduralMemAdapter import ProceduralMemAdapter


class CliffWalkingPAM(PAMConcreteFactory):
    def __init__(self, procedural_memory):
        super().__init__()
        # Storing associations
        self.associations = {}
        # Adding relevant modules
        self.add_module("procedural_memory", procedural_memory)
        self.add_module("ProceduralMemAdapter",
                        ProceduralMemAdapter())
        self.add_module("notifier", Notifier())
        self.get_module("notifier").add_observer(
            self.get_module("ProceduralMemAdapter")
        )
        # Adding relevant attributes
        self.add_attribute("state", None)
        self.add_attribute("position", None)
        self.add_attribute("position", None)
        self.add_attribute("action", None)
        self.add_attribute("percept", None)
        self.add_attribute("action_direction", {
            "0": "up",
            "1": "right",
            "2": "down",
            "3": "left",
        })

    def notify(self, event):
        self.update_attribute("state", event["state"])
        self.update_attribute("position",
                              event["position"])
        self.update_attribute("action", event["action"])
        self.learn(self.get_attribute("state"), self.get_attribute("action"),
                   self.get_attribute("position"))

    def add_association(self, cue, pattern):
        #Add new associations
        if self.associations.__eq__(None) or cue not in self.associations:
            self.associations[pattern] = []
        self.associations[pattern].append(cue)
        return pattern

    def retrieve_associations(self, cue):
        #Retreiving associations for the given cue
        if not self.associations.__eq__(None) and cue in self.associations:
            return self.associations[cue]
        else:
            # create default association
            pattern = self.add_association(cue,
                                           f"default-pattern-{cue}")
            return self.associations[pattern]


    def learn(self, state, action , outcome=None):
        action_direction = self.get_attribute("action_direction")
        if 46 >= state >= 36:
            if action_direction[str(action)] == "right":
                self.update_attribute("percept",
                                              self.add_association(
                                                  "Current state: " +
                                                  str(state),
                                                  "danger"))
            elif action_direction[str(action)] == "left":
                self.update_attribute("percept",
                                      self.add_association(
                                          "Current state: " +
                                          str(state),
                                          "danger"))
            elif action_direction[str(action)] == "up":
                self.update_attribute("percept",
                                      self.add_association(
                                          "Current state: " +
                                          str(state),
                                          "safe"))
            elif action_direction[str(action)] == "down":
                self.update_attribute("percept",
                                      self.add_association(
                                          "Current state: " +
                                          str(state),
                                          "danger"))

        elif 34 >= state >= 25:
            if action_direction[str(action)] == "down":
                self.update_attribute("percept",
                                      self.add_association(
                                          "Current state: " +
                                          str(state),
                                          "danger"))
            elif action_direction[str(action)] == "left":
                self.update_attribute("percept",
                                      self.add_association(
                                          "Current state: " +
                                          str(state),
                                          "safe"))
            elif action_direction[str(action)] == "right":
                self.update_attribute("percept",
                                      self.add_association(
                                          "Current state: " +
                                          str(state),
                                          "safe"))
            elif action_direction[str(action)] == "up":
                self.update_attribute("percept",
                                      self.add_association(
                                          "Current state: " +
                                          str(state),
                                          "safe"))
        else:
            self.update_attribute("percept",
                                  self.add_association(
                                      "Current state: " +
                                      str(state),
                                      "safe"))

        # Notify Procedural Memory of the outcome
        action_event = {"Current State":
                            self.retrieve_associations("Current state: " +
                                                       str(state)),
                        "Percept": self.get_attribute("percept"),
                        "Action": action,
                        "Position": self.get_attribute("position"),
                        "State": state
                        }
        self.get_module("ProceduralMemAdapter").notify(action_event,
                                        self.get_module("procedural_memory"))

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