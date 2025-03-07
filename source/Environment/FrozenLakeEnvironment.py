#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

import gymnasium as gym

from source.Environment.Environment import Environment
from source.ModuleInitialization.DefaultLogger import getLogger
from source.SensoryMotorMemory.SensoryMotorMemory import SensoryMotorMemory

"""
The environment is essential for receiving, processing, and
integrating all sensory information, enabling the agent to interact 
effectively.
Sends Sensory information to the Sensory Memory.
"""

class FrozenLake(Environment):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}
    def __init__(self, agent, render_mode="human", size=4):
        super().__init__()
        # generating the frozen lake environment
        self.env = gym.make(
            'FrozenLake-v1',
            desc=None,
            is_slippery=False,
            render_mode=render_mode)
        self.action_space = self.env.action_space  # action_space attribute
        self.state = None
        self.row = 0
        self.col = 0
        self.add_observer(agent)
        self.logger = getLogger(agent.__class__.__name__).logger

    # Reseting the environment to start a new episode
    def reset(self):
        # interacting with the environment by using Reset()
        state, info = self.env.reset()
        surrounding_tiles = self.get_surrounding_tiles(self.row, self.col)
        self.state = {"state": state, "info": info, "done": False,
                      "outcome": surrounding_tiles}
        self.logger.info(f"state: {state}, " + f"info: {info}, " +
                         f"done: False")
        self.notify_observers()

    # perform an action in environment:
    def step(self, action):
        # perform and update
        state, reward, done, truncated, info = self.env.step(action)
        self.update_position(action)
        surrounding_tiles = self.get_surrounding_tiles(self.row, self.col)
        self.state = {"state": state, "info": info, "done": done,
                      "outcome": surrounding_tiles}
        self.logger.info(f"state: {state}, " + f"info: {info}, " +
                          f"done: {done}, " + f"action: {action}")
        self.notify_observers()

    # render environment's current state:
    def render(self):
        self.env.render()

    def get_state(self):
        return self.state

    def notify(self, module):
        if isinstance(module, SensoryMotorMemory):
            action = module.receive_action()
            if not self.state["done"]:
                self.step(action)
            else:
                self.close()

    def update_position(self, action):
        if action == 3:  # up
            self.row = max(self.row - 1, 0)
        elif action == 2:  # Right
            self.row = min(self.col + 1, self.env.unwrapped.desc.shape[1] - 1)
        elif action == 1:  # down
            self.row = min(self.row + 1, self.env.unwrapped.desc.shape[0] - 1)
        elif action == 0:  # Left
            self.col = max(self.col - 1, 0)

    def get_surrounding_tiles(self, row, col):
        # gathering information about the tiles surrounding the agent
        desc = self.env.unwrapped.desc
        surrounding_tiles = {}
        directions = {
            "up": (max(row - 1, 0), col),
            "right": (row, min(col + 1, desc.shape[1] - 1)),
            "down": (min(row + 1, desc.shape[0] - 1), col),
            "left": (row, max(col - 1, 0)),
        }
        for direction, (r, c) in directions.items():
            surrounding_tiles[direction] = desc[r, c].decode(
                'utf-8')  # Decode byte to string
        return surrounding_tiles

    # close the environment:
    def close(self):
        self.env.close()