#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

from SensoryMemory.SensoryMemory import SensoryMemory
from Environment.Environment import FrozenLakeEnvironment
from MotorPlanExecution.MotorPlanExecution import MPExecution

class FrozenLakeAgent:
    def __init__(self):
        self.env =  FrozenLakeEnvironment()
        self.sensory_memory = SensoryMemory()
        self.motor_plan_execution = MPExecution(self.env)

    def run(self):
        #Agents behavior logic
        done = False
        state = self.sensory_memory.run_sensors
        print(f"Initial Observation: {state}")
        #Additional code needed for the agents action (MAYBE)?

        while not done:
            action = self.env.action_space.sample() #Replace when developed action selection logic
            print(f"Action: {action}")

            state, reward, done, truncated, info = self.env.step(action)
            self.env.render()
            print(f"State: {state}, Reward: {reward}, Done: {done}, Info: {info}")

        self.env.close()