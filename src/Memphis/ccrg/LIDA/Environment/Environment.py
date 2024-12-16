#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

import gymnasium as gym
import pygame
import numpy as np
from enum import Enum
from gymnasium import spaces
from gymnasium.envs.toy_text.frozen_lake import generate_random_map

"""
The environment is essential for preceiving, processing, and
integrating all sensory information, enabling the agent to interact 
effectively.
Sends Sensory information to the Sensory Memory.
"""

class FrozenLakeEnvironment():
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}
    col = 0     #Data to hold the current column the agent occupies
    row = 0     # Data to hold the current row the agent occupies
    def __init__(self, render_mode="human", size=4):
    #def __init__(self):
        #generating the frozen lake environment
        self.env = gym.make(
            'FrozenLake-v1',
            desc=generate_random_map(size=5),
            is_slippery=True,
            render_mode=render_mode)

        self.action_space = self.env.action_space  # action_space attribute

    #Reseting the environment to start a new episode
    def reset(self):
        #interacting with the environment by using Reset()
        state, info = self.env.reset()
        return state, info, self.col, self.row

    # perform an action in environment:
    def step(self, action):
        return self.env.step(action)     # action chosen by the agent
        # ^returns state, reward, done, truncated, info

    # render environment's current state:
    def render(self):
        self.env.render()

    # close the environment:
    def close(self):
        self.env.close()
