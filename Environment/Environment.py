#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

import gymnasium as gym
import pygame

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

    #done = False  #Episode is just starting
    # Printing the initial state
    #print(f"Initial observation: {state}")
    #Sampling a random action
    #while not done:
        #action = self.env.action_space.sample()   #Taking a random action
        #print(f"Action: {action}")

        #State: new state of the environment after the agent takes the action
        #reward: numerical value after agent performs the action
        #done: boolean value to indicate whether episode is done
        #Truncated: boolean, truncated due to time limit
        #state,reward,done,truncated,info= self.env.step(action) #Performing the action
        #self.env.render() #Rendering for visual feedback
        #Printing the outcome
        #print(f"State: {state}, Reward: {reward},Done: {done}, Info: {info}")

