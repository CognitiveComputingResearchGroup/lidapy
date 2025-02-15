#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

"""
This module can temporarily store sensory data from the environment and then
process and transfer to further working memory.
"""
from source.Framework.Agents.AgentAdapter import AgentAdapter
from source.Module.ModuleSubject import ModuleNotifier
from source.SensoryMotorMemory.Initialization.ConcreteSensoryMotorMemoryFactory import \
    ConcreteSensoryMotorMemoryFactory


class SensoryMotorMemoryImpl(ConcreteSensoryMotorMemoryFactory):
    def __init__(self, environment, agent):
        super().__init__()
        # Add modules relevant to Sensory Motor Memory
        self.add_module("environment", environment)
        self.add_module("agent", agent)
        self.add_module("AgentAdapter", AgentAdapter())
        self.add_module("notifier", ModuleNotifier())
        self.get_module("notifier").add_observer("AgentAdapter")

        #Add sensory motor memory attributes
        self.add_attribute("action", None)
        self.add_attribute("state", None)
        # initializing an empty list to store the listeners
        self.add_attribute("listeners", [])

    def add_sensory_listener(self, listener):
        """Adding the listener to the memory"""
        self.get_attribute("listeners").append(listener)
        #appending the listener to the list

    def notify(self, state, percept, action):
        """The selected action from action selection"""
        #Logic to gather information from the environment
        #Example: Reading the current state or rewards
        self.update_attribute("state", state)
        self.update_attribute("action", action)
        self.send_action_execution_command(action, percept)

    def send_action_execution_command(self, action_plan, percept):
        """
        Returning the content from this Sensory Motor Memory
        :param action_plan: Specifying the action(s) to take
        :return: content corresponding to the action_plan
        """
        if percept == "danger":
            print(f"\nPercept: {percept}!..Rerouting")
            self.get_module("AgentAdapter").notify(action_plan,
                                                   self.get_module("agent"))
        else:
            #Logic to retrieve and return data based on the modality.
            print(f"\nPercept: {percept}..")
            self.get_module("environment").step(action_plan,
                                                self.get_module("agent"))