#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

import gymnasium as gym
import pygame

"""
TC-001: Python Compatibility
This test will ensure that when inputted code not in Python 
will generate an error message.
"""

class FrozenLakeEnvironment:
    def __init__(self):
        #generating the frozen lake environment
        self.env = gym.make(
            'FrozenLake-v1',
            is_slippery=True,
            render_mode='human')
        self.action_space = self.env.action_space   # action_space attribute

    #Reseting the environment to start a new episode
    def reset(self):
        #interacting with the environment by using Reset()
        state, info = self.env.reset()
        return state, info

    # perform an action in environment:
    def step(self, action):
        return self.env.step(action) # action chosen by the agent
        # ^returns state, reward, done, truncated, info

    # render environment's current state:
    def render(self):
        self.env.render()

    # close the environment:
    def close(self):
        self.env.close()