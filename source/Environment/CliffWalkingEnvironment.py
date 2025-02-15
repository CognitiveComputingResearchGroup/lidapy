#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

import gymnasium as gym

from source.Environment.Initialization.ConcreteEnvironmentFactory import \
    ConcreteEnvironmentFactory
from source.Framework.Agents.AgentAdapter import AgentAdapter
from source.Module.ModuleSubject import ModuleNotifier
from source.SensoryMemory.SensoryMemoryModuleAdapter import \
    SensoryMemoryModuleAdapter

"""
The environment is essential for receiving, processing, and
integrating all sensory information, enabling the agent to interact 
effectively.
Sends Sensory information to the Sensory Memory.
"""

class CliffWalkingEnvironment(ConcreteEnvironmentFactory):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}
    col = 0     #Data to hold the current column the agent occupies
    row = 0     # Data to hold the current row the agent occupies
    def __init__(self, render_mode="human", size=4):
        super().__init__()
        # generate the frozen lake environment
        self.add_module("env", gym.make(
            'CliffWalking-v0',
            is_slippery=False,
            render_mode=render_mode))

        # Add module attributes
        # Assuming the agent is started at (0,0)
        self.add_attribute("col", 0)  # Agents column position
        self.add_attribute("row", 3)  # Agents row position
        self.add_attribute("action_space",
                           self.get_module("env").action_space)

        # Add modules relevant to the environment
        self.add_module("notifier", ModuleNotifier())
        self.add_module("SensoryMemoryModuleAdapter",
                        SensoryMemoryModuleAdapter())
        self.add_module("AgentAdapter", AgentAdapter())
        self.get_module("notifier").add_observer(
            self.get_module("SensoryMemoryModuleAdapter"))
        self.get_module("notifier").add_observer(
            self.get_module("AgentAdapter"))

    #Resetting the environment to start a new episode
    def reset(self, module):
        #interacting with the environment by using Reset()
        state, info = self.get_module("env").reset()
        self.col, self.row = 0, 3
        self.get_module("SensoryMemoryModuleAdapter").notify(state, module)
        return state, info, self.col, self.row

    # perform an action in environment:
    def step(self, action, module):
        #perform and update
        state, reward, done, truncated, info = (
            self.get_module("env").step(action))

        # updating the agents position based on the action
        self.update_position(action)
        self.get_module("AgentAdapter").notify_(state, module, reward, done,
                                                  truncated, info, action,
                                       None)

    # render environment's current state:
    def render(self):
        self.get_module("env").render()

    def update_position(self, action):
        if action == 3: #up
            self.update_attribute("row",
                                  max(self.get_attribute("row") - 1, 0))
        elif action == 2: #Right
            self.update_attribute("col",
                                  min(self.get_attribute("col") + 1,  11))
        elif action == 1: #down
            self.update_attribute("row",
                                  min(self.get_attribute("row") + 1, 3))
        elif action == 0: #Left
            self.update_attribute("col",
                                  max(self.get_attribute("col") - 1, 0))

    # close the environment:
    def close(self):
        self.get_module("env").close()
