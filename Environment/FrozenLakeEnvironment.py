#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

import gymnasium as gym
import pygame

#Creating the Frozen Lake Environment
env = gym.make(
     'FrozenLake-v1',
        is_slippery=True,
        render_mode='human')

#Reseting the environment to start a new episode
#State: complete description of the environment at a given time
#Observation: What an agent actually senses in the environment.
#interacting with the environment by using Reset()
state, info = env.reset()
done = False  #Episode is just starting

#Printing the initial state
print(f"Initial observation: {state}")

#Sampling a random action
while not done:
    action = env.action_space.sample()   #Taking a random action
    print(f"Action: {action}")

    #State: new state of the environment after the agent takes the action
    #reward: numerical value after agent performs the action
    #done: boolean value to indicate whether episode is done
    #Truncated: boolean, truncated due to time limit

    state,reward,done,truncated,info= env.step(action) #Performing the action
    env.render() #Rendering for visual feedback

    #Printing the outcome
    print(f"State: {state}, Reward: {reward},Done: {done}, Info: {info}")

env.close()
