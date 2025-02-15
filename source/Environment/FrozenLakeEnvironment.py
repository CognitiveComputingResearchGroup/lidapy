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

class FrozenLakeEnvironment(ConcreteEnvironmentFactory):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}
    col = 0     #Data to hold the current column the agent occupies
    row = 0     # Data to hold the current row the agent occupies
    def __init__(self, render_mode="human", size=4):
        super().__init__()
        # generate the frozen lake environment
        self.add_module("env", gym.make(
            'FrozenLake-v1',
            desc=None,
            is_slippery=False,
            render_mode=render_mode))

        # Add module attributes
        self.add_attribute("action_space",
                           self.get_module("env").action_space)
        # Assuming the agent is started at (0,0)
        self.add_attribute("col", 0) #Agents column position
        self.add_attribute("row", 0) #Agents row position
        self.add_attribute("surrounding_tiles", None)

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
        self.col, self.row = 0, 0
        self.update_attribute("surrounding_tiles",
                              self.get_surrounding_tiles(self.row, self.col))
        self.get_module("SensoryMemoryModuleAdapter").notify(state, module)
        return (state, info, self.get_attribute("surrounding_tiles"), self.col,
                self.row)

    # perform an action in environment:
    def step(self, action, module):
        #perform and update
        state, reward, done, truncated, info = (
            self.get_module("env").step(action))

        # updating the agents position based on the action
        self.update_position(action)
        self.update_attribute("surrounding_tiles",
            self.get_surrounding_tiles(self.get_attribute("row"),
                                       self.get_attribute("col")))
        self.get_module("AgentAdapter").notify_(state, module, reward, done,
                                                  truncated, info, action,
                                       self.get_attribute("surrounding_tiles"))
    # render environment's current state:
    def render(self):
        self.get_module("env").render()

    # close the environment:
    def close(self):
        self.get_module("env").close()

    # updating the agents position based on the action taken
    def update_position(self, action):
        if action == 3: #up
            self.update_attribute("row",
                                  max(self.get_attribute("row") - 1, 0))
        elif action == 2: #Right
            self.update_attribute("col",
                                  min(self.get_attribute("col") + 1,
                        self.get_module("env").unwrapped.desc.shape[1] - 1))
        elif action == 1: #down
            self.update_attribute("row",
                                  min(self.get_attribute("row") + 1,
                        self.get_module("env").unwrapped.desc.shape[0] - 1))
        elif action == 0: #Left
            self.update_attribute("col",
                                  max(self.get_attribute("col") - 1, 0))

    # gathering information about the tiles surrounding the agent
    def get_surrounding_tiles(self, row, col):
        desc = self.get_module("env").unwrapped.desc
        surrounding_tiles = {}
        directions = {
            "up":(max(row - 1, 0), col),
            "right":(row,min(col + 1,desc.shape[1] - 1)),
            "down":(min(row + 1, desc.shape[0] - 1), col),
            "left":(row,max(col - 1, 0)),
        }
        for direction, (r,c) in directions.items():
            surrounding_tiles[direction] = desc[r,c].decode('utf-8') #Decode byte to string
        return surrounding_tiles
