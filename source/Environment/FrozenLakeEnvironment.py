#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

import gymnasium as gym
from source.Environment.Environment import Environment

"""
The environment is essential for receiving, processing, and
integrating all sensory information, enabling the agent to interact 
effectively.
Sends Sensory information to the Sensory Memory.
"""

class FrozenLakeEnvironment(Environment):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}
    col = 0  # Data to hold the current column the agent occupies
    row = 0  # Data to hold the current row the agent occupies

    def __init__(self, render_mode="human", size=4):
        # def __init__(self):
        # generating the frozen lake environment
        self.env = gym.make(
            'FrozenLake-v1',
            desc=None,
            is_slippery=True,
            render_mode=render_mode)

        self.action_space = self.env.action_space  # action_space attribute
        # self.col = 0 #Agents column position
        # self.row = 0 #Agents row position

    # Reseting the environment to start a new episode
    def reset(self):
        # interacting with the environment by using Reset()
        state, info = self.env.reset()
        self.col, self.row = 0, 0  # Assuming the agent is started at (0,0)
        surrounding_tiles = self.get_surrounding_tiles(self.row, self.col)
        return state, info, surrounding_tiles, self.col, self.row

    # perform an action in environment:
    def step(self, action):
        # perform and update
        state, reward, done, truncated, info = self.env.step(action)
        self.update_position(
            action)  # updating the agents position based on the action
        surrounding_tiles = self.get_surrounding_tiles(self.row, self.col)
        return state, reward, done, truncated, info, surrounding_tiles  # action chosen by the agent
        # ^returns state, reward, done, truncated, info

    # render environment's current state:
    def render(self):
        self.env.render()

    # close the environment:
    def close(self):
        self.env.close()

    def update_position(self, action):
        # updating the agents position based on the action taken
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